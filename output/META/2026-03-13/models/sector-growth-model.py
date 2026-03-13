"""
Digital Advertising Sector Growth Model — Meta Platforms (META)
Analyst: Industry Analyst
Date: 2026-03-13
Purpose: Model digital advertising sector growth trajectories and Meta's revenue scenarios

Data sources:
- WARC Global Ad Forecast 2025 (Tier 5)
- WPP Media Global Ad Forecast December 2025 (Tier 5)
- Meta FY2025 earnings (Tier 1)
- Consensus estimates (Tier 5)
"""

import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple


# ============================================================
# CONSTANTS & INPUTS
# ============================================================

# Historical data (all $B unless noted)
META_HISTORICAL_REVENUE = {
    2019: 70.7,
    2020: 86.0,
    2021: 117.9,
    2022: 116.6,
    2023: 134.9,
    2024: 164.5,
    2025: 201.0,  # FY2025 actual
}

# TAM estimates ($B)
TAM_ESTIMATES = {
    "total_global_advertising_2025": 1140.0,  # WPP Media
    "digital_advertising_2025": 650.0,         # Precedence Research
    "social_media_advertising_2025_warc": 306.4,  # WARC (broader definition)
    "social_media_advertising_2025_narrow": 202.6,  # Independent estimate
    "meta_addressable_tam_2025": 430.0,        # INDUSTRY ANALYST ESTIMATE: social + video + messaging
}

# Growth rate assumptions by scenario (as decimals)
SECTOR_GROWTH_RATES = {
    "total_global_ad_spend": 0.071,     # WPP Media 2026 forecast
    "digital_advertising": 0.094,        # Precedence Research 2026-2035 CAGR
    "social_media_advertising": 0.134,   # WARC/independent 2026-2030 CAGR
    "meta_addressable_tam_cagr": 0.12,   # INDUSTRY ANALYST: social + video + messaging
}

# Meta revenue growth scenarios (as decimals)
META_GROWTH_SCENARIOS = {
    "bull": {
        "2026": 0.27,    # Consensus high; Advantage+ + WhatsApp inflection
        "2027": 0.22,
        "2028": 0.18,    # New formats (WhatsApp, Meta AI) maturing
        "2029": 0.15,
        "2030": 0.13,
        "terminal": 0.08,
        "description": "AI re-acceleration sustained; WhatsApp reaches $40B+; Meta AI subscription launches",
    },
    "base": {
        "2026": 0.25,    # Mid-consensus
        "2027": 0.18,
        "2028": 0.14,    # Deceleration as base compounds
        "2029": 0.12,
        "2030": 0.10,
        "terminal": 0.065,
        "description": "Social media sector growth + share maintenance; WhatsApp $15-25B by 2028",
    },
    "bear": {
        "2026": 0.12,    # Recession impact + EU regulatory headwinds
        "2027": 0.08,    # Recovery but structural headwinds
        "2028": 0.10,
        "2029": 0.09,
        "2030": 0.08,
        "terminal": 0.04,
        "description": "Recession -15% ad spend; EU DMA fine $16B; WhatsApp monetization fails",
    },
}

# Operating margin assumptions by scenario
META_MARGIN_SCENARIOS = {
    "bull": {
        "2026": 0.43,   # AI efficiency drives further expansion
        "2027": 0.44,
        "2028": 0.45,
        "2029": 0.45,
        "2030": 0.46,
        "terminal": 0.46,
    },
    "base": {
        "2026": 0.40,   # CapEx surge keeps margins flat; normalization
        "2027": 0.41,
        "2028": 0.42,
        "2029": 0.42,
        "2030": 0.43,
        "terminal": 0.43,
    },
    "bear": {
        "2026": 0.32,   # Recession + regulatory costs + Reality Labs losses
        "2027": 0.34,
        "2028": 0.35,
        "2029": 0.36,
        "2030": 0.37,
        "terminal": 0.38,
    },
}

