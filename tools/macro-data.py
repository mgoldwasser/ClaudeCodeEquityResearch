#!/usr/bin/env python3
"""
Macro and Industry Data Retrieval
Fetches economic data from FRED, BLS, BEA, and industry-specific government agencies.

Usage:
  python3 tools/macro-data.py fred GDP                    # Get GDP data from FRED
  python3 tools/macro-data.py fred FEDFUNDS,DGS10,DGS2    # Multiple FRED series
  python3 tools/macro-data.py rates                       # Key interest rates snapshot
  python3 tools/macro-data.py macro-snapshot               # Full macro dashboard
  python3 tools/macro-data.py industry energy              # Industry-specific data sources
  python3 tools/macro-data.py industry pharma              # Pharma/healthcare data sources
  python3 tools/macro-data.py industry tech                # Technology sector data sources
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# ============================================================
# CONFIGURATION
# ============================================================

# FRED API key (free — register at https://fred.stlouisfed.org/docs/api/api_key.html)
FRED_API_KEY = os.environ.get("FRED_API_KEY", "")

USER_AGENT = "EquityResearchSwarm/1.0 (research@example.com)"
HEADERS = {"User-Agent": USER_AGENT, "Accept": "application/json"}

# ============================================================
# FRED API
# ============================================================

# Key FRED series for equity research
FRED_SERIES = {
    # Interest Rates
    "FEDFUNDS": "Federal Funds Effective Rate",
    "DGS2": "2-Year Treasury Yield",
    "DGS10": "10-Year Treasury Yield",
    "DGS30": "30-Year Treasury Yield",
    "T10Y2Y": "10Y-2Y Treasury Spread (yield curve)",
    "T10Y3M": "10Y-3M Treasury Spread",
    "BAMLH0A0HYM2": "High Yield Option-Adjusted Spread",
    "BAMLC0A4CBBB": "BBB Corporate Bond Spread",
    "SOFR": "Secured Overnight Financing Rate",

    # Economic Activity
    "GDP": "Gross Domestic Product (nominal)",
    "GDPC1": "Real GDP",
    "A191RL1Q225SBEA": "Real GDP Growth Rate (annualized)",
    "INDPRO": "Industrial Production Index",
    "RSXFS": "Retail Sales (ex food services)",
    "UMCSENT": "Consumer Sentiment (Michigan)",
    "CSCICP03USM665S": "Consumer Confidence (OECD)",

    # Labor Market
    "UNRATE": "Unemployment Rate",
    "PAYEMS": "Total Nonfarm Payrolls",
    "CES0500000003": "Average Hourly Earnings (private)",
    "ICSA": "Initial Jobless Claims",
    "JTSJOL": "Job Openings (JOLTS)",

    # Inflation
    "CPIAUCSL": "CPI (All Urban Consumers)",
    "CPILFESL": "Core CPI (ex Food & Energy)",
    "PCEPI": "PCE Price Index",
    "PCEPILFE": "Core PCE Price Index",
    "T5YIE": "5-Year Breakeven Inflation Rate",
    "T10YIE": "10-Year Breakeven Inflation Rate",
    "MICH": "Michigan Inflation Expectations (1Y)",

    # Credit & Financial Conditions
    "DRTSCILM": "Bank Lending Standards (C&I loans)",
    "NFCI": "Chicago Fed Financial Conditions Index",
    "STLFSI4": "St. Louis Fed Financial Stress Index",
    "TOTRESNS": "Total Bank Reserves",

    # Housing
    "HOUST": "Housing Starts",
    "CSUSHPINSA": "Case-Shiller Home Price Index",
    "MORTGAGE30US": "30-Year Mortgage Rate",

    # Dollar & Commodities
    "DTWEXBGS": "Trade-Weighted Dollar Index",
    "DCOILWTICO": "WTI Crude Oil Price",
    "GOLDAMGBD228NLBM": "Gold Price (London Fix)",

    # Markets
    "SP500": "S&P 500 Index",
    "VIXCLS": "VIX Volatility Index",
    "WILLRESIPR": "Wilshire 5000 Total Market Index",
}


def fetch_fred_series(series_ids: List[str], api_key: str = "",
                      observation_start: str = "", limit: int = 60) -> Dict:
    """
    Fetch data series from FRED (Federal Reserve Economic Data).

    FRED has 816,000+ data series covering the US and global economy.
    Free API key required (register at fred.stlouisfed.org).

    Args:
        series_ids: List of FRED series IDs
        api_key: FRED API key (or set FRED_API_KEY env var)
        observation_start: Start date (YYYY-MM-DD), defaults to 5 years ago
        limit: Max observations per series

    Returns:
        Dict with series data
    """
    key = api_key or FRED_API_KEY

    if not key:
        # Return guidance on how to use FRED without API key
        return {
            "error": "No FRED API key provided",
            "instructions": {
                "register": "Get a free API key at https://fred.stlouisfed.org/docs/api/api_key.html",
                "set_key": "export FRED_API_KEY='your_key_here'",
                "alternative": "Use WebFetch to access FRED data directly:",
                "urls": {
                    series_id: f"https://fred.stlouisfed.org/series/{series_id}"
                    for series_id in series_ids
                },
                "csv_download": {
                    series_id: f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
                    for series_id in series_ids
                },
            },
            "note": "CSV download URLs work without an API key. "
                    "Use WebFetch to retrieve the CSV data directly."
        }

    if not observation_start:
        observation_start = (datetime.now() - timedelta(days=5 * 365)).strftime("%Y-%m-%d")

    results = {}

    for series_id in series_ids:
        series_id = series_id.strip().upper()
        url = (
            f"https://api.stlouisfed.org/fred/series/observations"
            f"?series_id={series_id}"
            f"&api_key={key}"
            f"&file_type=json"
            f"&observation_start={observation_start}"
            f"&sort_order=desc"
            f"&limit={limit}"
        )

        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode())

            observations = data.get("observations", [])

            # Get series info
            info_url = (
                f"https://api.stlouisfed.org/fred/series"
                f"?series_id={series_id}"
                f"&api_key={key}"
                f"&file_type=json"
            )
            req2 = urllib.request.Request(info_url, headers=HEADERS)
            with urllib.request.urlopen(req2, timeout=15) as resp2:
                info_data = json.loads(resp2.read().decode())

            series_info = info_data.get("seriess", [{}])[0] if info_data.get("seriess") else {}

            results[series_id] = {
                "title": series_info.get("title", FRED_SERIES.get(series_id, series_id)),
                "units": series_info.get("units", ""),
                "frequency": series_info.get("frequency", ""),
                "seasonal_adjustment": series_info.get("seasonal_adjustment", ""),
                "last_updated": series_info.get("last_updated", ""),
                "latest_value": observations[0]["value"] if observations else None,
                "latest_date": observations[0]["date"] if observations else None,
                "observation_count": len(observations),
                "observations": [
                    {"date": obs["date"], "value": obs["value"]}
                    for obs in observations[:20]
                ],
                "fred_url": f"https://fred.stlouisfed.org/series/{series_id}",
            }

        except Exception as e:
            results[series_id] = {
                "error": str(e),
                "title": FRED_SERIES.get(series_id, series_id),
                "fred_url": f"https://fred.stlouisfed.org/series/{series_id}",
                "csv_fallback": f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}",
            }

    return {
        "source": "FRED (Federal Reserve Economic Data)",
        "series_count": len(results),
        "data": results,
    }


# ============================================================
# MACRO SNAPSHOT
# ============================================================

def macro_snapshot(api_key: str = "") -> Dict:
    """
    Get a comprehensive macro dashboard for equity research.

    Retrieves the key macro indicators that matter for equity valuation:
    interest rates, growth, inflation, credit conditions, and market indicators.

    Args:
        api_key: FRED API key

    Returns:
        Dict with macro dashboard
    """
    key = api_key or FRED_API_KEY

    dashboard_series = [
        # Rates
        "FEDFUNDS", "DGS2", "DGS10", "T10Y2Y",
        # Growth
        "A191RL1Q225SBEA", "INDPRO", "UNRATE", "PAYEMS",
        # Inflation
        "CPIAUCSL", "PCEPILFE", "T5YIE",
        # Credit
        "BAMLH0A0HYM2", "BAMLC0A4CBBB",
        # Markets
        "SP500", "VIXCLS",
        # Dollar & Oil
        "DTWEXBGS", "DCOILWTICO",
    ]

    if not key:
        # Provide CSV download URLs that work without API key
        return {
            "note": "No FRED API key set. Providing direct data URLs instead.",
            "instructions": "Use WebFetch to retrieve CSV data from these URLs:",
            "dashboard": {
                series_id: {
                    "name": FRED_SERIES.get(series_id, series_id),
                    "url": f"https://fred.stlouisfed.org/series/{series_id}",
                    "csv": f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}",
                }
                for series_id in dashboard_series
            },
            "combined_csv": (
                "https://fred.stlouisfed.org/graph/fredgraph.csv?id="
                + ",".join(dashboard_series)
            ),
            "set_key": "export FRED_API_KEY='your_key_here' (register at fred.stlouisfed.org)",
        }

    return fetch_fred_series(dashboard_series, key, limit=12)


# ============================================================
# RATES SNAPSHOT
# ============================================================

def rates_snapshot(api_key: str = "") -> Dict:
    """
    Get current interest rate environment.

    Critical for WACC calculation, DCF discounting, and credit analysis.

    Args:
        api_key: FRED API key

    Returns:
        Dict with current rates
    """
    rate_series = [
        "FEDFUNDS", "SOFR",
        "DGS2", "DGS10", "DGS30",
        "T10Y2Y", "T10Y3M",
        "BAMLH0A0HYM2", "BAMLC0A4CBBB",
        "MORTGAGE30US",
        "T5YIE", "T10YIE",
    ]

    return fetch_fred_series(rate_series, api_key, limit=5)


# ============================================================
# INDUSTRY DATA SOURCES
# ============================================================

def industry_data_sources(sector: str) -> Dict:
    """
    Get industry-specific government data sources.

    Government agencies publish extensive industry data that's free and
    authoritative. This function maps sectors to their best data sources.

    Args:
        sector: Industry sector (energy, pharma, tech, financial, retail, etc.)

    Returns:
        Dict with data sources, URLs, and retrieval instructions
    """
    sources = {
        "energy": {
            "agencies": [
                {
                    "name": "EIA (Energy Information Administration)",
                    "url": "https://www.eia.gov/",
                    "api": "https://api.eia.gov/v2/",
                    "api_docs": "https://www.eia.gov/opendata/",
                    "key_datasets": [
                        "Crude oil prices and production",
                        "Natural gas prices and storage",
                        "Electricity generation by source",
                        "Renewable energy capacity and generation",
                        "Petroleum supply and demand",
                        "Energy consumption by sector",
                    ],
                    "registration": "Free API key required",
                    "example_endpoints": [
                        "https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key=YOUR_KEY&frequency=daily&data[0]=value&sort[0][column]=period&sort[0][direction]=desc&length=30",
                        "https://api.eia.gov/v2/natural-gas/pri/sum/data/?api_key=YOUR_KEY",
                    ],
                },
                {
                    "name": "FERC (Federal Energy Regulatory Commission)",
                    "url": "https://www.ferc.gov/",
                    "key_datasets": ["Pipeline approvals", "Electric rates", "Market oversight"],
                },
            ],
            "fred_series": ["DCOILWTICO", "DCOILBRENTEU", "DHHNGSP", "GASREGW"],
        },
        "pharma": {
            "agencies": [
                {
                    "name": "openFDA",
                    "url": "https://open.fda.gov/",
                    "api": "https://api.fda.gov/",
                    "key_datasets": [
                        "Drug approvals (NDA/BLA)",
                        "Adverse event reports (FAERS)",
                        "Drug labeling and recalls",
                        "Clinical trial results",
                        "Medical device approvals (510k, PMA)",
                    ],
                    "registration": "No API key needed (rate limited)",
                    "example_endpoints": [
                        "https://api.fda.gov/drug/drugsfda.json?search=sponsor_name:%22PFIZER%22&limit=10",
                        "https://api.fda.gov/drug/event.json?search=patient.drug.openfda.brand_name:%22LIPITOR%22&limit=5",
                    ],
                },
                {
                    "name": "ClinicalTrials.gov",
                    "url": "https://clinicaltrials.gov/",
                    "api": "https://clinicaltrials.gov/api/v2/",
                    "key_datasets": ["Active clinical trials", "Trial results", "Sponsor pipeline"],
                    "example_endpoints": [
                        "https://clinicaltrials.gov/api/v2/studies?query.spons=Pfizer&pageSize=10",
                    ],
                },
                {
                    "name": "CMS (Centers for Medicare & Medicaid Services)",
                    "url": "https://data.cms.gov/",
                    "key_datasets": ["Drug spending", "Provider payments", "Hospital quality"],
                },
            ],
            "fred_series": ["CUUR0000SEMC01", "CUSR0000SAM"],
        },
        "tech": {
            "agencies": [
                {
                    "name": "USPTO (US Patent & Trademark Office)",
                    "url": "https://patentsview.org/",
                    "api": "https://search.patentsview.org/api/v1/",
                    "key_datasets": [
                        "Patent grants and applications",
                        "Inventor and assignee data",
                        "Patent citations and technology classes",
                        "Patent litigation",
                    ],
                    "registration": "Free API, no key needed",
                    "example_endpoints": [
                        'https://search.patentsview.org/api/v1/patent/?q={"_and":[{"assignee_organization":"Apple Inc."},{"patent_date":{"_gte":"2024-01-01"}}]}&f=["patent_number","patent_title","patent_date"]&per_page=10',
                    ],
                },
                {
                    "name": "FCC (Federal Communications Commission)",
                    "url": "https://www.fcc.gov/",
                    "key_datasets": [
                        "Broadband deployment data",
                        "Spectrum auction results",
                        "Equipment authorization (new device filings)",
                        "Telecommunications market reports",
                    ],
                },
                {
                    "name": "NTIA (National Telecommunications & Information Administration)",
                    "url": "https://www.ntia.gov/",
                    "key_datasets": ["Internet usage statistics", "Broadband policy"],
                },
            ],
            "fred_series": ["ISRATIO", "NEWORDER"],
        },
        "financial": {
            "agencies": [
                {
                    "name": "FDIC",
                    "url": "https://www.fdic.gov/analysis/",
                    "key_datasets": ["Bank call reports", "Deposit data", "Bank failures", "Industry analysis"],
                },
                {
                    "name": "Federal Reserve (H.8 Report)",
                    "url": "https://www.federalreserve.gov/releases/h8/",
                    "key_datasets": ["Commercial bank assets/liabilities", "Lending trends"],
                },
                {
                    "name": "OCC (Comptroller of the Currency)",
                    "url": "https://www.occ.treas.gov/",
                    "key_datasets": ["Bank supervision data", "Enforcement actions"],
                },
                {
                    "name": "FINRA",
                    "url": "https://www.finra.org/finra-data",
                    "key_datasets": ["Short interest", "Trade reporting", "Margin statistics"],
                },
            ],
            "fred_series": ["TOTBKCR", "DRTSCILM", "DRTSCLCC", "BUSLOANS"],
        },
        "retail": {
            "agencies": [
                {
                    "name": "Census Bureau - Retail Trade",
                    "url": "https://www.census.gov/retail/",
                    "api": "https://api.census.gov/data/",
                    "key_datasets": ["Monthly retail sales", "E-commerce quarterly", "Inventory/sales ratios"],
                },
                {
                    "name": "BLS - Consumer Price Index",
                    "url": "https://www.bls.gov/cpi/",
                    "key_datasets": ["Category-level price changes", "Consumer spending patterns"],
                },
            ],
            "fred_series": ["RSXFS", "ECOMSA", "MRTSSM44X72USS", "UMCSENT"],
        },
        "industrial": {
            "agencies": [
                {
                    "name": "Census Bureau - Manufacturing",
                    "url": "https://www.census.gov/manufacturing/",
                    "key_datasets": ["New orders", "Shipments", "Inventories", "Capacity utilization"],
                },
                {
                    "name": "ISM (Institute for Supply Management)",
                    "url": "https://www.ismworld.org/",
                    "key_datasets": ["PMI (Manufacturing & Services)", "New orders", "Employment"],
                },
            ],
            "fred_series": ["INDPRO", "TCU", "NEWORDER", "AMTMNO", "DGORDER"],
        },
        "real_estate": {
            "agencies": [
                {
                    "name": "Census Bureau - Construction",
                    "url": "https://www.census.gov/construction/",
                    "key_datasets": ["Housing starts", "Building permits", "Construction spending"],
                },
                {
                    "name": "HUD (Housing & Urban Development)",
                    "url": "https://www.huduser.gov/portal/datasets/",
                    "key_datasets": ["Fair market rents", "Housing affordability", "Vacancy rates"],
                },
                {
                    "name": "FHFA (Federal Housing Finance Agency)",
                    "url": "https://www.fhfa.gov/data",
                    "key_datasets": ["House Price Index", "Mortgage statistics"],
                },
            ],
            "fred_series": ["HOUST", "CSUSHPINSA", "MORTGAGE30US", "PERMIT", "HSN1F"],
        },
    }

    sector_lower = sector.lower().strip()

    # Try to match sector
    if sector_lower in sources:
        result = sources[sector_lower]
    else:
        # Fuzzy match
        matched = None
        for key in sources:
            if sector_lower in key or key in sector_lower:
                matched = key
                break

        if matched:
            result = sources[matched]
        else:
            return {
                "error": f"Sector '{sector}' not found in database",
                "available_sectors": list(sources.keys()),
                "suggestion": "Use WebSearch to find industry-specific government data sources",
                "general_sources": {
                    "census": "https://data.census.gov/ — Economic census, industry statistics",
                    "bls": "https://www.bls.gov/iag/ — Industry at a Glance",
                    "bea": "https://www.bea.gov/data/industries — Industry economic accounts",
                },
            }

    result["sector"] = sector
    result["general_sources"] = {
        "bls_industry": f"https://www.bls.gov/iag/ — BLS Industry at a Glance",
        "census_data": "https://data.census.gov/ — Economic Census data",
        "bea_industries": "https://www.bea.gov/data/industries — GDP by industry",
    }

    return result


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Macro and Industry Data Retrieval",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 tools/macro-data.py fred GDP
  python3 tools/macro-data.py fred FEDFUNDS,DGS10,DGS2
  python3 tools/macro-data.py rates
  python3 tools/macro-data.py macro-snapshot
  python3 tools/macro-data.py industry energy
  python3 tools/macro-data.py industry pharma
  python3 tools/macro-data.py list-series

Available FRED series (common ones):
  Rates: FEDFUNDS, DGS2, DGS10, DGS30, T10Y2Y, BAMLH0A0HYM2
  Growth: GDP, GDPC1, A191RL1Q225SBEA, INDPRO, UNRATE, PAYEMS
  Inflation: CPIAUCSL, PCEPILFE, T5YIE, T10YIE
  Markets: SP500, VIXCLS, DCOILWTICO, GOLDAMGBD228NLBM
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # FRED
    fred_parser = subparsers.add_parser("fred", help="Fetch FRED series")
    fred_parser.add_argument("series", help="FRED series ID(s), comma-separated")
    fred_parser.add_argument("--api-key", default="", help="FRED API key")
    fred_parser.add_argument("--start", default="", help="Start date (YYYY-MM-DD)")
    fred_parser.add_argument("--limit", type=int, default=60, help="Max observations per series")

    # Rates
    subparsers.add_parser("rates", help="Interest rate snapshot")

    # Macro snapshot
    subparsers.add_parser("macro-snapshot", help="Full macro dashboard")

    # Industry
    industry_parser = subparsers.add_parser("industry", help="Industry-specific data sources")
    industry_parser.add_argument("sector", help="Industry sector")

    # List series
    subparsers.add_parser("list-series", help="List available FRED series")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "fred":
        series_list = [s.strip() for s in args.series.split(",")]
        result = fetch_fred_series(series_list, args.api_key, args.start, args.limit)
    elif args.command == "rates":
        result = rates_snapshot()
    elif args.command == "macro-snapshot":
        result = macro_snapshot()
    elif args.command == "industry":
        result = industry_data_sources(args.sector)
    elif args.command == "list-series":
        result = {
            "available_series": {
                k: v for k, v in sorted(FRED_SERIES.items())
            },
            "total": len(FRED_SERIES),
            "note": "Use any FRED series ID — there are 816,000+ series at fred.stlouisfed.org"
        }
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
