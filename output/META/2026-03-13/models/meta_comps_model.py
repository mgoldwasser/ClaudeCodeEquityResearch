"""
META Platforms, Inc. — Comparable Companies Valuation Model
============================================================
Model Builder Agent | Equity Research Swarm
Date: 2026-03-13
Ticker: META (NASDAQ)

Sources:
- META FY2025 financials: Meta Q4/FY2025 earnings press release (Tier 1)
- Peer multiples: Market data as of early March 2026 [ESTIMATED from consensus/press]
- Consensus estimates: 41-analyst consensus, March 2026 (Tier 5)

PRICE BLINDING: META current stock price is NOT used. All peer EV-based multiples
use reported/estimated figures. Implied fair value is the output — comparison to
market price is the Director's role in Step 2.7.

Peer Set Justification:
- GOOGL: Dominant digital advertising competitor; AI platform; similar revenue scale
- AMZN: Growing digital ad business ($60B+); technology infrastructure overlap; different margin profile
- SNAP: Social media advertising; smaller scale; useful as pure-play comparison
- PINS: Social commerce advertising; niche demographic overlap; high-growth comps

Note: Twitter/X and TikTok are private and excluded. Apple excluded (different business model).
"""

import json
import math
import os

# ============================================================
# SECTION 1: META METRICS (from FY2025 financials)
# ============================================================
# All values in USD millions unless noted

# --- META Actuals (FY2025) ---
META_REVENUE_2025 = 200966        # Meta earnings press release (Tier 1)
META_GROSS_PROFIT_2025 = 164791   # Meta earnings (Tier 1)
META_EBIT_2025 = 83276            # Operating income; Meta earnings (Tier 1)
META_NET_INCOME_2025 = 60458      # Reported; includes $15.93B one-time tax charge (Tier 1)
META_NET_INCOME_NORMALIZED = 78000  # [ESTIMATED: $60.5B + $15.9B tax charge ≈ $76-78B normalized]
META_OCF_2025 = 115800            # Operating cash flow; Meta earnings (Tier 1)
META_CAPEX_2025 = 69691           # Meta earnings (Tier 1)
META_FCF_2025 = 43585             # Meta earnings (Tier 1)
META_EBITDA_2025 = 110000         # [ESTIMATED: EBIT $83.3B + D&A ~$26.7B; D&A not directly disclosed]
META_CASH_2025 = 81592            # Cash + marketable securities (Tier 1)
META_DEBT_2025 = 58744            # Long-term debt (Tier 1)
META_NET_CASH = 22848             # Net cash = cash - LT debt
META_DILUTED_SHARES = 2574        # Millions (Tier 1)
META_EPS_2025_REPORTED = 23.49    # (Tier 1)
META_EPS_2025_NORMALIZED = 30.28  # [ESTIMATED: Net inc normalized / shares = ~$78B / 2574M]

# --- META Forward Estimates ---
META_REVENUE_2026E = 255200       # Consensus: $255.2B (41 analysts, March 2026) (Tier 5)
META_EPS_2026E = 30.19            # Consensus (Tier 5)
META_REVENUE_2027E = 301800       # Consensus (Tier 5)
META_EPS_2027E = 34.90            # Consensus (Tier 5)
# [ASSUMPTION: 2026 EBITDA estimated at ~$110-120B range given CapEx surge & R&D growth]
META_EBITDA_2026E = 115000        # [ESTIMATED: Op inc grows modestly per guidance; D&A also grows]
META_FCF_2026E = 27000            # [ESTIMATED: OCF ~$140B - CapEx ~$125B midpoint; per context memo]

# ============================================================
# SECTION 2: PEER COMPANY DATA
# ============================================================
# [DATA SOURCE: All peer data estimated from publicly available information as of March 2026]
# [NOTE: Enterprise values are ESTIMATED — exact figures require current stock prices]
# Flagged as [ESTIMATED] throughout; Director will update with post-price-reveal data

