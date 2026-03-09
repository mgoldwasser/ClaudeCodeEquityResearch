#!/usr/bin/env python3
"""
Alternative Data Retrieval
Fetches insider trading, institutional holdings, short interest,
and other alternative datasets from free public sources.

Usage:
  python3 tools/alt-data.py insider AAPL                # Insider trades (SEC Form 4)
  python3 tools/alt-data.py institutional AAPL          # Institutional holdings (13F)
  python3 tools/alt-data.py short-interest AAPL         # Short interest data
  python3 tools/alt-data.py ownership-summary AAPL      # Combined ownership picture
  python3 tools/alt-data.py analyst-estimates AAPL      # Consensus estimates from free sources
  python3 tools/alt-data.py peers AAPL                  # Peer/comparable company discovery
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ============================================================
# CONFIGURATION
# ============================================================

USER_AGENT = "EquityResearchSwarm/1.0 (research@example.com)"
HEADERS = {"User-Agent": USER_AGENT, "Accept": "application/json"}
FINNHUB_API_KEY = os.environ.get("FINNHUB_API_KEY", "")
FMP_API_KEY = os.environ.get("FMP_API_KEY", "")  # Financial Modeling Prep

# ============================================================
# HELPERS
# ============================================================

def _fetch_json(url: str, headers: Optional[Dict] = None) -> Dict:
    """Fetch JSON from URL with error handling."""
    h = headers or HEADERS
    req = urllib.request.Request(url, headers=h)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read().decode()
            return json.loads(data)
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "url": url}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response", "url": url}
    except Exception as e:
        return {"error": str(e), "url": url}


def _fetch_text(url: str) -> str:
    """Fetch text content from URL."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode()
    except Exception as e:
        return f"ERROR: {e}"


# ============================================================
# INSIDER TRADING
# ============================================================

def get_insider_trades(ticker: str) -> Dict:
    """
    Get insider trading data from multiple free sources.

    Insider trading (Form 4 filings) is one of the most valuable
    alternative data signals. Net insider buying, especially by
    CEOs/CFOs, is a positive signal. Cluster selling is negative.

    Args:
        ticker: Stock ticker

    Returns:
        Dict with insider trading data and source URLs
    """
    result = {
        "ticker": ticker.upper(),
        "data_sources": {},
        "retrieval_instructions": [],
    }

    # Source 1: OpenInsider (best free source, pre-parsed)
    openinsider_url = (
        f"http://openinsider.com/screener?"
        f"s={ticker.upper()}&o=&pl=&ph=&ll=&lh=&fd=730&fdr=&td=0&tdr=&"
        f"feession=&cession=&sidTids498=on&sidTidsOther=on&"
        f"ession=&vession=&pession=&aession=&dession=&tession=&"
        f"hasaliases=0&Order=5&Sort=0&maxresults=50&start=0"
    )
    result["data_sources"]["openinsider"] = {
        "name": "OpenInsider",
        "url": openinsider_url,
        "description": "Pre-parsed SEC Form 4 data with transaction details",
        "data_available": [
            "Filing date", "Trade date", "Insider name and title",
            "Transaction type (Purchase/Sale/Exercise)",
            "Shares traded", "Price per share", "Value",
            "Shares owned after transaction"
        ],
        "retrieval": f"Use WebFetch on: {openinsider_url}"
    }

    # Source 2: SEC EDGAR Form 4 (authoritative)
    result["data_sources"]["sec_edgar"] = {
        "name": "SEC EDGAR (Form 4)",
        "url": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&company={ticker}&CIK=&type=4&dateb=&owner=include&count=40",
        "description": "Official SEC Form 4 filings (XML format)",
        "retrieval": f"Use: python3 tools/edgar-enhanced.py insider {ticker}"
    }

    # Source 3: Finnhub (if API key available)
    if FINNHUB_API_KEY:
        finnhub_url = f"https://finnhub.io/api/v1/stock/insider-transactions?symbol={ticker}&token={FINNHUB_API_KEY}"
        data = _fetch_json(finnhub_url)
        if "error" not in data:
            result["data_sources"]["finnhub"] = {
                "name": "Finnhub API",
                "transactions": data.get("data", [])[:20],
                "total": len(data.get("data", [])),
            }
    else:
        result["data_sources"]["finnhub"] = {
            "name": "Finnhub API",
            "note": "Set FINNHUB_API_KEY for automated insider data",
            "register": "https://finnhub.io/register"
        }

    # Source 4: Yahoo Finance
    result["data_sources"]["yahoo_finance"] = {
        "name": "Yahoo Finance Insider Transactions",
        "url": f"https://finance.yahoo.com/quote/{ticker.upper()}/insider-transactions/",
        "description": "Summary of recent insider transactions",
        "retrieval": f"Use WebFetch on the URL above"
    }

    result["analysis_framework"] = {
        "bullish_signals": [
            "Cluster buying by multiple insiders",
            "CEO/CFO open-market purchases (not option exercises)",
            "Large purchases relative to existing holdings",
            "Buying after a price decline (catching a falling knife)",
        ],
        "bearish_signals": [
            "Cluster selling by multiple insiders",
            "CEO/CFO selling large portions of holdings",
            "Selling on unusual volume or timing",
            "Selling before earnings or major announcements",
        ],
        "neutral": [
            "10b5-1 pre-planned sales (automated, not signal)",
            "Option exercises without selling (increasing ownership)",
            "Small sales for tax purposes",
        ],
    }

    return result


