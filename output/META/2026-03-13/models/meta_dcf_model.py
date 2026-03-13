"""
META Platforms, Inc. — 5-Year DCF Model
=========================================
Model Builder Agent | Equity Research Swarm
Date: 2026-03-13
Ticker: META (NASDAQ)

Sources:
- FY2025 financials: Meta Q4/FY2025 earnings press release (Tier 1)
- Segment data: Meta Q4/FY2025 earnings press release (Tier 1)
- Consensus estimates: 41-analyst consensus, March 2026 (Tier 5)
- CapEx guidance: Meta Q4/FY2025 earnings press release (Tier 1)
- WACC components: Market data / standard CAPM (Tier 2)

PRICE BLINDING: No current stock price is used in this model.
Output is fair value per share; comparison to market price is done by Director.

Model Structure:
1. Segment revenue build (FoA Advertising, FoA Other, Reality Labs)
2. Margin model (gross, operating, net)
3. CapEx schedule (normalization from ~$125B peak to steady state)
4. WACC from components
5. Terminal value (perpetuity growth + exit multiple cross-check)
6. Bull / Base / Bear scenarios
7. Per-share fair value for each scenario
"""

import json
import os

# ============================================================
# SECTION 1: SCENARIO-INVARIANT BASE ASSUMPTIONS
# ============================================================

# Actuals: FY2025
FY2025_REVENUE = 200966          # USD millions; Meta Q4/FY2025 earnings (Tier 1)
FY2025_FOA_ADV_REVENUE = 196175  # FoA advertising; Meta earnings (Tier 1)
FY2025_FOA_OTHER_REVENUE = 2584  # FoA other (hardware, subs); Meta earnings (Tier 1)
FY2025_RL_REVENUE = 2207         # Reality Labs; Meta earnings (Tier 1)
FY2025_GROSS_PROFIT = 164791     # Meta earnings (Tier 1)
FY2025_OPERATING_INCOME = 83276  # Meta earnings (Tier 1)
FY2025_NET_INCOME = 60458        # Includes $15.93B one-time tax charge (Tier 1)
FY2025_EBITDA_APPROX = 110000    # [ESTIMATED: Op Inc $83.3B + D&A ~$26-28B]
FY2025_OCF = 115800              # Operating cash flow; Meta earnings (Tier 1)
FY2025_CAPEX = 69691             # Capital expenditures; Meta earnings (Tier 1)
FY2025_FCF = 43585               # Free cash flow; Meta earnings (Tier 1)
FY2025_FOA_OP_INCOME = 102469   # FoA operating income; Meta earnings (Tier 1)
FY2025_RL_OP_INCOME = -19193    # Reality Labs op loss; Meta earnings (Tier 1)
FY2025_SHARES_DILUTED = 2574    # Diluted shares, millions; Meta earnings (Tier 1)
FY2025_CASH_INVESTMENTS = 81592  # Cash + marketable securities; Meta earnings (Tier 1)
FY2025_LONG_TERM_DEBT = 58744   # Long-term debt; Meta earnings (Tier 1)
FY2025_NET_CASH = 22848         # Net cash position (FY2025_CASH - FY2025_LT_DEBT)
FY2025_OPERATING_MARGIN = 0.414  # FY2025 reported; Meta earnings (Tier 1)
FY2025_GROSS_MARGIN = 0.820      # FY2025; Meta earnings (Tier 1)
FY2025_NORMALIZED_TAX_RATE = 0.13  # Q4/FY2025 guidance 13-16%; using 13% (Tier 1)

# CapEx guidance / normalization assumptions
CAPEX_2026E_MID = 125000         # [ASSUMPTION: Midpoint of $115-135B 2026 guidance (Tier 1)]
CAPEX_DEPRECIATION_LIFE_YRS = 10  # [ASSUMPTION: ~10-year useful life for AI infra / data centers]
SHARE_BUYBACK_ANNUAL_REDUCTION = 0.015  # [ASSUMPTION: ~1.5%/yr diluted share reduction from net buybacks]

