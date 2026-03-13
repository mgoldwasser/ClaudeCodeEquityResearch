"""
META Platforms, Inc. — Risk Model (Monte Carlo + Stress Tests + VaR/CVaR)
==========================================================================
Model Builder Agent | Equity Research Swarm
Date: 2026-03-13
Ticker: META (NASDAQ)

Sources:
- FY2025 financials: Meta Q4/FY2025 earnings press release (Tier 1)
- CapEx guidance: Meta Q4/FY2025 earnings press release (Tier 1)
- Regulatory background: EC press releases (Tier 1), court filings
- Historical volatility context: Public market data [ESTIMATED]

PRICE BLINDING: No current stock price used. Monte Carlo outputs are in
fair-value-per-share space, derived from the DCF model framework.
Current price comparison is Director's responsibility in Step 2.7.

Monte Carlo Approach:
- Key uncertain parameters drawn from distributions
- 10,000 iterations with fixed random seed (reproducible)
- Parameters: revenue growth, operating margin, CapEx normalization, terminal rate
- Output: distribution of 5-year DCF fair values per share
"""

import json
import math
import os
import random

# Fixed seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# ============================================================
# SECTION 1: BASE PARAMETERS (mirrors DCF model)
# ============================================================

FY2025_REVENUE = 200966          # USD millions; Meta earnings (Tier 1)
FY2025_FCF = 43585               # Meta earnings (Tier 1)
FY2025_EBIT = 83276              # Meta earnings (Tier 1)
FY2025_FOA_ADV_REVENUE = 196175  # Meta earnings (Tier 1)
FY2025_FOA_OTHER_REVENUE = 2584  # Meta earnings (Tier 1)
FY2025_RL_REVENUE = 2207         # Meta earnings (Tier 1)
FY2025_RL_OP_LOSS = -19193      # Meta earnings (Tier 1)
FY2025_NET_CASH = 22848          # USD millions
FY2025_DILUTED_SHARES = 2574    # millions
BASE_WACC = 0.0942               # From DCF model (9.42%)
BASE_TAX_RATE = 0.145            # Normalized mid-case
BASE_CAPEX_2026_PCT = 0.490      # ~49% of revenue in 2026

