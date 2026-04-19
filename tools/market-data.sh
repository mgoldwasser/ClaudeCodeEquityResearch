#!/usr/bin/env bash
# market-data.sh — Retrieve current market data for a ticker
# Usage:
#   ./tools/market-data.sh quote <TICKER>         Get current price and basic data
#   ./tools/market-data.sh profile <TICKER>        Get company profile
#   ./tools/market-data.sh peers <TICKER>          Get peer companies
#   ./tools/market-data.sh stats <TICKER>          Get key statistics
#
# All commands accept --as-of YYYY-MM-DD (see tools/AS_OF.md).
# Most commands wrap Yahoo's live-snapshot API and will hard-fail in historical mode;
# the `history` command is natively filterable.

set -euo pipefail

# shellcheck source=_as_of.sh
source "$(dirname "$0")/_as_of.sh"

# Yahoo Finance unofficial API endpoints
YF_BASE="https://query1.finance.yahoo.com/v8/finance"
YF_V10="https://query1.finance.yahoo.com/v10/finance"
YF_V6="https://query2.finance.yahoo.com/v6/finance"

CURL_OPTS=(-s -L --max-time 10)

# Extract --as-of before argv dispatch; keep remaining args.
as_of_extract_flag "$@"
as_of_resolve "${AS_OF_CLI}"
if [[ ${#REST_ARGS[@]} -gt 0 ]]; then
    set -- "${REST_ARGS[@]}"
else
    set --
fi

usage() {
    echo "Usage: $0 <command> <TICKER> [options] [--as-of YYYY-MM-DD]"
    echo ""
    echo "Commands:"
    echo "  quote <TICKER>              Current price, market cap, volume, basic multiples"
    echo "  profile <TICKER>            Company description, sector, industry, employees"
    echo "  peers <TICKER>              Peer/comparable companies"
    echo "  stats <TICKER>              Key financial statistics and ratios"
    echo "  summary <TICKER>            All-in-one summary (quote + stats + profile)"
    echo "  history <TICKER> [PERIOD]   Historical price data (PERIOD: 1mo,3mo,6mo,1y,2y,5y,max)"
    echo "  options <TICKER>            Options chain data (nearest expiry)"
    echo ""
    echo "--as-of:  Historical retrieval (YYYY-MM-DD). Only 'history' supports past dates;"
    echo "          all other commands hard-fail because Yahoo returns only live data."
    echo ""
    echo "Examples:"
    echo "  $0 quote AAPL"
    echo "  $0 summary MSFT"
    echo "  $0 history GOOGL 1y"
    echo "  $0 history GOOGL 1y --as-of 2023-01-15"
    echo "  $0 options TSLA"
    echo "  $0 peers GOOGL"
    exit 1
}

# Seconds-per-period lookup for historical-mode period1 computation.
# max → 0 (use epoch 0 as period1, i.e., all available history up to as-of).
period_seconds() {
    case "$1" in
        1mo)  echo  2592000 ;;
        3mo)  echo  7776000 ;;
        6mo)  echo 15552000 ;;
        1y)   echo 31536000 ;;
        2y)   echo 63072000 ;;
        5y)   echo 157680000 ;;
        max)  echo 0 ;;  # sentinel: use epoch 0
        *)    echo 31536000 ;;
    esac
}