# WACC Components
RISK_FREE_RATE = 0.043           # [ASSUMPTION: US 10-year Treasury ~4.3%, March 2026 (Tier 2)]
EQUITY_RISK_PREMIUM = 0.055      # [ASSUMPTION: Damodaran US ERP ~5.5%]
BETA = 1.20                      # [ASSUMPTION: META beta ~1.2 vs. S&P 500; 5-yr weekly regression estimate]
COST_OF_EQUITY = RISK_FREE_RATE + BETA * EQUITY_RISK_PREMIUM   # CAPM
PRETAX_COST_OF_DEBT = 0.048      # [ASSUMPTION: Based on Aa3 Moody's rated debt; ~4.8% YTM estimate]
NORMALIZED_TAX_FOR_WACC = 0.145  # [ASSUMPTION: Midpoint of 13-16% 2026 guidance]
AFTER_TAX_COST_OF_DEBT = PRETAX_COST_OF_DEBT * (1 - NORMALIZED_TAX_FOR_WACC)

# Capital structure weights (market-value basis — Director will update post price reveal)
# [ASSUMPTION: Equity >> debt; approximate weights based on balance sheet + estimated equity value]
EQUITY_WEIGHT = 0.92             # [ASSUMPTION: Based on estimated enterprise value composition]
DEBT_WEIGHT = 0.08               # [ASSUMPTION: LT debt ~$58.7B vs. ~$740B+ implied equity]
WACC = EQUITY_WEIGHT * COST_OF_EQUITY + DEBT_WEIGHT * AFTER_TAX_COST_OF_DEBT

# Terminal value
TERMINAL_GROWTH_RATE = 0.035     # [ASSUMPTION: 3.5% — GDP growth (~2.5%) + 100bps for digital ad inflation premium]
EXIT_EV_EBITDA_MULTIPLE = 18.0   # [ASSUMPTION: Cross-check multiple; mature tech FCF comps ~15-22x EBITDA]

# Reality Labs trajectory
RL_LOSS_TRAJECTORY_PERYEAR_REDUCTION = 1000  # [ASSUMPTION: Losses improve by $1B/year in bull; stable in base]
RL_REVENUE_GROWTH = 0.05         # [ASSUMPTION: Ray-Ban glasses modest growth from small base]

# ============================================================
# SECTION 2: SCENARIO DEFINITIONS
# ============================================================
# [ASSUMPTION: Scenario weights set by analyst BEFORE calculating scenario prices — anti-anchoring protocol]