# --- Stress Test Scenarios (specific named scenarios) ---
STRESS_SCENARIOS = [
    {
        "name": "Recession_2027",
        "label": "Global Recession 2027 — Digital Ad Contraction",
        "description": "US/global recession in 2027 causes digital ad spend to contract 15-20%, "
                       "similar to 2022 pattern but amplified by fixed AI infrastructure costs. "
                       "Meta revenue declines -15% in 2027, recovers slowly.",
        "probability": 0.12,
        "revenue_shock_yr2": -0.15,       # -15% revenue decline in year 2 (2027)
        "revenue_recovery_yr3": 0.05,     # 5% partial recovery in 2028
        "margin_compression": -0.08,      # Op margin -8 percentage points at trough
        "capex_stuck_pct_extra": 0.05,   # CapEx remains elevated (fixed costs)
        "wacc_shock": 0.015,             # Risk-free rate rises +150bps in recession
        "terminal_growth": 0.025,
        "rl_loss_extra": 2000,            # Reality Labs losses persist
    },
    {
        "name": "EU_DMA_Fine_WhatsApp",
        "label": "EU DMA WhatsApp Maximum Fine + Forced Interoperability",
        "description": "EU DMA investigation concludes with maximum fine ($14-16B) AND "
                       "forced interoperability requirement that weakens WhatsApp moat. "
                       "EU revenue growth slows to near-zero for 2 years.",
        "probability": 0.10,
        "revenue_shock_yr1": -0.04,      # -4% EU revenue impact in 2026 (compliance + fine)
        "revenue_shock_yr2": -0.02,      # -2% ongoing in 2027
        "one_time_fine_M": 14000,        # $14B fine (one-time EV hit)
        "eu_growth_penalty": -0.03,      # Ongoing EU growth penalty
        "margin_compression": -0.01,     # Minimal ongoing margin impact
        "wacc_shock": 0.005,
        "terminal_growth": 0.032,
    },
    {
        "name": "CapEx_ROI_Failure",
        "label": "AI Infrastructure ROI Fails to Materialize by 2028",
        "description": "Meta invests $115-135B in 2026 and $80-100B in 2027 in AI compute "
                       "but cannot monetize meaningfully. No Meta AI subscription uptake, "
                       "Llama models fall behind OpenAI/Google. CapEx sunk, free cash flow "
                       "structurally impaired. Market re-rates at lower multiples.",
        "probability": 0.15,
        "revenue_growth_2026": 0.20,    # Revenue growth continues (ads still work)
        "revenue_growth_2027": 0.13,    # But deceleration faster than base
        "capex_yr1_pct": 0.52,          # CapEx at upper end
        "capex_yr2_pct": 0.42,          # Stays elevated as they try again
        "margin_compression_yr1": -0.04,
        "margin_compression_yr2": -0.03,
        "terminal_multiple_penalty": -4.0,  # Market re-rates from 18x to 14x EBITDA
        "wacc_shock": 0.008,
        "terminal_growth": 0.030,
    },
    {
        "name": "Chinese_Advertiser_Pullback",
        "label": "US-China Trade War: Chinese Advertisers Exit Meta",
        "description": "Temu, Shein, and other Chinese e-commerce players ($7B+ estimated spend) "
                       "are forced to exit or dramatically reduce US social media advertising "
                       "due to tariffs, app bans, or political pressure. "
                       "Sudden revenue gap of $5-8B in FY2026.",
        "probability": 0.10,
        "one_time_revenue_loss_M": 6500,  # $6.5B revenue gap [ESTIMATED]
        "growth_recovery_rate": 0.10,    # Partial recovery from other advertisers
        "margin_compression": -0.02,
        "wacc_shock": 0.003,
        "terminal_growth": 0.033,
    },
    {
        "name": "Youth_Mental_Health_Verdict",
        "label": "Youth Mental Health Trial: Adverse Verdict ~$10-20B Settlement",
        "description": "2026 trial calendar produces adverse verdict or settlement for "
                       "youth mental health cases. CFO confirmed 'may result in material loss.' "
                       "Conservative estimate: $10B settlement; aggressive: $20B. "
                       "Using $12B as base for this stress scenario.",
        "probability": 0.12,
        "settlement_M": 12000,           # $12B settlement [ESTIMATED; no disclosed figure]
        "ongoing_compliance_cost_M": 500, # Annual compliance costs post-settlement
        "reputational_revenue_impact": -0.02,  # -2% advertiser soft boycott risk
        "wacc_shock": 0.003,
        "terminal_growth": 0.033,
    },
    {
        "name": "Reality_Labs_Shutdown",
        "label": "Reality Labs Shutdown / Write-Down",
        "description": "Meta discontinues Reality Labs after cumulative losses exceed $90B. "
                       "Write-down of $10-15B in assets. Short-term EPS negative but "
                       "long-term FCF positive (eliminates $19B annual loss). "
                       "Net NPV: ambiguous (near-term charge, long-term positive).",
        "probability": 0.08,
        "write_down_M": 12000,           # One-time write-down [ESTIMATED]
        "annual_loss_elimination_M": 19193,  # Annual RL loss goes to 0
        "year_of_shutdown": 2027,
        "wacc_shock": -0.002,            # Actually reduces risk marginally
        "terminal_growth": 0.035,
    },
]

# ============================================================
# SECTION 2: MONTE CARLO SIMULATION ENGINE
# ============================================================

def normal_sample(mean: float, std: float) -> float:
    """Box-Muller transform for standard normal sample."""
    u1 = random.random()
    u2 = random.random()
    z = math.sqrt(-2 * math.log(max(u1, 1e-10))) * math.cos(2 * math.pi * u2)
    return mean + std * z


def truncated_normal(mean: float, std: float, low: float, high: float) -> float:
    """Normal sample truncated to [low, high]."""
    val = normal_sample(mean, std)
    return max(low, min(high, val))


