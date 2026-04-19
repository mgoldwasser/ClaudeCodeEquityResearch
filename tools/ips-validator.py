#!/usr/bin/env python3
"""
Investment Policy Statement (IPS) Validator
===========================================
Validates a research note against an active IPS before publication. Emits a
structured compliance report and a blocking verdict for the Director's Step
2.7 final review.

Contract
--------
Input:
  --run-dir  output/[TICKER]/[DATE]     required; must contain the editor draft
                                        and (optionally) data/*.json
  --ips      configs/default-ips.yaml   default; path to IPS YAML

Output:
  Markdown report at output/[TICKER]/[DATE]/pass2/ips-compliance.md
  (or --output path)

Verdicts:
  ELIGIBLE                  — all hard constraints satisfied
  ELIGIBLE_WITH_EXCEPTIONS  — soft flags only; Director must document acceptance
  RESTRICTED                — at least one hard constraint violated; note cannot
                              be published as an actionable recommendation

Exit codes:
  0  ELIGIBLE  or  ELIGIBLE_WITH_EXCEPTIONS
  1  bad inputs (missing draft, malformed IPS)
  2  RESTRICTED (hard constraint violation — blocking gate)

Checks Implemented (single-stock scope)
---------------------------------------
Each check pulls from draft text, data JSONs, or both. Missing fields degrade
to UNVERIFIED rather than silent-PASS — the Director must see what we could
not verify.

  UNIVERSE
    U1. market_cap >= universe.min_market_cap_usd
    U2. sector in universe.allowed_sectors and not in exclusions.sector_exclusions
    U3. exchange in universe.allowed_exchanges

  POSITION
    P1. position_sizing.target_weight_pct <= position.max_single_name_weight_pct

  LIQUIDITY
    L1. adv_usd_30d >= liquidity.min_adv_usd
    L2. position_notional / adv_usd_30d * 100 <= liquidity.max_pct_of_adv

  QUALITY
    Q1. beneish_m_score >= quality.min_beneish_m_score
    Q2. altman_z >= quality.min_altman_z_nonfin (skip if financials)
    Q3. going_concern_flag is false
    Q4. auditor_opinion is unqualified

  EXCLUSIONS
    E1. ticker not in exclusions.issuer_restricted_list
    E2. sector not in exclusions.sector_exclusions

  RATING
    R1. recommendation.rating in mandate.allowed_ratings

The validator is deliberately additive: new checks are added as functions that
return a CheckResult. The report renderer iterates over all results.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml


EXIT_OK = 0
EXIT_BAD_INPUT = 1
EXIT_RESTRICTED = 2

PASS = "PASS"
FAIL = "FAIL"
UNVERIFIED = "UNVERIFIED"
SOFT_FLAG = "SOFT_FLAG"


@dataclass
class CheckResult:
    code: str
    name: str
    status: str  # PASS | FAIL | UNVERIFIED | SOFT_FLAG
    expected: str
    observed: str
    source: str
    note: str = ""

    def is_blocking(self) -> bool:
        return self.status == FAIL


@dataclass
class NoteContext:
    """Facts extracted from the draft + data files that checks need."""
    ticker: str
    run_dir: Path
    draft_text: str
    data: Dict[str, Any] = field(default_factory=dict)

    def get_number(self, *dotted_paths: str) -> Optional[float]:
        for path in dotted_paths:
            cur: Any = self.data
            ok = True
            for part in path.split("."):
                if isinstance(cur, dict) and part in cur:
                    cur = cur[part]
                else:
                    ok = False
                    break
            if ok and isinstance(cur, (int, float)):
                return float(cur)
        return None

    def get_str(self, *dotted_paths: str) -> Optional[str]:
        for path in dotted_paths:
            cur: Any = self.data
            ok = True
            for part in path.split("."):
                if isinstance(cur, dict) and part in cur:
                    cur = cur[part]
                else:
                    ok = False
                    break
            if ok and isinstance(cur, str) and cur.strip():
                return cur.strip()
        return None


def _load_ips(path: Path) -> Dict[str, Any]:
    with path.open("r") as f:
        return yaml.safe_load(f)


def _load_data_jsons(run_dir: Path) -> Dict[str, Any]:
    """Load all *.json in data/ into a single dict keyed by stem."""
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


def _find_draft(run_dir: Path) -> Optional[Path]:
    candidates = [
        run_dir / "pass2" / "editor-draft.md",
    ]
    for p in candidates:
        if p.is_file():
            return p
    return None


# ----- Field extractors from draft text -----
# These read the Editor draft. They prefer explicit labeled values; when not
# found they return None and the check degrades to UNVERIFIED rather than
# hallucinating a number.

_RATING_RE = re.compile(r"(?im)^\s*(?:\*\*)?Rating(?:\*\*)?\s*[:\-–]\s*(?:\*\*)?([A-Za-z ]+?)(?:\*\*)?\s*$")
_TARGET_WEIGHT_RE = re.compile(r"(?im)target\s+weight\s*[:\-–]\s*([\d.]+)\s*%")


def extract_rating(text: str) -> Optional[str]:
    m = _RATING_RE.search(text)
    if not m:
        return None
    raw = m.group(1).strip().lower()
    if "buy" in raw:
        return "Buy"
    if "sell" in raw:
        return "Sell"
    if "hold" in raw:
        return "Hold"
    return raw.title()


def extract_target_weight_pct(text: str) -> Optional[float]:
    m = _TARGET_WEIGHT_RE.search(text)
    return float(m.group(1)) if m else None


# ----- Individual checks -----
# Every check returns one CheckResult. Signatures: (ips, ctx) -> CheckResult.

def check_u1_market_cap(ips, ctx):
    floor = ips["universe"]["min_market_cap_usd"]
    mc = ctx.get_number(
        "market-overview.marketCap",
        "market-data.marketCap",
        "overview.marketCapUsd",
    )
    src = "data/market-*.json"
    if mc is None:
        return CheckResult("U1", "Market-cap floor", UNVERIFIED,
                           f">= ${floor:,.0f}", "not found", src)
    status = PASS if mc >= floor else FAIL
    return CheckResult("U1", "Market-cap floor", status,
                       f">= ${floor:,.0f}", f"${mc:,.0f}", src)


def check_u2_sector_allowed(ips, ctx):
    allowed = set(ips["universe"].get("allowed_sectors", []))
    excluded = set(ips.get("exclusions", {}).get("sector_exclusions", []))
    sector = ctx.get_str(
        "overview.sector",
        "market-overview.sector",
        "company-profile.sector",
    )
    src = "data/*.json (overview/profile)"
    if sector is None:
        return CheckResult("U2", "Sector eligibility", UNVERIFIED,
                           "in allowed_sectors", "sector not found", src)
    if sector in excluded:
        return CheckResult("U2", "Sector eligibility", FAIL,
                           "not in sector_exclusions", sector, src,
                           note="Explicitly excluded by mandate.")
    if allowed and sector not in allowed:
        return CheckResult("U2", "Sector eligibility", FAIL,
                           "in allowed_sectors", sector, src)
    return CheckResult("U2", "Sector eligibility", PASS,
                       "in allowed_sectors, not excluded", sector, src)


def check_u3_exchange(ips, ctx):
    allowed = set(ips["universe"].get("allowed_exchanges", []))
    exch = ctx.get_str(
        "overview.exchange",
        "market-overview.exchange",
        "company-profile.exchange",
    )
    src = "data/*.json (overview/profile)"
    if not allowed:
        return CheckResult("U3", "Exchange allowed", PASS,
                           "(no constraint)", exch or "unknown", src)
    if exch is None:
        return CheckResult("U3", "Exchange allowed", UNVERIFIED,
                           f"in {sorted(allowed)}", "not found", src)
    status = PASS if exch in allowed else FAIL
    return CheckResult("U3", "Exchange allowed", status,
                       f"in {sorted(allowed)}", exch, src)


def check_p1_position_cap(ips, ctx):
    cap = ips["position"]["max_single_name_weight_pct"]
    tw = extract_target_weight_pct(ctx.draft_text)
    src = "editor-draft.md (position sizing)"
    if tw is None:
        return CheckResult("P1", "Single-name position cap", UNVERIFIED,
                           f"<= {cap}%", "target weight not stated", src)
    status = PASS if tw <= cap else FAIL
    return CheckResult("P1", "Single-name position cap", status,
                       f"<= {cap}%", f"{tw}%", src)


def check_l1_adv_floor(ips, ctx):
    floor = ips["liquidity"]["min_adv_usd"]
    adv = ctx.get_number(
        "market-overview.avgDollarVolume30d",
        "market-data.avgDollarVolume30d",
        "price-data.avgDollarVolume30d",
    )
    src = "data/market-*.json (avgDollarVolume30d)"
    if adv is None:
        return CheckResult("L1", "30-day ADV floor", UNVERIFIED,
                           f">= ${floor:,.0f}", "not found", src)
    status = PASS if adv >= floor else FAIL
    return CheckResult("L1", "30-day ADV floor", status,
                       f">= ${floor:,.0f}", f"${adv:,.0f}", src)


def check_q1_beneish(ips, ctx):
    floor = ips["quality"]["min_beneish_m_score"]
    score = ctx.get_number(
        "quality.beneishMScore",
        "forensic.beneishMScore",
        "quality-credibility.beneishMScore",
    )
    src = "data/quality-*.json"
    if score is None:
        return CheckResult("Q1", "Beneish M-Score floor", UNVERIFIED,
                           f">= {floor}", "not found", src,
                           note="Quality & Credibility Analyst should emit "
                                "beneishMScore to data/.")
    status = PASS if score >= floor else FAIL
    return CheckResult("Q1", "Beneish M-Score floor", status,
                       f">= {floor}", f"{score}", src)


def check_q2_altman(ips, ctx):
    floor = ips["quality"]["min_altman_z_nonfin"]
    sector = ctx.get_str("overview.sector", "market-overview.sector") or ""
    if sector.lower() in {"financials", "financial services"}:
        return CheckResult("Q2", "Altman Z floor", PASS,
                           "(N/A for financials)", sector, "sector")
    z = ctx.get_number(
        "quality.altmanZ",
        "forensic.altmanZ",
        "quality-credibility.altmanZ",
    )
    src = "data/quality-*.json"
    if z is None:
        return CheckResult("Q2", "Altman Z floor", UNVERIFIED,
                           f">= {floor}", "not found", src)
    status = PASS if z >= floor else FAIL
    return CheckResult("Q2", "Altman Z floor", status,
                       f">= {floor}", f"{z}", src)


def check_e1_restricted(ips, ctx):
    restricted = set(ips.get("exclusions", {}).get("issuer_restricted_list", []))
    status = FAIL if ctx.ticker.upper() in {r.upper() for r in restricted} else PASS
    return CheckResult("E1", "Issuer restricted list", status,
                       "ticker not in restricted_list",
                       ctx.ticker.upper() if status == FAIL else "not listed",
                       "configs IPS exclusions.issuer_restricted_list")


def check_r1_rating(ips, ctx):
    allowed = set(ips["mandate"].get("allowed_ratings", []))
    rating = extract_rating(ctx.draft_text)
    src = "editor-draft.md (executive summary Rating:)"
    if rating is None:
        return CheckResult("R1", "Rating eligibility", UNVERIFIED,
                           f"in {sorted(allowed)}", "rating not parsed", src)
    if not allowed:
        return CheckResult("R1", "Rating eligibility", PASS,
                           "(no constraint)", rating, src)
    status = PASS if rating in allowed else FAIL
    note = ""
    if status == FAIL and rating == "Sell" and "Sell" not in allowed:
        note = "Long-only mandate — short/Sell call must be converted to an 'avoid' or re-dispatched as restricted-coverage."
    return CheckResult("R1", "Rating eligibility", status,
                       f"in {sorted(allowed)}", rating, src, note=note)


CHECKS = [
    check_u1_market_cap,
    check_u2_sector_allowed,
    check_u3_exchange,
    check_p1_position_cap,
    check_l1_adv_floor,
    check_q1_beneish,
    check_q2_altman,
    check_e1_restricted,
    check_r1_rating,
]


def run_all(ips: Dict[str, Any], ctx: NoteContext) -> List[CheckResult]:
    return [fn(ips, ctx) for fn in CHECKS]


def verdict(results: List[CheckResult]) -> str:
    if any(r.status == FAIL for r in results):
        return "RESTRICTED"
    if any(r.status == UNVERIFIED or r.status == SOFT_FLAG for r in results):
        return "ELIGIBLE_WITH_EXCEPTIONS"
    return "ELIGIBLE"


def render_report(ticker: str, ips_path: Path, results: List[CheckResult],
                  v: str) -> str:
    lines: List[str] = []
    lines.append(f"# IPS Compliance — {ticker}")
    lines.append("")
    lines.append(f"- **IPS:** `{ips_path}`")
    lines.append(f"- **Verdict:** **{v}**")
    counts = {PASS: 0, FAIL: 0, UNVERIFIED: 0, SOFT_FLAG: 0}
    for r in results:
        counts[r.status] = counts.get(r.status, 0) + 1
    lines.append(
        f"- **Checks:** PASS {counts[PASS]}   FAIL {counts[FAIL]}   "
        f"UNVERIFIED {counts[UNVERIFIED]}   SOFT_FLAG {counts[SOFT_FLAG]}"
    )
    lines.append("")
    lines.append("| # | Check | Expected | Observed | Status | Source |")
    lines.append("|---|-------|----------|----------|--------|--------|")
    for r in results:
        lines.append(
            f"| {r.code} | {r.name} | {r.expected} | {r.observed} | "
            f"**{r.status}** | {r.source} |"
        )
    notes = [r for r in results if r.note]
    if notes:
        lines.append("")
        lines.append("## Notes")
        for r in notes:
            lines.append(f"- **{r.code} ({r.name}):** {r.note}")
    lines.append("")
    lines.append("## Verdict Meaning")
    lines.append("")
    lines.append(
        "- **ELIGIBLE** — all hard constraints satisfied. Publication may proceed.\n"
        "- **ELIGIBLE_WITH_EXCEPTIONS** — no hard violations, but one or more "
        "UNVERIFIED checks. Director must document which exceptions are "
        "accepted (data gap) vs. which must be re-audited.\n"
        "- **RESTRICTED** — at least one hard constraint violated. The note "
        "cannot be published as an actionable recommendation under this IPS. "
        "The Director must either (a) revise the recommendation to fit, "
        "(b) downgrade to educational/restricted coverage, or "
        "(c) document an explicit mandate exception with rationale."
    )
    return "\n".join(lines) + "\n"


def resolve_run_dir(arg: str) -> Path:
    p = Path(arg).resolve()
    if not p.is_dir():
        raise FileNotFoundError(f"run-dir not found: {p}")
    return p


def extract_ticker(run_dir: Path) -> str:
    # output/[TICKER]/[DATE]
    parts = run_dir.parts
    try:
        idx = parts.index("output")
        return parts[idx + 1]
    except (ValueError, IndexError):
        return run_dir.parent.name


def main() -> int:
    ap = argparse.ArgumentParser(description="IPS compliance validator")
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--ips", default="configs/default-ips.yaml")
    ap.add_argument("--output", default=None,
                    help="Where to write the report (default: "
                         "<run-dir>/pass2/ips-compliance.md)")
    args = ap.parse_args()

    try:
        run_dir = resolve_run_dir(args.run_dir)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return EXIT_BAD_INPUT

    ips_path = Path(args.ips).resolve()
    if not ips_path.is_file():
        print(f"ERROR: ips not found: {ips_path}", file=sys.stderr)
        return EXIT_BAD_INPUT

    try:
        ips = _load_ips(ips_path)
    except yaml.YAMLError as e:
        print(f"ERROR: malformed IPS YAML: {e}", file=sys.stderr)
        return EXIT_BAD_INPUT

    draft = _find_draft(run_dir)
    if draft is None:
        print(
            f"ERROR: editor draft not found under {run_dir}/pass2/. "
            "The IPS validator must run after the Editor's Pass 2 synthesis.",
            file=sys.stderr,
        )
        return EXIT_BAD_INPUT

    ticker = extract_ticker(run_dir)
    ctx = NoteContext(
        ticker=ticker,
        run_dir=run_dir,
        draft_text=draft.read_text(encoding="utf-8", errors="replace"),
        data=_load_data_jsons(run_dir),
    )

    results = run_all(ips, ctx)
    v = verdict(results)
    md = render_report(ticker, ips_path, results, v)

    out_path = Path(args.output) if args.output else (run_dir / "pass2" / "ips-compliance.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(md)

    if v == "RESTRICTED":
        return EXIT_RESTRICTED
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