# ============================================================
# INSTITUTIONAL HOLDINGS
# ============================================================

def get_institutional_holdings(ticker: str) -> Dict:
    """
    Get institutional ownership data from free sources.

    13F filings show what hedge funds, mutual funds, and other
    institutional investors hold. Changes in holdings signal
    conviction shifts.

    Args:
        ticker: Stock ticker

    Returns:
        Dict with institutional ownership data and sources
    """
    result = {
        "ticker": ticker.upper(),
        "data_sources": {},
    }

    # Source 1: Yahoo Finance holders page
    result["data_sources"]["yahoo_finance"] = {
        "name": "Yahoo Finance - Holders",
        "url": f"https://finance.yahoo.com/quote/{ticker.upper()}/holders/",
        "data_available": [
            "% held by institutions",
            "% held by insiders",
            "Top institutional holders (name, shares, % held, value, date)",
            "Top mutual fund holders",
        ],
        "retrieval": f"Use WebFetch on the URL above"
    }

    # Source 2: WhaleWisdom
    result["data_sources"]["whalewisdom"] = {
        "name": "WhaleWisdom",
        "url": f"https://whalewisdom.com/stock/{ticker.lower()}",
        "data_available": [
            "Top holders with position sizes",
            "Quarterly changes (new, increased, decreased, sold out)",
            "Ownership concentration (top 10/20 holders %)",
            "Historical ownership trends (last 9 quarters free)",
        ],
        "retrieval": f"Use WebFetch on the URL above"
    }

    # Source 3: Finnhub
    if FINNHUB_API_KEY:
        ownership_url = f"https://finnhub.io/api/v1/stock/ownership?symbol={ticker}&token={FINNHUB_API_KEY}"
        data = _fetch_json(ownership_url)
        if "error" not in data:
            result["data_sources"]["finnhub"] = {
                "name": "Finnhub API - Institutional Ownership",
                "ownership": data.get("ownership", [])[:15],
            }

    # Source 4: SEC 13F search
    result["data_sources"]["sec_13f"] = {
        "name": "SEC EDGAR 13F Filings",
        "url": "https://www.sec.gov/data-research/sec-markets-data/13f-securities-data-sets",
        "description": "Quarterly bulk 13F datasets from SEC",
        "note": "Use edgar-enhanced.py institutional command for more detail"
    }

    # Source 5: Finviz
    result["data_sources"]["finviz"] = {
        "name": "Finviz",
        "url": f"https://finviz.com/quote.ashx?t={ticker.upper()}",
        "data_available": ["Institutional ownership %", "Insider ownership %", "Short float %"],
    }

    result["analysis_framework"] = {
        "key_metrics": [
            "Institutional ownership % (typical: 60-90% for large caps)",
            "Insider ownership % (>5% = aligned, >20% = concentrated)",
            "Top 10 holder concentration (>50% = concentrated)",
            "Quarterly changes in institutional positions",
            "Number of institutional holders (breadth of ownership)",
        ],
        "bullish_signals": [
            "Increasing number of institutional holders",
            "Top-tier funds initiating new positions",
            "Activist investors building stakes (13D filings)",
        ],
        "bearish_signals": [
            "Decreasing institutional holders",
            "Major funds exiting or reducing",
            "High concentration = crowded trade risk",
        ],
    }

    return result