# Scenario probabilities
SCENARIO_PROBABILITIES = {
    "bull": 0.30,
    "base": 0.45,
    "bear": 0.25,
}


# ============================================================
# FUNCTIONS
# ============================================================

def project_revenue(
    base_revenue: float,
    growth_rates: Dict[str, float],
    years: List[int],
) -> Dict[int, float]:
    """Project revenue given base and year-by-year growth rates."""
    revenue = {}
    current = base_revenue
    for year in years:
        year_str = str(year)
        rate = growth_rates.get(year_str, growth_rates.get("terminal", 0.08))
        current = current * (1 + rate)
        revenue[year] = round(current, 1)
    return revenue


def project_operating_income(
    revenues: Dict[int, float],
    margins: Dict[str, float],
    years: List[int],
) -> Dict[int, float]:
    """Project operating income from revenue and margin assumptions."""
    op_income = {}
    for year in years:
        year_str = str(year)
        margin = margins.get(year_str, margins.get("terminal", 0.40))
        op_income[year] = round(revenues[year] * margin, 1)
    return op_income


def calculate_cagr(start_value: float, end_value: float, years: int) -> float:
    """Calculate CAGR from start to end value over N years."""
    return (end_value / start_value) ** (1 / years) - 1


def tam_projection(base_tam: float, cagr: float, years: int) -> Dict[int, float]:
    """Project TAM forward."""
    result = {}
    current = base_tam
    base_year = 2025
    for i in range(1, years + 1):
        current = current * (1 + cagr)
        result[base_year + i] = round(current, 1)
    return result


def probability_weighted_revenue(
    scenario_revenues: Dict[str, Dict[int, float]],
    probabilities: Dict[str, float],
    years: List[int],
) -> Dict[int, float]:
    """Calculate probability-weighted revenue across scenarios."""
    weighted = {}
    for year in years:
        weighted[year] = round(
            sum(
                scenario_revenues[sc][year] * probabilities[sc]
                for sc in probabilities
            ),
            1,
        )
    return weighted


# ============================================================
# MAIN MODEL EXECUTION
# ============================================================

