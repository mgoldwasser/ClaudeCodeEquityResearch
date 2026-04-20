#!/usr/bin/env python3
"""
Calibration Tracker
===================
Rolls up the graded records in ``output/meta-learning/grades.jsonl`` into
calibration statistics: Brier score over time, reliability bins, and a
by-horizon breakdown. The tool is designed to degrade gracefully — an
empty or all-PENDING grade file is a normal state at launch, not an error.

Scope (v1)
----------
Aggregates at the *note* level. The only predictor currently graded is the
3-bucket scenario probability distribution attached to the final note
(dcf-analyst authored, Director-weighted). Per-analyst Brier breakdowns
are a v1.1 item and require agent-attributed predictions in the grade
record.

What's a Brier score here?
--------------------------
For a note with scenarios ``{bull:p_bull, base:p_base, bear:p_bear}`` and a
realized outcome that lands in bucket *k*, the 3-bucket Brier is:

    sum_i (p_i - 1[i == k])^2       divided by 2 to bound in [0, 1]

Lower is better. A perfectly calibrated, certain forecast hits 0; assigning
100% to the wrong bucket gives 1.

Outputs
-------
- ``output/meta-learning/calibration/calibration-report.md``
- ``output/meta-learning/calibration/calibration.json``

Usage
-----
    python tools/calibration.py \\
        --grades-file output/meta-learning/grades.jsonl \\
        --output-dir  output/meta-learning/calibration \\
        --window      20
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple


DEFAULT_GRADES = "output/meta-learning/grades.jsonl"
DEFAULT_OUT = "output/meta-learning/calibration"
DEFAULT_WINDOW = 20
DEFAULT_BINS = [(0.0, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.4),
                (0.4, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.01)]


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------

def load_grades(path: Path) -> List[Dict]:
    if not path.exists():
        return []
    records: List[Dict] = []
    with path.open("r", encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"[warn] {path}:{i}: skipping malformed record: {e}",
                      file=sys.stderr)
    return records


# ---------------------------------------------------------------------------
# Bucket attribution
# ---------------------------------------------------------------------------

def nearest_bucket(scenarios: Dict, realized_price: float) -> Optional[str]:
    """Return the bucket name ('bull'|'base'|'bear') whose price is closest
    to ``realized_price``. Returns None if scenarios malformed."""
    if not scenarios:
        return None
    best: Optional[Tuple[str, float]] = None
    for name, sc in scenarios.items():
        if not isinstance(sc, dict) or "price" not in sc:
            continue
        d = abs(float(sc["price"]) - float(realized_price))
        if best is None or d < best[1]:
            best = (name, d)
    return best[0] if best else None


def brier_3bucket(scenarios: Dict, realized_bucket: str) -> Optional[float]:
    """3-bucket Brier, normalized to [0, 1]."""
    if not scenarios or realized_bucket not in scenarios:
        return None
    buckets = ["bull", "base", "bear"]
    total = 0.0
    for b in buckets:
        sc = scenarios.get(b)
        if not isinstance(sc, dict) or "prob" not in sc:
            return None
        p = float(sc["prob"])
        y = 1.0 if b == realized_bucket else 0.0
        total += (p - y) ** 2
    # Max sum-of-squared-errors for 3 buckets with prob summing to 1 is 2
    # (all mass on the wrong bucket). Normalize so perfect=0, worst=1.
    return total / 2.0


# ---------------------------------------------------------------------------
# Aggregation
# ---------------------------------------------------------------------------

def aggregate_graded(records: List[Dict]) -> Dict:
    graded = [r for r in records if r.get("status") == "GRADED"]
    pending = [r for r in records if r.get("status") == "PENDING"]
    ungradeable = [r for r in records if r.get("status") == "UNGRADEABLE"]

    summary = {
        "total_records": len(records),
        "graded": len(graded),
        "pending": len(pending),
        "ungradeable": len(ungradeable),
    }
    if not graded:
        summary["message"] = (
            "no GRADED records yet. Tracking begins once note horizons elapse."
        )
        return {"summary": summary, "graded_records": [],
                "by_horizon": {}, "reliability": [], "rolling": []}

    by_horizon: Dict[int, List[float]] = defaultdict(list)
    hit_counts: Dict[int, Dict[str, int]] = defaultdict(
        lambda: {"hits": 0, "total": 0}
    )
    enriched: List[Dict] = []

    for r in graded:
        scen = r.get("scenarios") or {}
        realized = r.get("realized_price")
        horizon = int(r.get("horizon_months") or 0)
        bucket = nearest_bucket(scen, realized) if realized is not None else None
        brier = r.get("brier_score")
        if brier is None and bucket is not None:
            brier = brier_3bucket(scen, bucket)

        dir_hit = r.get("directional_hit")
        if isinstance(dir_hit, bool):
            hit_counts[horizon]["total"] += 1
            if dir_hit:
                hit_counts[horizon]["hits"] += 1

        if brier is not None:
            by_horizon[horizon].append(brier)

        enriched.append({
            "grade_id": r.get("grade_id"),
            "ticker": r.get("ticker"),
            "note_date": r.get("note_date"),
            "horizon_months": horizon,
            "graded_at": r.get("graded_at"),
            "realized_price": realized,
            "realized_bucket": bucket,
            "brier_score": brier,
            "directional_hit": dir_hit,
        })

    horizon_stats = {}
    for h, briers in sorted(by_horizon.items()):
        horizon_stats[str(h)] = {
            "n": len(briers),
            "mean_brier": round(statistics.fmean(briers), 4),
            "stdev_brier": round(statistics.pstdev(briers), 4)
                if len(briers) > 1 else None,
            "directional_hit_rate": (
                round(hit_counts[h]["hits"] / hit_counts[h]["total"], 4)
                if hit_counts[h]["total"] > 0 else None
            ),
            "n_directional": hit_counts[h]["total"],
        }

    all_briers = [b for bs in by_horizon.values() for b in bs]
    if all_briers:
        summary["mean_brier"] = round(statistics.fmean(all_briers), 4)
        summary["stdev_brier"] = (
            round(statistics.pstdev(all_briers), 4)
            if len(all_briers) > 1 else None
        )

    total_dir = sum(v["total"] for v in hit_counts.values())
    hit_dir = sum(v["hits"] for v in hit_counts.values())
    summary["directional_hit_rate"] = (
        round(hit_dir / total_dir, 4) if total_dir > 0 else None
    )

    return {
        "summary": summary,
        "graded_records": enriched,
        "by_horizon": horizon_stats,
    }


def reliability_bins(graded_records: List[Dict],
                     grade_rows: List[Dict],
                     bins: List[Tuple[float, float]] = None) -> List[Dict]:
    """For each predicted-probability bin, report the empirical frequency
    that the predicted bucket was the realized bucket.

    We use the *bucket assigned the highest probability* as the prediction
    and check whether realized_bucket matches it. This collapses the three
    scenario probabilities into one binary prediction per note. A more
    granular variant (one observation per scenario) is v1.1 scope.
    """
    if bins is None:
        bins = DEFAULT_BINS
    by_id = {r["grade_id"]: r for r in graded_records}
    bin_data = [{"lo": lo, "hi": hi, "n": 0, "hits": 0, "pred_probs": []}
                for lo, hi in bins]

    for raw in grade_rows:
        if raw.get("status") != "GRADED":
            continue
        gid = raw.get("grade_id")
        enriched = by_id.get(gid)
        if not enriched:
            continue
        scen = raw.get("scenarios") or {}
        if not scen:
            continue
        # Pick the bucket with max assigned probability.
        pred_bucket, pred_prob = None, -1.0
        for b, sc in scen.items():
            p = float(sc.get("prob", 0.0))
            if p > pred_prob:
                pred_bucket, pred_prob = b, p
        if pred_bucket is None:
            continue
        realized = enriched.get("realized_bucket")
        hit = 1 if realized == pred_bucket else 0
        for slot in bin_data:
            if slot["lo"] <= pred_prob < slot["hi"]:
                slot["n"] += 1
                slot["hits"] += hit
                slot["pred_probs"].append(pred_prob)
                break

    out = []
    for slot in bin_data:
        if slot["n"] == 0:
            out.append({
                "bin": f"[{slot['lo']:.1f}, {slot['hi']:.2f})",
                "n": 0,
                "mean_predicted": None,
                "empirical_frequency": None,
                "calibration_gap": None,
            })
            continue
        mean_pred = sum(slot["pred_probs"]) / slot["n"]
        freq = slot["hits"] / slot["n"]
        out.append({
            "bin": f"[{slot['lo']:.1f}, {slot['hi']:.2f})",
            "n": slot["n"],
            "mean_predicted": round(mean_pred, 3),
            "empirical_frequency": round(freq, 3),
            "calibration_gap": round(freq - mean_pred, 3),
        })
    return out


def rolling_brier(graded_records: List[Dict], window: int) -> List[Dict]:
    """Chronological rolling-mean Brier over the last `window` graded notes."""
    if len(graded_records) < 1:
        return []
    # Sort by graded_at if present, else note_date as a fallback.
    def _key(r):
        return (r.get("graded_at") or r.get("note_date") or "", r.get("grade_id"))
    ordered = [r for r in sorted(graded_records, key=_key)
               if r.get("brier_score") is not None]
    out: List[Dict] = []
    for i in range(len(ordered)):
        start = max(0, i + 1 - window)
        window_slice = ordered[start:i + 1]
        briers = [r["brier_score"] for r in window_slice]
        out.append({
            "as_of": ordered[i].get("graded_at") or ordered[i].get("note_date"),
            "last_grade_id": ordered[i].get("grade_id"),
            "window_size": len(briers),
            "mean_brier": round(statistics.fmean(briers), 4),
        })
    return out


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def write_report(out_dir: Path, payload: Dict) -> Path:
    lines: List[str] = []
    s = payload["summary"]
    lines.append("# Calibration Report")
    lines.append("")
    lines.append(
        f"Records: **{s['total_records']}** total "
        f"— {s['graded']} graded, {s['pending']} pending, "
        f"{s['ungradeable']} ungradeable."
    )
    lines.append("")

    if s["graded"] == 0:
        lines.append("## Status")
        lines.append("")
        lines.append(
            "No GRADED records yet. This is the expected state before any "
            "note horizon has elapsed — the first real calibration signal "
            "arrives once a 6-month or 12-month target date passes and "
            "`tools/meta-learn.py grade` fills in `realized_price`. "
            "Re-run this tool after each grading cycle."
        )
        lines.append("")
        lines.append("### Pending pipeline")
        lines.append("")
        lines.append("| Grade ID | Target Date | Horizon |")
        lines.append("|---|---|---|")
        for r in payload.get("pending_preview", []):
            lines.append(
                f"| {r.get('grade_id')} | {r.get('target_grade_date')} "
                f"| {r.get('horizon_months')}m |"
            )
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / "calibration-report.md"
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    # GRADED state
    lines.append("## Aggregate")
    lines.append("")
    lines.append(f"- Mean Brier (all graded): **{s.get('mean_brier')}**")
    if s.get("stdev_brier") is not None:
        lines.append(f"- Stdev Brier: {s['stdev_brier']}")
    if s.get("directional_hit_rate") is not None:
        lines.append(
            f"- Directional hit rate: **{s['directional_hit_rate'] * 100:.1f}%**"
        )
    lines.append("")

    lines.append("## By Horizon")
    lines.append("")
    lines.append("| Horizon | N | Mean Brier | Stdev | Directional Hit Rate | N (dir) |")
    lines.append("|---|---|---|---|---|---|")
    for h, stats in payload.get("by_horizon", {}).items():
        stdev = stats["stdev_brier"] if stats["stdev_brier"] is not None else "—"
        hit = (f"{stats['directional_hit_rate'] * 100:.1f}%"
               if stats["directional_hit_rate"] is not None else "—")
        lines.append(
            f"| {h}m | {stats['n']} | {stats['mean_brier']} | {stdev} "
            f"| {hit} | {stats['n_directional']} |"
        )
    lines.append("")

    lines.append("## Reliability Diagram (bucketed)")
    lines.append("")
    lines.append(
        "For notes whose top-probability scenario fell in each bin, "
        "the empirical frequency that the top bucket was the realized "
        "bucket. Positive gap = underconfident; negative = overconfident."
    )
    lines.append("")
    lines.append("| Predicted Bin | N | Mean Predicted | Empirical Frequency | Gap |")
    lines.append("|---|---|---|---|---|")
    for row in payload.get("reliability", []):
        if row["n"] == 0:
            lines.append(f"| {row['bin']} | 0 | — | — | — |")
        else:
            lines.append(
                f"| {row['bin']} | {row['n']} | {row['mean_predicted']} "
                f"| {row['empirical_frequency']} | {row['calibration_gap']:+} |"
            )
    lines.append("")

    lines.append("## Rolling Brier")
    lines.append("")
    rolling = payload.get("rolling", [])
    if not rolling:
        lines.append("_(insufficient graded data)_")
    else:
        tail = rolling[-20:]
        lines.append("| As Of | Last Grade | Window | Mean Brier |")
        lines.append("|---|---|---|---|")
        for row in tail:
            lines.append(
                f"| {row['as_of']} | {row['last_grade_id']} "
                f"| {row['window_size']} | {row['mean_brier']} |"
            )
    lines.append("")

    lines.append("## Graded Records")
    lines.append("")
    lines.append("| Grade ID | Ticker | Horizon | Realized Bucket | Brier | Dir Hit |")
    lines.append("|---|---|---|---|---|---|")
    for r in payload.get("graded_records", []):
        brier = r.get("brier_score")
        brier_str = f"{brier:.4f}" if isinstance(brier, (int, float)) else "—"
        dh = r.get("directional_hit")
        dh_str = ("✓" if dh is True else "✗" if dh is False else "—")
        lines.append(
            f"| {r['grade_id']} | {r['ticker']} | {r['horizon_months']}m "
            f"| {r['realized_bucket'] or '—'} | {brier_str} | {dh_str} |"
        )
    lines.append("")

    lines.append("## Notes on scope (v1)")
    lines.append("")
    lines.append(
        "- Calibration is computed at the *note* level, not per-analyst. "
        "Per-analyst Brier requires tagging each analyst's own probability "
        "output in the grade record (v1.1)."
    )
    lines.append(
        "- The Brier numerator uses the note's 3-bucket scenario distribution; "
        "realized outcome is attributed to the nearest-price bucket."
    )
    lines.append(
        "- Reliability bins collapse each note to the top-probability scenario. "
        "A per-scenario reliability diagram (one observation per bucket) is "
        "v1.1 scope."
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "calibration-report.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description="Calibration / Brier tracker")
    p.add_argument("--grades-file", default=DEFAULT_GRADES,
                   help=f"path to grades.jsonl (default: {DEFAULT_GRADES})")
    p.add_argument("--output-dir", default=DEFAULT_OUT,
                   help=f"output directory (default: {DEFAULT_OUT})")
    p.add_argument("--window", type=int, default=DEFAULT_WINDOW,
                   help=f"rolling window size (default: {DEFAULT_WINDOW})")
    args = p.parse_args()

    grades_path = Path(args.grades_file)
    out_dir = Path(args.output_dir)

    records = load_grades(grades_path)
    agg = aggregate_graded(records)

    # If no GRADED records, add a pending preview for the markdown.
    if agg["summary"]["graded"] == 0:
        pending_preview = [
            {"grade_id": r.get("grade_id"),
             "target_grade_date": r.get("target_grade_date"),
             "horizon_months": r.get("horizon_months")}
            for r in records if r.get("status") == "PENDING"
        ]
        agg["pending_preview"] = pending_preview
    else:
        agg["reliability"] = reliability_bins(agg["graded_records"], records)
        agg["rolling"] = rolling_brier(agg["graded_records"], args.window)

    report_path = write_report(out_dir, agg)
    json_path = out_dir / "calibration.json"
    json_path.write_text(json.dumps(agg, indent=2), encoding="utf-8")

    print(f"wrote {report_path}")
    print(f"wrote {json_path}")
    print(f"  graded={agg['summary']['graded']} "
          f"pending={agg['summary']['pending']} "
          f"ungradeable={agg['summary']['ungradeable']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
