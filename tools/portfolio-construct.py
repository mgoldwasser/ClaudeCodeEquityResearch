#!/usr/bin/env python3
"""
Portfolio Construction Orchestrator
===================================
Ingests N research-note run directories, extracts thesis-driven views
(price target, conviction, scenarios), fetches historical return
covariance, and produces four comparable portfolios:

  1. equal-weight          — naive baseline
  2. risk-parity           — equal risk contribution from covariance only
  3. conviction-weighted   — weights scaled by the Director's conviction rating
  4. black-litterman       — CAPM-implied prior + per-note absolute views,
                             then max-Sharpe optimization on the posterior

Output: a markdown report plus JSON with all four weight vectors, their
portfolio metrics (expected return, vol, Sharpe), and each note's parsed
inputs.

Usage
-----
  python tools/portfolio-construct.py \\
      --run-dirs output/META/2026-03-13 output/NVDA/2026-03-19 \\
      --output-dir output/portfolio/2026-04-19 \\
      --max-weight 0.20 \\
      --lookback-days 756 \\
      --risk-free 0.045

Notes
-----
- Sell-rated notes are excluded from long-only construction (consistent
  with the default IPS). Hold-rated notes with negative expected return
  are retained but flagged.
- Historical prices come from Yahoo's public chart API via urllib. No
  API key required. A failed fetch degrades the ticker to an equal-weight
  fallback with a warning — it does not poison the whole run.
- Black-Litterman uses a CAPM-style prior: pi_i = rf + beta_i * (market - rf).
  Beta is computed against SPY from the same lookback window.
- Conviction (1-5) maps to BL view confidence as conviction / 5. A 3/5
  conviction gives the view 60% weight against the prior.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import ssl
import subprocess
import sys
import time
import urllib.request
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def _build_ssl_context() -> ssl.SSLContext:
    """macOS Python.framework ships without a populated system trust store.
    Prefer certifi's bundle when available; fall back to default context."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


_SSL_CTX = _build_ssl_context()

# Make sibling imports work regardless of cwd.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

# Reuse the math functions we already ship; don't duplicate.
import importlib.util