# Fetch quote data using Yahoo Finance
fetch_quote() {
    as_of_assert_live_only "market-data.sh" "quote" \
        "Yahoo /v7/quote returns only a live snapshot; historical intraday quotes are not available via the free API." \
        "Use: market-data.sh history $1 1mo --as-of <DATE>"
    local ticker="${1^^}"
    echo "Fetching quote for ${ticker}..." >&2

    # Use the Yahoo Finance quote summary endpoint
    local url="https://query1.finance.yahoo.com/v7/finance/quote?symbols=${ticker}"
    local result
    result=$(curl "${CURL_OPTS[@]}" \
        -H "User-Agent: Mozilla/5.0" \
        "$url" 2>/dev/null)

    if [ -z "$result" ]; then
        echo '{"error": "Failed to fetch data. Yahoo Finance may be rate-limiting requests."}'
        return
    fi

    echo "$result" | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)
    quotes = data.get('quoteResponse', {}).get('result', [])
    if not quotes:
        print(json.dumps({'error': 'No data found for ticker'}))
        sys.exit(0)

    q = quotes[0]

    output = {
        'ticker': q.get('symbol', ''),
        'name': q.get('shortName', q.get('longName', '')),
        'exchange': q.get('exchange', ''),
        'currency': q.get('currency', 'USD'),
        'price': {
            'current': q.get('regularMarketPrice', 0),
            'previous_close': q.get('regularMarketPreviousClose', 0),
            'change': q.get('regularMarketChange', 0),
            'change_pct': round(q.get('regularMarketChangePercent', 0), 2),
            'day_high': q.get('regularMarketDayHigh', 0),
            'day_low': q.get('regularMarketDayLow', 0),
            'fifty_two_week_high': q.get('fiftyTwoWeekHigh', 0),
            'fifty_two_week_low': q.get('fiftyTwoWeekLow', 0),
        },
        'valuation': {
            'market_cap_M': round(q.get('marketCap', 0) / 1e6, 1) if q.get('marketCap') else None,
            'enterprise_value_M': round(q.get('enterpriseValue', 0) / 1e6, 1) if q.get('enterpriseValue') else None,
            'trailing_pe': q.get('trailingPE'),
            'forward_pe': q.get('forwardPE'),
            'peg_ratio': q.get('pegRatio'),
            'price_to_book': q.get('priceToBook'),
            'ev_to_ebitda': q.get('enterpriseToEbitda'),
            'ev_to_revenue': q.get('enterpriseToRevenue'),
        },
        'fundamentals': {
            'eps_trailing': q.get('epsTrailingTwelveMonths'),
            'eps_forward': q.get('epsForward'),
            'dividend_yield_pct': round(q.get('dividendYield', 0) * 100, 2) if q.get('dividendYield') else None,
            'dividend_rate': q.get('dividendRate'),
            'beta': q.get('beta'),
        },
        'trading': {
            'volume': q.get('regularMarketVolume'),
            'avg_volume_10d': q.get('averageDailyVolume10Day'),
            'avg_volume_3m': q.get('averageDailyVolume3Month'),
            'shares_outstanding_M': round(q.get('sharesOutstanding', 0) / 1e6, 1) if q.get('sharesOutstanding') else None,
            'float_shares_M': round(q.get('floatShares', 0) / 1e6, 1) if q.get('floatShares') else None,
        },
        'fifty_day_avg': q.get('fiftyDayAverage'),
        'two_hundred_day_avg': q.get('twoHundredDayAverage'),
    }

    print(json.dumps(output, indent=2))
except json.JSONDecodeError:
    print(json.dumps({'error': 'Invalid response from Yahoo Finance'}))
except Exception as e:
    print(json.dumps({'error': str(e)}))
" 2>/dev/null
}

# Fetch company profile
fetch_profile() {
    as_of_assert_live_only "market-data.sh" "profile" \
        "Yahoo profile endpoint has no dated equivalent; sector/industry classifications are always current." \
        "For historical company classification, use: edgar-enhanced.py company $1 --as-of <DATE>"
    local ticker="${1^^}"
    echo "Fetching profile for ${ticker}..." >&2

    local url="https://query1.finance.yahoo.com/v7/finance/quote?symbols=${ticker}"
    local result
    result=$(curl "${CURL_OPTS[@]}" \
        -H "User-Agent: Mozilla/5.0" \
        "$url" 2>/dev/null)

    echo "$result" | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)
    quotes = data.get('quoteResponse', {}).get('result', [])
    if not quotes:
        print(json.dumps({'error': 'No data found'}))
        sys.exit(0)

    q = quotes[0]
    output = {
        'ticker': q.get('symbol', ''),
        'name': q.get('longName', q.get('shortName', '')),
        'sector': q.get('sector', 'N/A'),
        'industry': q.get('industry', 'N/A'),
        'exchange': q.get('exchange', ''),
        'market': q.get('market', ''),
        'quote_type': q.get('quoteType', ''),
        'market_cap_M': round(q.get('marketCap', 0) / 1e6, 1) if q.get('marketCap') else None,
    }
    print(json.dumps(output, indent=2))
except Exception as e:
    print(json.dumps({'error': str(e)}))
" 2>/dev/null
}

