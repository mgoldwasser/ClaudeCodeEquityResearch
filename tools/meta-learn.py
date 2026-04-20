#!/usr/bin/env python3
"""
Meta-Learning Loop v1 — Human-in-the-Loop Prompt Evolution
===========================================================

Narrow scope (v1):
  - One agent at a time (default: dcf-analyst)
  - One prediction type at a time (fair value + revenue CAGR)
  - Only notes with >=6 months of realized data are graded
  - The proposer detects systematic bias but does NOT auto-patch;
    every approved edit is a human-reviewed commit

Three subcommands:

  grade     For a run directory, compute a grade record at horizons 6m/12m.
            If the horizon has not elapsed yet, write status=PENDING; if it
            has elapsed, fetch realized price via tools/market-data.sh and
            write status=GRADED with residuals + Brier score.

  propose   Read all GRADED records. If an agent's fair-value residual has
            persistent sign across >= --min-samples notes AND |mean bias|
            exceeds --bias-threshold, emit a markdown proposal under
            output/meta-learning/proposals/ with a candidate prompt edit.
            The proposer is a starting point, not an answer — operator
            reads, refines, approves or rejects.

  review    List pending proposals, show diffs, approve or reject.
            Approve:
              - copies current agent file to
                prompts/history/<agent>/<YYYY-MM-DD>-<slug>/before.md
              - applies the old_string->new_string edit
              - writes after.md, rationale.md, metadata.json
              - moves the proposal to .../approved/
            Reject:
              - moves the proposal to .../rejected/ with rejection rationale

What this is and isn't
----------------------
This ships the mechanism. At v1-launch, there are ~0 notes with >=6mo
realized data — the first real learning signal is ~Q1 2027 (12mo after
the 2026-03 cohort). Shipping the mechanism with a visible "tracking
begins now" state is deliberate: the claim is reproducible discipline,
not instant insight.

What this is NOT: an autonomous self-rewriting agent. Every prompt change
is human-reviewed and git-committed. The reason is signal latency: for
fundamental research, a bad quarter can corrupt prompts for years if
auto-applied. Human review is slower but sound.

Contract
--------
  grade
    --run-dir output/<TICKER>/<DATE>   required
    --horizons "6,12"                  default (months)
    --grades-file PATH                 default output/meta-learning/grades.jsonl
    --force                            regrade even if record already GRADED

  propose
    --agent dcf-analyst                default
    --min-samples 3                    minimum graded notes required
    --bias-threshold-pct 10.0          minimum |mean residual %| to fire
    --grades-file PATH                 default output/meta-learning/grades.jsonl
    --proposals-dir PATH               default output/meta-learning/proposals

  review
    --list                             list pending proposals (default)
    --approve <proposal_id>            apply the edit + snapshot to history
    --reject <proposal_id>             move to rejected/
    --reason "..."                     required with --reject

Exit codes:
  0  success
  1  bad input
  2  no-op (pending grades, no bias detected, etc.) — distinct from error
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


EXIT_OK = 0
EXIT_BAD_INPUT = 1
EXIT_NOOP = 2

GRADES_DEFAULT = "output/meta-learning/grades.jsonl"
PROPOSALS_DEFAULT = "output/meta-learning/proposals"
HISTORY_DEFAULT = "prompts/history"


# ----------------------------------------------------------------------
# Extraction — parse final research note and DCF analysis for grading inputs
# ----------------------------------------------------------------------

PRICE_TARGET_RE = re.compile(
    r"\*\*12-Month Price Target:\*\*\s*\$(\d[\d,]*(?:\.\d+)?)",
    re.IGNORECASE,
)
CURRENT_PRICE_RE = re.compile(
    r"current price of \$(\d[\d,]*(?:\.\d+)?)|Current:\s*\$(\d[\d,]*(?:\.\d+)?)",
    re.IGNORECASE,
)
CONVICTION_RE = re.compile(
    r"\*\*Conviction(?:\s+Rating)?:?\*\*\s*([0-5])\s*/\s*5",
    re.IGNORECASE,
)
SCENARIO_LINE_RE = re.compile(
    r"Bull\s*\$?(\d[\d,]*(?:\.\d+)?)\s*@\s*([0-9]+(?:\.[0-9]+)?)%\s*/\s*"
    r"Base\s*\$?(\d[\d,]*(?:\.\d+)?)\s*@\s*([0-9]+(?:\.[0-9]+)?)%\s*/\s*"
    r"Bear\s*\$?(\d[\d,]*(?:\.\d+)?)\s*@\s*([0-9]+(?:\.[0-9]+)?)%",
    re.IGNORECASE,
)
DCF_BASE_FV_RE = re.compile(
    r"(?:DCF|Base[\s-]case|Base)\s*[Ff]air\s*[Vv]alue[^$]{0,40}\$"
    r"(\d[\d,]*(?:\.\d+)?)",
    re.IGNORECASE,
)
DCF_WACC_RE = re.compile(
    r"WACC\s*(?:\(Base\)|Base[^0-9]{0,20}|[^0-9]{0,30})"
    r"(\d+(?:\.\d+)?)\s*%",
    re.IGNORECASE,
)
DCF_TGR_RE = re.compile(
    r"[Tt]erminal\s*[Gg]rowth\s*(?:[Rr]ate)?[:\s]*"
    r"([0-9]+(?:\.[0-9]+)?)\s*%"
)


def _as_float(s: str) -> float:
    return float(s.replace(",", ""))


def _extract_note_fields(note_path: Path) -> Dict[str, Any]:
    text = note_path.read_text(encoding="utf-8")
    out: Dict[str, Any] = {
        "price_target": None,
        "current_price_at_call": None,
        "conviction": None,
        "scenarios": None,
    }

    m = PRICE_TARGET_RE.search(text)
    if m:
        out["price_target"] = _as_float(m.group(1))

    for m in CURRENT_PRICE_RE.finditer(text):
        val = m.group(1) or m.group(2)
        if val:
            out["current_price_at_call"] = _as_float(val)
            break

    m = CONVICTION_RE.search(text)
    if m:
        out["conviction"] = int(m.group(1))

    m = SCENARIO_LINE_RE.search(text)
    if m:
        out["scenarios"] = {
            "bull": {"price": _as_float(m.group(1)),
                     "prob": float(m.group(2)) / 100.0},
            "base": {"price": _as_float(m.group(3)),
                     "prob": float(m.group(4)) / 100.0},
            "bear": {"price": _as_float(m.group(5)),
                     "prob": float(m.group(6)) / 100.0},
        }

    return out


def _extract_dcf_fields(dcf_path: Path) -> Dict[str, Any]:
    if not dcf_path.is_file():
        return {}
    text = dcf_path.read_text(encoding="utf-8")
    out: Dict[str, Any] = {}

    m = DCF_BASE_FV_RE.search(text)
    if m:
        out["fair_value_base"] = _as_float(m.group(1))
    m = DCF_WACC_RE.search(text)
    if m:
        out["wacc_base"] = float(m.group(1))
    m = DCF_TGR_RE.search(text)
    if m:
        out["terminal_growth"] = float(m.group(1))
    return out


# ----------------------------------------------------------------------
# Realized-price fetch via tools/market-data.sh history
# ----------------------------------------------------------------------

def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _fetch_realized_price(ticker: str, grade_date: date) -> Optional[float]:
    """Return the close price of the last trading day on or before grade_date.

    Uses tools/market-data.sh history with --as-of. Returns None on failure.
    """
    script = _repo_root() / "tools" / "market-data.sh"
    if not script.is_file():
        return None
    cmd = [str(script), "history", ticker, "1mo",
           "--as-of", grade_date.isoformat()]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    if proc.returncode != 0:
        return None
    # The script prints a banner then JSON; find the JSON block.
    stdout = proc.stdout
    start = stdout.find("{")
    if start < 0:
        return None
    try:
        data = json.loads(stdout[start:])
    except json.JSONDecodeError:
        return None
    summary = data.get("summary") or {}
    px = summary.get("end_price")
    if isinstance(px, (int, float)):
        return float(px)
    return None


# ----------------------------------------------------------------------
# Grading
# ----------------------------------------------------------------------

@dataclass
class GradeRecord:
    grade_id: str
    ticker: str
    note_date: str
    note_path: str
    horizon_months: int
    target_grade_date: str
    price_target: Optional[float]
    current_price_at_call: Optional[float]
    conviction: Optional[int]
    scenarios: Optional[Dict[str, Any]]
    dcf_analyst: Dict[str, Any] = field(default_factory=dict)
    status: str = "PENDING"          # PENDING | GRADED | UNGRADEABLE
    graded_at: Optional[str] = None
    realized_price: Optional[float] = None
    realized_return_pct: Optional[float] = None
    directional_hit: Optional[bool] = None
    magnitude_error_pct: Optional[float] = None
    brier_score: Optional[float] = None
    unmet_reason: Optional[str] = None


def _add_months(d: date, months: int) -> date:
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    day = min(d.day, 28)
    return date(y, m, day)


def _locate_note(run_dir: Path) -> Optional[Path]:
    parts = run_dir.parts
    try:
        idx = parts.index("output")
        ticker = parts[idx + 1]
        run_date = parts[idx + 2]
    except (ValueError, IndexError):
        return None
    candidate = run_dir / f"{ticker}-research-note-{run_date}.md"
    if candidate.is_file():
        return candidate
    for p in run_dir.glob(f"{ticker}-research-note-*.md"):
        return p
    return None


def _dcf_path(run_dir: Path) -> Path:
    return run_dir / "pass1" / "dcf-analysis.md"


def _brier(scenarios: Optional[Dict[str, Any]],
           realized: float) -> Optional[float]:
    """Compute a 3-bucket Brier score against the realized price.

    The realized price is assigned to the nearest scenario bucket (bull, base,
    bear) by absolute distance. Brier = sum((p_i - o_i)^2), where o_i is 1
    for the realized bucket and 0 otherwise.
    """
    if not scenarios:
        return None
    try:
        probs = {k: float(scenarios[k]["prob"]) for k in ("bull", "base", "bear")}
        prices = {k: float(scenarios[k]["price"]) for k in ("bull", "base", "bear")}
    except (KeyError, TypeError):
        return None
    winner = min(prices, key=lambda k: abs(prices[k] - realized))
    brier = 0.0
    for k in ("bull", "base", "bear"):
        o = 1.0 if k == winner else 0.0
        brier += (probs[k] - o) ** 2
    return round(brier, 4)


def _grade_one(run_dir: Path, horizon_months: int,
               existing: Optional[GradeRecord]) -> GradeRecord:
    parts = run_dir.parts
    idx = parts.index("output")
    ticker = parts[idx + 1]
    run_date_str = parts[idx + 2]
    note_date = date.fromisoformat(run_date_str)
    target_date = _add_months(note_date, horizon_months)
    grade_id = f"{ticker}-{run_date_str}-{horizon_months}m"

    note_path = _locate_note(run_dir)
    if note_path is None:
        return GradeRecord(
            grade_id=grade_id, ticker=ticker, note_date=run_date_str,
            note_path=str(run_dir), horizon_months=horizon_months,
            target_grade_date=target_date.isoformat(),
            price_target=None, current_price_at_call=None,
            conviction=None, scenarios=None,
            status="UNGRADEABLE",
            unmet_reason="research note not found in run dir",
        )

    fields = _extract_note_fields(note_path)
    dcf = _extract_dcf_fields(_dcf_path(run_dir))

    rec = GradeRecord(
        grade_id=grade_id,
        ticker=ticker,
        note_date=run_date_str,
        note_path=str(note_path.relative_to(_repo_root())),
        horizon_months=horizon_months,
        target_grade_date=target_date.isoformat(),
        price_target=fields["price_target"],
        current_price_at_call=fields["current_price_at_call"],
        conviction=fields["conviction"],
        scenarios=fields["scenarios"],
        dcf_analyst=dcf,
    )

    today = date.today()
    if today < target_date:
        rec.status = "PENDING"
        rec.unmet_reason = f"horizon not elapsed (target {target_date.isoformat()})"
        return rec

    realized = _fetch_realized_price(ticker, target_date)
    if realized is None:
        rec.status = "UNGRADEABLE"
        rec.unmet_reason = "market-data.sh history returned no price for target date"
        return rec

    rec.status = "GRADED"
    rec.graded_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    rec.realized_price = realized
    if rec.current_price_at_call and rec.current_price_at_call > 0:
        rec.realized_return_pct = round(
            (realized / rec.current_price_at_call - 1.0) * 100.0, 3)
    if rec.price_target and rec.current_price_at_call:
        # Directional hit: did the stock move toward the target vs current?
        target_dir = rec.price_target - rec.current_price_at_call
        realized_dir = realized - rec.current_price_at_call
        rec.directional_hit = (target_dir > 0 and realized_dir > 0) or \
                              (target_dir < 0 and realized_dir < 0) or \
                              (abs(target_dir) < 1e-6 and abs(realized_dir) < 1e-6)
    if rec.price_target and rec.price_target > 0:
        rec.magnitude_error_pct = round(
            abs(rec.price_target - realized) / rec.price_target * 100.0, 3)
    rec.brier_score = _brier(rec.scenarios, realized)
    return rec


def _load_grades(grades_path: Path) -> List[GradeRecord]:
    if not grades_path.is_file():
        return []
    out: List[GradeRecord] = []
    for line in grades_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        out.append(GradeRecord(**obj))
    return out


def _save_grades(grades_path: Path, grades: List[GradeRecord]) -> None:
    grades_path.parent.mkdir(parents=True, exist_ok=True)
    with grades_path.open("w", encoding="utf-8") as f:
        for g in grades:
            f.write(json.dumps(asdict(g), sort_keys=True))
            f.write("\n")


def cmd_grade(args: argparse.Namespace) -> int:
    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
        print(f"ERROR: run-dir not found: {run_dir}", file=sys.stderr)
        return EXIT_BAD_INPUT
    try:
        horizons = [int(h.strip()) for h in args.horizons.split(",") if h.strip()]
    except ValueError:
        print(f"ERROR: --horizons must be comma-separated integers", file=sys.stderr)
        return EXIT_BAD_INPUT

    grades_path = Path(args.grades_file)
    existing = _load_grades(grades_path)
    by_id = {g.grade_id: g for g in existing}

    updated: List[GradeRecord] = []
    for h in horizons:
        rec = _grade_one(run_dir, h, by_id.get(
            f"{run_dir.parts[run_dir.parts.index('output')+1]}-"
            f"{run_dir.parts[run_dir.parts.index('output')+2]}-{h}m"))
        prior = by_id.get(rec.grade_id)
        if prior and prior.status == "GRADED" and not args.force:
            updated.append(prior)
            continue
        by_id[rec.grade_id] = rec
        updated.append(rec)

    out_list = list(by_id.values())
    out_list.sort(key=lambda r: (r.note_date, r.ticker, r.horizon_months))
    _save_grades(grades_path, out_list)

    summary = {
        "run_dir": str(run_dir),
        "horizons": horizons,
        "total_records": len(out_list),
        "this_run": [
            {"grade_id": r.grade_id, "status": r.status,
             "unmet_reason": r.unmet_reason,
             "realized_return_pct": r.realized_return_pct,
             "magnitude_error_pct": r.magnitude_error_pct,
             "brier_score": r.brier_score}
            for r in updated
        ],
    }
    print(json.dumps(summary, indent=2))
    return EXIT_OK


# ----------------------------------------------------------------------
# Propose — detect systematic bias in an agent's fair-value residuals
# ----------------------------------------------------------------------

def _graded_for_agent(grades: List[GradeRecord],
                      agent: str) -> List[GradeRecord]:
    if agent != "dcf-analyst":
        # v1 only supports dcf-analyst. Other agents: return empty + warn.
        return []
    out: List[GradeRecord] = []
    for g in grades:
        if g.status != "GRADED":
            continue
        if not g.dcf_analyst.get("fair_value_base"):
            continue
        if g.realized_price is None:
            continue
        out.append(g)
    return out


def _residuals(eligible: List[GradeRecord]) -> List[Tuple[GradeRecord, float]]:
    """Return (record, residual_pct) tuples. Positive residual = agent too
    conservative (fair value < realized). Negative = too optimistic."""
    out: List[Tuple[GradeRecord, float]] = []
    for g in eligible:
        fv = g.dcf_analyst["fair_value_base"]
        rp = g.realized_price
        if not (fv and rp and fv > 0):
            continue
        residual_pct = (rp - fv) / fv * 100.0
        out.append((g, residual_pct))
    return out


def _slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def cmd_propose(args: argparse.Namespace) -> int:
    grades_path = Path(args.grades_file)
    grades = _load_grades(grades_path)
    eligible = _graded_for_agent(grades, args.agent)

    if args.agent != "dcf-analyst":
        print(f"NOTE: v1 proposer supports dcf-analyst only. "
              f"Requested: {args.agent}. Exiting no-op.", file=sys.stderr)
        return EXIT_NOOP

    if len(eligible) < args.min_samples:
        msg = {
            "status": "NO_PROPOSAL",
            "reason": "insufficient graded samples",
            "eligible_count": len(eligible),
            "min_samples": args.min_samples,
            "note": ("Meta-learner has no signal yet. First real learning "
                     "signal arrives ~6-12 months after earliest note date."),
        }
        print(json.dumps(msg, indent=2))
        return EXIT_NOOP

    residuals = _residuals(eligible)
    mean_bias = sum(r for _, r in residuals) / len(residuals)
    same_sign = sum(1 for _, r in residuals if (r >= 0) == (mean_bias >= 0))
    sign_share = same_sign / len(residuals)

    if abs(mean_bias) < args.bias_threshold_pct or sign_share < 0.65:
        msg = {
            "status": "NO_PROPOSAL",
            "reason": "no systematic bias detected",
            "mean_bias_pct": round(mean_bias, 2),
            "sign_share": round(sign_share, 2),
            "threshold_pct": args.bias_threshold_pct,
            "sign_share_threshold": 0.65,
            "eligible_count": len(eligible),
        }
        print(json.dumps(msg, indent=2))
        return EXIT_NOOP

    proposals_dir = Path(args.proposals_dir) / "pending"
    proposals_dir.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    direction = "conservative" if mean_bias > 0 else "optimistic"
    slug = _slugify(f"{args.agent}-fair-value-{direction}")
    proposal_id = f"{today}-{slug}"
    proposal_path = proposals_dir / f"{proposal_id}.md"

    table_rows = "\n".join(
        f"| {g.ticker} | {g.note_date} | ${g.dcf_analyst['fair_value_base']:,.2f} | "
        f"${g.realized_price:,.2f} | {r:+.2f}% |"
        for g, r in residuals
    )

    # Heuristic candidate edit — operator is expected to refine.
    if mean_bias > 0:
        edit_note = ("Base-case assumptions appear conservative. Candidate "
                     "levers (pick one after analysis): terminal growth rate "
                     "default, exit multiple, or revenue CAGR band.")
    else:
        edit_note = ("Base-case assumptions appear optimistic. Candidate "
                     "levers (pick one after analysis): WACC, terminal growth "
                     "rate default, or bear-probability floor.")

    body = f"""---
