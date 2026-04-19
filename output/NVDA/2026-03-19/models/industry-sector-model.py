"""
NVIDIA (NVDA) — Industry Sector Model
Author: Industry Analyst
Date: 2026-03-19
Purpose: Quantify TAM growth, market share scenarios, and strategic power implications
         for the DCF and risk analysis teams.

Inputs: Demand decomposition, competitive landscape data, technology adoption analogues
Outputs:
  - TAM scenarios (bottom-up 2026-2032)
  - Market share erosion scenarios
  - NVIDIA implied revenue under each scenario
  - Jevons paradox sensitivity
  - Power Durability scoring simulation

Usage:
  python industry-sector-model.py           # Runs all scenarios, prints summary
  python industry-sector-model.py --export  # Also exports JSON for DCF team
"""

import json
import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import sys

# ============================================================
# 1. CONFIGURATION
# ============================================================

TICKER = "NVDA"
ANALYSIS_DATE = "2026-03-19"
BASE_YEAR = 2026
FORECAST_YEARS = list(range(2026, 2033))

# Current revenue anchor (FY2026 annualized, from earnings)
NVDA_FY2026_REVENUE_B = 215.9  # $215.9B actual
NVDA_DC_REVENUE_FY2026_B = 193.7  # $193.7B data center
NVDA_DC_SHARE_OF_TOTAL = NVDA_DC_REVENUE_FY2026_B / NVDA_FY2026_REVENUE_B

# Current AI accelerator market share
NVDA_AI_SHARE_2026 = 0.88  # 86-92% range, use midpoint

# ============================================================
# 2. TAM COMPONENTS — BOTTOM-UP DEMAND DECOMPOSITION
# ============================================================

@dataclass
class WorkloadScenario:
    name: str
    current_demand_b: float          # $B in 2026
    base_cagr: float                 # % annual growth, base case
    bull_cagr: float
    bear_cagr: float
    probability_of_materialization: float  # for emerging/pre-commercial workloads
    adoption_stage: str
    note: str = ""

WORKLOADS = [
    WorkloadScenario(
        name="LLM Training (frontier models)",
        current_demand_b=80.0,
        base_cagr=0.22,
        bull_cagr=0.32,
        bear_cagr=0.12,
        probability_of_materialization=0.95,
        adoption_stage="Early Majority",
        note="Model scale ~2x/yr; compute intensity growing"
    ),
    WorkloadScenario(
        name="LLM Inference (deployed models)",
        current_demand_b=55.0,
        base_cagr=0.38,
        bull_cagr=0.50,
        bear_cagr=0.22,
        probability_of_materialization=0.92,
        adoption_stage="Growth / Inflection",
        note="Jevons paradox dominant; flipping to >50% of market"
    ),
    WorkloadScenario(
        name="Agentic AI",
        current_demand_b=10.0,
        base_cagr=0.65,
        bull_cagr=0.90,
        bear_cagr=0.30,
        probability_of_materialization=0.65,
        adoption_stage="Early Adopter",
        note="Jensen: ChatGPT moment for agents; multi-step loops = high compute"
    ),
    WorkloadScenario(
        name="Sovereign AI",
        current_demand_b=12.5,
        base_cagr=0.42,
        bull_cagr=0.60,
        bear_cagr=0.20,
        probability_of_materialization=0.72,
        adoption_stage="Early Adopter",
        note="Policy-driven; GDP-correlated; 20+ country programs active"
    ),
    WorkloadScenario(
        name="Physical AI / Robotics",
        current_demand_b=3.5,
        base_cagr=0.70,
        bull_cagr=1.20,
        bear_cagr=0.20,
        probability_of_materialization=0.45,
        adoption_stage="Pre-Commercial",
        note="GTC 2026: BYD, Hyundai, ABB, KUKA; meaningful revenue FY2028+"
    ),
    WorkloadScenario(
        name="Enterprise AI / Edge Inference",
        current_demand_b=28.0,
        base_cagr=0.25,
        bull_cagr=0.35,
        bear_cagr=0.15,
        probability_of_materialization=0.85,
        adoption_stage="Early Majority",
        note="Cost-sensitive; more AMD/Qualcomm competition"
    ),
]

# ============================================================
# 3. MARKET SHARE EROSION SCENARIOS
# ============================================================

@dataclass
class ShareScenario:
    name: str
    share_2026: float
    share_2028: float
    share_2030: float
    share_2032: float
    description: str

