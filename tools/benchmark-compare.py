#!/usr/bin/env python3
"""
Benchmark Comparison
====================
For a given ticker + our price target + horizon, produce a side-by-side
comparison against four alternative return baselines:

  (a) Bloomberg / Wall Street consensus price target
  (b) Sector ETF 12-month trailing return (a benchmark for "beat sector")
  (c) A simple 5-factor composite fair value (value, quality, momentum,
      low-vol, size) derived from screening.py output
  (d) S&P 500 trailing return

The purpose is accountability, not pseudo-precision. Every column shows its
source and its caveat; when a datum is missing the tool emits `N/A` rather
than hallucinating. The output is designed to be pasted verbatim into
Section 12 of the research note as the "Benchmark Comparison" subsection.

Contract
--------
Input:
  --run-dir     output/[TICKER]/[DATE]     required
  --price-target FLOAT                      our note's price target (required)
  --current-price FLOAT                     required
  --horizon-months INT                      default 12
  --output PATH                             default <run-dir>/pass2/benchmark-comparison.md

Exit codes:
  0   report written
  1   bad inputs

Design notes
------------
- The tool reads `data/*.json` inside the run dir; it does NOT make network
  calls. All live data must already have been retrieved by the Research
  Analyst. This is intentional: keeps `--as-of` historical runs deterministic
  and avoids reintroducing lookahead bias.
- If a field is missing the tool emits `N/A` with a pointer to the Research
  Analyst tool that should have populated it.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


EXIT_OK = 0
EXIT_BAD_INPUT = 1


SECTOR_TO_ETF = {
    "Communication Services": "XLC",
    "Consumer Discretionary": "XLY",
    "Consumer Staples": "XLP",
    "Energy": "XLE",
    "Financials": "XLF",
    "Health Care": "XLV",
    "Industrials": "XLI",
    "Information Technology": "XLK",
    "Materials": "XLB",
    "Real Estate": "XLRE",
    "Utilities": "XLU",
}


@dataclass
class Row:
    label: str
    implied_price: Optional[float]
    implied_return_pct: Optional[float]
    source: str
    note: str = ""

    def fmt_price(self) -> str:
        return f"${self.implied_price:,.2f}" if self.implied_price is not None else "N/A"

    def fmt_return(self) -> str:
        if self.implied_return_pct is None:
            return "N/A"
        sign = "+" if self.implied_return_pct >= 0 else ""
        return f"{sign}{self.implied_return_pct:.1f}%"


def _load_data(run_dir: Path) -> Dict[str, Any]:
    data_dir = run_dir / "data"
    out: Dict[str, Any] = {}
    if not data_dir.is_dir():
        return out
    for p in sorted(data_dir.glob("*.json")):
        try:
            out[p.stem] = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
    return out


def _walk(data: Dict[str, Any], *dotted_paths: str) -> Optional[Any]:
    for path in dotted_paths:
        cur: Any = data
        ok = True
        for part in path.split("."):
            if isinstance(cur, dict) and part in cur:
                cur = cur[part]
            else:
                ok = False
                break
        if ok and cur is not None and cur != "":
            return cur
    return None


def _pct_return(target: float, current: float) -> float:
    return (target / current - 1.0) * 100.0


def build_rows(data: Dict[str, Any], ticker: str, price_target: float,
               current_price: float) -> List[Row]:
    rows: List[Row] = []

    # Our note
    rows.append(Row(
        label=f"Our note — {ticker}",
        implied_price=price_target,
        implied_return_pct=_pct_return(price_target, current_price),
        source="this research note",
    ))

    # Consensus PT
    consensus = _walk(data,
        "estimates.consensusPriceTarget",
        "estimates.medianTargetPrice",
        "analyst-estimates.consensusPriceTarget",
        "consensus.priceTarget",
    )
    if isinstance(consensus, (int, float)):
        rows.append(Row(
            label="Street consensus",
            implied_price=float(consensus),
            implied_return_pct=_pct_return(float(consensus), current_price),
            source="data/*.json (consensus PT)",
        ))
    else:
        rows.append(Row(
            label="Street consensus",
            implied_price=None, implied_return_pct=None,
            source="—",
            note="Research Analyst: run `tools/alt-data.py estimates` and "
                 "persist consensus PT to data/.",
        ))

    # Sector ETF trailing 12-month return
    sector = _walk(data,
        "overview.sector", "market-overview.sector",
        "company-profile.sector",
    )
    etf = SECTOR_TO_ETF.get(sector) if isinstance(sector, str) else None
    etf_ret = _walk(data,
        f"sector-etf.{etf}.return12m" if etf else "",
        "sector-etf.return12m",
        "benchmarks.sectorEtfReturn12m",
    )
    if etf and isinstance(etf_ret, (int, float)):
        rows.append(Row(
            label=f"Sector ETF ({etf}) trailing 12m",
            implied_price=current_price * (1 + float(etf_ret) / 100.0),
            implied_return_pct=float(etf_ret),
            source=f"data/*.json (sector-etf.{etf})",
            note="Trailing return used as naive benchmark — sector beta is "
                 "assumed 1.0.",
        ))
    else:
        rows.append(Row(
            label=f"Sector ETF ({etf or 'unknown'}) trailing 12m",
            implied_price=None, implied_return_pct=None,
            source="—",
            note="Research Analyst: populate sector-etf.<ETF>.return12m using "
                 "`tools/market-data.sh quote <ETF>` + period comparison.",
        ))

    # 5-factor composite implied fair value
    ff = _walk(data,
        "five-factor.impliedFairValue",
        "factor-model.impliedFairValue",
        "screening.fiveFactorImpliedValue",
    )
    if isinstance(ff, (int, float)):
        rows.append(Row(
            label="5-factor composite fair value",
            implied_price=float(ff),
            implied_return_pct=_pct_return(float(ff), current_price),
            source="data/*.json (five-factor)",
            note="Equal-weighted value/quality/momentum/low-vol/size "
                 "z-score composite.",
        ))
    else:
        rows.append(Row(
            label="5-factor composite fair value",
            implied_price=None, implied_return_pct=None,
            source="—",
            note="Quant Analyst: run `tools/screening.py composite` and write "
                 "`five-factor.impliedFairValue` to data/.",
        ))

    # SPX
    spx_ret = _walk(data,
        "benchmarks.spxReturn12m",
        "sp500.return12m",
        "market-overview.spxReturn12m",
    )
    if isinstance(spx_ret, (int, float)):
        rows.append(Row(
            label="S&P 500 trailing 12m",
            implied_price=current_price * (1 + float(spx_ret) / 100.0),
            implied_return_pct=float(spx_ret),
            source="data/*.json (benchmarks.spxReturn12m)",
            note="Assumes stock beta 1.0 to SPX — naive baseline.",
        ))
    else:
        rows.append(Row(
            label="S&P 500 trailing 12m",
            implied_price=None, implied_return_pct=None,
            source="—",
            note="Research Analyst: populate benchmarks.spxReturn12m "
                 "(`tools/market-data.sh quote SPY`).",
        ))

    return rows


def render(ticker: str, horizon_months: int, current_price: float,
           rows: List[Row]) -> str:
    lines: List[str] = []
    lines.append("### Benchmark Comparison")
    lines.append("")
    lines.append(
        f"Our {horizon_months}-month price target vs. alternative baselines. "
        f"Current price: ${current_price:,.2f}."
    )
    lines.append("")
    lines.append("| Baseline | Implied Price | Implied Return | Source |")
    lines.append("|----------|---------------|----------------|--------|")
    for r in rows:
        lines.append(f"| {r.label} | {r.fmt_price()} | {r.fmt_return()} | {r.source} |")
    notes = [r for r in rows if r.note]
    if notes:
        lines.append("")
        lines.append("**Notes:**")
        for r in notes:
            lines.append(f"- *{r.label}:* {r.note}")
    lines.append("")
    lines.append(
        "This table is generated by `tools/benchmark-compare.py`. Missing "
        "baselines (`N/A`) are not approximations; the tool refuses to "
        "hallucinate a comparison when the underlying data was not retrieved."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Benchmark comparison block")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--price-target", type=float, required=True)
    ap.add_argument("--current-price", type=float, required=True)
    ap.add_argument("--horizon-months", type=int, default=12)
    ap.add_argument("--output", default=None)
    args = ap.parse_args()

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
        print(f"ERROR: run-dir not found: {run_dir}", file=sys.stderr)
        return EXIT_BAD_INPUT

    # ticker = output/TICKER/DATE
    parts = run_dir.parts
    try:
        idx = parts.index("output")
        ticker = parts[idx + 1]
    except (ValueError, IndexError):
        ticker = run_dir.parent.name

    data = _load_data(run_dir)
    rows = build_rows(data, ticker, args.price_target, args.current_price)
    md = render(ticker, args.horizon_months, args.current_price, rows)

    out = Path(args.output) if args.output else (run_dir / "pass2" / "benchmark-comparison.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(md)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