def run_single_dcf(
    rev_growth_yr1: float,
    rev_growth_yr2: float,
    rev_growth_yr3: float,
    rev_growth_yr4: float,
    rev_growth_yr5: float,
    foa_op_margin_yr1: float,
    foa_op_margin_yr5: float,  # linearly interpolated
    capex_pct_yr1: float,
    capex_pct_yr5: float,  # linearly interpolated
    wacc: float,
    terminal_growth: float,
    tax_rate: float,
    rl_loss_yr5: float,
    share_reduction_annual: float,
    dna_pct: float,
) -> float:
    """
    Simplified 5-year DCF for Monte Carlo — returns fair value per share.
    """
    rev_growths = [rev_growth_yr1, rev_growth_yr2, rev_growth_yr3, rev_growth_yr4, rev_growth_yr5]
    revenue = FY2025_REVENUE
    rl_loss = FY2025_RL_OP_LOSS
    shares = FY2025_DILUTED_SHARES
    cumulative_pv = 0.0

    for i in range(5):
        revenue = revenue * (1 + rev_growths[i])
        # Linearly interpolate FoA margin
        t = i / 4 if i < 4 else 1.0
        foa_margin = foa_op_margin_yr1 + t * (foa_op_margin_yr5 - foa_op_margin_yr1)
        foa_op_income = revenue * foa_margin  # approximate: nearly all revenue is FoA

        # RL loss improves linearly to target
        rl_loss = rl_loss + ((-rl_loss_yr5 - (-FY2025_RL_OP_LOSS)) / 5)  # step toward yr5 target
        ebit = foa_op_income + rl_loss
        nopat = ebit * (1 - tax_rate)

        # CapEx
        t_capex = i / 4 if i < 4 else 1.0
        capex_pct = capex_pct_yr1 + t_capex * (capex_pct_yr5 - capex_pct_yr1)
        capex = revenue * capex_pct
        dna = revenue * dna_pct

        ufcf = nopat + dna - capex
        pv = ufcf / (1 + wacc) ** (i + 1)
        cumulative_pv += pv
        shares = shares * (1 - share_reduction_annual)

    # Terminal value
    terminal_ufcf = ufcf * (1 + terminal_growth)
    if wacc <= terminal_growth:
        return 0.0  # degenerate case
    tv = terminal_ufcf / (wacc - terminal_growth)
    pv_tv = tv / (1 + wacc) ** 5

    ev = cumulative_pv + pv_tv
    equity_val = ev + FY2025_NET_CASH
    # equity_val in $M, shares in M → result in $/share directly
    return max(0.0, equity_val / shares)