SHARE_SCENARIOS = {
    "bull": ShareScenario(
        name="Bull: Moat Holds",
        share_2026=0.90, share_2028=0.84, share_2030=0.78, share_2032=0.74,
        description="CUDA moat intact; AMD gains limited to inference; ASICs grow slowly"
    ),
    "base": ShareScenario(
        name="Base: Gradual Erosion",
        share_2026=0.88, share_2028=0.78, share_2030=0.70, share_2032=0.65,
        description="AMD gains 2-3pp/yr; custom ASICs reach 25-30% of hyperscaler compute by 2030"
    ),
    "bear": ShareScenario(
        name="Bear: Accelerated Erosion",
        share_2026=0.85, share_2028=0.70, share_2030=0.58, share_2032=0.50,
        description="ROCm parity by 2027; hyperscaler ASIC share >35% by 2028; CUDA moat cracks"
    ),
}

# ============================================================
# 4. TAM CALCULATION ENGINE
# ============================================================

def interpolate_share(scenario: ShareScenario, year: int) -> float:
    """Linear interpolation between milestone years."""
    milestones = {2026: scenario.share_2026, 2028: scenario.share_2028,
                  2030: scenario.share_2030, 2032: scenario.share_2032}
    years = sorted(milestones.keys())
    if year <= years[0]:
        return milestones[years[0]]
    if year >= years[-1]:
        return milestones[years[-1]]
    for i in range(len(years) - 1):
        y0, y1 = years[i], years[i+1]
        if y0 <= year <= y1:
            frac = (year - y0) / (y1 - y0)
            return milestones[y0] + frac * (milestones[y1] - milestones[y0])
    return milestones[years[-1]]


def project_workload(workload: WorkloadScenario, scenario_type: str = "base") -> Dict[int, float]:
    """Project workload demand from 2026 to 2032."""
    cagr_map = {"bull": workload.bull_cagr, "base": workload.base_cagr, "bear": workload.bear_cagr}
    cagr = cagr_map[scenario_type]
    result = {}
    for year in FORECAST_YEARS:
        t = year - BASE_YEAR
        raw = workload.current_demand_b * ((1 + cagr) ** t)
        # Apply probability of materialization (linear from 1.0 in 2026 to full prob weight by 2030)
        if workload.adoption_stage == "Pre-Commercial":
            # Ramp: starts contributing after 2027, full weight by 2030
            prob_factor = min(1.0, max(0.0, (year - 2027) / 3)) * workload.probability_of_materialization
        else:
            prob_factor = workload.probability_of_materialization
        result[year] = raw * prob_factor
    return result


def compute_tam_scenario(scenario_type: str = "base") -> Dict[int, Dict]:
    """Compute total AI accelerator TAM and NVIDIA implied revenue by year."""
    results = {}
    for year in FORECAST_YEARS:
        workload_breakdown = {}
        total_tam = 0.0
        for workload in WORKLOADS:
            proj = project_workload(workload, scenario_type)
            demand = proj[year]
            workload_breakdown[workload.name] = round(demand, 2)
            total_tam += demand

        share = interpolate_share(SHARE_SCENARIOS[scenario_type], year)
        nvda_dc_revenue = total_tam * share
        nvda_total_revenue = nvda_dc_revenue / NVDA_DC_SHARE_OF_TOTAL  # assume DC mix stable [ASSUMPTION]

        results[year] = {
            "total_tam_b": round(total_tam, 1),
            "nvda_share": round(share, 3),
            "nvda_dc_revenue_b": round(nvda_dc_revenue, 1),
            "nvda_total_revenue_b": round(nvda_total_revenue, 1),
            "workload_breakdown": workload_breakdown,
        }
    return results


# ============================================================
# 5. JEVONS PARADOX SENSITIVITY MODEL
# ============================================================

def jevons_sensitivity(
    base_demand_b: float,
    cost_reduction_per_year: float = 0.50,  # 50% cost reduction/yr (Rubin = 10x cheaper)
    demand_elasticity: float = -1.8,         # price elasticity: % volume change per 1% price change
    years: int = 5
) -> Tuple[float, float, float]:
    """
    Model the net TAM effect of efficiency improvements.

    TAM = Price × Volume
    Each year: price drops by cost_reduction_per_year
                volume grows by |elasticity| * cost_reduction_per_year (Jevons)
    Net TAM per year = (1 - cost_reduction) * (1 + |elasticity| * cost_reduction)

    Returns:
        (cumulative_cost_factor, cumulative_volume_factor, net_tam_multiplier)
    """
    per_year_cost = (1 - cost_reduction_per_year)
    per_year_volume = (1 + abs(demand_elasticity) * cost_reduction_per_year)
    per_year_net = per_year_cost * per_year_volume

    cumulative_cost = per_year_cost ** years
    cumulative_volume = per_year_volume ** years
    net_multiplier = per_year_net ** years

    return cumulative_cost, cumulative_volume, net_multiplier