SCENARIOS = {
    "bull": {
        "weight": 0.25,
        "label": "Bull Case",
        "description": (
            "AI monetization materializes faster (Meta AI subs $5B+ by 2027), "
            "Reels/Threads ad load continues expanding, TikTok US exit boosts share, "
            "CapEx ROI validates via high-margin AI revenue streams. "
            "Reality Labs losses begin to moderate. Operating leverage drives margins above 45%."
        ),
        # Revenue growth rates for FoA Advertising
        "foa_adv_growth": [0.28, 0.24, 0.20, 0.17, 0.15],   # FY2026-FY2030
        # FoA Other (hardware, subscriptions, Meta AI) growth rates
        "foa_other_growth": [1.00, 0.60, 0.45, 0.35, 0.30],  # High growth from Meta AI subs
        # Reality Labs revenue growth
        "rl_rev_growth": [0.10, 0.15, 0.20, 0.25, 0.30],
        # Reality Labs op loss improvement per year ($M absolute)
        "rl_loss_improve": [1500, 2000, 2500, 3000, 3500],
        # FoA operating margin by year
        "foa_op_margin": [0.525, 0.535, 0.545, 0.550, 0.555],
        # CapEx as % of revenue
        "capex_pct_rev": [0.49, 0.42, 0.33, 0.27, 0.22],    # Normalizes faster
        # Normalized tax rate
        "tax_rate": 0.13,
        # Terminal growth rate
        "terminal_growth": 0.040,
        # Terminal EBITDA multiple cross-check
        "terminal_multiple": 20.0,
        # Shares: annual % reduction
        "share_reduction_annual": 0.020,
    },
    "base": {
        "weight": 0.50,
        "label": "Base Case",
        "description": (
            "Consensus-aligned: FY2026 +27% growth, deceleration to ~12% by FY2030. "
            "AI investment ROI is real but diffuse — improves ad targeting and efficiency, "
            "not discrete new revenue streams in the near term. "
            "Operating margin compresses in 2026-2027 due to CapEx/R&D then recovers. "
            "Reality Labs losses stable."
        ),
        "foa_adv_growth": [0.27, 0.19, 0.15, 0.13, 0.11],
        "foa_other_growth": [0.50, 0.35, 0.25, 0.20, 0.18],
        "rl_rev_growth": [0.05, 0.05, 0.08, 0.10, 0.12],
        "rl_loss_improve": [500, 500, 1000, 1000, 1500],
        "foa_op_margin": [0.510, 0.515, 0.520, 0.525, 0.530],
        "capex_pct_rev": [0.49, 0.44, 0.36, 0.28, 0.23],
        "tax_rate": 0.145,
        "terminal_growth": 0.035,
        "terminal_multiple": 18.0,
        "share_reduction_annual": 0.015,
    },
    "bear": {
        "weight": 0.25,
        "label": "Bear Case",
        "description": (
            "CapEx ROI disappoints (AI revenue fails to materialize at scale by 2028), "
            "EU DMA WhatsApp fine ~$10-16B in 2026-2027, "
            "youth mental health trial losses >$5B in 2026, "
            "Chinese advertisers (Temu/Shein) pull back $5-8B on trade tensions, "
            "margin remains compressed through 2028. "
            "Revenue growth decelerates sharply to ~8% by 2029-2030."
        ),
        "foa_adv_growth": [0.24, 0.15, 0.11, 0.09, 0.08],
        "foa_other_growth": [0.25, 0.20, 0.15, 0.12, 0.10],
        "rl_rev_growth": [0.02, 0.02, 0.02, 0.02, 0.02],
        "rl_loss_improve": [-500, 0, 0, 500, 500],           # Losses worsen slightly then stabilize
        "foa_op_margin": [0.490, 0.495, 0.500, 0.505, 0.510],
        "capex_pct_rev": [0.50, 0.47, 0.40, 0.32, 0.26],    # CapEx persists longer
        "tax_rate": 0.175,                                     # EU fines + settlement payments raise ETR
        "terminal_growth": 0.025,
        "terminal_multiple": 14.0,
        "share_reduction_annual": 0.010,
    },
}


# ============================================================
# SECTION 3: DCF CALCULATION ENGINE
# ============================================================

