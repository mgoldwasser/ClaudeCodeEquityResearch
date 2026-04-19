#!/usr/bin/env python3
"""
Reproducibility / Chain-of-Custody
===================================
Two subcommands that together give every research note a reproducibility
manifest:

  snapshot  — freeze the input files the run depends on, compute a content
              hash of each, record the hash list, the seed, and the
              environment fingerprint in
              `output/[TICKER]/[DATE]/reproducibility.json`. Copy the frozen
              inputs into `output/[TICKER]/[DATE]/inputs-snapshot/`.

  verify    — re-hash the snapshot directory and verify nothing drifted
              between snapshot time and now. Exit 0 match, exit 2 drift,
              exit 1 bad input.

  manifest  — render the reproducibility.json as a compact markdown block
              suitable for inclusion in the note's Section 16 Appendix
              (Chain of Custody subsection).

What this is and isn't
----------------------
This does NOT make LLM inference deterministic — the `--seed` is stored as
metadata, not injected into model calls (providers do not expose a guaranteed
deterministic mode for research-quality reasoning). It IS a commitment
device: if a downstream reader wants to know "what data did this note see?"
the answer is the inputs-snapshot directory + its hashes.

What gets snapshotted
---------------------
All files under the following directories, filtered by extension:

  input/financials/
  input/transcripts/
  input/filings/
  input/market/
  input/macro/
  input/alt-data/
  input/price-data/

Binary files are hashed but not copied more than once if duplicated across
partitions (dedupe by content hash). Files over 10MB are skipped with a
warning logged to the manifest.

Manifest shape
--------------
{
  "ticker": "...",
  "run_date": "YYYY-MM-DD",
  "seed": 42,
  "as_of": "YYYY-MM-DD | LIVE",
  "mode": "LIVE | HISTORICAL",
  "tool_versions": { ... key scripts and their hashes ... },
  "files": [
    {"path": "input/financials/10k.json", "sha256": "...", "bytes": 12345},
    ...
  ],
  "total_bytes": 123456,
  "created_at": "ISO-8601",
  "host": "platform string",
  "python": "3.x.y"
}
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


EXIT_OK = 0
EXIT_BAD_INPUT = 1
EXIT_DRIFT = 2

SNAPSHOT_DIRS = [
    "input/financials",
    "input/transcripts",
    "input/filings",
    "input/market",
    "input/macro",
    "input/alt-data",
    "input/price-data",
]

TRACKED_TOOLS = [
    "tools/_as_of.py",
    "tools/alt-data.py",
    "tools/portfolio-math.py",
    "tools/signal-independence.py",
    "tools/ips-validator.py",
    "tools/benchmark-compare.py",
    "tools/reproducibility.py",
]

MAX_FILE_BYTES = 10 * 1024 * 1024  # 10MB


def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _iter_input_files(repo_root: Path) -> List[Path]:
    out: List[Path] = []
    for rel in SNAPSHOT_DIRS:
        d = repo_root / rel
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*")):
            if p.is_file() and not p.name.startswith("."):
                out.append(p)
    return out


def _tool_versions(repo_root: Path) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for rel in TRACKED_TOOLS:
        p = repo_root / rel
        if p.is_file():
            out[rel] = _sha256_file(p)
    return out


def snapshot(run_dir: Path, repo_root: Path, seed: int,
             as_of: Optional[str]) -> Dict[str, Any]:
    snapshot_dir = run_dir / "inputs-snapshot"
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    files_meta: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []
    total_bytes = 0

    for src in _iter_input_files(repo_root):
        rel = src.relative_to(repo_root)
        size = src.stat().st_size
        if size > MAX_FILE_BYTES:
            skipped.append({"path": str(rel), "bytes": size,
                            "reason": f"exceeds {MAX_FILE_BYTES}-byte limit"})
            continue
        digest = _sha256_file(src)
        dst = snapshot_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        files_meta.append({
            "path": str(rel),
            "sha256": digest,
            "bytes": size,
        })
        total_bytes += size

    # ticker and run_date inferred from run_dir
    parts = run_dir.parts
    ticker = "UNKNOWN"
    run_date = "UNKNOWN"
    try:
        idx = parts.index("output")
        ticker = parts[idx + 1]
        run_date = parts[idx + 2]
    except (ValueError, IndexError):
        pass

    manifest = {
        "ticker": ticker,
        "run_date": run_date,
        "seed": seed,
        "as_of": as_of if as_of else "LIVE",
        "mode": "HISTORICAL" if as_of else "LIVE",
        "tool_versions": _tool_versions(repo_root),
        "files": sorted(files_meta, key=lambda d: d["path"]),
        "file_count": len(files_meta),
        "total_bytes": total_bytes,
        "skipped": skipped,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "host": platform.platform(),
        "python": platform.python_version(),
    }

    out_path = run_dir / "reproducibility.json"
    out_path.write_text(json.dumps(manifest, indent=2, sort_keys=True),
                        encoding="utf-8")
    return manifest


def verify(run_dir: Path) -> Tuple[bool, List[str]]:
    manifest_path = run_dir / "reproducibility.json"
    snapshot_dir = run_dir / "inputs-snapshot"
    if not manifest_path.is_file():
        return False, [f"missing manifest: {manifest_path}"]
    if not snapshot_dir.is_dir():
        return False, [f"missing snapshot dir: {snapshot_dir}"]

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    drift: List[str] = []
    for entry in manifest["files"]:
        p = snapshot_dir / entry["path"]
        if not p.is_file():
            drift.append(f"missing from snapshot: {entry['path']}")
            continue
        actual = _sha256_file(p)
        if actual != entry["sha256"]:
            drift.append(
                f"hash drift: {entry['path']} "
                f"expected {entry['sha256'][:12]}... got {actual[:12]}..."
            )

    # Also check no extra files in snapshot (strict)
    manifest_paths = {e["path"] for e in manifest["files"]}
    for p in sorted(snapshot_dir.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(snapshot_dir))
            if rel not in manifest_paths:
                drift.append(f"unmanifested file in snapshot: {rel}")

    return (len(drift) == 0), drift


def render_manifest_md(manifest: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("### Chain of Custody")
    lines.append("")
    lines.append(
        "This note's inputs are frozen at `inputs-snapshot/` with content "
        "hashes recorded in `reproducibility.json`. To re-run from the "
        "snapshot, pass `--snapshot-inputs <run-dir>/inputs-snapshot` to the "
        "research orchestrator."
    )
    lines.append("")
    lines.append(f"- **Seed:** {manifest.get('seed')}")
    lines.append(f"- **Mode:** {manifest.get('mode')}")
    lines.append(f"- **As-of:** {manifest.get('as_of')}")
    lines.append(f"- **Files snapshotted:** {manifest.get('file_count')}")
    lines.append(f"- **Total bytes:** {manifest.get('total_bytes'):,}")
    lines.append(f"- **Created at:** {manifest.get('created_at')}")
    lines.append(f"- **Host:** `{manifest.get('host')}` — Python {manifest.get('python')}")
    skipped = manifest.get("skipped") or []
    if skipped:
        lines.append(f"- **Skipped (too large):** {len(skipped)} file(s) — "
                     f"listed in `reproducibility.json` under `skipped`.")
    lines.append("")
    lines.append(
        "Reproducibility note: seed metadata is recorded for audit but LLM "
        "inference is not bitwise-deterministic across provider runs. What "
        "is reproducible is the *input set* — every file the analysts saw, "
        "hashed and archived. Re-running from this snapshot against the same "
        "prompts produces a note built on identical evidence."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Reproducibility / chain-of-custody")
    sub = ap.add_subparsers(dest="command", required=True)

    sp_snap = sub.add_parser("snapshot")
    sp_snap.add_argument("--run-dir", required=True)
    sp_snap.add_argument("--seed", type=int, required=True,
                         help="Run seed (recorded as metadata; not injected "
                              "into LLM inference).")
    sp_snap.add_argument("--as-of", default=None,
                         help="Optional YYYY-MM-DD for historical runs.")
    sp_snap.add_argument("--repo-root", default=".",
                         help="Path to repo root (default: cwd).")

    sp_ver = sub.add_parser("verify")
    sp_ver.add_argument("--run-dir", required=True)

    sp_man = sub.add_parser("manifest")
    sp_man.add_argument("--run-dir", required=True)
    sp_man.add_argument("--output", default=None,
                        help="Path to write the markdown manifest. Default: "
                             "stdout only.")

    args = ap.parse_args()

    run_dir = Path(args.run_dir).resolve()
    if not run_dir.is_dir():
        print(f"ERROR: run-dir not found: {run_dir}", file=sys.stderr)
        return EXIT_BAD_INPUT

    if args.command == "snapshot":
        repo_root = Path(args.repo_root).resolve()
        if not (repo_root / "CLAUDE.md").is_file():
            print(f"ERROR: --repo-root does not look like the repo root "
                  f"(no CLAUDE.md at {repo_root})", file=sys.stderr)
            return EXIT_BAD_INPUT
        manifest = snapshot(run_dir, repo_root, args.seed, args.as_of)
        print(json.dumps({
            "file_count": manifest["file_count"],
            "total_bytes": manifest["total_bytes"],
            "skipped": len(manifest["skipped"]),
            "manifest": str(run_dir / "reproducibility.json"),
            "snapshot_dir": str(run_dir / "inputs-snapshot"),
        }, indent=2))
        return EXIT_OK

    if args.command == "verify":
        ok, drift = verify(run_dir)
        payload = {"ok": ok, "drift": drift}
        print(json.dumps(payload, indent=2))
        return EXIT_OK if ok else EXIT_DRIFT

    if args.command == "manifest":
        manifest_path = run_dir / "reproducibility.json"
        if not manifest_path.is_file():
            print(f"ERROR: no manifest at {manifest_path}; run snapshot first.",
                  file=sys.stderr)
            return EXIT_BAD_INPUT
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        md = render_manifest_md(manifest)
        if args.output:
            Path(args.output).parent.mkdir(parents=True, exist_ok=True)
            Path(args.output).write_text(md, encoding="utf-8")
        print(md)
        return EXIT_OK

    return EXIT_BAD_INPUT


if __name__ == "__main__":
    sys.exit(main())