def run_monte_carlo(n_iterations: int = 10000) -> dict:
    """
    Run 10,000 DCF iterations with stochastic key parameters.

    Parameter Distributions:
    All [ASSUMPTION] unless noted with data source.
    """
    random.seed(RANDOM_SEED)
    results = []

    # --- Parameter Distributions ---
    # Revenue growth Year 1 (2026): Consensus $255B = +27%; std 3%
    REV_GR_YR1_MEAN = 0.270; REV_GR_YR1_STD = 0.030   # [ASSUMPTION based on consensus ±1σ]
    # Revenue growth Year 2 (2027): Consensus +18%; std 4%
    REV_GR_YR2_MEAN = 0.180; REV_GR_YR2_STD = 0.040
    # Revenue growth Years 3-5: decelerating; std 4-5%
    REV_GR_YR3_MEAN = 0.140; REV_GR_YR3_STD = 0.045
    REV_GR_YR4_MEAN = 0.115; REV_GR_YR4_STD = 0.040
    REV_GR_YR5_MEAN = 0.095; REV_GR_YR5_STD = 0.035

    # FoA operating margin (Year 1)
    FOA_MARGIN_YR1_MEAN = 0.510; FOA_MARGIN_YR1_STD = 0.020
    # FoA operating margin (Year 5, terminal trend)
    FOA_MARGIN_YR5_MEAN = 0.525; FOA_MARGIN_YR5_STD = 0.025

    # CapEx as % of revenue Year 1
    CAPEX_YR1_MEAN = 0.490; CAPEX_YR1_STD = 0.030    # Guidance midpoint ±3%
    # CapEx normalization by Year 5
    CAPEX_YR5_MEAN = 0.235; CAPEX_YR5_STD = 0.030

    # WACC
    WACC_MEAN = 0.0942; WACC_STD = 0.008             # ±80bps uncertainty

    # Terminal growth rate
    TGR_MEAN = 0.035; TGR_STD = 0.006

    # Tax rate
    TAX_MEAN = 0.145; TAX_STD = 0.015

    # Reality Labs loss at Year 5 (absolute, millions; negative = still loss)
    RL_LOSS_YR5_MEAN = 14000; RL_LOSS_YR5_STD = 3000  # still $14B loss but with uncertainty

    # Share reduction annual rate
    SHARE_REDUCTION_MEAN = 0.015; SHARE_REDUCTION_STD = 0.005

    # D&A % of revenue (simplification)
    DNA_MEAN = 0.135; DNA_STD = 0.010

    for _ in range(n_iterations):
        rv1 = truncated_normal(REV_GR_YR1_MEAN, REV_GR_YR1_STD, -0.10, 0.45)
        rv2 = truncated_normal(REV_GR_YR2_MEAN, REV_GR_YR2_STD, -0.20, 0.35)
        rv3 = truncated_normal(REV_GR_YR3_MEAN, REV_GR_YR3_STD, -0.15, 0.30)
        rv4 = truncated_normal(REV_GR_YR4_MEAN, REV_GR_YR4_STD, -0.10, 0.25)
        rv5 = truncated_normal(REV_GR_YR5_MEAN, REV_GR_YR5_STD, -0.05, 0.20)
        foa_m1 = truncated_normal(FOA_MARGIN_YR1_MEAN, FOA_MARGIN_YR1_STD, 0.35, 0.65)
        foa_m5 = truncated_normal(FOA_MARGIN_YR5_MEAN, FOA_MARGIN_YR5_STD, 0.35, 0.65)
        cx1 = truncated_normal(CAPEX_YR1_MEAN, CAPEX_YR1_STD, 0.35, 0.65)
        cx5 = truncated_normal(CAPEX_YR5_MEAN, CAPEX_YR5_STD, 0.15, 0.40)
        wacc_v = truncated_normal(WACC_MEAN, WACC_STD, 0.06, 0.14)
        tgr_v = truncated_normal(TGR_MEAN, TGR_STD, 0.015, 0.055)
        tax_v = truncated_normal(TAX_MEAN, TAX_STD, 0.08, 0.25)
        rl_v = truncated_normal(RL_LOSS_YR5_MEAN, RL_LOSS_YR5_STD, 5000, 25000)
        sr_v = truncated_normal(SHARE_REDUCTION_MEAN, SHARE_REDUCTION_STD, 0.005, 0.030)
        dna_v = truncated_normal(DNA_MEAN, DNA_STD, 0.090, 0.180)

        # Ensure WACC > terminal growth (model constraint)
        if wacc_v <= tgr_v:
            tgr_v = wacc_v - 0.01

        fv = run_single_dcf(
            rev_growth_yr1=rv1,
            rev_growth_yr2=rv2,
            rev_growth_yr3=rv3,
            rev_growth_yr4=rv4,
            rev_growth_yr5=rv5,
            foa_op_margin_yr1=foa_m1,
            foa_op_margin_yr5=foa_m5,
            capex_pct_yr1=cx1,
            capex_pct_yr5=cx5,
            wacc=wacc_v,
            terminal_growth=tgr_v,
            tax_rate=tax_v,
            rl_loss_yr5=rl_v,
            share_reduction_annual=sr_v,
            dna_pct=dna_v,
        )
        results.append(fv)

    return analyze_distribution(results)