def run_dcf_scenario(scenario_name: str, params: dict) -> dict:
    """
    Run a single DCF scenario for META.

    Revenue is built segment-by-segment:
    - FoA Advertising (core business)
    - FoA Other (hardware, subscriptions, Meta AI)
    - Reality Labs (hardware + software)

    EBIT is calculated from FoA segment margins minus Reality Labs losses.
    Unlevered FCF = EBIT*(1-tax) + D&A - CapEx - delta_NWC
    """

    results = {"scenario": scenario_name, "label": params["label"]}
    projection_years = list(range(2026, 2031))  # FY2026-FY2030

    # --- Revenue Build ---
    foa_adv_rev = FY2025_FOA_ADV_REVENUE
    foa_other_rev = FY2025_FOA_OTHER_REVENUE
    rl_rev = FY2025_RL_REVENUE
    rl_op_loss = FY2025_RL_OP_INCOME  # negative number

    year_data = []
    cumulative_pv_fcf = 0.0

    # Shares outstanding at start (declining via buybacks)
    shares = FY2025_SHARES_DILUTED

    for i, year in enumerate(projection_years):
        # --- Revenue projection ---
        foa_adv_rev = foa_adv_rev * (1 + params["foa_adv_growth"][i])
        foa_other_rev = foa_other_rev * (1 + params["foa_other_growth"][i])
        rl_rev = rl_rev * (1 + params["rl_rev_growth"][i])
        total_revenue = foa_adv_rev + foa_other_rev + rl_rev

        # --- FoA Operating Income ---
        foa_total_rev = foa_adv_rev + foa_other_rev
        foa_op_income = foa_total_rev * params["foa_op_margin"][i]

        # --- Reality Labs Operating Loss (improves/worsens per scenario) ---
        # rl_loss_improve[i] = change in LOSS (positive = improvement, negative = worsening)
        rl_op_loss = rl_op_loss + params["rl_loss_improve"][i]  # rl_op_loss is negative; adding improvement reduces the absolute loss
        # Note: rl_op_loss starts negative; adding positive improvement makes it less negative

        # --- Corporate EBIT (total company) ---
        # [NOTE: Corporate overhead absorbed in FoA margin; RL loss is explicit]
        ebit = foa_op_income + rl_op_loss

        # --- D&A Estimation ---
        # [ASSUMPTION: D&A = prior year CapEx / useful_life + continuing prior asset base amortization]
        # Simplified: D&A grows with CapEx build; approx 18-22% of revenue as CapEx peak absorbs
        # Using a proxy: prior_capex / 10 + rolling base D&A
        capex_curr = total_revenue * params["capex_pct_rev"][i]
        # D&A estimate: prior cumulative asset base / life + new additions
        # [ASSUMPTION: D&A approximated as 14-15% of revenue in transition, 12% at steady state]
        dna_pct = 0.145 - i * 0.005  # Declining as CapEx normalizes; floors at ~12%
        dna_pct = max(dna_pct, 0.120)
        dna = total_revenue * dna_pct

        # --- NOPAT (Net Operating Profit After Tax) ---
        nopat = ebit * (1 - params["tax_rate"])

        # --- Unlevered Free Cash Flow ---
        # [ASSUMPTION: Working capital change ~0.5% of revenue change (asset-light business)]
        rev_change = total_revenue - (year_data[-1]["revenue"] if i > 0 else FY2025_REVENUE)
        delta_nwc = rev_change * 0.005
        ufcf = nopat + dna - capex_curr - delta_nwc

        # --- Present Value of FCF ---
        discount_factor = (1 + WACC) ** (i + 1)
        pv_fcf = ufcf / discount_factor
        cumulative_pv_fcf += pv_fcf

        # --- Shares (declining via buybacks) ---
        shares = shares * (1 - params["share_reduction_annual"])

        year_data.append({
            "year": year,
            "foa_adv_revenue": round(foa_adv_rev, 0),
            "foa_other_revenue": round(foa_other_rev, 0),
            "rl_revenue": round(rl_rev, 0),
            "revenue": round(total_revenue, 0),
            "revenue_growth_pct": round((total_revenue / (year_data[-1]["revenue"] if i > 0 else FY2025_REVENUE) - 1) * 100, 1),
            "foa_op_income": round(foa_op_income, 0),
            "rl_op_loss": round(rl_op_loss, 0),
            "ebit": round(ebit, 0),
            "ebit_margin_pct": round(ebit / total_revenue * 100, 1),
            "dna": round(dna, 0),
            "capex": round(capex_curr, 0),
            "capex_pct_rev": round(params["capex_pct_rev"][i] * 100, 1),
            "nopat": round(nopat, 0),
            "ufcf": round(ufcf, 0),
            "discount_factor": round(discount_factor, 4),
            "pv_fcf": round(pv_fcf, 0),
            "shares_diluted_M": round(shares, 0),
        })

    # --- Terminal Value (Perpetuity Growth Method) ---
    terminal_year_ufcf = year_data[-1]["ufcf"]
    terminal_fcf = terminal_year_ufcf * (1 + params["terminal_growth"])
    terminal_value = terminal_fcf / (WACC - params["terminal_growth"])
    pv_terminal = terminal_value / (1 + WACC) ** 5
    tv_pct_of_total = pv_terminal / (cumulative_pv_fcf + pv_terminal) * 100

    # --- Terminal Value Cross-Check (Exit EBITDA Multiple) ---
    # [ASSUMPTION: Use terminal year EBITDA = EBIT + D&A for cross-check]
    terminal_ebit = year_data[-1]["ebit"]
    terminal_dna = year_data[-1]["dna"]
    terminal_ebitda = terminal_ebit + terminal_dna
    tv_exit_multiple = terminal_ebitda * params["terminal_multiple"]
    pv_tv_exit_multiple = tv_exit_multiple / (1 + WACC) ** 5

    # --- Enterprise Value ---
    enterprise_value_perp = cumulative_pv_fcf + pv_terminal
    enterprise_value_multiple = cumulative_pv_fcf + pv_tv_exit_multiple

    # --- Equity Value Bridge ---
    # EV + net cash - minority interest = equity value
    # [ASSUMPTION: No significant minority interest; use FY2025 net cash]
    equity_value_perp = enterprise_value_perp + FY2025_NET_CASH
    equity_value_multiple = enterprise_value_multiple + FY2025_NET_CASH

    # --- Per-Share Fair Value ---
    terminal_shares = year_data[-1]["shares_diluted_M"]
    # equity_value in $M, terminal_shares in M shares → result in $/share (no conversion needed)
    fair_value_perp = equity_value_perp / terminal_shares
    fair_value_multiple = equity_value_multiple / terminal_shares

    # Blended fair value (70% perpetuity, 30% exit multiple as cross-check)
    fair_value_blended = 0.70 * fair_value_perp + 0.30 * fair_value_multiple

    results.update({
        "projections": year_data,
        "terminal_value_perpetuity": round(terminal_value, 0),
        "pv_terminal_value": round(pv_terminal, 0),
        "tv_pct_of_total_ev": round(tv_pct_of_total, 1),
        "terminal_value_exit_multiple": round(tv_exit_multiple, 0),
        "pv_tv_exit_multiple": round(pv_tv_exit_multiple, 0),
        "cumulative_pv_fcf": round(cumulative_pv_fcf, 0),
        "enterprise_value_perpetuity": round(enterprise_value_perp, 0),
        "enterprise_value_exit_multiple": round(enterprise_value_multiple, 0),
        "net_cash_added": FY2025_NET_CASH,
        "equity_value_perpetuity": round(equity_value_perp, 0),
        "equity_value_exit_multiple": round(equity_value_multiple, 0),
        "terminal_shares_M": round(terminal_shares, 0),
        "fair_value_per_share_perpetuity": round(fair_value_perp, 2),
        "fair_value_per_share_exit_multiple": round(fair_value_multiple, 2),
        "fair_value_per_share_blended": round(fair_value_blended, 2),
        "wacc_used": round(WACC * 100, 2),
        "terminal_growth_rate": params["terminal_growth"],
    })

    return results


