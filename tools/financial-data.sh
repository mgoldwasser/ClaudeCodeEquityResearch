#!/usr/bin/env bash
# financial-data.sh — SEC EDGAR filing retrieval and basic financial data extraction
# Usage:
#   ./tools/financial-data.sh cik <CIK_NUMBER>           Fetch filings by CIK
#   ./tools/financial-data.sh ticker <TICKER>              Resolve ticker to CIK, then fetch
#   ./tools/financial-data.sh filing <TICKER> <TYPE>       Fetch specific filing (10-K, 10-Q, 8-K)
#   ./tools/financial-data.sh company <TICKER>             Fetch company facts (financials)
#   ./tools/financial-data.sh submissions <TICKER>         List recent submissions

set -euo pipefail

EDGAR_BASE="https://efts.sec.gov/LATEST"
EDGAR_DATA="https://data.sec.gov"
USER_AGENT="EquityResearchSwarm/1.0 (research@example.com)"

# SEC EDGAR requires a User-Agent header with contact info
CURL_OPTS=(-s -H "User-Agent: ${USER_AGENT}" -H "Accept: application/json")

usage() {
    echo "Usage: $0 <command> [args]"
    echo ""
    echo "Commands:"
    echo "  ticker <TICKER>          Resolve ticker to CIK number"
    echo "  cik <CIK>               Fetch filing index by CIK"
    echo "  filing <TICKER> <TYPE>   Fetch specific filing type (10-K, 10-Q, 8-K)"
    echo "  company <TICKER>         Fetch company financial facts from XBRL"
    echo "  submissions <TICKER>     List recent SEC submissions"
    echo ""
    echo "Examples:"
    echo "  $0 ticker AAPL"
    echo "  $0 filing AAPL 10-K"
    echo "  $0 company MSFT"
    echo "  $0 submissions GOOGL"
    exit 1
}