def analyze_distribution(values: list) -> dict:
    """Compute summary statistics and percentile distribution."""
    v_sorted = sorted(values)
    n = len(v_sorted)

    def percentile(p):
        idx = int(p / 100 * n)
        return round(v_sorted[min(idx, n-1)], 2)

    mean_v = sum(v_sorted) / n
    variance = sum((x - mean_v)**2 for x in v_sorted) / n
    std_v = math.sqrt(variance)

    # VaR and CVaR at 5% and 10% confidence levels
    var_5pct_idx = int(0.05 * n)
    var_10pct_idx = int(0.10 * n)
    var_5pct = v_sorted[var_5pct_idx]   # Value at Risk: 5th percentile
    var_10pct = v_sorted[var_10pct_idx]  # Value at Risk: 10th percentile
    cvar_5pct = sum(v_sorted[:var_5pct_idx]) / max(var_5pct_idx, 1)   # CVaR: mean of bottom 5%
    cvar_10pct = sum(v_sorted[:var_10pct_idx]) / max(var_10pct_idx, 1)  # CVaR: mean of bottom 10%

    # Build histogram buckets
    min_v = v_sorted[0]
    max_v = v_sorted[-1]
    n_buckets = 20
    bucket_size = (max_v - min_v) / n_buckets if max_v > min_v else 1
    histogram = []
    for b in range(n_buckets):
        low = min_v + b * bucket_size
        high = low + bucket_size
        count = sum(1 for x in v_sorted if low <= x < high)
        histogram.append({
            "bucket_low": round(low, 0),
            "bucket_high": round(high, 0),
            "count": count,
            "pct_of_total": round(count / n * 100, 1),
        })

    return {
        "n_iterations": n,
        "mean": round(mean_v, 2),
        "median": percentile(50),
        "std_dev": round(std_v, 2),
        "min": round(min_v, 2),
        "max": round(max_v, 2),
        "p5": percentile(5),
        "p10": percentile(10),
        "p25": percentile(25),
        "p75": percentile(75),
        "p90": percentile(90),
        "p95": percentile(95),
        "var_5pct": round(var_5pct, 2),
        "var_10pct": round(var_10pct, 2),
        "cvar_5pct": round(cvar_5pct, 2),
        "cvar_10pct": round(cvar_10pct, 2),
        "histogram": histogram,
        "probability_above_300": round(sum(1 for x in v_sorted if x > 300) / n * 100, 1),
        "probability_above_400": round(sum(1 for x in v_sorted if x > 400) / n * 100, 1),
        "probability_above_500": round(sum(1 for x in v_sorted if x > 500) / n * 100, 1),
        "probability_above_600": round(sum(1 for x in v_sorted if x > 600) / n * 100, 1),
        "probability_above_700": round(sum(1 for x in v_sorted if x > 700) / n * 100, 1),
        "probability_below_200": round(sum(1 for x in v_sorted if x < 200) / n * 100, 1),
        "probability_below_300": round(sum(1 for x in v_sorted if x < 300) / n * 100, 1),
        "probability_below_400": round(sum(1 for x in v_sorted if x < 400) / n * 100, 1),
    }


# ============================================================
# SECTION 3: STRESS TEST CALCULATIONS
# ============================================================