def run_sector_growth_model():
    BASE_YEAR = 2025
    BASE_REVENUE = META_HISTORICAL_REVENUE[2025]
    FORECAST_YEARS = [2026, 2027, 2028, 2029, 2030]

    print("=" * 70)
    print("DIGITAL ADVERTISING SECTOR GROWTH MODEL — META PLATFORMS (META)")
    print("Date: 2026-03-13 | Analyst: Industry Analyst | Price-Blinded")
    print("=" * 70)

    # --- TAM PROJECTIONS ---
    print("\n--- 1. TAM PROJECTIONS (2026-2030, $B) ---")
    header = f"{'Market':<40} {'2025':>8} {'2026E':>8} {'2028E':>8} {'2030E':>8} {'CAGR':>8}"
    print(header)
    print("-" * 80)

    tam_segments = [
        ("Total Global Advertising", 1140.0, 0.071),
        ("Digital Advertising", 650.0, 0.094),
        ("Social Media Advertising (WARC)", 306.4, 0.134),
        ("Meta Addressable TAM (Est.)", 430.0, 0.120),
    ]
    tam_projections = {}
    for name, base, cagr in tam_segments:
        proj = tam_projection(base, cagr, 10)
        print(
            f"{name:<40} {base:>8.0f} {proj[2026]:>8.0f} {proj[2028]:>8.0f} "
            f"{proj[2030]:>8.0f} {cagr*100:>7.1f}%"
        )
        tam_projections[name] = proj

    # --- META REVENUE SCENARIOS ---
    print("\n\n--- 2. META REVENUE SCENARIOS ($B) ---")
    scenario_revenues = {}
    scenario_op_incomes = {}

    for scenario_name in ["bull", "base", "bear"]:
        growth = META_GROWTH_SCENARIOS[scenario_name]
        margins = META_MARGIN_SCENARIOS[scenario_name]
        prob = SCENARIO_PROBABILITIES[scenario_name]
        rev = project_revenue(BASE_REVENUE, growth, FORECAST_YEARS)
        oi = project_operating_income(rev, margins, FORECAST_YEARS)
        scenario_revenues[scenario_name] = rev
        scenario_op_incomes[scenario_name] = oi

    # Print header
    print(f"\n{'Scenario':<10} {'Prob':>5} {'2026E':>8} {'2027E':>8} {'2028E':>8} "
          f"{'2029E':>8} {'2030E':>8} {'5Y CAGR':>9}")
    print("-" * 70)
    for sc in ["bull", "base", "bear"]:
        rev = scenario_revenues[sc]
        prob = SCENARIO_PROBABILITIES[sc]
        cagr_5y = calculate_cagr(BASE_REVENUE, rev[2030], 5)
        print(
            f"{sc.capitalize():<10} {prob*100:>4.0f}% "
            f"{rev[2026]:>8.1f} {rev[2027]:>8.1f} {rev[2028]:>8.1f} "
            f"{rev[2029]:>8.1f} {rev[2030]:>8.1f} {cagr_5y*100:>8.1f}%"
        )

    # Probability-weighted
    pw_rev = probability_weighted_revenue(scenario_revenues, SCENARIO_PROBABILITIES, FORECAST_YEARS)
    pw_cagr = calculate_cagr(BASE_REVENUE, pw_rev[2030], 5)
    print(
        f"{'Prob-Wtd':<10} {'100%':>5} "
        f"{pw_rev[2026]:>8.1f} {pw_rev[2027]:>8.1f} {pw_rev[2028]:>8.1f} "
        f"{pw_rev[2029]:>8.1f} {pw_rev[2030]:>8.1f} {pw_cagr*100:>8.1f}%"
    )

    # --- OPERATING INCOME SCENARIOS ---
    print("\n\n--- 3. META OPERATING INCOME SCENARIOS ($B) ---")
    print(f"\n{'Scenario':<10} {'2026E':>8} {'2027E':>8} {'2028E':>8} {'2029E':>8} {'2030E':>8}")
    print("-" * 55)
    for sc in ["bull", "base", "bear"]:
        oi = scenario_op_incomes[sc]
        print(
            f"{sc.capitalize():<10} "
            f"{oi[2026]:>8.1f} {oi[2027]:>8.1f} {oi[2028]:>8.1f} "
            f"{oi[2029]:>8.1f} {oi[2030]:>8.1f}"
        )

    # --- META SHARE OF ADDRESSABLE TAM ---
    print("\n\n--- 4. META SHARE OF ADDRESSABLE TAM (Est. $400-430B base) ---")
    meta_tam_proj = tam_projections["Meta Addressable TAM (Est.)"]
    print(f"\n{'Scenario':<10} {'2026 Rev':>9} {'2026 TAM':>9} {'Share':>7} "
          f"{'2030 Rev':>9} {'2030 TAM':>9} {'Share':>7}")
    print("-" * 60)
    for sc in ["bull", "base", "bear"]:
        rev = scenario_revenues[sc]
        share_2026 = rev[2026] / meta_tam_proj[2026] * 100
        share_2030 = rev[2030] / meta_tam_proj[2030] * 100
        print(
            f"{sc.capitalize():<10} {rev[2026]:>9.1f} {meta_tam_proj[2026]:>9.1f} "
            f"{share_2026:>6.1f}% {rev[2030]:>9.1f} {meta_tam_proj[2030]:>9.1f} "
            f"{share_2030:>6.1f}%"
        )

    # --- HISTORICAL CAGR BENCHMARKS ---
    print("\n\n--- 5. HISTORICAL CAGR BENCHMARKS ---")
    hist_periods = [
        ("1-Year (2024-2025)", 164.5, 201.0, 1),
        ("3-Year (2022-2025)", 116.6, 201.0, 3),
        ("5-Year (2020-2025)", 86.0, 201.0, 5),
        ("6-Year (2019-2025)", 70.7, 201.0, 6),
    ]
    for label, start, end, yrs in hist_periods:
        cagr = calculate_cagr(start, end, yrs)
        print(f"  {label:<30} {cagr*100:.1f}%")

    print(f"\n  Forward consensus CAGR (2025-2027):  ~22-25%")
    print(f"  Forward consensus CAGR (2025-2030):  {pw_cagr*100:.1f}% (prob-weighted)")
    print(f"  Divergence from 5-year hist CAGR:    {(pw_cagr - 0.185)*100:+.1f}pp")
    print(f"  Justification: AI ad tools (Advantage+ $60B run rate) + Reels CPM")
    print(f"  maturation + WhatsApp monetization inflection")

    # --- AD FORMAT DECOMPOSITION ---
    print("\n\n--- 6. AD FORMAT DECOMPOSITION (2025E vs 2030E, $B) ---")
    formats = [
        ("Feed Ads (FB + IG)",           95.0, 0.07, 130.0),
        ("Reels & Stories Video",        55.0, 0.15, 110.0),
        ("Click-to-Message / WhatsApp",  17.0, 0.30,  65.0),
        ("AI-Powered (Advantage+)",      60.0, 0.18, 137.0),  # Overlay; partial double-count
        ("Threads Ads",                   0.8, 0.60,  20.0),
        ("WhatsApp Status & Channels",    1.5, 0.45,  30.0),
        ("Meta AI / Subscription",        0.0,  None,  10.0),
        ("AR/Smart Glasses Ads",          0.0,  None,   6.0),
    ]
    print(f"\n{'Format':<35} {'2025E ($B)':>11} {'2030E ($B)':>11} {'Note':<20}")
    print("-" * 80)
    for name, rev25, growth, rev30 in formats:
        note = "Overlap w/ Feed/Reels" if "Advantage" in name else ""
        print(f"{name:<35} {rev25:>11.1f} {rev30:>11.1f} {note:<20}")

    # --- SAVE RESULTS ---
    results = {
        "model": "sector-growth-model",
        "ticker": "META",
        "date": "2026-03-13",
        "base_revenue_2025": BASE_REVENUE,
        "scenario_revenues": {
            sc: {str(k): v for k, v in scenario_revenues[sc].items()}
            for sc in ["bull", "base", "bear"]
        },
        "scenario_operating_income": {
            sc: {str(k): v for k, v in scenario_op_incomes[sc].items()}
            for sc in ["bull", "base", "bear"]
        },
        "probability_weighted_revenue": {str(k): v for k, v in pw_rev.items()},
        "scenario_probabilities": SCENARIO_PROBABILITIES,
        "tam_projections": {
            name: {str(k): v for k, v in proj.items()}
            for name, proj in tam_projections.items()
        },
        "key_assumptions": {
            "social_media_sector_cagr": 0.134,
            "meta_addressable_tam_2025_bn": 430.0,
            "jevons_paradox_net_effect": "tailwind — efficiency drives demand expansion",
            "cliff_risk_year": "2029-2030",
            "whatsapp_2030_base_case_bn": 25.0,
            "whatsapp_2030_bull_case_bn": 60.0,
        },
    }

    output_path = "output/META/2026-03-13/data/meta-sector-growth-results.json"
    try:
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"\n\nResults saved to: {output_path}")
    except Exception as e:
        print(f"\nNote: Could not save to {output_path}: {e}")
        print("Results available in model output above.")

    print("\n" + "=" * 70)
    print("MODEL COMPLETE — Sector Growth Model")
    print("=" * 70)

    return results


if __name__ == "__main__":
    results = run_sector_growth_model()