# Resolve ticker to CIK using SEC full-text search
resolve_ticker() {
    local ticker="${1^^}"  # uppercase
    echo "Resolving ticker: ${ticker}" >&2

    # Use the SEC EDGAR company search API
    local result
    result=$(curl "${CURL_OPTS[@]}" \
        "${EDGAR_BASE}/search-index?q=%22${ticker}%22&dateRange=custom&startdt=2020-01-01&forms=10-K")

    if [ -z "$result" ]; then
        # Fallback: use the company tickers JSON
        local tickers_json
        tickers_json=$(curl "${CURL_OPTS[@]}" "${EDGAR_DATA}/files/company_tickers.json")
        local cik
        cik=$(echo "$tickers_json" | python3 -c "
import sys, json
data = json.load(sys.stdin)
ticker = '${ticker}'
for key, val in data.items():
    if val.get('ticker', '').upper() == ticker:
        print(str(val['cik_str']).zfill(10))
        sys.exit(0)
print('NOT_FOUND')
" 2>/dev/null)
        echo "$cik"
    else
        echo "$result" | python3 -c "
import sys, json
data = json.load(sys.stdin)
hits = data.get('hits', {}).get('hits', [])
if hits:
    cik = str(hits[0].get('_source', {}).get('entity_id', '')).zfill(10)
    print(cik)
else:
    print('NOT_FOUND')
" 2>/dev/null
    fi
}

# Fetch company submissions (filing list) by CIK
fetch_submissions() {
    local cik="$1"
    echo "Fetching submissions for CIK: ${cik}" >&2
    curl "${CURL_OPTS[@]}" "${EDGAR_DATA}/submissions/CIK${cik}.json"
}

# Fetch company financial facts (XBRL data)
fetch_company_facts() {
    local cik="$1"
    echo "Fetching company facts for CIK: ${cik}" >&2
    curl "${CURL_OPTS[@]}" "${EDGAR_DATA}/api/xbrl/companyfacts/CIK${cik}.json"
}

# Fetch specific filing type
fetch_filing() {
    local ticker="$1"
    local filing_type="$2"

    local cik
    cik=$(resolve_ticker "$ticker")

    if [ "$cik" = "NOT_FOUND" ] || [ -z "$cik" ]; then
        echo "ERROR: Could not resolve ticker ${ticker} to CIK" >&2
        exit 1
    fi

    echo "Fetching ${filing_type} for ${ticker} (CIK: ${cik})" >&2

    # Get submissions to find the filing
    local submissions
    submissions=$(fetch_submissions "$cik")

    # Extract the most recent filing of the requested type
    echo "$submissions" | python3 -c "
import sys, json

data = json.load(sys.stdin)
recent = data.get('filings', {}).get('recent', {})
forms = recent.get('form', [])
accessions = recent.get('accessionNumber', [])
dates = recent.get('filingDate', [])
primary_docs = recent.get('primaryDocument', [])

filing_type = '${filing_type}'
cik = '${cik}'

found = False
for i, form in enumerate(forms):
    if form == filing_type:
        accession = accessions[i].replace('-', '')
        doc = primary_docs[i]
        date = dates[i]
        url = f'https://www.sec.gov/Archives/edgar/data/{cik.lstrip(\"0\")}/{accession}/{doc}'
        print(json.dumps({
            'form': form,
            'date': date,
            'accession': accessions[i],
            'url': url,
            'company': data.get('name', 'Unknown'),
            'ticker': data.get('tickers', ['Unknown'])[0] if data.get('tickers') else 'Unknown'
        }, indent=2))
        found = True
        break

if not found:
    print(json.dumps({'error': f'No {filing_type} filing found for this company'}))
" 2>/dev/null
}

# Parse financial facts for key metrics
parse_financials() {
    local cik="$1"
    local facts
    facts=$(fetch_company_facts "$cik")

    echo "$facts" | python3 -c "
import sys, json

data = json.load(sys.stdin)
us_gaap = data.get('facts', {}).get('us-gaap', {})

# Key metrics to extract
metrics = {
    'Revenue': ['Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax', 'SalesRevenueNet'],
    'Net Income': ['NetIncomeLoss'],
    'Total Assets': ['Assets'],
    'Total Liabilities': ['Liabilities'],
    'Operating Income': ['OperatingIncomeLoss'],
    'Cash': ['CashAndCashEquivalentsAtCarryingValue'],
    'Total Debt': ['LongTermDebt', 'LongTermDebtAndCapitalLeaseObligations'],
    'Shares Outstanding': ['CommonStockSharesOutstanding', 'WeightedAverageNumberOfShareOutstandingBasicAndDiluted'],
    'EPS': ['EarningsPerShareDiluted'],
    'EBITDA': ['EarningsBeforeInterestTaxesDepreciationAndAmortization']
}

results = {}
for label, keys in metrics.items():
    for key in keys:
        if key in us_gaap:
            units = us_gaap[key].get('units', {})
            for unit_type, values in units.items():
                # Get the most recent annual (10-K) values
                annual = [v for v in values if v.get('form') == '10-K']
                if annual:
                    recent = sorted(annual, key=lambda x: x.get('end', ''), reverse=True)[:5]
                    results[label] = {
                        'unit': unit_type,
                        'values': [{
                            'period_end': v.get('end'),
                            'value': v.get('val'),
                            'filed': v.get('filed')
                        } for v in recent]
                    }
                    break
            if label in results:
                break

print(json.dumps({
    'company': data.get('entityName', 'Unknown'),
    'cik': data.get('cik', ''),
    'metrics': results
}, indent=2))
" 2>/dev/null
}

# Main command dispatch
case "${1:-}" in
    ticker)
        [ -z "${2:-}" ] && usage
        cik=$(resolve_ticker "$2")
        echo "Ticker: ${2^^}"
        echo "CIK: ${cik}"
        ;;
    cik)
        [ -z "${2:-}" ] && usage
        fetch_submissions "$2"
        ;;
    filing)
        [ -z "${2:-}" ] || [ -z "${3:-}" ] && usage
        fetch_filing "$2" "$3"
        ;;
    company)
        [ -z "${2:-}" ] && usage
        cik=$(resolve_ticker "$2")
        if [ "$cik" = "NOT_FOUND" ] || [ -z "$cik" ]; then
            echo "ERROR: Could not resolve ticker $2" >&2
            exit 1
        fi
        parse_financials "$cik"
        ;;
    submissions)
        [ -z "${2:-}" ] && usage
        cik=$(resolve_ticker "$2")
        if [ "$cik" = "NOT_FOUND" ] || [ -z "$cik" ]; then
            echo "ERROR: Could not resolve ticker $2" >&2
            exit 1
        fi
        fetch_submissions "$cik" | python3 -c "
import sys, json
data = json.load(sys.stdin)
recent = data.get('filings', {}).get('recent', {})
forms = recent.get('form', [])
dates = recent.get('filingDate', [])
descs = recent.get('primaryDocDescription', [])

print(f\"Company: {data.get('name', 'Unknown')}\")
print(f\"CIK: {data.get('cik', 'Unknown')}\")
print(f\"SIC: {data.get('sic', 'Unknown')} - {data.get('sicDescription', 'Unknown')}\")
print(f\"\\nRecent Filings (last 20):\")
print(f\"{'Date':<12} {'Form':<10} {'Description'}\")
print('-' * 60)
for i in range(min(20, len(forms))):
    desc = descs[i] if i < len(descs) else ''
    print(f\"{dates[i]:<12} {forms[i]:<10} {desc}\")
" 2>/dev/null
        ;;
    *)
        usage
        ;;
esac