# ============================================================
# 6. TECHNOLOGY ADOPTION ANALOGUES
# ============================================================

@dataclass
class TechAnalogue:
    name: str
    inception_year: int
    current_analogue_year: int   # What year in that analogue's lifecycle = AI infra 2026
    cagr_at_same_stage: float
    peak_growth_period: str
    lessons: str

ANALOGUES = [
    TechAnalogue(
        name="Cloud Computing (AWS/Azure/GCP)",
        inception_year=2006,
        current_analogue_year=2013,
        cagr_at_same_stage=0.28,
        peak_growth_period="2013-2020",
        lessons="25-30% CAGR sustained 7+ years post-inflection. $100B+ capex/yr milestone "
                "reached ~2018. AI is scaling 3-5x faster in absolute dollars."
    ),
    TechAnalogue(
        name="Mobile Internet (iPhone 2007 → mass market)",
        inception_year=2007,
        current_analogue_year=2012,
        cagr_at_same_stage=0.40,
        peak_growth_period="2010-2015",
        lessons="Supply constraints (ASML EUV = CoWoS today) gated adoption even with "
                "clear demand. Price-to-performance improvements drove Jevons paradox in data."
    ),
]


# ============================================================
# 7. STRATEGIC POWER COMPOSITE SCORE
# ============================================================

POWER_SCORES = {
    "Scale Economies": {"score": 8, "trend": "Strengthening", "half_life_year": 2030},
    "Network Effects": {"score": 9, "trend": "Stable (eroding slowly)", "half_life_year": 2030},
    "Counter-Positioning": {"score": 6, "trend": "Eroding", "half_life_year": 2027},
    "Switching Costs": {"score": 9, "trend": "Stable (eroding 2028+)", "half_life_year": 2029},
    "Branding": {"score": 7, "trend": "Stable", "half_life_year": 2029},
    "Cornered Resource": {"score": 8, "trend": "Eroding", "half_life_year": 2027},
    "Process Power": {"score": 7, "trend": "Strengthening", "half_life_year": 2031},
}

COMPETITOR_SCORES = {
    "AMD": {
        "Scale Economies": 5, "Network Effects": 3, "Counter-Positioning": 4,
        "Switching Costs": 3, "Branding": 4, "Cornered Resource": 4, "Process Power": 5,
    },
    "Google TPU": {
        "Scale Economies": 6, "Network Effects": 1, "Counter-Positioning": 8,
        "Switching Costs": 9, "Branding": 2, "Cornered Resource": 5, "Process Power": 7,
    },
}


# ============================================================
# 8. MAIN REPORT
# ============================================================

def print_section(title: str):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