PEERS = {
    "GOOGL": {
        "name": "Alphabet Inc.",
        "business": "Digital advertising (Search + YouTube), Cloud, Other Bets",
        "revenue_ltm": 370000,          # [ESTIMATED: ~$370B FY2025 estimated] (Tier 2)
        "ebit_ltm": 109000,             # [ESTIMATED: ~29.5% op margin] (Tier 2)
        "ebitda_ltm": 130000,           # [ESTIMATED: EBIT + ~$21B D&A] (Tier 2)
        "net_income_ltm": 88000,        # [ESTIMATED] (Tier 2)
        "fcf_ltm": 68000,               # [ESTIMATED: OCF - CapEx] (Tier 2)
        "revenue_fwd_1yr": 405000,      # [ESTIMATED: ~+10% growth] (Tier 2)
        "eps_ltm": 6.85,                # [ESTIMATED; ~12.8B shares] (Tier 2)
        "eps_fwd_1yr": 8.20,            # [ESTIMATED] (Tier 2)
        "ev": 2100000,                  # [ESTIMATED: ~$2.1T EV] (Tier 2)
        "net_cash": 60000,              # [ESTIMATED: ~$60B net cash] (Tier 2)
        "revenue_growth_1yr": 0.12,     # [ESTIMATED: ~12% FY2025] (Tier 2)
        "gross_margin": 0.585,          # [ESTIMATED] (Tier 2)
        "op_margin": 0.295,             # [ESTIMATED] (Tier 2)
        "ad_revenue_pct": 0.77,         # ~77% of revenue from ads (Tier 2)
    },
    "AMZN": {
        "name": "Amazon.com, Inc.",
        "business": "E-commerce, AWS Cloud, Advertising (~$60B+ run rate)",
        "revenue_ltm": 640000,          # [ESTIMATED: ~$640B FY2025] (Tier 2)
        "ebit_ltm": 68000,              # [ESTIMATED: ~10.6% op margin] (Tier 2)
        "ebitda_ltm": 140000,           # [ESTIMATED: high D&A from fulfillment network] (Tier 2)
        "net_income_ltm": 52000,        # [ESTIMATED] (Tier 2)
        "fcf_ltm": 58000,               # [ESTIMATED] (Tier 2)
        "revenue_fwd_1yr": 710000,      # [ESTIMATED: ~+11% growth] (Tier 2)
        "eps_ltm": 5.04,                # [ESTIMATED; ~10.3B shares] (Tier 2)
        "eps_fwd_1yr": 6.50,            # [ESTIMATED] (Tier 2)
        "ev": 2300000,                  # [ESTIMATED: ~$2.3T EV] (Tier 2)
        "net_cash": -50000,             # [ESTIMATED: net debt position] (Tier 2)
        "revenue_growth_1yr": 0.11,     # [ESTIMATED] (Tier 2)
        "gross_margin": 0.495,          # [ESTIMATED: blended across segments] (Tier 2)
        "op_margin": 0.106,             # [ESTIMATED] (Tier 2)
        "ad_revenue_pct": 0.09,         # ~9% from ads (Tier 2)
    },
    "SNAP": {
        "name": "Snap Inc.",
        "business": "Social media advertising (Snapchat)",
        "revenue_ltm": 6500,            # [ESTIMATED: ~$6.5B FY2025] (Tier 2)
        "ebit_ltm": -500,               # [ESTIMATED: still unprofitable on EBIT basis] (Tier 2)
        "ebitda_ltm": 600,              # [ESTIMATED: EBITDA positive] (Tier 2)
        "net_income_ltm": -600,         # [ESTIMATED: net loss] (Tier 2)
        "fcf_ltm": 200,                 # [ESTIMATED: marginally FCF positive] (Tier 2)
        "revenue_fwd_1yr": 7500,        # [ESTIMATED: ~+15% growth] (Tier 2)
        "eps_ltm": -0.37,               # [ESTIMATED] (Tier 2)
        "eps_fwd_1yr": 0.05,            # [ESTIMATED: approaching breakeven] (Tier 2)
        "ev": 22000,                    # [ESTIMATED: ~$22B EV] (Tier 2)
        "net_cash": 2500,               # [ESTIMATED] (Tier 2)
        "revenue_growth_1yr": 0.16,     # [ESTIMATED] (Tier 2)
        "gross_margin": 0.52,           # [ESTIMATED] (Tier 2)
        "op_margin": -0.077,            # [ESTIMATED] (Tier 2)
        "ad_revenue_pct": 0.98,         # Nearly all ad revenue (Tier 2)
    },
    "PINS": {
        "name": "Pinterest, Inc.",
        "business": "Social commerce advertising (Pinterest)",
        "revenue_ltm": 4000,            # [ESTIMATED: ~$4.0B FY2025] (Tier 2)
        "ebit_ltm": 400,                # [ESTIMATED: ~10% op margin] (Tier 2)
        "ebitda_ltm": 550,              # [ESTIMATED: +D&A ~$150M] (Tier 2)
        "net_income_ltm": 350,          # [ESTIMATED] (Tier 2)
        "fcf_ltm": 480,                 # [ESTIMATED] (Tier 2)
        "revenue_fwd_1yr": 4700,        # [ESTIMATED: ~+17.5% growth] (Tier 2)
        "eps_ltm": 0.50,                # [ESTIMATED] (Tier 2)
        "eps_fwd_1yr": 0.70,            # [ESTIMATED] (Tier 2)
        "ev": 18000,                    # [ESTIMATED: ~$18B EV] (Tier 2)
        "net_cash": 1800,               # [ESTIMATED] (Tier 2)
        "revenue_growth_1yr": 0.18,     # [ESTIMATED] (Tier 2)
        "gross_margin": 0.77,           # [ESTIMATED] (Tier 2)
        "op_margin": 0.100,             # [ESTIMATED] (Tier 2)
        "ad_revenue_pct": 0.99,         # Nearly all ad revenue (Tier 2)
    },
}