# Fetch key statistics
fetch_stats() {
    as_of_assert_live_only "market-data.sh" "stats" \
        "Yahoo key statistics are a live snapshot (TTM metrics computed against current date)." \
        "Use: edgar-enhanced.py financials $1 --as-of <DATE> for historical XBRL facts."
    local ticker="${1^^}"
    echo "Fetching key statistics for ${ticker}..." >&2

    # Get quote data which includes many stats
    local url="https://query1.finance.yahoo.com/v7/finance/quote?symbols=${ticker}"
    local result
    result=$(curl "${CURL_OPTS[@]}" \
        -H "User-Agent: Mozilla/5.0" \
        "$url" 2>/dev/null)

    echo "$result" | python3 -c "
import sys, json

try:
    data = json.load(sys.stdin)
    quotes = data.get('quoteResponse', {}).get('result', [])
    if not quotes:
        print(json.dumps({'error': 'No data found'}))
        sys.exit(0)

    q = quotes[0]

    output = {
        'ticker': q.get('symbol', ''),
        'name': q.get('shortName', ''),
        'valuation_metrics': {
            'market_cap_M': round(q.get('marketCap', 0) / 1e6, 1) if q.get('marketCap') else None,
            'enterprise_value_M': round(q.get('enterpriseValue', 0) / 1e6, 1) if q.get('enterpriseValue') else None,
            'trailing_pe': q.get('trailingPE'),
            'forward_pe': q.get('forwardPE'),
            'peg_ratio': q.get('pegRatio'),
            'price_to_sales_ttm': q.get('priceToSalesTrailing12Months'),
            'price_to_book': q.get('priceToBook'),
            'ev_to_revenue': q.get('enterpriseToRevenue'),
            'ev_to_ebitda': q.get('enterpriseToEbitda'),
        },
        'profitability': {
            'profit_margin': q.get('profitMargins'),
            'operating_margin': q.get('operatingMargins'),
            'return_on_equity': q.get('returnOnEquity'),
            'return_on_assets': q.get('returnOnAssets'),
        },
        'growth': {
            'revenue_growth_quarterly': q.get('revenueGrowth'),
            'earnings_growth_quarterly': q.get('earningsGrowth'),
            'eps_trailing': q.get('epsTrailingTwelveMonths'),
            'eps_forward': q.get('epsForward'),
        },
        'balance_sheet': {
            'total_cash_M': round(q.get('totalCash', 0) / 1e6, 1) if q.get('totalCash') else None,
            'total_debt_M': round(q.get('totalDebt', 0) / 1e6, 1) if q.get('totalDebt') else None,
            'current_ratio': q.get('currentRatio'),
            'book_value_per_share': q.get('bookValue'),
        },
        'risk': {
            'beta': q.get('beta'),
            'fifty_two_week_change': q.get('fiftyTwoWeekChange'),
            'sp500_fifty_two_week_change': q.get('SandP52WeekChange'),
        },
        'shares': {
            'outstanding_M': round(q.get('sharesOutstanding', 0) / 1e6, 1) if q.get('sharesOutstanding') else None,
            'float_M': round(q.get('floatShares', 0) / 1e6, 1) if q.get('floatShares') else None,
            'short_pct_of_float': q.get('shortPercentOfFloat'),
        }
    }
    print(json.dumps(output, indent=2))
except Exception as e:
    print(json.dumps({'error': str(e)}))
" 2>/dev/null
}

# Fetch historical price data
fetch_history() {
    # `history` is Category A: naturally filterable via period2 epoch.
    local ticker
    ticker="$(as_of_upper "$1")"
    local period="${2:-1y}"
    echo "Fetching ${period} historical prices for ${ticker}..." >&2

    # Map period to Yahoo Finance parameters
    local interval="1d"
    case "$period" in
        1mo|3mo) interval="1d" ;;
        6mo|1y) interval="1d" ;;
        2y|5y|max) interval="1wk" ;;
    esac

    local url
    if as_of_is_historical; then
        local p2="${AS_OF_EPOCH}"
        local seconds p1
        seconds="$(period_seconds "$period")"
        if [[ "$seconds" == "0" ]]; then
            p1=0
        else
            p1=$(( p2 - seconds ))
        fi
        url="https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?period1=${p1}&period2=${p2}&interval=${interval}"
        echo "[as-of] history window: $(date -u -r "${p1}" '+%Y-%m-%d' 2>/dev/null || date -u -d "@${p1}" '+%Y-%m-%d') to ${AS_OF}" >&2
    else
        url="https://query1.finance.yahoo.com/v8/finance/chart/${ticker}?range=${period}&interval=${interval}"
    fi
    local result
    result=$(curl "${CURL_OPTS[@]}" \
        -H "User-Agent: Mozilla/5.0" \
        "$url" 2>/dev/null)

    echo "$result" | python3 -c "
import sys, json
from datetime import datetime