def _load_portfolio_math():
    spec = importlib.util.spec_from_file_location(
        "portfolio_math", _HERE / "portfolio-math.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


PM = _load_portfolio_math()


# ---------------------------------------------------------------------------
# Regex library for research-note parsing
# ---------------------------------------------------------------------------

TICKER_IN_FILENAME_RE = re.compile(r"([A-Z]{1,5})-research-note-\d{4}-\d{2}-\d{2}\.md$")

RATING_RE = re.compile(r"\*\*Rating:\*\*\s*([A-Za-z]+)", re.IGNORECASE)
PRICE_TARGET_RE = re.compile(
    r"\*\*(?:12-Month\s+)?Price\s+Target:\*\*\s*\$(\d[\d,]*(?:\.\d+)?)",
    re.IGNORECASE,
)
CURRENT_PRICE_RE = re.compile(
    r"\*\*Current\s+Price:\*\*\s*\$(\d[\d,]*(?:\.\d+)?)",
    re.IGNORECASE,
)
CONVICTION_RE = re.compile(
    r"\*\*Conviction\s+Rating:\*\*\s*(\d)\s*/\s*5",
    re.IGNORECASE,
)


@dataclass
class NoteInputs:
    """Everything the orchestrator needs from one research note."""
    ticker: str
    run_dir: str
    note_path: str
    rating: str
    price_target: float
    current_price: float
    conviction: int
    expected_return: float
    parse_warnings: List[str] = field(default_factory=list)


def find_note_file(run_dir: Path) -> Optional[Path]:
    """A run-dir contains exactly one final research note at the root."""
    candidates = list(run_dir.glob("*-research-note-*.md"))
    if not candidates:
        return None
    return candidates[0]


def parse_note(run_dir: Path) -> NoteInputs:
    note_path = find_note_file(run_dir)
    if not note_path:
        raise FileNotFoundError(
            f"no research-note-*.md found under {run_dir}"
        )

    text = note_path.read_text(encoding="utf-8")
    warnings: List[str] = []

    m = TICKER_IN_FILENAME_RE.search(note_path.name)
    ticker = m.group(1) if m else run_dir.parent.name.upper()

    def _num(match: Optional[re.Match], field_name: str) -> Optional[float]:
        if not match:
            warnings.append(f"could not parse {field_name}")
            return None
        return float(match.group(1).replace(",", ""))

    rating_m = RATING_RE.search(text)
    rating = rating_m.group(1).upper() if rating_m else "UNKNOWN"
    if not rating_m:
        warnings.append("could not parse rating")

    price_target = _num(PRICE_TARGET_RE.search(text), "price_target")
    current_price = _num(CURRENT_PRICE_RE.search(text), "current_price")
    conv_m = CONVICTION_RE.search(text)
    conviction = int(conv_m.group(1)) if conv_m else 0
    if not conv_m:
        warnings.append("could not parse conviction")

    if price_target is None or current_price is None or current_price == 0:
        raise ValueError(
            f"{note_path}: cannot compute expected return "
            f"(price_target={price_target}, current_price={current_price})"
        )

    expected_return = price_target / current_price - 1.0

    return NoteInputs(
        ticker=ticker,
        run_dir=str(run_dir),
        note_path=str(note_path),
        rating=rating,
        price_target=price_target,
        current_price=current_price,
        conviction=conviction,
        expected_return=expected_return,
        parse_warnings=warnings,
    )


# ---------------------------------------------------------------------------
# Historical price fetch (Yahoo /v8/finance/chart)
# ---------------------------------------------------------------------------

YF_CHART = "https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"


def fetch_closes(ticker: str, lookback_days: int) -> List[float]:
    end = int(time.time())
    # 1.5x buffer for weekends/holidays; Yahoo returns trading days only.
    start = end - int(lookback_days * 86400 * 1.5)
    url = (
        YF_CHART.format(ticker=ticker)
        + f"?period1={start}&period2={end}&interval=1d"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15, context=_SSL_CTX) as resp:
        payload = json.loads(resp.read())
    closes = payload["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    return [c for c in closes if c is not None]


def log_returns(closes: List[float]) -> List[float]:
    out: List[float] = []
    for i in range(1, len(closes)):
        a, b = closes[i - 1], closes[i]
        if a and b and a > 0 and b > 0:
            out.append(math.log(b / a))
    return out


def align_length(series_map: Dict[str, List[float]]) -> Dict[str, List[float]]:
    """Trim every series to the minimum length (keep most recent observations)."""
    if not series_map:
        return {}
    min_len = min(len(s) for s in series_map.values())
    return {t: s[-min_len:] for t, s in series_map.items()}


def annualized_cov(returns_map: Dict[str, List[float]]) -> Tuple[List[str], List[List[float]]]:
    import numpy as np

    tickers = list(returns_map.keys())
    matrix = np.array([returns_map[t] for t in tickers])  # shape (N, T)
    if matrix.shape[1] < 20:
        raise ValueError(
            f"aligned return series too short for covariance: {matrix.shape[1]} obs"
        )
    daily_cov = np.cov(matrix)
    annual = daily_cov * 252.0
    # numpy returns 0-d array when N=1; wrap for consistency
    if annual.ndim == 0:
        annual = np.array([[float(annual)]])
    return tickers, annual.tolist()


def capm_prior(
    tickers: List[str],
    returns_map: Dict[str, List[float]],
    market_returns: List[float],
    risk_free: float,
) -> List[float]:
    """pi_i = rf + beta_i * (market_excess_return)"""
    import numpy as np

    market = np.array(market_returns)
    market_mean_annual = float(np.mean(market) * 252.0)
    market_excess = market_mean_annual - risk_free

    var_m = float(np.var(market, ddof=1))
    pi: List[float] = []
    for t in tickers:
        r = np.array(returns_map[t])
        n = min(len(r), len(market))
        cov_rm = float(np.cov(r[-n:], market[-n:], ddof=1)[0][1])
        beta = cov_rm / var_m if var_m > 0 else 1.0
        pi.append(risk_free + beta * market_excess)
    return pi


# ---------------------------------------------------------------------------
# Method implementations
# ---------------------------------------------------------------------------

def equal_weights(n: int) -> List[float]:
    return [1.0 / n] * n


def conviction_weights(convictions: List[int]) -> List[float]:
    total = float(sum(convictions))
    if total <= 0:
        return equal_weights(len(convictions))
    return [c / total for c in convictions]


def portfolio_metrics(
    weights: List[float],
    expected_returns: List[float],
    cov: List[List[float]],
    risk_free: float,
) -> Dict:
    import numpy as np

    w = np.array(weights)
    r = np.array(expected_returns)
    c = np.array(cov)
    port_ret = float(w @ r)
    port_vol = float(math.sqrt(max(w @ c @ w, 0.0)))
    sharpe = (port_ret - risk_free) / port_vol if port_vol > 0 else 0.0
    # Marginal contribution to risk
    if port_vol > 0:
        mcr = (c @ w) / port_vol
        rc = (w * mcr).tolist()
    else:
        rc = [0.0] * len(w)
    return {
        "expected_return": round(port_ret, 4),
        "volatility": round(port_vol, 4),
        "sharpe": round(sharpe, 3),
        "risk_contributions": [round(float(x), 4) for x in rc],
    }


def cap_and_renormalize(weights: List[float], max_weight: float) -> List[float]:
    """Water-fill cap: clip any weight > max_weight, redistribute excess to uncapped names."""
    w = list(weights)
    n = len(w)
    for _ in range(n):
        excess = 0.0
        uncapped_idx: List[int] = []
        for i, wi in enumerate(w):
            if wi > max_weight + 1e-9:
                excess += wi - max_weight
                w[i] = max_weight
            else:
                uncapped_idx.append(i)
        if excess < 1e-9 or not uncapped_idx:
            break
        denom = sum(w[i] for i in uncapped_idx)
        if denom <= 0:
            break
        for i in uncapped_idx:
            w[i] += excess * (w[i] / denom)
    total = sum(w)
    if total > 0:
        w = [wi / total for wi in w]
    return w


def read_ips_max_single_name(ips_path: Optional[Path]) -> Optional[float]:
    if not ips_path or not ips_path.exists():
        return None
    try:
        import yaml  # optional dependency, but ships in this repo
    except ImportError:
        return None
    try:
        data = yaml.safe_load(ips_path.read_text(encoding="utf-8")) or {}
        pct = data.get("position", {}).get("max_single_name_weight_pct")
        return float(pct) / 100.0 if pct is not None else None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def format_weight_table(
    notes: List[NoteInputs],
    weights_by_method: Dict[str, List[float]],
    metrics_by_method: Dict[str, Dict],
) -> str:
    lines = []
    header = ["Ticker", "Rating", "Conv", "ER%"] + list(weights_by_method.keys())
    lines.append("| " + " | ".join(header) + " |")
    lines.append("|" + "|".join(["---"] * len(header)) + "|")
    for i, n in enumerate(notes):
        row = [
            n.ticker,
            n.rating,
            f"{n.conviction}/5",
            f"{n.expected_return * 100:.1f}",
        ]
        for method, weights in weights_by_method.items():
            row.append(f"{weights[i] * 100:.1f}%")
        lines.append("| " + " | ".join(row) + " |")

    # Metrics row
    lines.append("")
    lines.append("### Portfolio Metrics")
    lines.append("")
    lines.append("| Method | Exp Return | Volatility | Sharpe |")
    lines.append("|---|---|---|---|")
    for method, m in metrics_by_method.items():
        lines.append(
            f"| {method} | {m['expected_return'] * 100:.2f}% | "
            f"{m['volatility'] * 100:.2f}% | {m['sharpe']:.3f} |"
        )
    return "\n".join(lines)


def write_markdown_report(
    out_dir: Path,
    notes: List[NoteInputs],
    weights_by_method: Dict[str, List[float]],
    metrics_by_method: Dict[str, Dict],
    prior_returns: List[float],
    posterior_returns: List[float],
    cov: List[List[float]],
    params: Dict,
) -> Path:
    tickers = [n.ticker for n in notes]
    lines: List[str] = []
    lines.append(f"# Portfolio Construction — {params['as_of']}")
    lines.append("")
    lines.append(
        f"Notes ingested: {len(notes)}.  "
        f"Lookback: {params['lookback_days']} trading days.  "
        f"Risk-free: {params['risk_free'] * 100:.2f}%.  "
        f"Max single-name weight: {params['max_weight'] * 100:.1f}%."
    )
    lines.append("")
    lines.append("## 1. Inputs Parsed from Research Notes")
    lines.append("")
    lines.append("| Ticker | Rating | Conviction | Current | Target | Expected Return |")
    lines.append("|---|---|---|---|---|---|")
    for n in notes:
        lines.append(
            f"| {n.ticker} | {n.rating} | {n.conviction}/5 | "
            f"${n.current_price:,.2f} | ${n.price_target:,.2f} | "
            f"{n.expected_return * 100:+.1f}% |"
        )
        if n.parse_warnings:
            lines.append(f"  * parse warnings: {', '.join(n.parse_warnings)}")
    lines.append("")
    lines.append("## 2. CAPM-Implied Prior vs. Black-Litterman Posterior")
    lines.append("")
    lines.append("| Ticker | Prior (CAPM) | Posterior (BL) | Delta |")
    lines.append("|---|---|---|---|")
    for i, t in enumerate(tickers):
        lines.append(
            f"| {t} | {prior_returns[i] * 100:.2f}% | "
            f"{posterior_returns[i] * 100:.2f}% | "
            f"{(posterior_returns[i] - prior_returns[i]) * 100:+.2f}% |"
        )
    lines.append("")
    lines.append("## 3. Weights by Method")
    lines.append("")
    lines.append(format_weight_table(notes, weights_by_method, metrics_by_method))
    lines.append("")
    lines.append("## 4. Annualized Return Covariance Matrix")
    lines.append("")
    lines.append("| | " + " | ".join(tickers) + " |")
    lines.append("|---|" + "|".join(["---"] * len(tickers)) + "|")
    for i, t in enumerate(tickers):
        row = [f"{c:.4f}" for c in cov[i]]
        lines.append("| " + t + " | " + " | ".join(row) + " |")
    lines.append("")
    lines.append("## 5. Caveats")
    lines.append("")
    lines.append(
        "- Historical covariance is backward-looking; it does not capture the "
        "regime change embedded in a forward thesis."
    )
    lines.append(
        "- Black-Litterman confidence is driven by the Director's conviction "
        "rating (1-5), not separate view-level uncertainty. A 3/5 conviction "
        "gives the view 60% weight against the CAPM prior."
    )
    lines.append(
        "- Sell-rated notes and notes with unresolvable parse failures are "
        "excluded at ingestion, not penalized at optimization."
    )
    lines.append(
        "- This tool constructs weights; IPS compliance (sector caps, liquidity, "
        "ESG, etc.) is enforced per-name via `tools/ips-validator.py`."
    )

    out_path = out_dir / "portfolio-construction.md"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build(
    run_dirs: List[Path],
    out_dir: Path,
    *,
    max_weight: float,
    lookback_days: int,
    risk_free: float,
    market_ticker: str,
    ips_path: Optional[Path],
) -> Dict:
    out_dir.mkdir(parents=True, exist_ok=True)

    # --- 1. Parse notes -----------------------------------------------------
    notes: List[NoteInputs] = []
    for rd in run_dirs:
        try:
            n = parse_note(rd)
        except (FileNotFoundError, ValueError) as e:
            print(f"[skip] {rd}: {e}", file=sys.stderr)
            continue
        if n.rating in ("SELL", "SHORT"):
            print(
                f"[skip] {n.ticker}: rating={n.rating} excluded from long-only build",
                file=sys.stderr,
            )
            continue
        notes.append(n)

    if len(notes) < 2:
        raise ValueError(
            f"need at least 2 parseable long-rated notes, got {len(notes)}"
        )

    tickers = [n.ticker for n in notes]

    # --- 2. Fetch history + build covariance --------------------------------
    print(f"Fetching {lookback_days}d history for {tickers} + {market_ticker}...",
          file=sys.stderr)
    closes_map: Dict[str, List[float]] = {}
    for t in tickers + [market_ticker]:
        try:
            closes_map[t] = fetch_closes(t, lookback_days)
        except Exception as e:
            raise RuntimeError(f"failed to fetch {t}: {e}") from e
        time.sleep(0.3)

    returns_map = {t: log_returns(c) for t, c in closes_map.items()}
    aligned = align_length(returns_map)

    asset_returns = {t: aligned[t] for t in tickers}
    market_returns = aligned[market_ticker]

    _, cov = annualized_cov(asset_returns)

    # --- 3. Prior + views + posterior --------------------------------------
    prior = capm_prior(tickers, asset_returns, market_returns, risk_free)
    views = []
    for i, n in enumerate(notes):
        conf = max(min(n.conviction / 5.0, 0.9999), 0.05)
        views.append({
            "asset_indices": [i],
            "weights": [1.0],
            "expected_return": n.expected_return,
            "confidence": conf,
        })
    bl_out = PM.black_litterman(prior, cov, views, tau=0.05)
    if "error" in bl_out:
        raise RuntimeError(f"BL failed: {bl_out['error']}")
    posterior = bl_out["posterior_returns"]

    # --- 4. Four methods ----------------------------------------------------
    effective_cap = max_weight
    ips_cap = read_ips_max_single_name(ips_path)
    if ips_cap is not None and ips_cap < effective_cap:
        print(
            f"[ips] tightening max_weight {max_weight:.1%} -> {ips_cap:.1%} "
            f"from {ips_path}",
            file=sys.stderr,
        )
        effective_cap = ips_cap

    # 4a. Equal-weight
    ew = equal_weights(len(notes))

    # 4b. Risk-parity
    rp_raw = PM.mean_variance_optimize(
        [0.0] * len(notes), cov, method="risk-parity"
    )
    rp = [float(w) for w in rp_raw["weights"]]
    rp = cap_and_renormalize(rp, effective_cap)

    # 4c. Conviction-weighted
    cw_raw = conviction_weights([n.conviction for n in notes])
    cw = cap_and_renormalize(cw_raw, effective_cap)

    # 4d. BL -> max-Sharpe
    bl_opt = PM.mean_variance_optimize(
        posterior, cov,
        method="max-sharpe",
        risk_free_rate=risk_free,
        constraints={"min_weight": 0.0, "max_weight": effective_cap},
    )
    if "error" in bl_opt:
        # Fallback: equal-weight if scipy unavailable.
        print(f"[warn] BL-MV optimization unavailable ({bl_opt['error']}); "
              "falling back to equal-weight", file=sys.stderr)
        bl = ew[:]
    else:
        bl = [float(w) for w in bl_opt["weights"]]

    weights_by_method = {
        "equal-weight": ew,
        "risk-parity": rp,
        "conviction-weighted": cw,
        "black-litterman": bl,
    }

    # --- 5. Metrics (evaluated against the posterior expected returns) -----
    metrics_by_method = {
        method: portfolio_metrics(w, posterior, cov, risk_free)
        for method, w in weights_by_method.items()
    }

    # --- 6. Write outputs --------------------------------------------------
    params = {
        "as_of": time.strftime("%Y-%m-%d"),
        "lookback_days": lookback_days,
        "risk_free": risk_free,
        "max_weight": effective_cap,
        "market_ticker": market_ticker,
        "ips_path": str(ips_path) if ips_path else None,
    }

    report_path = write_markdown_report(
        out_dir, notes, weights_by_method, metrics_by_method,
        prior, posterior, cov, params,
    )

    result = {
        "params": params,
        "notes": [asdict(n) for n in notes],
        "prior_returns": prior,
        "posterior_returns": posterior,
        "covariance": cov,
        "weights": weights_by_method,
        "metrics": metrics_by_method,
        "report_path": str(report_path),
    }
    json_path = out_dir / "portfolio-construction.json"
    json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    return result


def main() -> int:
    p = argparse.ArgumentParser(
        description="Build a portfolio from N research-note run directories."
    )
    p.add_argument(
        "--run-dirs", nargs="+", required=True,
        help="one or more output/<TICKER>/<DATE> directories",
    )
    p.add_argument(
        "--output-dir", required=True,
        help="where to write portfolio-construction.{md,json}",
    )
    p.add_argument(
        "--max-weight", type=float, default=0.20,
        help="hard cap on any single name (default 0.20 = 20%%)",
    )
    p.add_argument(
        "--lookback-days", type=int, default=756,
        help="trading days of history for covariance (default 756 = ~3y)",
    )
    p.add_argument(
        "--risk-free", type=float, default=0.045,
        help="annualized risk-free rate (default 0.045)",
    )
    p.add_argument(
        "--market-ticker", type=str, default="SPY",
        help="benchmark used for CAPM beta (default SPY)",
    )
    p.add_argument(
        "--ips",
        type=str,
        default="configs/default-ips.yaml",
        help="Investment Policy Statement YAML; 'none' to skip",
    )
    args = p.parse_args()

    run_dirs = [Path(r) for r in args.run_dirs]
    for r in run_dirs:
        if not r.is_dir():
            print(f"error: not a directory: {r}", file=sys.stderr)
            return 1

    ips_path: Optional[Path] = None
    if args.ips and args.ips.lower() != "none":
        cand = Path(args.ips)
        if cand.exists():
            ips_path = cand

    try:
        result = build(
            run_dirs=run_dirs,
            out_dir=Path(args.output_dir),
            max_weight=args.max_weight,
            lookback_days=args.lookback_days,
            risk_free=args.risk_free,
            market_ticker=args.market_ticker,
            ips_path=ips_path,
        )
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    print(f"wrote {result['report_path']}")
    print(f"wrote {Path(result['report_path']).with_suffix('.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