# ============================================================
# SECTION 3: MULTIPLE CALCULATIONS
# ============================================================

def calculate_peer_multiples(peers: dict) -> dict:
    """Calculate EV/EBITDA, P/E, EV/Revenue, PEG, EV/FCF for each peer."""
    multiples = {}
    for ticker, data in peers.items():
        m = {"ticker": ticker, "name": data["name"]}

        # EV/EBITDA (LTM)
        m["ev_ebitda_ltm"] = round(data["ev"] / data["ebitda_ltm"], 1) if data["ebitda_ltm"] > 0 else None

        # EV/Revenue (LTM)
        m["ev_revenue_ltm"] = round(data["ev"] / data["revenue_ltm"], 2) if data["revenue_ltm"] > 0 else None

        # EV/Revenue (Forward 1yr)
        m["ev_revenue_fwd"] = round(data["ev"] / data["revenue_fwd_1yr"], 2) if data["revenue_fwd_1yr"] > 0 else None

        # P/E (LTM, normalized) — using EV - net cash to get approximate market cap
        approx_mktcap = data["ev"] - data.get("net_cash", 0)
        if data["net_income_ltm"] > 0 and data.get("eps_ltm", 0) > 0:
            m["pe_ltm"] = round(approx_mktcap / data["net_income_ltm"], 1)
        else:
            m["pe_ltm"] = None

        # P/E (Forward 1yr)
        if data.get("eps_fwd_1yr", 0) > 0:
            # Approximate share price from market cap / estimated shares
            # [ASSUMPTION: Using EV and net cash to derive approx market cap]
            est_shares = data["net_income_ltm"] / data["eps_ltm"] if data["eps_ltm"] > 0 else None
            if est_shares:
                approx_price = approx_mktcap / est_shares / 1  # already in millions
                m["pe_fwd"] = round(approx_price / data["eps_fwd_1yr"], 1)
            else:
                m["pe_fwd"] = None
        else:
            m["pe_fwd"] = None

        # EV/FCF (LTM)
        m["ev_fcf_ltm"] = round(data["ev"] / data["fcf_ltm"], 1) if data.get("fcf_ltm", 0) > 0 else None

        # PEG (P/E forward / growth rate)
        if m["pe_fwd"] and data["revenue_growth_1yr"] > 0:
            m["peg_fwd"] = round(m["pe_fwd"] / (data["revenue_growth_1yr"] * 100), 2)
        else:
            m["peg_fwd"] = None

        # Gross margin, op margin
        m["gross_margin_pct"] = round(data["gross_margin"] * 100, 1)
        m["op_margin_pct"] = round(data["op_margin"] * 100, 1)
        m["revenue_growth_1yr_pct"] = round(data["revenue_growth_1yr"] * 100, 1)

        multiples[ticker] = m
    return multiples