try:
    data = json.load(sys.stdin)
    chart = data.get('chart', {}).get('result', [])
    if not chart:
        print(json.dumps({'error': 'No data found'}))
        sys.exit(0)

    c = chart[0]
    timestamps = c.get('timestamp', [])
    indicators = c.get('indicators', {})
    quote = indicators.get('quote', [{}])[0]
    adjclose = indicators.get('adjclose', [{}])[0]

    opens = quote.get('open', [])
    highs = quote.get('high', [])
    lows = quote.get('low', [])
    closes = quote.get('close', [])
    volumes = quote.get('volume', [])
    adj_closes = adjclose.get('adjclose', closes)

    # Calculate summary statistics
    valid_closes = [c for c in closes if c is not None]
    valid_volumes = [v for v in volumes if v is not None]

    if valid_closes:
        current = valid_closes[-1]
        start_price = valid_closes[0]
        max_price = max(valid_closes)
        min_price = min(valid_closes)
        total_return = (current - start_price) / start_price * 100

        # Calculate simple volatility (annualized)
        if len(valid_closes) > 1:
            daily_returns = [(valid_closes[i] - valid_closes[i-1]) / valid_closes[i-1]
                           for i in range(1, len(valid_closes)) if valid_closes[i-1] != 0]
            if daily_returns:
                import math
                mean_return = sum(daily_returns) / len(daily_returns)
                variance = sum((r - mean_return)**2 for r in daily_returns) / len(daily_returns)
                daily_vol = math.sqrt(variance)
                annual_vol = daily_vol * math.sqrt(252) * 100
            else:
                annual_vol = None
        else:
            annual_vol = None

        # Max drawdown
        peak = valid_closes[0]
        max_dd = 0
        for price in valid_closes:
            if price > peak:
                peak = price
            dd = (price - peak) / peak
            if dd < max_dd:
                max_dd = dd
    else:
        total_return = None
        annual_vol = None
        max_dd = None
        max_price = None
        min_price = None

    # Build price data (sample: first 5, last 5, plus monthly samples)
    price_data = []
    for i in range(len(timestamps)):
        if closes[i] is not None:
            price_data.append({
                'date': datetime.fromtimestamp(timestamps[i]).strftime('%Y-%m-%d'),
                'open': round(opens[i], 2) if opens[i] else None,
                'high': round(highs[i], 2) if highs[i] else None,
                'low': round(lows[i], 2) if lows[i] else None,
                'close': round(closes[i], 2) if closes[i] else None,
                'volume': volumes[i],
            })

    output = {
        'ticker': c.get('meta', {}).get('symbol', ''),
        'period': '${period}',
        'data_points': len(price_data),
        'summary': {
            'start_price': round(valid_closes[0], 2) if valid_closes else None,
            'end_price': round(valid_closes[-1], 2) if valid_closes else None,
            'total_return_pct': round(total_return, 2) if total_return else None,
            'period_high': round(max_price, 2) if max_price else None,
            'period_low': round(min_price, 2) if min_price else None,
            'annualized_volatility_pct': round(annual_vol, 2) if annual_vol else None,
            'max_drawdown_pct': round(max_dd * 100, 2) if max_dd else None,
            'avg_daily_volume': round(sum(valid_volumes) / len(valid_volumes)) if valid_volumes else None,
        },
        'prices_sample': {
            'first_5': price_data[:5],
            'last_5': price_data[-5:],
        },
        'full_data_available': f'Total {len(price_data)} data points available',
        'note': 'For full price data, save to CSV using: python3 -c \"import yfinance; yfinance.download(\\'${ticker}\\', period=\\'${period}\\').to_csv(\\'prices.csv\\')\"',
    }

    print(json.dumps(output, indent=2))
except Exception as e:
    print(json.dumps({'error': str(e)}))
" 2>/dev/null
}