# ============================================================
# SHORT INTEREST
# ============================================================

def get_short_interest(ticker: str) -> Dict:
    """
    Get short interest data from free sources.

    Short interest measures bearish sentiment. High short interest
    can signal either overvaluation concerns or squeeze potential.

    Args:
        ticker: Stock ticker

    Returns:
        Dict with short interest data and sources
    """
    result = {
        "ticker": ticker.upper(),
        "data_sources": {},
    }

    # Source 1: FINRA (official)
    result["data_sources"]["finra"] = {
        "name": "FINRA Short Interest",
        "api": "https://developer.finra.org/",
        "description": "Official short interest data, published twice monthly",
        "frequency": "Bi-monthly (mid-month and end-of-month settlement dates)",
        "delay": "~10 business days after settlement date",
        "note": "FINRA API requires free registration at developer.finra.org",
        "daily_short_volume": {
            "description": "Daily short sale volume (different from short interest)",
            "url": "https://www.finra.org/finra-data/browse-catalog/short-interest/data",
        }
    }

    # Source 2: Yahoo Finance
    result["data_sources"]["yahoo_finance"] = {
        "name": "Yahoo Finance",
        "url": f"https://finance.yahoo.com/quote/{ticker.upper()}/key-statistics/",
        "data_available": [
            "Short % of float",
            "Short % of shares outstanding",
            "Short ratio (days to cover)",
            "Shares short (current and prior month)",
        ],
        "retrieval": f"Use WebFetch or tools/market-data.sh stats {ticker}"
    }

    # Source 3: Finviz
    result["data_sources"]["finviz"] = {
        "name": "Finviz",
        "url": f"https://finviz.com/quote.ashx?t={ticker.upper()}",
        "data_available": ["Short float %", "Short ratio"],
    }

    # Source 4: MarketBeat
    result["data_sources"]["marketbeat"] = {
        "name": "MarketBeat Short Interest",
        "url": f"https://www.marketbeat.com/stocks/NYSE/{ticker.upper()}/short-interest/",
        "data_available": ["Short interest history", "Days to cover trend"],
    }

    result["analysis_framework"] = {
        "key_metrics": {
            "short_percent_float": {
                "description": "Short shares as % of float",
                "thresholds": {
                    "low": "< 5%: Normal, no significant bearish sentiment",
                    "moderate": "5-10%: Moderate bearish interest",
                    "high": "10-20%: Elevated short interest, potential squeeze",
                    "extreme": "> 20%: Very high conviction bearish bet or squeeze candidate",
                },
            },
            "days_to_cover": {
                "description": "Shares short / avg daily volume",
                "thresholds": {
                    "low": "< 3 days: Can be covered quickly",
                    "moderate": "3-7 days: Moderate time to cover",
                    "high": "> 7 days: Significant time to cover, squeeze risk",
                },
            },
            "trend": "Compare current short interest to 3-6 months ago",
        },
    }

    return result


# ============================================================
# OWNERSHIP SUMMARY
# ============================================================

def get_ownership_summary(ticker: str) -> Dict:
    """
    Get combined ownership picture: insider + institutional + short interest.

    Combines all ownership signals into one view for the analyst team.

    Args:
        ticker: Stock ticker

    Returns:
        Dict with combined ownership data
    """
    return {
        "ticker": ticker.upper(),
        "insider_trades": get_insider_trades(ticker),
        "institutional_holdings": get_institutional_holdings(ticker),
        "short_interest": get_short_interest(ticker),
        "combined_sources": {
            "yahoo_all_in_one": f"https://finance.yahoo.com/quote/{ticker.upper()}/holders/",
            "finviz_summary": f"https://finviz.com/quote.ashx?t={ticker.upper()}",
        },
        "retrieval_priority": [
            f"1. WebFetch: https://finance.yahoo.com/quote/{ticker.upper()}/holders/",
            f"2. WebFetch: https://finance.yahoo.com/quote/{ticker.upper()}/key-statistics/",
            f"3. WebFetch: http://openinsider.com/screener?s={ticker.upper()}&fd=365",
            f"4. python3 tools/edgar-enhanced.py insider {ticker}",
            f"5. python3 tools/edgar-enhanced.py institutional {ticker}",
        ],
    }