def run_stress_test(scenario: dict) -> dict:
    """
    Run a named stress test scenario. Returns impact on fair value per share.
    Uses a simplified 5-year DCF adjusted for the scenario.
    """
    name = scenario["name"]
    result = {"scenario": name, "label": scenario["label"],
              "probability": scenario["probability"],
              "description": scenario["description"]}

    if name == "Recession_2027":
        rev_growths = [0.24, scenario["revenue_shock_yr2"],
                       scenario["revenue_recovery_yr3"], 0.10, 0.09]
        foa_margin_yr1 = 0.510 + scenario["margin_compression"]
        foa_margin_yr5 = 0.515
        cx1 = BASE_CAPEX_2026_PCT + scenario.get("capex_stuck_pct_extra", 0)
        cx5 = 0.260  # stays elevated
        wacc = BASE_WACC + scenario["wacc_shock"]
        tgr = scenario["terminal_growth"]
        rl_y5 = 15000

    elif name == "EU_DMA_Fine_WhatsApp":
        rev_growths = [0.27 + scenario.get("revenue_shock_yr1", 0),
                       0.18 + scenario.get("revenue_shock_yr2", 0),
                       0.14, 0.11, 0.09]
        foa_margin_yr1 = 0.510 + scenario.get("margin_compression", 0)
        foa_margin_yr5 = 0.522
        cx1 = BASE_CAPEX_2026_PCT
        cx5 = 0.235
        wacc = BASE_WACC + scenario["wacc_shock"]
        tgr = scenario["terminal_growth"]
        rl_y5 = 14000
        # One-time fine as EV reduction
        result["one_time_ev_reduction_M"] = scenario.get("one_time_fine_M", 0)

    elif name == "CapEx_ROI_Failure":
        rev_growths = [scenario["revenue_growth_2026"],
                       scenario["revenue_growth_2027"],
                       0.11, 0.09, 0.08]
        foa_margin_yr1 = 0.510 + scenario["margin_compression_yr1"]
        foa_margin_yr5 = 0.515
        cx1 = scenario["capex_yr1_pct"]
        cx5 = 0.260
        wacc = BASE_WACC + scenario["wacc_shock"]
        tgr = scenario["terminal_growth"]
        rl_y5 = 16000
        result["terminal_multiple_penalty"] = scenario["terminal_multiple_penalty"]

    elif name == "Chinese_Advertiser_Pullback":
        one_time_rev_loss = scenario["one_time_revenue_loss_M"]
        rev_adj_yr1 = (FY2025_REVENUE * 0.27 - one_time_rev_loss) / FY2025_REVENUE
        rev_growths = [rev_adj_yr1,
                       0.20 + scenario["revenue_shock_yr1"] if "revenue_shock_yr1" in scenario else 0.20,
                       0.15, 0.12, 0.10]
        foa_margin_yr1 = 0.510 + scenario.get("margin_compression", 0)
        foa_margin_yr5 = 0.522
        cx1 = BASE_CAPEX_2026_PCT
        cx5 = 0.235
        wacc = BASE_WACC + scenario["wacc_shock"]
        tgr = scenario["terminal_growth"]
        rl_y5 = 14000

    elif name == "Youth_Mental_Health_Verdict":
        rev_growths = [0.27 + scenario.get("reputational_revenue_impact", 0),
                       0.18, 0.14, 0.11, 0.09]
        foa_margin_yr1 = 0.510
        foa_margin_yr5 = 0.522
        cx1 = BASE_CAPEX_2026_PCT
        cx5 = 0.235
        wacc = BASE_WACC + scenario["wacc_shock"]
        tgr = scenario["terminal_growth"]
        rl_y5 = 14000
        result["one_time_ev_reduction_M"] = scenario.get("settlement_M", 0)
        result["ongoing_cost_M"] = scenario.get("ongoing_compliance_cost_M", 0)

    elif name == "Reality_Labs_Shutdown":
        # Bull scenario: kills $19B/yr in losses but takes write-down
        rev_growths = [0.27, 0.19, 0.15, 0.12, 0.10]  # Revenue same (RL was tiny)
        foa_margin_yr1 = 0.515
        foa_margin_yr5 = 0.530
        cx1 = BASE_CAPEX_2026_PCT - 0.02  # Some CapEx saved
        cx5 = 0.220
        wacc = BASE_WACC + scenario["wacc_shock"]
        tgr = scenario["terminal_growth"]
        rl_y5 = 0  # No more RL losses after shutdown
        result["one_time_ev_reduction_M"] = scenario.get("write_down_M", 0)
    else:
        return {"error": f"Unknown scenario: {name}"}

    fv = run_single_dcf(
        rev_growth_yr1=rev_growths[0],
        rev_growth_yr2=rev_growths[1],
        rev_growth_yr3=rev_growths[2],
        rev_growth_yr4=rev_growths[3],
        rev_growth_yr5=rev_growths[4],
        foa_op_margin_yr1=foa_margin_yr1,
        foa_op_margin_yr5=foa_margin_yr5,
        capex_pct_yr1=cx1,
        capex_pct_yr5=cx5,
        wacc=wacc,
        terminal_growth=tgr,
        tax_rate=BASE_TAX_RATE,
        rl_loss_yr5=rl_y5,
        share_reduction_annual=0.015,
        dna_pct=0.135,
    )

    # Apply one-time EV deductions
    one_time_reduction = result.pop("one_time_ev_reduction_M", 0)
    # one_time_reduction in $M, shares in M → per-share impact = $M / M shares = $/share
    fv_after_one_time = fv - (one_time_reduction / FY2025_DILUTED_SHARES)

    result.update({
        "fair_value_before_one_time": round(fv, 2),
        "one_time_ev_reduction_M": one_time_reduction,
        "per_share_one_time_impact": round(one_time_reduction / FY2025_DILUTED_SHARES, 2),
        "fair_value_after_one_time": round(fv_after_one_time, 2),
        "wacc_used": round(wacc * 100, 2),
        "terminal_growth_used": tgr,
    })

    return result