# ============================================================
# SECTION 4: SENSITIVITY ANALYSIS
# ============================================================

def run_sensitivity(scenario_name: str = "base") -> dict:
    """
    WACC vs Terminal Growth Rate sensitivity for the base case.
    Returns a 2D table of fair values per share.
    """
    params = SCENARIOS[scenario_name]
    wacc_range = [0.07, 0.08, 0.09, 0.10, 0.11, 0.12]
    tgr_range = [0.020, 0.025, 0.030, 0.035, 0.040]

    table = {}
    for w in wacc_range:
        row = {}
        for tg in tgr_range:
            modified_params = dict(params)
            modified_params["terminal_growth"] = tg
            # Run DCF with modified WACC (temporarily override global)
            global WACC
            original_wacc = WACC
            WACC = w
            result = run_dcf_scenario("sensitivity", modified_params)
            WACC = original_wacc
            row[f"tg_{int(tg*1000)}bps"] = result["fair_value_per_share_blended"]
        table[f"wacc_{int(w*100)}pct"] = row

    return {
        "scenario_base": scenario_name,
        "wacc_values": wacc_range,
        "tgr_values": tgr_range,
        "sensitivity_table_fair_value": table,
    }


# ============================================================
# SECTION 5: WACC SUMMARY
# ============================================================