# ============================================================
# ANALYST ESTIMATES / CONSENSUS
# ============================================================

def get_analyst_estimates(ticker: str) -> Dict:
    """
    Get consensus analyst estimates from free sources.

    Consensus estimates are critical for understanding market expectations.
    Beat/miss vs. consensus drives short-term stock price moves.

    Args:
        ticker: Stock ticker

    Returns:
        Dict with consensus estimate sources
    """
    result = {
        "ticker": ticker.upper(),
        "data_sources": {},
    }

    # Source 1: Yahoo Finance
    result["data_sources"]["yahoo_finance"] = {
        "name": "Yahoo Finance - Analysis",
        "url": f"https://finance.yahoo.com/quote/{ticker.upper()}/analysis/",
        "data_available": [
            "EPS estimates (current Q, next Q, current Y, next Y)",
            "Revenue estimates (current Q, next Q, current Y, next Y)",
            "EPS trend (7/30/60/90 day revisions)",
            "EPS revisions (up/down counts)",
            "Growth estimates (next 5Y, past 5Y, next Y)",
        ],
        "retrieval": f"Use WebFetch on the URL above"
    }

    # Source 2: Finnhub
    if FINNHUB_API_KEY:
        # Recommendation trends
        rec_url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={ticker}&token={FINNHUB_API_KEY}"
        rec_data = _fetch_json(rec_url)

        # EPS estimates
        eps_url = f"https://finnhub.io/api/v1/stock/eps-estimate?symbol={ticker}&token={FINNHUB_API_KEY}"
        eps_data = _fetch_json(eps_url)

        # Price target
        pt_url = f"https://finnhub.io/api/v1/stock/price-target?symbol={ticker}&token={FINNHUB_API_KEY}"
        pt_data = _fetch_json(pt_url)

        result["data_sources"]["finnhub"] = {
            "name": "Finnhub API",
            "recommendations": rec_data[:6] if isinstance(rec_data, list) else rec_data,
            "eps_estimates": eps_data.get("data", [])[:4] if isinstance(eps_data, dict) else eps_data,
            "price_target": pt_data if isinstance(pt_data, dict) else {},
        }
    else:
        result["data_sources"]["finnhub"] = {
            "name": "Finnhub API",
            "note": "Set FINNHUB_API_KEY for automated estimates",
            "register": "https://finnhub.io/register",
            "endpoints": [
                f"Recommendations: /stock/recommendation?symbol={ticker}",
                f"EPS estimates: /stock/eps-estimate?symbol={ticker}",
                f"Price target: /stock/price-target?symbol={ticker}",
                f"Revenue estimates: /stock/revenue-estimate?symbol={ticker}",
            ]
        }

    # Source 3: MarketBeat
    result["data_sources"]["marketbeat"] = {
        "name": "MarketBeat",
        "url": f"https://www.marketbeat.com/stocks/NYSE/{ticker.upper()}/forecast/",
        "data_available": ["Analyst ratings", "Price targets", "EPS estimates"],
    }

    # Source 4: CNN Money / TipRanks
    result["data_sources"]["cnn_forecast"] = {
        "name": "CNN Money Forecast",
        "url": f"https://money.cnn.com/quote/forecast/forecast.html?symb={ticker.upper()}",
        "data_available": ["Analyst consensus", "Price target range"],
    }

    # Source 5: Zacks (limited free)
    result["data_sources"]["zacks"] = {
        "name": "Zacks",
        "url": f"https://www.zacks.com/stock/quote/{ticker.upper()}/detailed-estimates",
        "data_available": ["EPS estimates", "Zacks rank", "Estimate revisions"],
    }

    return result


# ============================================================
# PEER DISCOVERY
# ============================================================