def calculate_meta_multiples() -> dict:
    """Calculate META's current multiples on actuals (no current price — EV unknown)."""
    # [NOTE: Cannot calculate market-cap-based multiples (P/E, EV) without current price]
    # Instead: calculate what current price would imply at various multiples
    meta = {
        "revenue_ltm": META_REVENUE_2025,
        "ebitda_ltm": META_EBITDA_2025,
        "ebit_ltm": META_EBIT_2025,
        "net_income_ltm_reported": META_NET_INCOME_2025,
        "net_income_ltm_normalized": META_NET_INCOME_NORMALIZED,
        "fcf_ltm": META_FCF_2025,
        "revenue_fwd_1yr": META_REVENUE_2026E,
        "eps_fwd_1yr": META_EPS_2026E,
        "diluted_shares_M": META_DILUTED_SHARES,
        "eps_ltm_reported": META_EPS_2025_REPORTED,
        "eps_ltm_normalized": META_EPS_2025_NORMALIZED,
        "net_cash": META_NET_CASH,
        "gross_margin_pct": round(META_GROSS_PROFIT_2025 / META_REVENUE_2025 * 100, 1),
        "op_margin_pct": round(META_EBIT_2025 / META_REVENUE_2025 * 100, 1),
        "revenue_growth_pct": 22.2,  # FY2025 YoY
        "note": "EV/P-based multiples require current stock price (blinded). Implied fair values provided below.",
    }
    return meta


