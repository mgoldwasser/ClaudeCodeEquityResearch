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
from datetime import datetime
from typing import Dict, List, Optional, Tuple

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

def search_motley_fool(ticker: str, count: int = 1) -> List[Dict]:
    """
    Search Motley Fool for earnings call transcripts.

    The Motley Fool publishes free, full-text earnings call transcripts
    at fool.com/earnings-call-transcripts/. URLs follow a predictable
    pattern based on company name and date.

    Args:
        ticker: Stock ticker symbol
        count: Number of transcripts to find

    Returns:
        List of dicts with 'title', 'url', 'date' keys
    """
    results = []

    # Search for transcript pages
    search_url = (
        f"https://www.fool.com/earnings-call-transcripts/"
        f"?q={ticker.upper()}"
    )

    # Also try a broader search pattern
    search_urls = [
        f"https://www.google.com/search?q=site:fool.com+%22earnings+call+transcript%22+{ticker.upper()}&num={count * 2}",
    ]

    print(f"[Transcript Search] Searching Motley Fool for {ticker} transcripts...")
    print(f"[Transcript Search] Motley Fool transcript index: {search_url}")
    print(f"[Transcript Search] Direct search: Use WebSearch for 'site:fool.com \"{ticker}\" earnings call transcript'")
    print()

    # Provide structured search guidance for the agent
    print(json.dumps({
        "search_guidance": {
            "motley_fool": {
                "index_url": search_url,
                "search_query": f'site:fool.com "{ticker}" "earnings call transcript"',
                "url_pattern": f"https://www.fool.com/earnings-call-transcripts/...",
                "notes": "Motley Fool is the most reliable free transcript source. "
                         "Use WebSearch to find transcript URLs, then WebFetch to retrieve content."
            },
            "company_ir": {
                "search_query": f'"{ticker}" investor relations earnings transcript',
                "notes": "Many companies publish transcripts directly on their IR page."
            },
            "alternative_sources": [
                {
                    "name": "Finnhub",
                    "api": f"https://finnhub.io/api/v1/stock/transcripts?symbol={ticker}&token=YOUR_KEY",
                    "notes": "Free API, 60 calls/minute. Requires registration for API key."
                },
            ]
        }
    }, indent=2))

    return results


# ============================================================
# COMPANY IR PAGE FINDER
# ============================================================

def find_ir_page(ticker: str) -> Dict:
    """
    Find a company's Investor Relations page.

    Most public companies have an IR page with transcripts, presentations,
    SEC filings, and other materials. This function provides search
    guidance to locate it.

    Args:
        ticker: Stock ticker symbol

    Returns:
        Dict with search guidance
    """
    # Common IR page URL patterns
    ir_patterns = {
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

def fetch_finnhub_transcript(ticker: str, api_key: str = "") -> Dict:
    """
    Fetch earnings transcripts from Finnhub API.

    Finnhub offers free earnings call transcripts via their API.
    Requires a free API key (register at finnhub.io).

    Args:
        ticker: Stock ticker symbol
        api_key: Finnhub API key (or set FINNHUB_API_KEY env var)

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
        print(f"[Finnhub] Found {len(transcripts)} transcript(s) for {ticker}")

        # Fetch the most recent transcript
        if transcripts:
            latest = transcripts[0]
            transcript_id = latest.get("id", "")
            detail_url = f"https://finnhub.io/api/v1/stock/transcripts?id={transcript_id}&token={key}"

            req2 = urllib.request.Request(detail_url, headers=HEADERS)
            with urllib.request.urlopen(req2, timeout=15) as resp2:
                detail = json.loads(resp2.read().decode())

            return {
                "available_transcripts": transcripts[:10],
                "latest_transcript": detail,
                "source": "Finnhub API"
            }

        return {"available_transcripts": transcripts, "source": "Finnhub API"}

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

    # IR page finder
    ir_parser = subparsers.add_parser("ir", help="Find company IR page")
    ir_parser.add_argument("ticker", help="Stock ticker symbol")

    # Finnhub
    finnhub_parser = subparsers.add_parser("finnhub", help="Fetch from Finnhub API")
    finnhub_parser.add_argument("ticker", help="Stock ticker symbol")
    finnhub_parser.add_argument("--api-key", default="",
                               help="Finnhub API key (or set FINNHUB_API_KEY env var)")

    # Extract
    extract_parser = subparsers.add_parser("extract", help="Extract key quotes from transcript text")
    extract_parser.add_argument("file", help="Path to transcript text file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "search":
        search_motley_fool(args.ticker, args.count)

    elif args.command == "ir":
        find_ir_page(args.ticker)

    elif args.command == "finnhub":
        result = fetch_finnhub_transcript(args.ticker, args.api_key)
        print(json.dumps(result, indent=2, default=str))

    elif args.command == "extract":
        with open(args.file, "r") as f:
            text = f.read()
        result = extract_key_quotes(text)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