def run_analysis(export: bool = False):
    print(f"\nNVIDIA (NVDA) — Industry Sector Model")
    print(f"Analysis Date: {ANALYSIS_DATE}")
    print(f"[PRICE-BLINDED: No price inputs used in this model]")

    # 8.1 TAM Scenarios
    print_section("1. TAM & NVDA REVENUE SCENARIOS (2026-2032)")

    all_scenarios = {}
    for scenario_type in ["bull", "base", "bear"]:
        results = compute_tam_scenario(scenario_type)
        all_scenarios[scenario_type] = results
        print(f"\n  {SHARE_SCENARIOS[scenario_type].name}")
        print(f"  {SHARE_SCENARIOS[scenario_type].description}")
        print(f"  {'Year':<8} {'AI TAM ($B)':<16} {'NVDA Share':<14} {'NVDA DC Rev ($B)':<20} {'NVDA Total ($B)'}")
        print(f"  {'-'*75}")
        for year in FORECAST_YEARS:
            r = results[year]
            print(f"  {year:<8} {r['total_tam_b']:<16.1f} {r['nvda_share']:<14.1%} "
                  f"{r['nvda_dc_revenue_b']:<20.1f} {r['nvda_total_revenue_b']:.1f}")

    # 8.2 Bottom-up workload breakdown (base case)
    print_section("2. WORKLOAD DEMAND DECOMPOSITION — BASE CASE ($B)")
    base_results = all_scenarios["base"]
    header = f"  {'Workload':<40}"
    for yr in [2026, 2028, 2030, 2032]:
        header += f" {yr:<12}"
    print(header)
    print(f"  {'-'*88}")

    for workload in WORKLOADS:
        row = f"  {workload.name:<40}"
        for yr in [2026, 2028, 2030, 2032]:
            row += f" {base_results[yr]['workload_breakdown'][workload.name]:<12.1f}"
        print(row)

    total_row = f"  {'TOTAL TAM':<40}"
    for yr in [2026, 2028, 2030, 2032]:
        total_row += f" {base_results[yr]['total_tam_b']:<12.1f}"
    print(total_row)

    # 8.3 Jevons Paradox
    print_section("3. JEVONS PARADOX SENSITIVITY ANALYSIS")
    print(f"\n  Reference: DeepSeek R1 (Jan 2025) = -90% cost → hyperscaler AI spend INCREASED 36% in 2025")
    print(f"  Rubin vs. Blackwell: 10x lower inference cost per GTC 2026 → ~37%/yr cost reduction over ~6yr roadmap")
    print(f"\n  Demand Elasticity Scenarios (5-year, 25% annual cost reduction [ASSUMPTION: ~H100→Blackwell→Rubin pace]):")
    print(f"  {'Scenario':<36} {'Elasticity':<12} {'5yr Cost':<14} {'5yr Volume':<16} {'Net TAM Mult'}")
    print(f"  {'-'*86}")

    base_demand = sum(w.current_demand_b for w in WORKLOADS)
    # Use 25%/yr cost reduction: consistent with ~4x cost reduction per generation over ~6yr cycle
    # (10x over Blackwell->Rubin ~3yr cycle implies ~37%/yr; smooth over 5yr: use 25% as conservative)
    annual_cost_reduction = 0.25
    elasticity_scenarios = [
        ("Low elasticity (efficiency dominant)", -0.8),
        ("Base case (Jevons dominant)", -1.8),
        ("High elasticity (demand explosion)", -3.0),
    ]
    for name, elasticity in elasticity_scenarios:
        cf, vf, nm = jevons_sensitivity(base_demand, annual_cost_reduction, elasticity, 5)
        print(f"  {name:<36} {elasticity:<12.1f} {cf:<14.2%} {vf:<16.2%} {nm:.2f}x")

    print(f"\n  [ASSUMPTION: 25%/yr cost reduction — conservative; actual Blackwell→Rubin pace implies ~37%/yr]")
    print(f"  [Base elasticity -1.8: each 1% cost reduction → 1.8% volume increase — cloud analogue-calibrated]")
    print(f"  [Net >1.0x = Jevons dominates (TAM expands); <1.0x = efficiency headwind dominates]")

    # 8.4 Technology Adoption Positioning
    print_section("4. TECHNOLOGY ADOPTION FRAMEWORK")
    for analogue in ANALOGUES:
        years_at_inception = BASE_YEAR - analogue.inception_year
        print(f"\n  Analogue: {analogue.name}")
        print(f"  AI infra (2026) maps to year {analogue.current_analogue_year} in this analogue's lifecycle")
        print(f"  ({years_at_inception} years since AI infra inflection [2017 AlphaGo/2022 ChatGPT])")
        print(f"  CAGR at equivalent stage: {analogue.cagr_at_same_stage:.0%}")
        print(f"  Peak growth period of analogue: {analogue.peak_growth_period}")
        print(f"  Key lesson: {analogue.lessons}")

    print(f"\n  Assessment: AI infrastructure is at ~2013 equivalent in cloud adoption curve.")
    print(f"  Historical analogue implies 25-40% CAGR sustainable for 4-7 more years.")
    print(f"  This SUPPORTS the base case 28-35% revenue CAGR assumption for FY2027-FY2029.")

    # 8.5 Strategic Power Summary
    print_section("5. STRATEGIC POWER COMPOSITE SCORES")
    print(f"\n  {'Power':<25} {'NVDA':<8} {'AMD':<8} {'Google TPU':<12} {'Trend':<25} {'Half-Life'}")
    print(f"  {'-'*90}")
    nvda_total = 0
    for power, details in POWER_SCORES.items():
        amd_score = COMPETITOR_SCORES["AMD"][power]
        goog_score = COMPETITOR_SCORES["Google TPU"][power]
        nvda_score = details["score"]
        nvda_total += nvda_score
        print(f"  {power:<25} {nvda_score:<8} {amd_score:<8} {goog_score:<12} "
              f"{details['trend']:<25} {details['half_life_year']}")
    amd_total = sum(COMPETITOR_SCORES["AMD"].values())
    goog_total = sum(COMPETITOR_SCORES["Google TPU"].values())
    print(f"  {'-'*90}")
    print(f"  {'COMPOSITE':<25} {nvda_total:<8} {amd_total:<8} {goog_total}")
    print(f"\n  NVDA Composite: {nvda_total}/70 ({nvda_total/70:.0%})")
    print(f"  AMD Composite:  {amd_total}/70 ({amd_total/70:.0%})")
    print(f"  Google TPU:     {goog_total}/70 ({goog_total/70:.0%}) [captive use only]")

    # Cliff risk assessment
    print_section("6. CLIFF RISK ASSESSMENT (Powers eroding in same 2-yr window)")
    eroding_by_window = {}
    for power, details in POWER_SCORES.items():
        if details["trend"] in ("Eroding", "Stable (eroding 2028+)", "Stable (eroding slowly)"):
            hl = details["half_life_year"]
            window_key = f"{hl-1}-{hl}"  # 2-year window centered on half-life
            if window_key not in eroding_by_window:
                eroding_by_window[window_key] = []
            eroding_by_window[window_key].append(power)

    for window, powers in sorted(eroding_by_window.items()):
        flag = " *** CLIFF RISK FLAG ***" if len(powers) >= 3 else ""
        print(f"\n  {window}: {len(powers)} Power(s) at half-life{flag}")
        for p in powers:
            print(f"    - {p} ({POWER_SCORES[p]['score']}/10)")

    # 8.6 Scenario Summary for DCF team
    print_section("7. SCENARIO SUMMARY FOR DCF TEAM")
    print(f"\n  {'Scenario':<12} {'2027E Rev ($B)':<18} {'2029E Rev ($B)':<18} {'2032E Rev ($B)':<18} {'Share 2030'}")
    print(f"  {'-'*80}")
    for s in ["bull", "base", "bear"]:
        r = all_scenarios[s]
        print(f"  {s.upper():<12} "
              f"{r[2027]['nvda_total_revenue_b']:<18.1f} "
              f"{r[2029]['nvda_total_revenue_b']:<18.1f} "
              f"{r[2032]['nvda_total_revenue_b']:<18.1f} "
              f"{r[2030]['nvda_share']:.0%}")

    print(f"\n  Key assumptions:")
    print(f"  - Base case: Jevons paradox sustains demand; AMD gains 2-3pp/yr; ASICs ~25% hyperscaler compute by 2030")
    print(f"  - Bull case: Physical AI & Agentic AI materialize at scale; CUDA moat holds through 2030")
    print(f"  - Bear case: ROCm parity by 2027; hyperscaler ASIC >35% by 2028; PyTorch abstraction accelerates")
    print(f"  [ASSUMPTION: DC revenue remains 90% of total NVIDIA revenue throughout forecast period]")
    print(f"  [DATA GAP: No Gartner/IDC independent TAM; estimates based on Tier 5-7 sources]")

    # 8.7 Export for DCF team
    if export:
        export_data = {
            "ticker": TICKER,
            "analysis_date": ANALYSIS_DATE,
            "model": "Industry Sector Model v1.0",
            "tam_scenarios": {
                scenario: {
                    str(year): {
                        "total_tam_b": data["total_tam_b"],
                        "nvda_share": data["nvda_share"],
                        "nvda_dc_revenue_b": data["nvda_dc_revenue_b"],
                        "nvda_total_revenue_b": data["nvda_total_revenue_b"],
                    }
                    for year, data in scenario_data.items()
                }
                for scenario, scenario_data in all_scenarios.items()
            },
            "power_scores": {
                "nvda_composite": nvda_total,
                "nvda_composite_pct": round(nvda_total / 70, 3),
                "amd_composite": amd_total,
                "google_tpu_composite": goog_total,
                "by_power": POWER_SCORES,
            },
            "jevons_base_case_5yr_multiplier": round(
                jevons_sensitivity(base_demand, 0.50, -1.8, 5)[2], 3
            ),
            "cliff_risk_windows": eroding_by_window,
            "notes": [
                "All TAM estimates from Tier 5-7 sources. CRITICAL DATA GAP: No Gartner/IDC estimate.",
                "Market share estimates are AI GPU/accelerator market only, excluding custom ASICs.",
                "DC revenue % of total assumed stable at 89.7% — validate with DCF team.",
                "Physical AI scenario (Pre-Commercial) probability-adjusted; HIGH UNCERTAINTY on timing.",
            ]
        }
        output_path = f"output/NVDA/2026-03-19/data/NVDA-sector-scenarios.json"
        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=2)
        print(f"\n  [Exported JSON to {output_path}]")

    print(f"\n{'='*70}")
    print(f"  Model complete. Run with --export flag to save JSON for DCF team.")
    print('='*70)


# ============================================================
# 9. ENTRY POINT
# ============================================================

if __name__ == "__main__":
    export_flag = "--export" in sys.argv
    run_analysis(export=export_flag)