# ============================================================
# SECTION 4: COMBINED TAIL RISK SCENARIO
# ============================================================

def combined_tail_risk() -> dict:
    """
    Compound stress test: recession + EU fine + CapEx ROI failure simultaneously.
    This is the 'perfect storm' bear case.
    Approximate probability: 2-3% (joint probability of correlated events).
    """
    random.seed(RANDOM_SEED)
    # Worst-of parameters
    fv = run_single_dcf(
        rev_growth_yr1=0.18,    # Growth below consensus + Chinese pullback
        rev_growth_yr2=-0.12,   # Recession in 2027
        rev_growth_yr3=0.03,    # Slow recovery
        rev_growth_yr4=0.07,
        rev_growth_yr5=0.08,
        foa_op_margin_yr1=0.45,  # Severe compression
        foa_op_margin_yr5=0.49,
        capex_pct_yr1=0.52,
        capex_pct_yr5=0.28,
        wacc=0.1100,             # Risk-free rate up 170bps
        terminal_growth=0.025,
        tax_rate=0.175,          # EU fines raise ETR
        rl_loss_yr5=17000,       # RL losses remain elevated
        share_reduction_annual=0.008,  # Buybacks reduced to conserve cash
        dna_pct=0.140,
    )
    # Additional one-time charges: EU fine $14B + litigation settlement $12B + RL writedown $8B
    total_one_time = 34000  # $34B
    fv_adj = fv - (total_one_time / FY2025_DILUTED_SHARES)

    return {
        "scenario": "Combined_Tail_Risk",
        "label": "Perfect Storm Bear Case (Recession + EU + CapEx Failure)",
        "probability": 0.02,
        "fair_value_before_charges": round(fv, 2),
        "total_one_time_charges_M": total_one_time,
        "per_share_one_time": round(total_one_time / FY2025_DILUTED_SHARES, 2),
        "fair_value_after_charges": round(max(fv_adj, 0), 2),
        "wacc_used": 11.00,
        "components": ["Recession 2027", "EU WhatsApp fine $14B", "Youth mental health $12B",
                       "RL write-down $8B", "CapEx ROI failure"],
    }


# ============================================================
# SECTION 5: MAIN
# ============================================================