proposal_id: {proposal_id}
agent: {args.agent}
agent_file: agents/{args.agent}.md
created: {today}
status: pending
samples: {len(residuals)}
mean_bias_pct: {round(mean_bias, 2)}
sign_share: {round(sign_share, 2)}
direction: {direction}
---

# Proposal: {args.agent} fair value appears systematically {direction}

## Finding

Across {len(residuals)} graded notes, the {args.agent}'s base-case fair
value has a mean residual of **{mean_bias:+.2f}%** relative to realized
price, with {sign_share*100:.0f}% of notes showing the same-sign error.

## Residuals

| Ticker | Note date | DCF base FV | Realized | Residual |
|--------|-----------|-------------|----------|----------|
{table_rows}

## Hypothesis

{edit_note}

## Proposed edit (operator to refine)

**File:** `agents/{args.agent}.md`

The tool did not auto-generate `old_string` / `new_string` — v1 requires
the operator to read the residual pattern, identify the specific lever to
move, and fill in the edit block below before approving.

```yaml
old_string: |
  <paste verbatim from agents/{args.agent}.md>

new_string: |
  <proposed replacement>

rationale: |
  <one paragraph: why this lever, why this magnitude, what it costs if wrong>
```

## How to approve

1. Edit this file to fill in `old_string`, `new_string`, and `rationale`.
2. Run `python tools/meta-learn.py review --approve {proposal_id}`.

