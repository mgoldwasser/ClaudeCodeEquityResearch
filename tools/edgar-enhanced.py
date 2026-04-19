#!/usr/bin/env python3
"""
Enhanced SEC EDGAR Data Retrieval
Extends basic EDGAR access with full filing text, insider trades,
institutional holdings, proxy statements, and structured financial data.

Usage:
  python3 tools/edgar-enhanced.py filing AAPL 10-K          # Get latest 10-K full text URL + metadata
  python3 tools/edgar-enhanced.py filing AAPL 10-Q          # Get latest 10-Q
  python3 tools/edgar-enhanced.py filing AAPL DEF-14A       # Get proxy statement
  python3 tools/edgar-enhanced.py insider AAPL              # Insider trading (Form 4)
  python3 tools/edgar-enhanced.py institutional AAPL        # 13F institutional holdings
  python3 tools/edgar-enhanced.py financials AAPL           # Structured XBRL financials
  python3 tools/edgar-enhanced.py search "artificial intelligence" --form 10-K  # Full-text search
  python3 tools/edgar-enhanced.py company AAPL              # Company info + all recent filings
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _as_of  # noqa: E402

# ============================================================
# CONFIGURATION
# ============================================================

# SEC requires a User-Agent with contact info
USER_AGENT = os.environ.get(
    "SEC_USER_AGENT",
    "EquityResearchSwarm/1.0 (research@example.com)"
)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json",
}

# SEC rate limit: 10 requests per second
SEC_RATE_LIMIT = 0.11  # seconds between requests

BASE_URL = "https://data.sec.gov"
EFTS_URL = "https://efts.sec.gov/LATEST"
EDGAR_URL = "https://www.sec.gov/cgi-bin/browse-edgar"

# ============================================================
# HELPERS
# ============================================================

def _fetch_json(url: str) -> Dict:
    """Fetch JSON from SEC API with rate limiting."""
    time.sleep(SEC_RATE_LIMIT)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}", "url": url, "message": e.read().decode()[:500]}
    except Exception as e:
        return {"error": str(e), "url": url}


def _resolve_cik(ticker: str) -> Optional[str]:
    """Resolve ticker to CIK number."""
    url = f"{BASE_URL}/submissions/CIK{ticker.upper()}.json"
    # Try direct lookup first (works if ticker matches entity name)
    tickers_url = "https://www.sec.gov/files/company_tickers.json"
    data = _fetch_json(tickers_url)
    if "error" in data:
        return None

    for entry in data.values():
        if entry.get("ticker", "").upper() == ticker.upper():
            cik = str(entry["cik_str"]).zfill(10)
            return cik
    return None


# ============================================================
# FILING RETRIEVAL
# ============================================================

def get_filing(ticker: str, filing_type: str, count: int = 1,
               as_of: Optional[date] = None) -> Dict:
    """
    Get SEC filing metadata and URLs for a specific filing type.

    Supports: 10-K, 10-Q, 8-K, DEF-14A (proxy), 20-F, 6-K, S-1, etc.

    Args:
        ticker: Stock ticker
        filing_type: SEC form type (10-K, 10-Q, DEF-14A, etc.)
        count: Number of recent filings to return
        as_of: If set, return only filings with filingDate <= as_of.

    Returns:
        Dict with filing metadata, URLs, and retrieval instructions
    """
    cik = _resolve_cik(ticker)
    if not cik:
        return {"error": f"Could not resolve ticker {ticker} to CIK"}

    # Normalize filing type for URL matching
    filing_type_normalized = filing_type.upper().replace("-", "")

    # Get submissions
    submissions_url = f"{BASE_URL}/submissions/CIK{cik}.json"
    data = _fetch_json(submissions_url)
    if "error" in data:
        return data

    company_name = data.get("name", "Unknown")
    recent = data.get("filings", {}).get("recent", {})

    if not recent:
        return {"error": "No recent filings found", "cik": cik}

    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])
    descriptions = recent.get("primaryDocDescription", [])

    as_of_str = as_of.isoformat() if as_of else None

    results = []
    for i, form in enumerate(forms):
        form_normalized = form.upper().replace("-", "").replace("/A", "")
        target_normalized = filing_type.upper().replace("-", "")

        if as_of_str and dates[i] > as_of_str:
            continue  # lookahead guard

        if form_normalized == target_normalized or form.upper() == filing_type.upper():
            accession_clean = accessions[i].replace("-", "")
            filing_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{cik.lstrip('0')}/{accession_clean}/{primary_docs[i]}"
            )
            index_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{cik.lstrip('0')}/{accession_clean}/"
            )

            results.append({
                "form": form,
                "filing_date": dates[i],
                "accession_number": accessions[i],
                "primary_document": primary_docs[i],
                "description": descriptions[i] if i < len(descriptions) else "",
                "filing_url": filing_url,
                "index_url": index_url,
                "retrieval_instructions": (
                    f"Use WebFetch to retrieve the filing text from: {filing_url}\n"
                    f"If the filing is HTML, extract the text content.\n"
                    f"For the full filing index (all exhibits): {index_url}"
                )
            })

            if len(results) >= count:
                break

    if not results:
        return {
            "error": f"No {filing_type} filings found for {ticker}",
            "company": company_name,
            "cik": cik,
            "suggestion": f"Try searching at: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type={filing_type}&dateb=&owner=include&count=10"
        }

    return {
        "ticker": ticker.upper(),
        "company": company_name,
        "cik": cik,
        "filing_type": filing_type.upper(),
        "filings": results,
        "total_found": len(results),
    }


# ============================================================
# INSIDER TRADING (FORM 4)
# ============================================================

def get_insider_trades(ticker: str, months: int = 12,
                       as_of: Optional[date] = None) -> Dict:
    """
    Get insider trading data from SEC Form 4 filings.

    Form 4 filings are required within 2 business days of any insider
    transaction (purchase, sale, option exercise, gift).

    Args:
        ticker: Stock ticker
        months: Number of months of history to retrieve
        as_of: If set, the window ends on as_of (not today) and Form 4s
               filed after as_of are excluded.

    Returns:
        Dict with insider trading summary and individual transactions
    """
    cik = _resolve_cik(ticker)
    if not cik:
        return {"error": f"Could not resolve ticker {ticker} to CIK"}

    # Get Form 4 filings
    submissions_url = f"{BASE_URL}/submissions/CIK{cik}.json"
    data = _fetch_json(submissions_url)
    if "error" in data:
        return data

    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])

    window_end = as_of if as_of else datetime.now().date()
    cutoff_date = (
        datetime.combine(window_end, datetime.min.time())
        - timedelta(days=months * 30)
    ).strftime("%Y-%m-%d")
    window_end_str = window_end.isoformat()

    form4_filings = []
    for i, form in enumerate(forms):
        if form not in ("4", "4/A"):
            continue
        if dates[i] < cutoff_date or dates[i] > window_end_str:
            continue
        accession_clean = accessions[i].replace("-", "")
        filing_url = (
            f"https://www.sec.gov/Archives/edgar/data/"
            f"{cik.lstrip('0')}/{accession_clean}/{primary_docs[i]}"
        )
        form4_filings.append({
            "form": form,
            "filing_date": dates[i],
            "accession_number": accessions[i],
            "filing_url": filing_url,
        })

    # Also provide OpenInsider as an alternative
    openinsider_url = f"http://openinsider.com/screener?s={ticker.upper()}&o=&pl=&ph=&ll=&lh=&fd=0&fdr=&td=0&tdr=&feession=&cession=&sidTids498=on&sidTidsOther=on&ession=&vession=&pession=&aession=&dession=&tession=&hasaliases=0&Order=5&Sort=0&maxresults=50&start=0"

    return {
        "ticker": ticker.upper(),
        "company": data.get("name", "Unknown"),
        "cik": cik,
        "period": f"Last {months} months (since {cutoff_date})",
        "form4_count": len(form4_filings),
        "form4_filings": form4_filings[:20],  # Latest 20
        "openinsider_url": openinsider_url,
        "retrieval_instructions": (
            f"Found {len(form4_filings)} Form 4 filings in the last {months} months.\n"
            f"To parse individual transactions, use WebFetch on each filing URL.\n"
            f"Form 4 XML contains: reporting person, relationship, transaction type,\n"
            f"shares traded, price, shares owned after transaction.\n\n"
            f"Alternative: Use WebFetch on OpenInsider URL for a pre-parsed summary:\n"
            f"{openinsider_url}"
        ),
        "note": "Form 4 filings are XML. Key fields: reportingOwner/rptOwnerName, "
                "transactionAmounts/transactionShares, transactionPricePerShare, "
                "transactionCode (P=Purchase, S=Sale, A=Award, M=Exercise)"
    }


# ============================================================
# INSTITUTIONAL HOLDINGS (13F)
# ============================================================

def get_institutional_holdings(ticker: str,
                               as_of: Optional[date] = None) -> Dict:
    """
    Get institutional ownership data from SEC 13F filings.

    13F filings are required quarterly from institutional investment managers
    with >$100M AUM. Shows which institutions hold the stock and how much.

    Note: 13F data is delayed (filed 45 days after quarter end).

    Args:
        ticker: Stock ticker
        as_of: If set, the EFTS search window ends on as_of. Third-party
               aggregators (WhaleWisdom, Finviz, Yahoo) are live snapshots
               and are flagged as unsafe for historical mode.

    Returns:
        Dict with institutional ownership guidance and data sources
    """
    cik = _resolve_cik(ticker)
    if not cik:
        return {"error": f"Could not resolve ticker {ticker} to CIK"}

    window_end = as_of if as_of else datetime.now().date()
    window_start = window_end - timedelta(days=120)
    window_end_str = window_end.strftime("%Y-%m-%d")
    window_start_str = window_start.strftime("%Y-%m-%d")
    historical = _as_of.is_historical(as_of)

    aggregator_note = (
        "WARNING: live snapshot — reflects holdings as of today, not as_of. "
        "Use SEC bulk 13F or EFTS search for point-in-time data."
        if historical else
        "Snapshot as of today."
    )

    return {
        "ticker": ticker.upper(),
        "cik": cik,
        "as_of": as_of.isoformat() if as_of else None,
        "data_sources": {
            "sec_bulk_13f": {
                "url": "https://www.sec.gov/data-research/sec-markets-data/13f-securities-data-sets",
                "description": "SEC provides quarterly bulk 13F datasets. "
                               "These contain ALL 13F-reported holdings across ALL institutions.",
                "format": "Tab-separated files, downloadable by quarter",
                "delay": "Available ~2 months after quarter end",
                "as_of_safe": True,
            },
            "sec_efts_search": {
                "url": f"{EFTS_URL}/search-index?q=%22{ticker}%22&dateRange=custom&startdt={window_start_str}&enddt={window_end_str}&forms=13F-HR",
                "description": "Search for 13F-HR filings that mention this ticker",
                "as_of_safe": True,
            },
            "whalewisdom_free": {
                "url": f"https://whalewisdom.com/stock/{ticker.lower()}",
                "description": "WhaleWisdom provides free 13F data for the last 9 quarters. "
                               "Shows top holders, position changes, and ownership concentration.",
                "as_of_safe": False,
                "note": aggregator_note,
            },
            "finviz": {
                "url": f"https://finviz.com/quote.ashx?t={ticker.upper()}&ty=c&ta=1&p=d",
                "description": "Finviz shows institutional ownership percentage and insider ownership.",
                "as_of_safe": False,
                "note": aggregator_note,
            },
            "yahoo_finance": {
                "url": f"https://finance.yahoo.com/quote/{ticker.upper()}/holders/",
                "description": "Yahoo Finance holders tab shows top institutional and mutual fund holders.",
                "as_of_safe": False,
                "note": aggregator_note,
            },
        },
        "retrieval_instructions": (
            (
                f"Historical mode (as_of={window_end_str}): use ONLY sec_bulk_13f "
                "or sec_efts_search. The third-party aggregators are live snapshots "
                "and will leak future holdings into a historical backtest.\n"
            ) if historical else (
                f"Institutional ownership data for {ticker} is available from multiple sources.\n"
                f"Best approach: Use WebFetch on Yahoo Finance holders page for a quick summary,\n"
                f"or WhaleWisdom for more detailed 13F history.\n"
                f"For the most authoritative data, search SEC EDGAR for 13F-HR filings."
            )
        )
    }


# ============================================================
# STRUCTURED FINANCIALS (XBRL)
# ============================================================

def get_financials(ticker: str, metrics: Optional[List[str]] = None,
                   as_of: Optional[date] = None) -> Dict:
    """
    Get structured financial data from SEC XBRL API.

    Retrieves standardized financial metrics from SEC's XBRL database.
    This is the most reliable source of historical financial data.

    Args:
        ticker: Stock ticker
        metrics: Optional list of specific XBRL concepts to retrieve
        as_of: If set, only include observations whose `filed` date is
               on or before as_of (vintage filter — eliminates retroactive
               restatements from being visible in a historical run).

    Returns:
        Dict with structured financial data
    """
    cik = _resolve_cik(ticker)
    if not cik:
        return {"error": f"Could not resolve ticker {ticker} to CIK"}

    if not metrics:
        metrics = [
            # Income Statement
            ("Revenues", "us-gaap"),
            ("RevenueFromContractWithCustomerExcludingAssessedTax", "us-gaap"),
            ("CostOfRevenue", "us-gaap"),
            ("CostOfGoodsAndServicesSold", "us-gaap"),
            ("GrossProfit", "us-gaap"),
            ("OperatingIncomeLoss", "us-gaap"),
            ("NetIncomeLoss", "us-gaap"),
            ("EarningsPerShareBasic", "us-gaap"),
            ("EarningsPerShareDiluted", "us-gaap"),
            # Balance Sheet
            ("Assets", "us-gaap"),
            ("Liabilities", "us-gaap"),
            ("StockholdersEquity", "us-gaap"),
            ("CashAndCashEquivalentsAtCarryingValue", "us-gaap"),
            ("LongTermDebt", "us-gaap"),
            ("LongTermDebtNoncurrent", "us-gaap"),
            ("ShortTermBorrowings", "us-gaap"),
            ("CommonStockSharesOutstanding", "us-gaap"),
            # Cash Flow
            ("NetCashProvidedByUsedInOperatingActivities", "us-gaap"),
            ("PaymentsToAcquirePropertyPlantAndEquipment", "us-gaap"),
            ("PaymentOfDividends", "us-gaap"),
            ("PaymentsForRepurchaseOfCommonStock", "us-gaap"),
            # Profitability
            ("OperatingExpenses", "us-gaap"),
            ("ResearchAndDevelopmentExpense", "us-gaap"),
            ("SellingGeneralAndAdministrativeExpense", "us-gaap"),
            ("InterestExpense", "us-gaap"),
            ("IncomeTaxExpenseBenefit", "us-gaap"),
        ]

    results = {}
    company_url = f"{BASE_URL}/api/xbrl/companyfacts/CIK{cik}.json"
    data = _fetch_json(company_url)

    if "error" in data:
        return data

    company_name = data.get("entityName", "Unknown")
    facts = data.get("facts", {})
    us_gaap = facts.get("us-gaap", {})

    as_of_str = as_of.isoformat() if as_of else None

    for metric_name, taxonomy in metrics:
        if metric_name in us_gaap:
            concept = us_gaap[metric_name]
            units = concept.get("units", {})

            # Get the most common unit (USD, shares, USD/shares)
            for unit_type, values in units.items():
                # Filter to annual (10-K) filings, most recent 5
                annual_values = [
                    v for v in values
                    if v.get("form") in ("10-K", "20-F")
                    and v.get("fp") in ("FY",)
                ]

                # Vintage filter: drop observations filed after as_of so that
                # retroactive restatements can't leak into a historical run.
                if as_of_str:
                    annual_values = [
                        v for v in annual_values
                        if v.get("filed") and v.get("filed") <= as_of_str
                    ]

                if annual_values:
                    # Sort by date, take most recent
                    annual_values.sort(key=lambda x: x.get("end", ""), reverse=True)
                    results[metric_name] = {
                        "label": concept.get("label", metric_name),
                        "unit": unit_type,
                        "annual_data": [
                            {
                                "period_end": v.get("end"),
                                "value": v.get("val"),
                                "form": v.get("form"),
                                "filed": v.get("filed"),
                            }
                            for v in annual_values[:5]
                        ]
                    }
                    break

    return {
        "ticker": ticker.upper(),
        "company": company_name,
        "cik": cik,
        "source": "SEC EDGAR XBRL API",
        "as_of": as_of_str,
        "metrics_found": len(results),
        "metrics_requested": len(metrics),
        "financials": results,
    }


# ============================================================
# FULL-TEXT SEARCH
# ============================================================

def search_filings(query: str, form_type: str = "", ticker: str = "",
                   date_start: str = "", date_end: str = "",
                   as_of: Optional[date] = None) -> Dict:
    """
    Full-text search across all SEC filings.

    Uses SEC's EFTS (Electronic Filing Text Search) system to search
    the full text of all SEC filings since 2001.

    Args:
        query: Search query (supports boolean operators)
        form_type: Filter by form type (10-K, 10-Q, 8-K, etc.)
        ticker: Filter by company ticker
        date_start: Start date (YYYY-MM-DD)
        date_end: End date (YYYY-MM-DD)
        as_of: If set and date_end is unset, caps the search window at as_of.
               Post-fetch result filtering also drops any hit with
               file_date > as_of.

    Returns:
        Dict with search results
    """
    as_of_str = as_of.isoformat() if as_of else None
    if as_of_str and not date_end:
        date_end = as_of_str

    params = {
        "q": query,
        "dateRange": "custom" if (date_start or date_end) else "",
    }

    if form_type:
        params["forms"] = form_type
    if date_start:
        params["startdt"] = date_start
    if date_end:
        params["enddt"] = date_end
    if ticker:
        # Need to resolve ticker to entity name or CIK for filtering
        cik = _resolve_cik(ticker)
        if cik:
            params["q"] = f'"{query}"'  # Exact phrase
            # EFTS doesn't filter by CIK directly in search, but we can add it
            # We'll use the entityName approach instead

    query_string = urllib.parse.urlencode(params)
    search_url = f"{EFTS_URL}/search-index?{query_string}"

    data = _fetch_json(search_url)

    if "error" in data:
        # EFTS might return HTML, try alternate approach
        return {
            "search_url": search_url,
            "alternative_url": f"https://efts.sec.gov/LATEST/search-index?q={urllib.parse.quote(query)}&forms={form_type}",
            "instructions": f"Use WebFetch to search: {search_url}",
            "error": data.get("error", "Unknown error")
        }

    hits = data.get("hits", {})
    total = hits.get("total", {}).get("value", 0)
    results = hits.get("hits", [])

    if as_of_str:
        results = [
            r for r in results
            if r.get("_source", {}).get("file_date", "") <= as_of_str
        ]

    return {
        "query": query,
        "form_type": form_type or "all",
        "as_of": as_of_str,
        "total_results": total,
        "results": [
            {
                "entity": r.get("_source", {}).get("entity_name", ""),
                "form": r.get("_source", {}).get("form_type", ""),
                "filed": r.get("_source", {}).get("file_date", ""),
                "url": f"https://www.sec.gov/Archives/edgar/data/{r.get('_source', {}).get('entity_id', '')}/{r.get('_source', {}).get('file_num', '')}",
                "snippet": r.get("highlight", {}).get("content", [""])[0][:500] if r.get("highlight") else "",
            }
            for r in results[:10]
        ],
        "search_url": search_url,
    }


# ============================================================
# COMPANY OVERVIEW
# ============================================================

def get_company_overview(ticker: str,
                         as_of: Optional[date] = None) -> Dict:
    """
    Get comprehensive company information from SEC.

    Returns company metadata, recent filing list, and links to key documents.

    Args:
        ticker: Stock ticker
        as_of: If set, the filing summary and counts include only filings
               with filingDate <= as_of.

    Returns:
        Dict with company overview
    """
    cik = _resolve_cik(ticker)
    if not cik:
        return {"error": f"Could not resolve ticker {ticker} to CIK"}

    submissions_url = f"{BASE_URL}/submissions/CIK{cik}.json"
    data = _fetch_json(submissions_url)

    if "error" in data:
        return data

    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])

    as_of_str = as_of.isoformat() if as_of else None
    if as_of_str:
        pairs = [(f, d) for f, d in zip(forms, dates) if d <= as_of_str]
        forms = [f for f, _ in pairs]
        dates = [d for _, d in pairs]

    # Categorize recent filings
    filing_summary = {}
    for form, d in zip(forms, dates):
        if form not in filing_summary:
            filing_summary[form] = {"count": 0, "latest": d}
        filing_summary[form]["count"] += 1

    return {
        "ticker": ticker.upper(),
        "company": data.get("name", "Unknown"),
        "cik": cik,
        "as_of": as_of_str,
        "sic": data.get("sic", ""),
        "sic_description": data.get("sicDescription", ""),
        "state": data.get("stateOfIncorporation", ""),
        "fiscal_year_end": data.get("fiscalYearEnd", ""),
        "exchanges": data.get("exchanges", []),
        "ein": data.get("ein", ""),
        "website": data.get("website", ""),
        "phone": data.get("phone", ""),
        "address": data.get("addresses", {}).get("business", {}),
        "filing_summary": dict(sorted(filing_summary.items(), key=lambda x: x[1]["latest"], reverse=True)[:15]),
        "total_recent_filings": len(forms),
        "edgar_page": f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=&dateb=&owner=include&count=40",
        "key_filings": {
            "10-K": f"Use: python3 tools/edgar-enhanced.py filing {ticker} 10-K",
            "10-Q": f"Use: python3 tools/edgar-enhanced.py filing {ticker} 10-Q",
            "DEF-14A": f"Use: python3 tools/edgar-enhanced.py filing {ticker} DEF-14A",
            "8-K": f"Use: python3 tools/edgar-enhanced.py filing {ticker} 8-K",
        }
    }


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Enhanced SEC EDGAR Data Retrieval",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 tools/edgar-enhanced.py filing AAPL 10-K
  python3 tools/edgar-enhanced.py filing AAPL DEF-14A
  python3 tools/edgar-enhanced.py insider MSFT --months 6
  python3 tools/edgar-enhanced.py institutional GOOGL
  python3 tools/edgar-enhanced.py financials AMZN
  python3 tools/edgar-enhanced.py search "artificial intelligence" --form 10-K
  python3 tools/edgar-enhanced.py company TSLA
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Filing
    filing_parser = subparsers.add_parser("filing", help="Get filing metadata and URL")
    filing_parser.add_argument("ticker", help="Stock ticker")
    filing_parser.add_argument("form_type", help="Filing type (10-K, 10-Q, DEF-14A, 8-K, etc.)")
    filing_parser.add_argument("--count", type=int, default=1, help="Number of filings (default: 1)")
    _as_of.add_argument(filing_parser)

    # Insider
    insider_parser = subparsers.add_parser("insider", help="Insider trading data")
    insider_parser.add_argument("ticker", help="Stock ticker")
    insider_parser.add_argument("--months", type=int, default=12, help="Months of history (default: 12)")
    _as_of.add_argument(insider_parser)

    # Institutional
    inst_parser = subparsers.add_parser("institutional", help="Institutional holdings guidance")
    inst_parser.add_argument("ticker", help="Stock ticker")
    _as_of.add_argument(inst_parser)

    # Financials
    fin_parser = subparsers.add_parser("financials", help="XBRL structured financials")
    fin_parser.add_argument("ticker", help="Stock ticker")
    _as_of.add_argument(fin_parser)

    # Search
    search_parser = subparsers.add_parser("search", help="Full-text filing search")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--form", default="", help="Form type filter")
    search_parser.add_argument("--ticker", default="", help="Company ticker filter")
    search_parser.add_argument("--start", default="", help="Start date (YYYY-MM-DD)")
    search_parser.add_argument("--end", default="", help="End date (YYYY-MM-DD)")
    _as_of.add_argument(search_parser)

    # Company
    company_parser = subparsers.add_parser("company", help="Company overview")
    company_parser.add_argument("ticker", help="Stock ticker")
    _as_of.add_argument(company_parser)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    as_of = _as_of.resolve(getattr(args, "as_of", None))

    if args.command == "filing":
        result = get_filing(args.ticker, args.form_type, args.count, as_of=as_of)
    elif args.command == "insider":
        result = get_insider_trades(args.ticker, args.months, as_of=as_of)
    elif args.command == "institutional":
        result = get_institutional_holdings(args.ticker, as_of=as_of)
    elif args.command == "financials":
        result = get_financials(args.ticker, as_of=as_of)
    elif args.command == "search":
        result = search_filings(args.query, args.form, args.ticker, args.start, args.end, as_of=as_of)
    elif args.command == "company":
        result = get_company_overview(args.ticker, as_of=as_of)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