def discover_peers(ticker: str) -> Dict:
    """
    Discover comparable/peer companies from multiple sources.

    Peer selection is critical for relative valuation. This function
    aggregates peer suggestions from multiple sources for the
    Quant Analyst to validate and refine.

    Args:
        ticker: Stock ticker

    Returns:
        Dict with peer company suggestions from multiple sources
    """
    result = {
        "ticker": ticker.upper(),
        "data_sources": {},
    }

    # Source 1: Finnhub peers
    if FINNHUB_API_KEY:
        peers_url = f"https://finnhub.io/api/v1/stock/peers?symbol={ticker}&token={FINNHUB_API_KEY}"
        peers_data = _fetch_json(peers_url)
        if isinstance(peers_data, list):
            result["data_sources"]["finnhub"] = {
                "name": "Finnhub Peers",
                "peers": peers_data,
            }

    # Source 2: Yahoo Finance
    result["data_sources"]["yahoo_finance"] = {
        "name": "Yahoo Finance - Comparison",
        "url": f"https://finance.yahoo.com/quote/{ticker.upper()}/",
        "note": "Yahoo shows 'People Also Watch' and sector peers on the quote page",
        "retrieval": f"Use WebFetch on the URL and look for peer company mentions"
    }

    # Source 3: Finviz sector screening
    result["data_sources"]["finviz_sector"] = {
        "name": "Finviz - Sector Peers",
        "url": f"https://finviz.com/screener.ashx?v=111&f=ind_stocksonly&t={ticker.upper()}",
        "description": "Screen for companies in the same industry and similar market cap",
    }

    # Source 4: SEC SIC code
    result["data_sources"]["sec_sic"] = {
        "name": "SEC - Same SIC Code",
        "description": "Companies with the same SIC code filed with the SEC",
        "retrieval": f"Use: python3 tools/edgar-enhanced.py company {ticker} — note the SIC code, "
                     f"then search EDGAR for other companies with the same SIC",
    }

    # Source 5: Web search
    result["data_sources"]["web_search"] = {
        "name": "Web Search",
        "queries": [
            f'"{ticker}" competitors',
            f'"{ticker}" comparable companies',
            f'"{ticker}" peer group valuation',
        ],
        "description": "Search for analyst reports that define the peer group",
    }

    result["peer_selection_criteria"] = {
        "required": [
            "Same or adjacent industry/sub-industry",
            "Similar business model (B2B vs B2C, subscription vs transactional, etc.)",
            "Within 0.5x-2x market cap range (ideally)",
        ],
        "preferred": [
            "Similar growth profile (high-growth with high-growth, mature with mature)",
            "Similar margin structure",
            "Same geographic focus",
            "Similar capital intensity",
        ],
        "avoid": [
            "Conglomerates with mixed segments unless sum-of-parts comparable",
            "Companies in fundamentally different life-cycle stages",
            "Companies with distressed balance sheets (unless subject is also distressed)",
        ],
    }

    return result


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Alternative Data Retrieval",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 tools/alt-data.py insider AAPL
  python3 tools/alt-data.py institutional MSFT
  python3 tools/alt-data.py short-interest TSLA
  python3 tools/alt-data.py ownership-summary GOOGL
  python3 tools/alt-data.py analyst-estimates AMZN
  python3 tools/alt-data.py peers NVDA
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Insider
    insider_parser = subparsers.add_parser("insider", help="Insider trading data")
    insider_parser.add_argument("ticker", help="Stock ticker")

    # Institutional
    inst_parser = subparsers.add_parser("institutional", help="Institutional holdings")
    inst_parser.add_argument("ticker", help="Stock ticker")

    # Short interest
    short_parser = subparsers.add_parser("short-interest", help="Short interest data")
    short_parser.add_argument("ticker", help="Stock ticker")

    # Ownership summary
    own_parser = subparsers.add_parser("ownership-summary", help="Combined ownership picture")
    own_parser.add_argument("ticker", help="Stock ticker")

    # Analyst estimates
    est_parser = subparsers.add_parser("analyst-estimates", help="Consensus estimates")
    est_parser.add_argument("ticker", help="Stock ticker")

    # Peers
    peers_parser = subparsers.add_parser("peers", help="Peer company discovery")
    peers_parser.add_argument("ticker", help="Stock ticker")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "insider":
        result = get_insider_trades(args.ticker)
    elif args.command == "institutional":
        result = get_institutional_holdings(args.ticker)
    elif args.command == "short-interest":
        result = get_short_interest(args.ticker)
    elif args.command == "ownership-summary":
        result = get_ownership_summary(args.ticker)
    elif args.command == "analyst-estimates":
        result = get_analyst_estimates(args.ticker)
    elif args.command == "peers":
        result = discover_peers(args.ticker)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