def compute_peer_statistics(multiples: dict, metric: str) -> dict:
    """Compute mean, median, min, max for a given metric across peers."""
    values = [v[metric] for v in multiples.values() if v.get(metric) is not None]
    if not values:
        return {"mean": None, "median": None, "min": None, "max": None, "n": 0}
    values_sorted = sorted(values)
    n = len(values_sorted)
    mean_val = sum(values_sorted) / n
    if n % 2 == 0:
        median_val = (values_sorted[n//2 - 1] + values_sorted[n//2]) / 2
    else:
        median_val = values_sorted[n//2]
    return {
        "mean": round(mean_val, 2),
        "median": round(median_val, 2),
        "min": round(min(values_sorted), 2),
        "max": round(max(values_sorted), 2),
        "n": n,
    }


def compute_z_scores(multiples: dict, metric: str) -> dict:
    """Compute z-scores for a metric across peers."""
    values = {k: v[metric] for k, v in multiples.items() if v.get(metric) is not None}
    if len(values) < 2:
        return {}
    vals = list(values.values())
    mean_v = sum(vals) / len(vals)
    std_v = math.sqrt(sum((x - mean_v)**2 for x in vals) / (len(vals) - 1))
    if std_v == 0:
        return {k: 0.0 for k in values}
    return {k: round((v - mean_v) / std_v, 2) for k, v in values.items()}


def implied_fair_value_from_multiples(peer_stats: dict, meta_metrics: dict) -> dict:
    """
    Derive implied fair value per META share from peer median multiples.

    Method:
    1. Apply peer median EV/EBITDA to META EBITDA → implied EV
    2. Apply peer median EV/Revenue to META revenue → implied EV
    3. Apply peer median P/E to META normalized EPS → implied price
    4. Apply peer median EV/FCF to META FCF → implied EV
    5. Convert EV to per-share equity value using net cash bridge
    """
    implied = {}

    shares = META_DILUTED_SHARES  # millions; no annual share reduction applied here (LTM basis)

    # --- Method 1: EV/EBITDA (LTM) ---
    if peer_stats.get("ev_ebitda_ltm", {}).get("median"):
        m = peer_stats["ev_ebitda_ltm"]["median"]
        ev = META_EBITDA_2025 * m
        equity_v = ev + META_NET_CASH
        implied["ev_ebitda_ltm"] = {
            "multiple_applied": m,
            "implied_ev_M": round(ev, 0),
            "implied_equity_value_M": round(equity_v, 0),
            "implied_price_per_share": round(equity_v / shares, 2),
            "method": "Peer median EV/EBITDA (LTM) × META EBITDA $110B + net cash $22.8B",
            "caveat": "META EBITDA is [ESTIMATED]; D&A not directly disclosed",
        }

    # --- Method 2: EV/Revenue (LTM) ---
    if peer_stats.get("ev_revenue_ltm", {}).get("median"):
        m = peer_stats["ev_revenue_ltm"]["median"]
        ev = META_REVENUE_2025 * m
        equity_v = ev + META_NET_CASH
        implied["ev_revenue_ltm"] = {
            "multiple_applied": m,
            "implied_ev_M": round(ev, 0),
            "implied_equity_value_M": round(equity_v, 0),
            "implied_price_per_share": round(equity_v / shares, 2),
            "method": "Peer median EV/Revenue (LTM) × META revenue $201B + net cash",
            "caveat": "Revenue multiples less relevant for META given margin premium vs. peers",
        }

    # --- Method 3: EV/Revenue (Forward) ---
    if peer_stats.get("ev_revenue_fwd", {}).get("median"):
        m = peer_stats["ev_revenue_fwd"]["median"]
        ev = META_REVENUE_2026E * m
        equity_v = ev + META_NET_CASH
        implied["ev_revenue_fwd"] = {
            "multiple_applied": m,
            "implied_ev_M": round(ev, 0),
            "implied_equity_value_M": round(equity_v, 0),
            "implied_price_per_share": round(equity_v / shares, 2),
            "method": "Peer median EV/Revenue (Fwd) × META consensus FY2026E rev $255.2B + net cash",
        }

    # --- Method 4: P/E (normalized LTM) ---
    # [ASSUMPTION: Use normalized net income ($78B) to remove one-time tax charge]
    if peer_stats.get("pe_ltm", {}).get("median"):
        m = peer_stats["pe_ltm"]["median"]
        # P/E-implied market cap
        implied_mktcap = META_NET_INCOME_NORMALIZED * m  # net income × P/E
        implied_price = implied_mktcap / shares
        implied["pe_ltm_normalized"] = {
            "multiple_applied": m,
            "net_income_used_M": META_NET_INCOME_NORMALIZED,
            "implied_price_per_share": round(implied_price, 2),
            "method": "Peer median P/E (LTM) × META normalized net income $78B / 2574M shares",
            "caveat": "META 2025 net income inflated by $15.93B one-time tax charge; normalized figure used",
        }

    # --- Method 5: P/E (Forward) ---
    if peer_stats.get("pe_fwd", {}).get("median"):
        m = peer_stats["pe_fwd"]["median"]
        implied_price = META_EPS_2026E * m
        implied["pe_fwd"] = {
            "multiple_applied": m,
            "eps_used": META_EPS_2026E,
            "implied_price_per_share": round(implied_price, 2),
            "method": "Peer median P/E (Fwd) × META consensus FY2026E EPS $30.19",
        }

    # --- Method 6: EV/FCF (LTM) ---
    if peer_stats.get("ev_fcf_ltm", {}).get("median"):
        m = peer_stats["ev_fcf_ltm"]["median"]
        ev = META_FCF_2025 * m
        equity_v = ev + META_NET_CASH
        implied["ev_fcf_ltm"] = {
            "multiple_applied": m,
            "implied_ev_M": round(ev, 0),
            "implied_equity_value_M": round(equity_v, 0),
            "implied_price_per_share": round(equity_v / shares, 2),
            "method": "Peer median EV/FCF × META FCF $43.6B + net cash",
            "caveat": "META FCF depressed by CapEx surge; FCF will compress further in 2026-2027",
        }

    # Summary: range of implied values
    prices = [v["implied_price_per_share"] for v in implied.values() if "implied_price_per_share" in v]
    if prices:
        implied["_summary"] = {
            "min_implied_price": round(min(prices), 2),
            "max_implied_price": round(max(prices), 2),
            "mean_implied_price": round(sum(prices) / len(prices), 2),
            "median_implied_price": round(sorted(prices)[len(prices)//2], 2),
            "methodology_count": len(prices),
        }

    return implied


# ============================================================
# SECTION 4: PEER COMP TABLE (printable)
# ============================================================

def print_comp_table(multiples: dict, peer_stats_summary: dict):
    headers = ["Ticker", "EV/EBITDA", "EV/Rev", "EV/Rev Fwd", "P/E LTM", "P/E Fwd", "EV/FCF", "PEG", "GrMgn%", "OpMgn%", "Rev Gr%"]
    print("\n" + "=" * 110)
    print("COMPARABLE COMPANIES TABLE — All multiples [ESTIMATED] from public data")
    print("=" * 110)
    fmt = "{:<8} {:>9} {:>8} {:>10} {:>8} {:>8} {:>8} {:>6} {:>8} {:>8} {:>8}"
    print(fmt.format(*headers))
    print("-" * 110)
    for ticker, m in multiples.items():
        print(fmt.format(
            ticker,
            f"{m.get('ev_ebitda_ltm', 'N/A')}" if m.get('ev_ebitda_ltm') else "N/A",
            f"{m.get('ev_revenue_ltm', 'N/A')}" if m.get('ev_revenue_ltm') else "N/A",
            f"{m.get('ev_revenue_fwd', 'N/A')}" if m.get('ev_revenue_fwd') else "N/A",
            f"{m.get('pe_ltm', 'N/A')}" if m.get('pe_ltm') else "N/A",
            f"{m.get('pe_fwd', 'N/A')}" if m.get('pe_fwd') else "N/A",
            f"{m.get('ev_fcf_ltm', 'N/A')}" if m.get('ev_fcf_ltm') else "N/A",
            f"{m.get('peg_fwd', 'N/A')}" if m.get('peg_fwd') else "N/A",
            f"{m.get('gross_margin_pct', 'N/A')}%" if m.get('gross_margin_pct') else "N/A",
            f"{m.get('op_margin_pct', 'N/A')}%" if m.get('op_margin_pct') else "N/A",
            f"{m.get('revenue_growth_1yr_pct', 'N/A')}%" if m.get('revenue_growth_1yr_pct') else "N/A",
        ))

    print("-" * 110)
    print("\nPeer Median / Mean:")
    for metric in ["ev_ebitda_ltm", "ev_revenue_ltm", "pe_ltm", "pe_fwd", "ev_fcf_ltm"]:
        stats = peer_stats_summary.get(metric, {})
        if stats.get("median"):
            print(f"  {metric}: median={stats['median']}, mean={stats.get('mean')}, "
                  f"min={stats.get('min')}, max={stats.get('max')}")


# ============================================================
# SECTION 5: MAIN
# ============================================================

def main():
    print("=" * 70)
    print("META Platforms Comparable Companies Model — 2026-03-13")
    print("=" * 70)
    print("\nNOTE: All peer data is [ESTIMATED] from public sources (Tier 2).")
    print("Peer EVs use approximate market data; exact figures require live price data.\n")

    # Calculate peer multiples
    peer_multiples = calculate_peer_multiples(PEERS)

    # Calculate statistics for each key metric
    key_metrics = ["ev_ebitda_ltm", "ev_revenue_ltm", "ev_revenue_fwd", "pe_ltm", "pe_fwd", "ev_fcf_ltm", "peg_fwd"]
    peer_stats_summary = {}
    for metric in key_metrics:
        peer_stats_summary[metric] = compute_peer_statistics(peer_multiples, metric)

    # Z-scores
    z_scores = {}
    for metric in ["ev_ebitda_ltm", "pe_ltm", "pe_fwd"]:
        z_scores[metric] = compute_z_scores(peer_multiples, metric)

    # Print comp table
    print_comp_table(peer_multiples, peer_stats_summary)

    # META metrics (no price)
    meta_metrics = calculate_meta_multiples()

    # Implied fair values
    implied_fvs = implied_fair_value_from_multiples(peer_stats_summary, meta_metrics)

    print("\n" + "=" * 70)
    print("IMPLIED FAIR VALUE FOR META FROM PEER COMPS")
    print("=" * 70)
    print("\n[NOTE: PRICE BLINDED — Director compares these to actual price in Step 2.7]\n")
    for method, val in implied_fvs.items():
        if method == "_summary":
            continue
        print(f"  {method}: ${val.get('implied_price_per_share', 'N/A'):,.2f}/share  "
              f"(Multiple: {val.get('multiple_applied', 'N/A')}x)")
        print(f"    → {val.get('method', '')}")
        if val.get('caveat'):
            print(f"    ⚠ Caveat: {val['caveat']}")

    summary = implied_fvs.get("_summary", {})
    if summary:
        print(f"\n  IMPLIED RANGE: ${summary['min_implied_price']:,.2f} — ${summary['max_implied_price']:,.2f}")
        print(f"  MEAN:          ${summary['mean_implied_price']:,.2f}")
        print(f"  MEDIAN:        ${summary['median_implied_price']:,.2f}")

    # META quality vs. peer comparison
    print("\n" + "=" * 70)
    print("META QUALITY METRICS vs. PEER MEDIANS")
    print("=" * 70)
    peer_gross_margins = [v["gross_margin"] for v in PEERS.values()]
    peer_op_margins = [v["op_margin"] for v in PEERS.values()]
    peer_growth = [v["revenue_growth_1yr"] for v in PEERS.values()]
    median_gross = sorted(peer_gross_margins)[len(peer_gross_margins)//2]
    median_op = sorted(peer_op_margins)[len(peer_op_margins)//2]
    median_growth = sorted(peer_growth)[len(peer_growth)//2]
    print(f"  Gross Margin:     META {meta_metrics['gross_margin_pct']:.1f}%  |  Peer Median {median_gross*100:.1f}%  → META PREMIUM")
    print(f"  Op Margin:        META {meta_metrics['op_margin_pct']:.1f}%    |  Peer Median {median_op*100:.1f}%   → META LARGE PREMIUM")
    print(f"  Revenue Growth:   META {meta_metrics['revenue_growth_pct']:.1f}%    |  Peer Median {median_growth*100:.1f}%    → META AT/ABOVE MEDIAN")
    print(f"\n  Conclusion: META deserves a premium to peer median multiples given:")
    print(f"    1. Significantly higher operating margins (41% vs. ~10-30% for peers)")
    print(f"    2. 82% gross margins — highest in peer set")
    print(f"    3. Scale advantages (3.58B DAP — largest social user base)")
    print(f"    4. Constraint: CapEx surge compresses near-term FCF; P/FCF premium less justified in 2026-2027")

    # Compile output
    output = {
        "model": "META_COMPS",
        "date": "2026-03-13",
        "ticker": "META",
        "currency": "USD_millions",
        "price_blinded": True,
        "data_quality": "All peer EVs are ESTIMATED from public sources (Tier 2); Director should update with live market data",
        "peer_set": list(PEERS.keys()),
        "peer_set_justification": {
            "GOOGL": "Primary digital ad competitor; AI platform; similar revenue scale",
            "AMZN": "Growing digital ad business; technology infrastructure overlap",
            "SNAP": "Pure-play social media advertising comps; younger demographic overlap",
            "PINS": "Social commerce; high-growth comps; ad-dependent revenue model",
        },
        "peer_multiples": peer_multiples,
        "peer_statistics": peer_stats_summary,
        "peer_z_scores": z_scores,
        "meta_metrics": meta_metrics,
        "implied_fair_values_per_share": implied_fvs,
        "quality_premium_justification": {
            "gross_margin_pct": meta_metrics["gross_margin_pct"],
            "op_margin_pct": meta_metrics["op_margin_pct"],
            "assessment": "META merits 10-20% premium to peer median multiples on profitability; "
                         "discount warranted on FCF yield given 2026-2027 CapEx surge",
        },
        "key_caveats": [
            "All peer EV data is [ESTIMATED] — update with current market prices for precise multiples",
            "META EV/FCF depressed by historic CapEx surge; FCF will compress further in FY2026",
            "META normalized EPS adjusts for $15.93B one-time FY2025 tax charge",
            "AMZN and GOOGL have significant non-advertising businesses; multiples not directly comparable",
            "No price-based META multiples calculated (blinded)",
        ],
    }

    output_path = "output/META/2026-03-13/models/meta_comps_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {output_path}")

    return output


if __name__ == "__main__":
    main()
