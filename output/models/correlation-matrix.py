#!/usr/bin/env python3
"""Correlation Matrix Calculator for: META,GOOGL,SNAP,PINS"""
import json
import urllib.request
import time

tickers = ["META", "GOOGL", "SNAP", "PINS"]
period = "3y"

def fetch_prices(ticker, days=756):
    """Fetch historical closing prices from Yahoo Finance."""
    end = int(time.time())
    start = end - (days * 86400 * 1.5)  # Extra buffer for weekends
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={int(start)}&period2={end}&interval=1d"
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    prices = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    return [p for p in prices if p is not None]

def calculate_returns(prices):
    """Calculate daily log returns."""
    import math
    returns = []
    for i in range(1, len(prices)):
        if prices[i] > 0 and prices[i-1] > 0:
            returns.append(math.log(prices[i] / prices[i-1]))
    return returns

def correlation(x, y):
    """Pearson correlation coefficient."""
    n = min(len(x), len(y))
    x, y = x[:n], y[:n]
    mx = sum(x) / n
    my = sum(y) / n
    cov = sum((x[i]-mx)*(y[i]-my) for i in range(n)) / (n-1)
    sx = (sum((xi-mx)**2 for xi in x) / (n-1)) ** 0.5
    sy = (sum((yi-my)**2 for yi in y) / (n-1)) ** 0.5
    return cov / (sx * sy) if sx > 0 and sy > 0 else 0

# Fetch all prices
print(f"Fetching {period} historical prices for {len(tickers)} tickers...")
all_returns = {}
for t in tickers:
    try:
        prices = fetch_prices(t)
        all_returns[t] = calculate_returns(prices)
        print(f"  {t}: {len(prices)} prices, {len(all_returns[t])} returns")
        time.sleep(0.5)
    except Exception as e:
        print(f"  {t}: ERROR - {e}")

# Build correlation matrix
print("\nCorrelation Matrix:")
header = "       " + "  ".join(f"{t:>7s}" for t in tickers)
print(header)
matrix = []
for t1 in tickers:
    row = []
    row_str = f"{t1:>6s} "
    for t2 in tickers:
        if t1 in all_returns and t2 in all_returns:
            c = correlation(all_returns[t1], all_returns[t2])
        else:
            c = 0
        row.append(round(c, 3))
        row_str += f"  {c:>6.3f}"
    matrix.append(row)
    print(row_str)

# Effective independent bets (using simplified eigenvalue approach)
avg_corr = 0
count = 0
for i in range(len(tickers)):
    for j in range(i+1, len(tickers)):
        avg_corr += abs(matrix[i][j])
        count += 1
avg_corr /= max(count, 1)

n = len(tickers)
effective_bets = n / (1 + (n-1) * avg_corr)
print(f"\nAverage pairwise correlation: {avg_corr:.3f}")
print(f"Number of positions: {n}")
print(f"Effective independent bets: {effective_bets:.1f}")

# Save to JSON
output = {
    "tickers": tickers,
    "correlation_matrix": matrix,
    "avg_pairwise_correlation": round(avg_corr, 3),
    "effective_independent_bets": round(effective_bets, 1),
    "num_positions": n,
}
with open("output/data/correlation-matrix.json", "w") as f:
    json.dump(output, f, indent=2)
print("\nSaved to output/data/correlation-matrix.json")