def compute_wacc_summary() -> dict:
    return {
        "risk_free_rate": RISK_FREE_RATE,
        "equity_risk_premium": EQUITY_RISK_PREMIUM,
        "beta": BETA,
        "cost_of_equity": round(COST_OF_EQUITY, 4),
        "pretax_cost_of_debt": PRETAX_COST_OF_DEBT,
        "after_tax_cost_of_debt": round(AFTER_TAX_COST_OF_DEBT, 4),
        "equity_weight": EQUITY_WEIGHT,
        "debt_weight": DEBT_WEIGHT,
        "wacc": round(WACC, 4),
        "wacc_pct": round(WACC * 100, 2),
        "notes": [
            "ASSUMPTION: Beta 1.2 estimated from 5-year weekly regression vs. S&P 500",
            "ASSUMPTION: Risk-free rate = 10-yr Treasury ~4.3% as of March 2026",
            "ASSUMPTION: ERP = 5.5% (Damodaran US market premium)",
            "ASSUMPTION: Equity weight 92% / Debt 8% based on estimated EV composition",
            "ASSUMPTION: Cost of debt ~4.8% based on Aa3 Moody's rated bonds",
        ],
    }


# ============================================================
# SECTION 6: MAIN — RUN ALL SCENARIOS
# ============================================================