## How to reject

`python tools/meta-learn.py review --reject {proposal_id} --reason "..."`
"""
    proposal_path.write_text(body, encoding="utf-8")
    print(json.dumps({
        "status": "PROPOSAL_WRITTEN",
        "proposal_id": proposal_id,
        "path": str(proposal_path),
        "mean_bias_pct": round(mean_bias, 2),
        "eligible_count": len(residuals),
    }, indent=2))
    return EXIT_OK


# ----------------------------------------------------------------------
# Review — approve / reject
# ----------------------------------------------------------------------

YAML_BLOCK_RE = re.compile(
    r"```yaml\s*\n(.*?)\n```", re.DOTALL
)


def _parse_edit_block(proposal_text: str) -> Optional[Dict[str, str]]:
    """Extract old_string / new_string / rationale from the yaml block.

    The proposal embeds them as YAML with block scalars. To avoid a PyYAML
    dependency just for this, parse the simple block-scalar format manually.
    """
    m = YAML_BLOCK_RE.search(proposal_text)
    if not m:
        return None
    block = m.group(1)
    # Split into three sections by top-level keys old_string:/new_string:/rationale:
    fields: Dict[str, List[str]] = {"old_string": [], "new_string": [], "rationale": []}
    current = None
    for line in block.splitlines():
        if re.match(r"^old_string:\s*\|?\s*$", line):
            current = "old_string"
            continue
        if re.match(r"^new_string:\s*\|?\s*$", line):
            current = "new_string"
            continue
        if re.match(r"^rationale:\s*\|?\s*$", line):
            current = "rationale"
            continue
        if current is None:
            continue
        # Strip the 2-space indent of block scalars when present.
        if line.startswith("  "):
            fields[current].append(line[2:])
        elif line.strip() == "":
            fields[current].append("")
        else:
            # Unindented non-empty line = next key or invalid. Stop current.
            current = None
    out = {k: "\n".join(v).rstrip() for k, v in fields.items()}
    if not out["old_string"] or not out["new_string"]:
        return None
    if out["old_string"].strip().startswith("<paste verbatim"):
        return None
    return out


def _pending_dir(proposals_dir: Path) -> Path:
    return proposals_dir / "pending"


def _list_pending(proposals_dir: Path) -> List[Path]:
    d = _pending_dir(proposals_dir)
    if not d.is_dir():
        return []
    return sorted(d.glob("*.md"))


def _frontmatter(text: str) -> Dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    out: Dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def cmd_review(args: argparse.Namespace) -> int:
    proposals_dir = Path(args.proposals_dir)

    if args.reject:
        if not args.reason:
            print("ERROR: --reject requires --reason", file=sys.stderr)
            return EXIT_BAD_INPUT
        src = _pending_dir(proposals_dir) / f"{args.reject}.md"
        if not src.is_file():
            print(f"ERROR: no pending proposal {args.reject}", file=sys.stderr)
            return EXIT_BAD_INPUT
        dst_dir = (proposals_dir / "rejected").resolve()
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / src.name
        text = src.read_text(encoding="utf-8")
        text = re.sub(r"status:\s*pending", "status: rejected", text)
        text += (f"\n\n## Rejection\n\n- **Rejected at:** "
                 f"{datetime.now(timezone.utc).isoformat()}\n"
                 f"- **Reason:** {args.reason}\n")
        dst.write_text(text, encoding="utf-8")
        src.unlink()
        try:
            rel = dst.relative_to(_repo_root())
            print(json.dumps({"status": "REJECTED", "path": str(rel)}, indent=2))
        except ValueError:
            print(json.dumps({"status": "REJECTED", "path": str(dst)}, indent=2))
        return EXIT_OK

    if args.approve:
        src = _pending_dir(proposals_dir) / f"{args.approve}.md"
        if not src.is_file():
            print(f"ERROR: no pending proposal {args.approve}", file=sys.stderr)
            return EXIT_BAD_INPUT
        text = src.read_text(encoding="utf-8")
        fm = _frontmatter(text)
        agent = fm.get("agent")
        if not agent:
            print(f"ERROR: proposal missing `agent` in frontmatter",
                  file=sys.stderr)
            return EXIT_BAD_INPUT
        agent_file = _repo_root() / "agents" / f"{agent}.md"
        if not agent_file.is_file():
            print(f"ERROR: agent file not found: {agent_file}",
                  file=sys.stderr)
            return EXIT_BAD_INPUT

        edit = _parse_edit_block(text)
        if edit is None:
            print(f"ERROR: proposal {args.approve} has no valid edit "
                  f"block. Fill in old_string/new_string/rationale first.",
                  file=sys.stderr)
            return EXIT_BAD_INPUT

        agent_text = agent_file.read_text(encoding="utf-8")
        count = agent_text.count(edit["old_string"])
        if count == 0:
            print(f"ERROR: old_string not found in {agent_file}. "
                  f"The agent file may have drifted since the proposal was "
                  f"written.", file=sys.stderr)
            return EXIT_BAD_INPUT
        if count > 1:
            print(f"ERROR: old_string matches {count} times in {agent_file}. "
                  f"Add surrounding context to make it unique.",
                  file=sys.stderr)
            return EXIT_BAD_INPUT

        # Snapshot before/after to prompts/history/<agent>/<proposal_id>/
        hist_dir = _repo_root() / HISTORY_DEFAULT / agent / args.approve
        hist_dir.mkdir(parents=True, exist_ok=True)
        (hist_dir / "before.md").write_text(agent_text, encoding="utf-8")

        new_agent_text = agent_text.replace(edit["old_string"],
                                            edit["new_string"], 1)
        agent_file.write_text(new_agent_text, encoding="utf-8")
        (hist_dir / "after.md").write_text(new_agent_text, encoding="utf-8")
        (hist_dir / "rationale.md").write_text(
            edit["rationale"] + "\n", encoding="utf-8")
        (hist_dir / "metadata.json").write_text(json.dumps({
            "proposal_id": args.approve,
            "agent": agent,
            "agent_file": str(agent_file.relative_to(_repo_root())),
            "approved_at": datetime.now(timezone.utc).isoformat().replace(
                "+00:00", "Z"),
            "mean_bias_pct": fm.get("mean_bias_pct"),
            "samples": fm.get("samples"),
            "direction": fm.get("direction"),
        }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        dst_dir = (proposals_dir / "approved").resolve()
        dst_dir.mkdir(parents=True, exist_ok=True)
        dst = dst_dir / src.name
        text = re.sub(r"status:\s*pending", "status: approved", text)
        text += (f"\n\n## Approval\n\n- **Approved at:** "
                 f"{datetime.now(timezone.utc).isoformat()}\n"
                 f"- **Snapshot:** `{hist_dir.relative_to(_repo_root())}/`\n")
        dst.write_text(text, encoding="utf-8")
        src.unlink()

        print(json.dumps({
            "status": "APPROVED",
            "proposal_id": args.approve,
            "agent_file_edited": str(agent_file.relative_to(_repo_root())),
            "history_snapshot": str(hist_dir.relative_to(_repo_root())),
            "proposal_moved_to": str(dst.relative_to(_repo_root())),
        }, indent=2))
        return EXIT_OK

    # Default: list pending
    pending = _list_pending(proposals_dir)
    if not pending:
        print(json.dumps({"pending": []}, indent=2))
        return EXIT_OK
    out = []
    for p in pending:
        fm = _frontmatter(p.read_text(encoding="utf-8"))
        out.append({
            "proposal_id": fm.get("proposal_id", p.stem),
            "agent": fm.get("agent"),
            "direction": fm.get("direction"),
            "samples": fm.get("samples"),
            "mean_bias_pct": fm.get("mean_bias_pct"),
            "path": str(p),
        })
    print(json.dumps({"pending": out}, indent=2))
    return EXIT_OK


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Meta-Learning Loop v1")
    sub = ap.add_subparsers(dest="command", required=True)

    sp_g = sub.add_parser("grade")
    sp_g.add_argument("--run-dir", required=True)
    sp_g.add_argument("--horizons", default="6,12",
                      help="Comma-separated horizon months (default: 6,12)")
    sp_g.add_argument("--grades-file", default=GRADES_DEFAULT)
    sp_g.add_argument("--force", action="store_true",
                      help="Regrade even if record is already GRADED")

    sp_p = sub.add_parser("propose")
    sp_p.add_argument("--agent", default="dcf-analyst")
    sp_p.add_argument("--min-samples", type=int, default=3)
    sp_p.add_argument("--bias-threshold-pct", type=float, default=10.0)
    sp_p.add_argument("--grades-file", default=GRADES_DEFAULT)
    sp_p.add_argument("--proposals-dir", default=PROPOSALS_DEFAULT)

    sp_r = sub.add_parser("review")
    sp_r.add_argument("--list", action="store_true",
                      help="List pending proposals (default)")
    sp_r.add_argument("--approve", default=None, metavar="PROPOSAL_ID")
    sp_r.add_argument("--reject", default=None, metavar="PROPOSAL_ID")
    sp_r.add_argument("--reason", default=None,
                      help="Required with --reject")
    sp_r.add_argument("--proposals-dir", default=PROPOSALS_DEFAULT)

    args = ap.parse_args()

    if args.command == "grade":
        return cmd_grade(args)
    if args.command == "propose":
        return cmd_propose(args)
    if args.command == "review":
        return cmd_review(args)
    return EXIT_BAD_INPUT


if __name__ == "__main__":
    sys.exit(main())
