#!/usr/bin/env python3
"""
Signal Independence Audit
=========================
Computes the Signal Independence Ratio for a research run and gates publication
on a 0.5 threshold. Designed to be called by the Editor (to populate the note
appendix) and by the Director (as a blocking pre-publication gate).

Definitions
-----------
Every Pass 1 analyst tags the data points that materially shaped their conclusions
with a SIGNAL-ID tag of the form:

    [SIGNAL-ID: NAMESPACE-CODE]

Namespace is a short per-analyst prefix (QC, DCF, IND, MAC, etc.); code is a
stable identifier unique within the namespace. Analysts cite other analysts'
signals by reproducing the tag verbatim.

Two ratios are computed:

  1. Hard ratio (unique-citer share):
       R_hard = (signals cited by exactly one agent) / (total unique signals)
     This is the ratio that appears in the note appendix and drives the gate.

  2. Weighted ratio (citation dispersion):
       R_weighted = mean_i(1 / n_citers_i)
     An information-theoretic view: a signal with 1 citer contributes 1.0;
     a signal with 4 citers contributes 0.25. Reported alongside R_hard.

Gate:   R_hard >= 0.5 is required for publication. Below that the Director
        must re-dispatch the offending analyst with stricter partitioning.

CLI
---
  python tools/signal-independence.py audit --run-dir output/TICKER/DATE
  python tools/signal-independence.py audit --run-dir output/TICKER/DATE \\
                                            --output output/.../signal-audit.json
  python tools/signal-independence.py report --run-dir output/TICKER/DATE
  python tools/signal-independence.py gate  --run-dir output/TICKER/DATE
      (exit 0 = pass, exit 2 = fail, exit 1 = bad inputs)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


SIGNAL_RE = re.compile(r"\[SIGNAL-ID:\s*([A-Za-z0-9][A-Za-z0-9_\-]*)\s*\]")
GATE_THRESHOLD = 0.5
EXIT_OK = 0
EXIT_BAD_INPUT = 1
EXIT_GATE_FAIL = 2


ANALYST_FILENAME_TO_AGENT = {
    "data-intelligence-memo.md": "Research Analyst",
    "dcf-analysis.md": "DCF Analyst",
    "quant-analysis.md": "Quant Analyst",
    "industry-analysis.md": "Industry Analyst",
    "risk-contrarian-report.md": "Risk & Contrarian Analyst",
    "credit-analysis.md": "Credit Analyst",
    "catalyst-analysis.md": "Catalyst Analyst",
    "esg-governance-analysis.md": "ESG & Governance Analyst",
    "technical-analysis.md": "Technical Analyst",
    "quality-credibility-report.md": "Quality & Credibility Analyst",
}


def _extract_signals(text: str) -> List[str]:
    return [m.group(1).upper() for m in SIGNAL_RE.finditer(text)]


def _agent_for_filename(name: str) -> str:
    return ANALYST_FILENAME_TO_AGENT.get(name, name)


def scan(run_dir: Path) -> Dict:
    """Scan pass1/ markdown files and build {signal -> set(agents)} mapping."""
    pass1 = run_dir / "pass1"
    if not pass1.is_dir():
        raise FileNotFoundError(f"pass1 directory not found: {pass1}")

    signal_to_agents: Dict[str, set] = defaultdict(set)
    per_file_counts: Dict[str, int] = {}

    for md in sorted(pass1.glob("*.md")):
        text = md.read_text(encoding="utf-8", errors="replace")
        found = _extract_signals(text)
        per_file_counts[md.name] = len(found)
        agent = _agent_for_filename(md.name)
        for s in found:
            signal_to_agents[s].add(agent)

    return {
        "run_dir": str(run_dir),
        "files_scanned": per_file_counts,
        "signal_to_agents": {s: sorted(a) for s, a in signal_to_agents.items()},
    }


def compute(scan_result: Dict) -> Dict:
    """Compute both ratios and the gate verdict."""
    sig_map: Dict[str, List[str]] = scan_result["signal_to_agents"]
    total = len(sig_map)

    if total == 0:
        return {
            **scan_result,
            "total_unique_signals": 0,
            "r_hard": None,
            "r_weighted": None,
            "threshold": GATE_THRESHOLD,
            "verdict": "NO_SIGNALS",
            "by_citer_count": {},
            "offenders": [],
            "message": (
                "No SIGNAL-ID tags found in pass1/. Every analyst must tag "
                "the data points that materially shaped their conclusions "
                "with [SIGNAL-ID: NAMESPACE-CODE]. See "
                "agents/<analyst>.md for namespace conventions."
            ),
        }

    single = sum(1 for agents in sig_map.values() if len(agents) == 1)
    r_hard = single / total
    r_weighted = sum(1.0 / len(agents) for agents in sig_map.values()) / total

    by_citer_count: Dict[int, List[str]] = defaultdict(list)
    for s, agents in sig_map.items():
        by_citer_count[len(agents)].append(s)

    # "offenders" = the signals that hurt the score the most (most citers).
    offenders = sorted(
        ({"signal": s, "n_citers": len(a), "agents": a}
         for s, a in sig_map.items() if len(a) > 1),
        key=lambda d: (-d["n_citers"], d["signal"]),
    )

    verdict = "PASS" if r_hard >= GATE_THRESHOLD else "FAIL"

    return {
        **scan_result,
        "total_unique_signals": total,
        "r_hard": round(r_hard, 4),
        "r_weighted": round(r_weighted, 4),
        "threshold": GATE_THRESHOLD,
        "verdict": verdict,
        "by_citer_count": {str(k): sorted(v) for k, v in by_citer_count.items()},
        "offenders": offenders,
        "message": _verdict_message(verdict, r_hard, offenders),
    }


def _verdict_message(verdict: str, r_hard: float,
                     offenders: List[Dict]) -> str:
    if verdict == "PASS":
        return (f"R_hard = {r_hard:.2f} >= {GATE_THRESHOLD}. "
                f"Signal sourcing is sufficiently independent.")
    if not offenders:
        return (f"R_hard = {r_hard:.2f} < {GATE_THRESHOLD}. "
                f"No over-shared signals — this likely indicates a nearly "
                f"empty signal set. Require analysts to tag more signals.")
    top = offenders[0]
    return (
        f"R_hard = {r_hard:.2f} < {GATE_THRESHOLD}. "
        f"Most-shared signal: {top['signal']} cited by {top['n_citers']} "
        f"agents ({', '.join(top['agents'])}). Director should re-dispatch "
        f"the secondary citers with stricter data partitioning."
    )


def render_report(result: Dict) -> str:
    """Render a markdown block suitable for Appendix F."""
    lines: List[str] = []
    lines.append("### F. Signal Independence Audit")
    lines.append("")
    if result["total_unique_signals"] == 0:
        lines.append(f"> {result['message']}")
        return "\n".join(lines) + "\n"

    lines.append(f"- **R_hard:** {result['r_hard']:.2f} "
                 f"(threshold ≥ {result['threshold']:.2f}) — "
                 f"**{result['verdict']}**")
    lines.append(f"- **R_weighted:** {result['r_weighted']:.2f}")
    lines.append(f"- **Total unique signals:** {result['total_unique_signals']}")
    lines.append("")
    lines.append("| SIGNAL-ID | # Citers | Agents |")
    lines.append("|-----------|----------|--------|")
    for sig, agents in sorted(result["signal_to_agents"].items()):
        lines.append(f"| {sig} | {len(agents)} | {', '.join(agents)} |")
    lines.append("")
    lines.append(f"**Assessment:** {result['message']}")
    return "\n".join(lines) + "\n"


def _resolve_run_dir(arg: str) -> Path:
    p = Path(arg).resolve()
    if not p.is_dir():
        raise FileNotFoundError(f"run-dir not found: {p}")
    return p


def main() -> int:
    parser = argparse.ArgumentParser(description="Signal Independence Audit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for cmd in ("audit", "report", "gate"):
        sp = subparsers.add_parser(cmd)
        sp.add_argument("--run-dir", required=True,
                        help="Path to output/[TICKER]/[DATE]/ run directory")
        if cmd in ("audit", "report"):
            sp.add_argument("--output", default=None,
                            help="Optional output file path")

    args = parser.parse_args()

    try:
        run_dir = _resolve_run_dir(args.run_dir)
        scan_result = scan(run_dir)
        result = compute(scan_result)
    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_BAD_INPUT

    if args.command == "audit":
        payload = json.dumps(result, indent=2, sort_keys=True)
        if args.output:
            Path(args.output).write_text(payload)
        else:
            print(payload)
        return EXIT_OK

    if args.command == "report":
        md = render_report(result)
        if args.output:
            Path(args.output).write_text(md)
        else:
            print(md)
        return EXIT_OK

    if args.command == "gate":
        print(json.dumps({
            "verdict": result["verdict"],
            "r_hard": result["r_hard"],
            "threshold": result["threshold"],
            "message": result["message"],
        }, indent=2))
        if result["verdict"] == "PASS":
            return EXIT_OK
        return EXIT_GATE_FAIL

    return EXIT_BAD_INPUT


if __name__ == "__main__":
    sys.exit(main())