def main():
    print("=" * 70)
    print("META Platforms DCF Model — 2026-03-13")
    print("=" * 70)

    wacc_summary = compute_wacc_summary()
    print(f"\nWACC Summary:")
    print(f"  Risk-Free Rate:       {wacc_summary['risk_free_rate']*100:.1f}%")
    print(f"  Equity Risk Premium:  {wacc_summary['equity_risk_premium']*100:.1f}%")
    print(f"  Beta:                 {wacc_summary['beta']:.2f}")
    print(f"  Cost of Equity:       {wacc_summary['cost_of_equity']*100:.2f}%")
    print(f"  After-Tax Cost Debt:  {wacc_summary['after_tax_cost_of_debt']*100:.2f}%")
    print(f"  WACC:                 {wacc_summary['wacc_pct']:.2f}%")

    all_scenario_results = {}
    print("\n" + "=" * 70)
    print("SCENARIO RESULTS")
    print("=" * 70)

    for scenario_name, params in SCENARIOS.items():
        result = run_dcf_scenario(scenario_name, params)
        all_scenario_results[scenario_name] = result

        print(f"\n--- {result['label']} ({params['weight']*100:.0f}% probability) ---")
        print(f"  {params['description'][:80]}...")
        print(f"\n  Revenue Projections (FY2026-FY2030, $M):")
        for yr in result["projections"]:
            print(f"    {yr['year']}: ${yr['revenue']:,.0f}M  ({yr['revenue_growth_pct']:+.1f}%)  "
                  f"CapEx: ${yr['capex']:,.0f}M  UFCF: ${yr['ufcf']:,.0f}M")
        print(f"\n  Valuation Summary:")
        print(f"    PV of FCFs (5yr):           ${result['cumulative_pv_fcf']:,.0f}M")
        print(f"    PV of Terminal Value:        ${result['pv_terminal_value']:,.0f}M")
        print(f"    TV as % of total EV:         {result['tv_pct_of_total_ev']:.1f}%")
        print(f"    Enterprise Value (Perp.):    ${result['enterprise_value_perpetuity']:,.0f}M")
        print(f"    Enterprise Value (Multiple): ${result['enterprise_value_exit_multiple']:,.0f}M")
        print(f"    + Net Cash:                  ${result['net_cash_added']:,.0f}M")
        print(f"    Equity Value (Perp.):        ${result['equity_value_perpetuity']:,.0f}M")
        print(f"\n  Fair Value Per Share:")
        print(f"    Perpetuity Growth Method:    ${result['fair_value_per_share_perpetuity']:,.2f}")
        print(f"    Exit Multiple Cross-Check:   ${result['fair_value_per_share_exit_multiple']:,.2f}")
        print(f"    Blended (70/30):             ${result['fair_value_per_share_blended']:,.2f}")

    # Probability-weighted fair value
    weighted_fv = sum(
        SCENARIOS[s]["weight"] * all_scenario_results[s]["fair_value_per_share_blended"]
        for s in SCENARIOS
    )
    print(f"\n{'='*70}")
    print(f"PROBABILITY-WEIGHTED FAIR VALUE: ${weighted_fv:,.2f} per share")
    print(f"  Bull ({SCENARIOS['bull']['weight']*100:.0f}%): ${all_scenario_results['bull']['fair_value_per_share_blended']:,.2f}")
    print(f"  Base ({SCENARIOS['base']['weight']*100:.0f}%): ${all_scenario_results['base']['fair_value_per_share_blended']:,.2f}")
    print(f"  Bear ({SCENARIOS['bear']['weight']*100:.0f}%): ${all_scenario_results['bear']['fair_value_per_share_blended']:,.2f}")
    print(f"{'='*70}")

    # Sensitivity table
    print("\nRunning WACC / Terminal Growth Rate sensitivity...")
    sensitivity = run_sensitivity("base")

    # Compile full output
    output = {
        "model": "META_DCF",
        "date": "2026-03-13",
        "ticker": "META",
        "currency": "USD_millions",
        "price_blinded": True,
        "wacc_summary": wacc_summary,
        "scenarios": all_scenario_results,
        "probability_weighted_fair_value_per_share": round(weighted_fv, 2),
        "scenario_weights": {s: SCENARIOS[s]["weight"] for s in SCENARIOS},
        "scenario_fair_values_blended": {
            s: all_scenario_results[s]["fair_value_per_share_blended"] for s in SCENARIOS
        },
        "sensitivity_analysis": sensitivity,
        "key_assumptions": [
            f"WACC: {WACC*100:.2f}% (Beta 1.2, Rf 4.3%, ERP 5.5%)",
            "Terminal growth rate: 3.5% base (3.0% bear, 4.0% bull)",
            "Exit EBITDA multiple cross-check: 18x base (14x bear, 20x bull)",
            "CapEx peaks at ~$125B in 2026 (midpoint of $115-135B guidance), normalizes to ~22-23% of revenue by 2030",
            "FoA op margin: 51-55% range (D&A and CapEx below operating income line)",
            "Reality Labs: stable losses base; improvement in bull; modest deterioration in bear",
            "Net cash bridge: +$22,848M (FY2025 cash $81.6B minus LT debt $58.7B)",
            "Shares decline ~1.5%/yr base (net buybacks post-dividend)",
        ],
        "data_quality_flags": [
            "D&A estimated as % of revenue (not from filing); [ESTIMATED]",
            "WACC equity weight approximate pending current stock price reveal [ASSUMPTION]",
            "NWC change minimal for asset-light business [ASSUMPTION]",
        ],
    }

    # Save to JSON
    output_path = "output/META/2026-03-13/models/meta_dcf_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=str)
    print(f"\nResults saved to {output_path}")

    return output


if __name__ == "__main__":
    main()