# Fetch options data
fetch_options() {
    as_of_assert_live_only "market-data.sh" "options" \
        "Yahoo options chains are live-only; historical options data requires a paid provider." \
        "No free alternative — flag as [DATA GAP] in historical runs."
    local ticker="${1^^}"
    echo "Fetching options data for ${ticker}..." >&2

    local url="https://query1.finance.yahoo.com/v7/finance/options/${ticker}"
    local result
    result=$(curl "${CURL_OPTS[@]}" \
        -H "User-Agent: Mozilla/5.0" \
        "$url" 2>/dev/null)

    echo "$result" | python3 -c "
import sys, json
from datetime import datetime

try:
    data = json.load(sys.stdin)
    chain = data.get('optionChain', {}).get('result', [])
    if not chain:
        print(json.dumps({'error': 'No options data found'}))
        sys.exit(0)

    c = chain[0]
    quote = c.get('quote', {})
    options = c.get('options', [{}])[0]
    expiration_dates = c.get('expirationDates', [])

    calls = options.get('calls', [])
    puts = options.get('puts', [])

    current_price = quote.get('regularMarketPrice', 0)

    # Find ATM options (closest to current price)
    def find_atm(contracts, price):
        if not contracts:
            return None
        closest = min(contracts, key=lambda x: abs(x.get('strike', 0) - price))
        return {
            'strike': closest.get('strike'),
            'last_price': closest.get('lastPrice'),
            'bid': closest.get('bid'),
            'ask': closest.get('ask'),
            'implied_volatility': round(closest.get('impliedVolatility', 0) * 100, 1),
            'open_interest': closest.get('openInterest', 0),
            'volume': closest.get('volume', 0),
            'in_the_money': closest.get('inTheMoney', False),
        }

    # Put/Call ratio
    total_call_oi = sum(c.get('openInterest', 0) for c in calls)
    total_put_oi = sum(p.get('openInterest', 0) for p in puts)
    pc_ratio = round(total_put_oi / total_call_oi, 2) if total_call_oi > 0 else None

    # ATM implied vol
    atm_call = find_atm(calls, current_price)
    atm_put = find_atm(puts, current_price)

    output = {
        'ticker': quote.get('symbol', ''),
        'current_price': current_price,
        'nearest_expiry': datetime.fromtimestamp(options.get('expirationDate', 0)).strftime('%Y-%m-%d') if options.get('expirationDate') else None,
        'all_expiries': [datetime.fromtimestamp(d).strftime('%Y-%m-%d') for d in expiration_dates[:10]],
        'summary': {
            'total_call_contracts': len(calls),
            'total_put_contracts': len(puts),
            'total_call_open_interest': total_call_oi,
            'total_put_open_interest': total_put_oi,
            'put_call_ratio': pc_ratio,
            'atm_call_iv_pct': atm_call.get('implied_volatility') if atm_call else None,
            'atm_put_iv_pct': atm_put.get('implied_volatility') if atm_put else None,
        },
        'atm_call': atm_call,
        'atm_put': atm_put,
        'note': 'Put/Call ratio > 1.0 = bearish sentiment, < 0.7 = bullish sentiment',
    }

    print(json.dumps(output, indent=2))
except Exception as e:
    print(json.dumps({'error': str(e)}))
" 2>/dev/null
}

# All-in-one summary
fetch_summary() {
    as_of_assert_live_only "market-data.sh" "summary" \
        "Summary is a composite of Yahoo live-snapshot endpoints (quote + stats)." \
        "Build a historical snapshot by combining: market-data.sh history $1 1mo --as-of <DATE> + edgar-enhanced.py financials $1 --as-of <DATE>"
    local ticker="${1^^}"
    echo "=== Market Data Summary: ${ticker} ===" >&2
    echo ""
    echo "--- Quote ---"
    fetch_quote "$ticker"
    echo ""
    echo "--- Key Statistics ---"
    fetch_stats "$ticker"
}

# Main command dispatch
case "${1:-}" in
    quote)
        [ -z "${2:-}" ] && usage
        fetch_quote "$2"
        ;;
    profile)
        [ -z "${2:-}" ] && usage
        fetch_profile "$2"
        ;;
    peers)
        [ -z "${2:-}" ] && usage
        as_of_assert_live_only "market-data.sh" "peers" \
            "Yahoo peer lists are live-only and change frequently; no dated equivalent is published." \
            "For historical peer construction, use same-SIC companies from SEC EDGAR as of the as-of date."
        echo "Note: Use python3 tools/alt-data.py peers $2 for comprehensive peer discovery." >&2
        echo "Fetching basic sector/industry info to help identify peers..." >&2
        fetch_profile "$2"
        ;;
    stats)
        [ -z "${2:-}" ] && usage
        fetch_stats "$2"
        ;;
    summary)
        [ -z "${2:-}" ] && usage
        fetch_summary "$2"
        ;;
    history)
        [ -z "${2:-}" ] && usage
        fetch_history "$2" "${3:-1y}"
        ;;
    options)
        [ -z "${2:-}" ] && usage
        fetch_options "$2"
        ;;
    *)
        usage
        ;;
esac