def main():
    print("=" * 70)
    print("META Platforms Risk Model — 2026-03-13")
    print(f"Monte Carlo: 10,000 iterations (seed={RANDOM_SEED})")
    print("=" * 70)

    # --- Run Monte Carlo ---
    print("\nRunning Monte Carlo simulation (10,000 iterations)...")
    mc_results = run_monte_carlo(10000)

    print(f"\nMonte Carlo Results (Fair Value Per Share Distribution):")
    print(f"  Mean:        ${mc_results['mean']:>8,.2f}")
    print(f"  Median:      ${mc_results['median']:>8,.2f}")
    print(f"  Std Dev:     ${mc_results['std_dev']:>8,.2f}")
    print(f"  P5  (5th):   ${mc_results['p5']:>8,.2f}")
    print(f"  P10 (10th):  ${mc_results['p10']:>8,.2f}")
    print(f"  P25 (25th):  ${mc_results['p25']:>8,.2f}")
    print(f"  P50 (50th):  ${mc_results['median']:>8,.2f}")
    print(f"  P75 (75th):  ${mc_results['p75']:>8,.2f}")
    print(f"  P90 (90th):  ${mc_results['p90']:>8,.2f}")
    print(f"  P95 (95th):  ${mc_results['p95']:>8,.2f}")
    print(f"\n  VaR (5%):    ${mc_results['var_5pct']:>8,.2f}  [5% chance FV < this]")
    print(f"  CVaR (5%):   ${mc_results['cvar_5pct']:>8,.2f}  [Mean of bottom 5% outcomes]")
    print(f"  VaR (10%):   ${mc_results['var_10pct']:>8,.2f}")
    print(f"  CVaR (10%):  ${mc_results['cvar_10pct']:>8,.2f}")

    print(f"\n  Probability FV > $300:  {mc_results['probability_above_300']:.1f}%")
    print(f"  Probability FV > $400:  {mc_results['probability_above_400']:.1f}%")
    print(f"  Probability FV > $500:  {mc_results['probability_above_500']:.1f}%")
    print(f"  Probability FV > $600:  {mc_results['probability_above_600']:.1f}%")
    print(f"  Probability FV > $700:  {mc_results['probability_above_700']:.1f}%")
    print(f"  Probability FV < $200:  {mc_results['probability_below_200']:.1f}%")
    print(f"  Probability FV < $300:  {mc_results['probability_below_300']:.1f}%")
    print(f"  Probability FV < $400:  {mc_results['probability_below_400']:.1f}%")

    # --- Run Named Stress Tests ---
    print("\n" + "=" * 70)
    print("NAMED STRESS TEST RESULTS")
    print("=" * 70)
    stress_results = []
    for scenario in STRESS_SCENARIOS:
        sr = run_stress_test(scenario)
        stress_results.append(sr)
        print(f"\n  {sr['label']}")
        print(f"  Probability: {sr['probability']*100:.0f}%")
        print(f"  Fair Value Before One-Time Charges: ${sr.get('fair_value_before_one_time', 'N/A'):,.2f}")
        if sr.get("one_time_ev_reduction_M", 0) > 0:
            print(f"  One-Time EV Reduction: ${sr.get('one_time_ev_reduction_M', 0):,.0f}M "
                  f"(${sr.get('per_share_one_time', 0):.2f}/share)")
        print(f"  Fair Value After One-Time Charges: ${sr.get('fair_value_after_one_time', sr.get('fair_value_before_one_time', 'N/A')):,.2f}")

    # --- Combined Tail Risk ---
    print("\n" + "=" * 70)
    print("COMBINED TAIL RISK (PERFECT STORM)")
    print("=" * 70)
    tail_risk = combined_tail_risk()
    print(f"  {tail_risk['label']}")
    print(f"  Probability: {tail_risk['probability']*100:.0f}%")
    print(f"  Fair Value Before Charges: ${tail_risk['fair_value_before_charges']:,.2f}")
    print(f"  Total One-Time Charges: ${tail_risk['total_one_time_charges_M']:,.0f}M (${tail_risk['per_share_one_time']:,.2f}/share)")
    print(f"  Fair Value After Charges: ${tail_risk['fair_value_after_charges']:,.2f}")

    # Compile output
    output = {
        "model": "META_RISK",
        "date": "2026-03-13",
        "ticker": "META",
        "currency": "USD_millions",
        "price_blinded": True,
        "random_seed": RANDOM_SEED,
        "monte_carlo": mc_results,
        "stress_tests": stress_results,
        "tail_risk": tail_risk,
        "key_risk_factors": [
            "CapEx ROI uncertainty ($115-135B 2026 investment with no quantified ROI timeline)",
            "EU DMA WhatsApp investigation — potential $14-16B fine or forced interoperability",
            "Youth mental health litigation — 2026 trial calendar; CFO flagged 'material loss' risk",
            "Chinese advertiser pullback risk (~$7B estimated Meta revenue from Temu/Shein)",
            "Revenue cyclicality — digital ad market declined in 2022; recession scenario models -15% YoY",
            "Reality Labs — $19.2B annual loss with no path to profitability disclosed",
            "Governance concentration — Zuckerberg retains majority control via Class B shares",
            "AI model competitive gap — Llama 4 received tepid developer reception; Avocado unproven",
        ],
        "model_assumptions": [
            "ASSUMPTION: Monte Carlo parameter distributions based on analyst estimates and historical volatility",
            "ASSUMPTION: Revenue growth distributions based on consensus estimates ± historical vol",
            "ASSUMPTION: CapEx normalization trajectory based on management guidance + analyst estimates",
            "ASSUMPTION: All distributions are truncated normal — tails are not fat-tailed",
            f"ASSUMPTION: Random seed {RANDOM_SEED} for full reproducibility",
        ],
    }

    output_path = "output/META/2026-03-13/models/meta_risk_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {output_path}")

    return output


if __name__ == "__main__":
    main()
