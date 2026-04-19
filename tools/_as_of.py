"""
Shared --as-of contract helper for Python data-retrieval tools.

See tools/AS_OF.md for the full specification. This module implements:
  - Flag + env var resolution with precedence
  - Historical vs. live mode detection
  - Hard-fail for current-only sources
  - Date filtering helpers for natively filterable sources

Usage:
    from _as_of import resolve, is_historical, assert_live_only, filter_by_date

    as_of = resolve(args.as_of)           # date or None
    if is_historical(as_of):
        assert_live_only("market-data.sh", "quote",
                         "Yahoo /v7/quote is a live snapshot",
                         alternative="history command supports --as-of")
"""

from __future__ import annotations

import os
import sys
from datetime import date, datetime, timezone
from typing import Iterable, Optional, Sequence


ENV_VAR = "EQUITY_SWARM_AS_OF"
MIN_DATE = date(1990, 1, 1)

EXIT_PARSE_ERROR = 1
EXIT_CURRENT_ONLY = 2


def _parse(s: str, source: str) -> date:
    try:
        d = datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        print(
            f"ERROR: invalid --as-of value '{s}' from {source}. "
            f"Expected format YYYY-MM-DD.",
            file=sys.stderr,
        )
        sys.exit(EXIT_PARSE_ERROR)
    if d < MIN_DATE:
        print(
            f"ERROR: --as-of {s} is before minimum supported date {MIN_DATE.isoformat()}.",
            file=sys.stderr,
        )
        sys.exit(EXIT_PARSE_ERROR)
    return d


def resolve(cli_value: Optional[str]) -> Optional[date]:
    """
    Resolve the effective as-of date from CLI flag > env var > unset.

    Returns None when the resolved date is today or in the future ("live mode").
    Returns a date when historical mode applies.
    Emits the '[as-of] historical mode' stderr line on first historical resolution.
    """
    raw = cli_value if cli_value else os.environ.get(ENV_VAR, "").strip() or None
    if not raw:
        return None

    source = "--as-of flag" if cli_value else f"${ENV_VAR}"
    d = _parse(raw, source)
    today = datetime.now(timezone.utc).date()
    if d >= today:
        return None

    print(f"[as-of] historical mode: {d.isoformat()}", file=sys.stderr)
    return d


def is_historical(as_of: Optional[date]) -> bool:
    return as_of is not None


def assert_live_only(
    tool: str,
    command: str,
    reason: str,
    alternative: Optional[str] = None,
    as_of: Optional[date] = None,
) -> None:
    """
    Hard-fail for Category C (current-only) commands when as-of is historical.
    No-op in live mode.
    """
    if not is_historical(as_of):
        return
    as_of_str = as_of.isoformat() if as_of else "<unknown>"
    print(
        f"ERROR: {tool} {command} --as-of {as_of_str} is not supported.\n"
        f"  Reason: {reason}",
        file=sys.stderr,
    )
    if alternative:
        print(f"  Alternative: {alternative}", file=sys.stderr)
    sys.exit(EXIT_CURRENT_ONLY)


def _parse_date(value) -> Optional[date]:
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    s = str(value).strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ", "%Y/%m/%d"):
        try:
            return datetime.strptime(s[: len(fmt) + 2].split("+")[0], fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).date()
    except ValueError:
        return None


def filter_by_date(
    records: Sequence[dict],
    date_field: str,
    as_of: Optional[date],
    tool_tag: str = "",
) -> list:
    """
    Return only records whose date_field value is <= as_of.
    In live mode returns the input unchanged.
    Records with missing or unparseable dates are DROPPED in historical mode
    (conservative: we cannot prove they existed by as-of).
    Logs the filter count to stderr.
    """
    if not is_historical(as_of):
        return list(records)

    kept = []
    dropped = 0
    dropped_undated = 0
    for r in records:
        d = _parse_date(r.get(date_field) if isinstance(r, dict) else None)
        if d is None:
            dropped_undated += 1
            continue
        if d <= as_of:
            kept.append(r)
        else:
            dropped += 1

    total_dropped = dropped + dropped_undated
    if total_dropped:
        tag = f" [{tool_tag}]" if tool_tag else ""
        msg = f"[as-of]{tag} filtered {dropped} records with date > {as_of.isoformat()}"
        if dropped_undated:
            msg += f" (+{dropped_undated} dropped as undated)"
        print(msg, file=sys.stderr)
    return kept


def epoch(d: date, end_of_day: bool = False) -> int:
    """Convert a date to a UTC epoch integer (for Yahoo period1/period2)."""
    hour = 23 if end_of_day else 0
    minute = 59 if end_of_day else 0
    second = 59 if end_of_day else 0
    dt = datetime(d.year, d.month, d.day, hour, minute, second, tzinfo=timezone.utc)
    return int(dt.timestamp())


def add_argument(parser) -> None:
    """Attach --as-of to an argparse parser uniformly across tools."""
    parser.add_argument(
        "--as-of",
        dest="as_of",
        default=None,
        metavar="YYYY-MM-DD",
        help=(
            "Historical retrieval: return only data available on or before this date. "
            f"Can also be set via ${ENV_VAR}. See tools/AS_OF.md."
        ),
    )
