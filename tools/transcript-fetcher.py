#!/usr/bin/env python3
"""
Earnings Call Transcript Fetcher
Retrieves earnings call transcripts from free public sources.

Sources (in priority order):
  1. Motley Fool Transcripts (most reliable free source)
  2. Company IR pages (direct links)
  3. Finnhub API (requires free API key)

Usage:
  python3 tools/transcript-fetcher.py search AAPL              # Find latest transcript
  python3 tools/transcript-fetcher.py search AAPL --count 4    # Find last 4 transcripts
  python3 tools/transcript-fetcher.py fetch URL                 # Fetch transcript from URL
  python3 tools/transcript-fetcher.py ir AAPL                   # Find company IR page
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import date, datetime
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _as_of  # noqa: E402

# ============================================================
# CONFIGURATION
# ============================================================

USER_AGENT = "EquityResearchSwarm/1.0 (research@example.com)"

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/json",
}

# Finnhub API key (optional — set via environment variable)
FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY", "")

# ============================================================
# MOTLEY FOOL TRANSCRIPT SEARCH
# ============================================================

def search_motley_fool(ticker: str, count: int = 1,
                       as_of: Optional[date] = None) -> List[Dict]:
    """
    Search Motley Fool for earnings call transcripts.

    The Motley Fool publishes free, full-text earnings call transcripts
    at fool.com/earnings-call-transcripts/. URLs follow a predictable
    pattern based on company name and date.

    Args:
        ticker: Stock ticker symbol
        count: Number of transcripts to find
        as_of: If set, agent must filter results to transcripts dated
               on or before as_of (Motley Fool URLs embed the call date).

    Returns:
        List of dicts with 'title', 'url', 'date' keys
    """
    results = []

    # Search for transcript pages
    search_url = (
        f"https://www.fool.com/earnings-call-transcripts/"
        f"?q={ticker.upper()}"
    )

    as_of_str = as_of.isoformat() if as_of else None
    date_filter_note = (
        f"HISTORICAL MODE: drop any transcript with call date > {as_of_str}. "
        "Motley Fool URLs embed the date (e.g., .../2021/07/28/...). "
        "Check that date first, then WebFetch."
        if as_of_str else
        "Use WebSearch to find transcript URLs, then WebFetch to retrieve content."
    )

    print(f"[Transcript Search] Searching Motley Fool for {ticker} transcripts...")
    print(f"[Transcript Search] Motley Fool transcript index: {search_url}")
    print(f"[Transcript Search] Direct search: Use WebSearch for 'site:fool.com \"{ticker}\" earnings call transcript'")
    print()

    # Provide structured search guidance for the agent
    print(json.dumps({
        "as_of": as_of_str,
        "search_guidance": {
            "motley_fool": {
                "index_url": search_url,
                "search_query": f'site:fool.com "{ticker}" "earnings call transcript"',
                "url_pattern": f"https://www.fool.com/earnings-call-transcripts/...",
                "notes": f"Motley Fool is the most reliable free transcript source. {date_filter_note}"
            },
            "company_ir": {
                "search_query": f'"{ticker}" investor relations earnings transcript',
                "notes": (
                    "Many companies publish transcripts directly on their IR page. "
                    + (f"In historical mode, only fetch transcripts dated <= {as_of_str}."
                       if as_of_str else "")
                )
            },
            "alternative_sources": [
                {
                    "name": "Finnhub",
                    "api": f"https://finnhub.io/api/v1/stock/transcripts?symbol={ticker}&token=YOUR_KEY",
                    "notes": "Free API, 60 calls/minute. Requires registration for API key. "
                             "This tool's 'finnhub' subcommand already applies the as_of filter."
                },
            ]
        }
    }, indent=2))

    return results


# ============================================================
# COMPANY IR PAGE FINDER
# ============================================================

def find_ir_page(ticker: str, as_of: Optional[date] = None) -> Dict:
    """
    Find a company's Investor Relations page.

    Most public companies have an IR page with transcripts, presentations,
    SEC filings, and other materials. This function provides search
    guidance to locate it.

    Args:
        ticker: Stock ticker symbol
        as_of: If set, agent must filter IR materials to items dated
               on or before as_of. IR pages themselves are live snapshots;
               individual materials (transcripts, filings) are dated.

    Returns:
        Dict with search guidance
    """
    as_of_str = as_of.isoformat() if as_of else None

    # Common IR page URL patterns
    ir_patterns = {
        "as_of": as_of_str,
        "historical_mode_warning": (
            f"IR pages are live — they show current management, current capital "
            f"structure, and current press releases. When operating --as-of {as_of_str}, "
            f"only retrieve dated artifacts (transcripts, PDF 10-Ks, press releases) "
            f"whose publication date is on or before {as_of_str}. Do not use the "
            f"'About' or 'Leadership' pages for historical management tenure."
            if as_of_str else None
        ),
        "search_queries": [
            f'"{ticker}" investor relations',
            f'"{ticker}" IR earnings transcript',
            f'"{ticker}" annual report investor',
        ],
        "common_url_patterns": [
            "investor.[company].com",
            "ir.[company].com",
            "[company].com/investor-relations",
            "[company].com/investors",
            "[company].com/ir",
        ],
        "what_to_look_for": [
            "Earnings call transcripts or webcast replays",
            "SEC filings section (direct links to 10-K, 10-Q, proxy)",
            "Investor presentations and fact sheets",
            "Analyst day / investor day materials",
            "Press releases (earnings releases)",
            "Annual reports (often have more context than 10-K)",
            "ESG / sustainability reports",
            "Corporate governance documents",
        ]
    }

    print(f"[IR Page Finder] Finding investor relations page for {ticker}...")
    print()
    print(json.dumps(ir_patterns, indent=2))

    return ir_patterns


# ============================================================
# FINNHUB TRANSCRIPT API
# ============================================================

def fetch_finnhub_transcript(ticker: str, api_key: str = "",
                             as_of: Optional[date] = None) -> Dict:
    """
    Fetch earnings transcripts from Finnhub API.

    Finnhub offers free earnings call transcripts via their API.
    Requires a free API key (register at finnhub.io).

    Args:
        ticker: Stock ticker symbol
        api_key: Finnhub API key (or set FINNHUB_API_KEY env var)
        as_of: If set, drop transcripts whose call date is after as_of and
               return the most recent transcript <= as_of.

    Returns:
        Dict with transcript data or error
    """
    key = api_key or FINNHUB_API_KEY

    if not key:
        return {
            "error": "No Finnhub API key provided",
            "instructions": "Register for a free API key at https://finnhub.io/register",
            "set_key": "export FINNHUB_API_KEY='your_key_here'",
            "api_docs": "https://finnhub.io/docs/api/transcripts"
        }

    # First, list available transcripts
    list_url = f"https://finnhub.io/api/v1/stock/transcripts/list?symbol={ticker}&token={key}"

    try:
        req = urllib.request.Request(list_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())

        if not data or "transcripts" not in data:
            return {"error": f"No transcripts found for {ticker}", "raw": data}

        transcripts = data["transcripts"]
        total_before = len(transcripts)

        # Vintage filter: drop transcripts whose call date is after as_of.
        # Finnhub transcript list entries include 'time' (YYYY-MM-DD HH:MM:SS).
        as_of_str = as_of.isoformat() if as_of else None
        if as_of_str:
            def _before(t):
                t_str = str(t.get("time", "") or t.get("year", ""))
                return t_str[:10] <= as_of_str
            transcripts = [t for t in transcripts if _before(t)]
            print(
                f"[Finnhub] as_of={as_of_str}: {total_before} → {len(transcripts)} "
                f"transcripts after vintage filter",
                file=sys.stderr,
            )

        print(f"[Finnhub] Found {len(transcripts)} transcript(s) for {ticker}")

        # Fetch the most recent transcript (after filtering)
        if transcripts:
            latest = transcripts[0]
            transcript_id = latest.get("id", "")
            detail_url = f"https://finnhub.io/api/v1/stock/transcripts?id={transcript_id}&token={key}"

            req2 = urllib.request.Request(detail_url, headers=HEADERS)
            with urllib.request.urlopen(req2, timeout=15) as resp2:
                detail = json.loads(resp2.read().decode())

            return {
                "as_of": as_of_str,
                "available_transcripts": transcripts[:10],
                "latest_transcript": detail,
                "source": "Finnhub API"
            }

        return {
            "as_of": as_of_str,
            "available_transcripts": transcripts,
            "source": "Finnhub API",
            "note": (
                f"No transcripts available on or before {as_of_str}"
                if as_of_str else "No transcripts available"
            )
        }

    except urllib.error.HTTPError as e:
        return {"error": f"Finnhub API error: {e.code}", "message": str(e)}
    except Exception as e:
        return {"error": str(e)}


# ============================================================
# TRANSCRIPT TEXT EXTRACTION
# ============================================================

def extract_key_quotes(transcript_text: str, sections: Optional[List[str]] = None) -> Dict:
    """
    Extract key sections and quotes from a transcript.

    Looks for:
    - Prepared remarks by CEO and CFO
    - Guidance / outlook statements
    - Q&A highlights (analyst questions with management responses)
    - Forward-looking language
    - Numbers and metrics mentioned

    Args:
        transcript_text: Full transcript text
        sections: Optional list of sections to extract

    Returns:
        Dict with extracted sections and key quotes
    """
    if not sections:
        sections = ["guidance", "outlook", "growth", "margin", "competitive",
                     "risk", "capex", "m&a", "buyback", "dividend"]

    result = {
        "total_length": len(transcript_text),
        "word_count": len(transcript_text.split()),
        "key_topics_found": [],
        "guidance_mentions": [],
        "numbers_mentioned": [],
    }

    # Find guidance-related statements
    guidance_patterns = [
        r"(?i)(we expect|we anticipate|guidance|outlook|forecast|target|goal)[^.]*\.",
        r"(?i)(full[- ]year|fiscal year|quarter)[^.]*(?:revenue|earnings|eps|growth|margin)[^.]*\.",
        r"(?i)(raising|lowering|reaffirming|maintaining)[^.]*(?:guidance|outlook|target)[^.]*\.",
    ]

    for pattern in guidance_patterns:
        matches = re.findall(pattern, transcript_text)
        if matches:
            result["guidance_mentions"].extend(matches[:5])

    # Find numbers and metrics
    number_patterns = [
        r"\$[\d,]+(?:\.\d+)?(?:\s*(?:million|billion|M|B))?",
        r"[\d]+(?:\.\d+)?%",
        r"[\d]+(?:\.\d+)?x",
    ]

    for pattern in number_patterns:
        matches = re.findall(pattern, transcript_text)
        result["numbers_mentioned"].extend(matches[:20])

    # Check which topics are discussed
    for topic in sections:
        if topic.lower() in transcript_text.lower():
            result["key_topics_found"].append(topic)

    return result


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Earnings Call Transcript Fetcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 tools/transcript-fetcher.py search AAPL
  python3 tools/transcript-fetcher.py search MSFT --count 4
  python3 tools/transcript-fetcher.py ir GOOGL
  python3 tools/transcript-fetcher.py finnhub AMZN
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search for transcripts")
    search_parser.add_argument("ticker", help="Stock ticker symbol")
    search_parser.add_argument("--count", type=int, default=1,
                              help="Number of transcripts to find (default: 1)")
    _as_of.add_argument(search_parser)

    # IR page finder
    ir_parser = subparsers.add_parser("ir", help="Find company IR page")
    ir_parser.add_argument("ticker", help="Stock ticker symbol")
    _as_of.add_argument(ir_parser)

    # Finnhub
    finnhub_parser = subparsers.add_parser("finnhub", help="Fetch from Finnhub API")
    finnhub_parser.add_argument("ticker", help="Stock ticker symbol")
    finnhub_parser.add_argument("--api-key", default="",
                               help="Finnhub API key (or set FINNHUB_API_KEY env var)")
    _as_of.add_argument(finnhub_parser)

    # Extract — local file; as_of is a no-op but accepted for uniformity
    extract_parser = subparsers.add_parser("extract", help="Extract key quotes from transcript text")
    extract_parser.add_argument("file", help="Path to transcript text file")
    _as_of.add_argument(extract_parser)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    as_of = _as_of.resolve(getattr(args, "as_of", None))

    if args.command == "search":
        search_motley_fool(args.ticker, args.count, as_of=as_of)

    elif args.command == "ir":
        find_ir_page(args.ticker, as_of=as_of)

    elif args.command == "finnhub":
        result = fetch_finnhub_transcript(args.ticker, args.api_key, as_of=as_of)
        print(json.dumps(result, indent=2, default=str))

    elif args.command == "extract":
        with open(args.file, "r") as f:
            text = f.read()
        result = extract_key_quotes(text)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
