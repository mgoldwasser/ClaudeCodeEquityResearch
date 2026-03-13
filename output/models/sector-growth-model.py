#!/usr/bin/env python3
"""
AI Accelerator Sector Growth Model
Models TAM expansion and adoption curves for AI accelerator market
Supports multiple curve fits: linear, S-curve (logistic), exponential
"""

import json
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class GrowthDriver:
    name: str
    current_magnitude: float  # Current value or penetration
    growth_rate: float  # Annual growth rate as decimal
    contribution_to_cagr: float  # Contribution to total sector CAGR

# Historical data points for AI accelerator market (2024-2025)
HISTORICAL_MARKET_DATA = {
    2024: 116,    # Market size in billions USD (Bloomberg)
    2025: 165,    # Estimated based on 42% YoY growth
}

# Growth drivers decomposition
# Note: Contributions are multiplicative, not additive - they represent weighted contributions
GROWTH_DRIVERS = [
    GrowthDriver(
        name="AI Capex Cycle (Hyperscaler Capex)",
        current_magnitude=65,  # $65B of $116B total
        growth_rate=0.50,  # 50% CAGR hyperscaler capex
        contribution_to_cagr=0.14  # Weighted component
    ),
    GrowthDriver(
        name="TAM Expansion (Training + Inference Workloads)",
        current_magnitude=116,  # Full TAM
        growth_rate=0.30,  # 30% CAGR as new use cases emerge
        contribution_to_cagr=0.12  # Weighted component
    ),
    GrowthDriver(
        name="Custom Silicon Adoption",
        current_magnitude=8,  # ~$8B custom silicon spend (estimated)
        growth_rate=0.50,  # 50% CAGR custom silicon
        contribution_to_cagr=0.03  # Weighted component (smaller base)
    ),
    GrowthDriver(
        name="Inference Workload Proliferation",
        current_magnitude=35,  # Inference growth
        growth_rate=0.40,  # 40% CAGR inference
        contribution_to_cagr=0.08  # Weighted component
    ),
    GrowthDriver(
        name="Price Erosion (Unit Volume Offset)",
        current_magnitude=1.0,  # Index
        growth_rate=-0.05,  # -5% price decline per year
        contribution_to_cagr=-0.01  # Negative offset
    ),
]

def linear_growth(t: np.ndarray, initial: float, cagr: float) -> np.ndarray:
    """Linear extrapolation of CAGR"""
    return initial * np.power(1 + cagr, t)

def logistic_growth(t: np.ndarray, L: float, k: float, t0: float) -> np.ndarray:
    """S-curve logistic growth model
    L: market carrying capacity (TAM)
    k: steepness (adoption rate)
    t0: inflection point (midpoint)
    """
    return L / (1 + np.exp(-k * (t - t0)))

def exponential_growth(t: np.ndarray, initial: float, doubling_period: float) -> np.ndarray:
    """Exponential growth with fixed doubling period"""
    return initial * np.power(2, t / doubling_period)

class AIAcceleratorGrowthModel:
    def __init__(self, base_year: int = 2024, base_value: float = 116):
        self.base_year = base_year
        self.base_value = base_value
        self.drivers = GROWTH_DRIVERS
        self.forecast_years = np.arange(0, 7)  # 2024-2030 (0-6 years)

    def calculate_implied_cagr(self) -> float:
        """Calculate implied sector CAGR from drivers"""
        total_contribution = sum(d.contribution_to_cagr for d in self.drivers)
        return total_contribution

    def forecast_linear(self, cagr: float = None) -> Dict:
        """Linear forecast (constant CAGR)"""
        if cagr is None:
            cagr = self.calculate_implied_cagr()

        values = linear_growth(self.forecast_years, self.base_value, cagr)

        return {
            "method": "linear",
            "cagr": cagr,
            "forecast": {int(self.base_year + int(t)): float(v) for t, v in zip(self.forecast_years, values)},
            "2030_value": float(values[-1]),
            "description": f"Constant {cagr*100:.1f}% annual growth"
        }

    def forecast_scurve(self, tam: float = 500, k: float = 0.6, t0: float = 3.5) -> Dict:
        """S-curve forecast (logistic adoption)
        tam: Total Addressable Market by 2030 (billions USD)
        k: Steepness of adoption curve
        t0: Inflection point (years from base)
        """
        values = logistic_growth(self.forecast_years, tam, k, t0)

        # Calculate implied CAGR 2024-2030
        cagr_implied = np.power(values[-1] / self.base_value, 1/6) - 1

        return {
            "method": "s_curve",
            "tam": tam,
            "steepness": k,
            "inflection_year": self.base_year + t0,
            "implied_cagr": cagr_implied,
            "forecast": {int(self.base_year + int(t)): float(v) for t, v in zip(self.forecast_years, values)},
            "2030_value": float(values[-1]),
            "description": f"Logistic S-curve with TAM=${tam}B, inflection @{self.base_year + int(t0)}"
        }

    def forecast_exponential(self, doubling_period: float = 1.5) -> Dict:
        """Exponential forecast (constant doubling period)"""
        values = exponential_growth(self.forecast_years, self.base_value, doubling_period)

        cagr_implied = np.power(2, 1 / doubling_period) - 1

        return {
            "method": "exponential",
            "doubling_period": doubling_period,
            "implied_cagr": cagr_implied,
            "forecast": {int(self.base_year + int(t)): float(v) for t, v in zip(self.forecast_years, values)},
            "2030_value": float(values[-1]),
            "description": f"Exponential with {doubling_period:.1f}-year doubling period"
        }

    def monte_carlo_scenarios(self, n_simulations: int = 1000) -> Dict:
        """Monte Carlo simulation of growth scenarios"""
        results_2030 = []

        for _ in range(n_simulations):
            # Vary each driver's growth rate by ±30%
            varied_cagr = 0
            for driver in self.drivers:
                varied_rate = driver.growth_rate * np.random.normal(1.0, 0.3)
                varied_cagr += driver.contribution_to_cagr * (varied_rate / driver.growth_rate)

            value_2030 = self.base_value * np.power(1 + varied_cagr, 6)
            results_2030.append(value_2030)

        results_2030 = np.array(results_2030)

        return {
            "method": "monte_carlo",
            "n_simulations": n_simulations,
            "mean_2030": float(np.mean(results_2030)),
            "median_2030": float(np.median(results_2030)),
            "std_2030": float(np.std(results_2030)),
            "percentile_10": float(np.percentile(results_2030, 10)),
            "percentile_90": float(np.percentile(results_2030, 90)),
            "p_growth_gt_25pct_cagr": float(np.mean(results_2030 > (self.base_value * np.power(1.25, 6)))),
            "p_growth_gt_35pct_cagr": float(np.mean(results_2030 > (self.base_value * np.power(1.35, 6)))),
            "p_growth_lt_15pct_cagr": float(np.mean(results_2030 < (self.base_value * np.power(1.15, 6)))),
        }

    def sensitivity_analysis(self, driver_name: str, shock_pct: float = 0.5) -> Dict:
        """Sensitivity to specific driver changes"""
        # Find the driver
        driver = next((d for d in self.drivers if d.name == driver_name), None)
        if not driver:
            return {"error": f"Driver '{driver_name}' not found"}

        # Base case CAGR
        base_cagr = self.calculate_implied_cagr()

        # Shocked case: driver growth rate changes by shock_pct
        shocked_contribution = driver.contribution_to_cagr * (1 + shock_pct)
        other_contribution = base_cagr - driver.contribution_to_cagr
        shocked_cagr = other_contribution + shocked_contribution

        base_2030 = self.base_value * np.power(1 + base_cagr, 6)
        shocked_2030 = self.base_value * np.power(1 + shocked_cagr, 6)

        return {
            "driver": driver_name,
            "shock_pct": shock_pct,
            "base_cagr": base_cagr,
            "base_2030_value": float(base_2030),
            "shocked_cagr": shocked_cagr,
            "shocked_2030_value": float(shocked_2030),
            "delta_2030": float(shocked_2030 - base_2030),
            "delta_pct": float((shocked_2030 - base_2030) / base_2030 * 100),
        }

    def generate_report(self) -> str:
        """Generate full analysis report"""
        report = []
        report.append("=" * 80)
        report.append("AI ACCELERATOR SECTOR GROWTH MODEL")
        report.append("=" * 80)
        report.append("")

        # Growth drivers
        report.append("GROWTH DRIVERS DECOMPOSITION:")
        report.append("-" * 80)
        total_cagr = 0
        for driver in self.drivers:
            report.append(f"{driver.name:50s} | Growth: {driver.growth_rate:6.1%} | Contribution: {driver.contribution_to_cagr:6.1%}")
            total_cagr += driver.contribution_to_cagr
        report.append("-" * 80)
        report.append(f"{'IMPLIED SECTOR CAGR':50s} | {total_cagr:6.1%}")
        report.append("")

        # Scenario forecasts
        linear = self.forecast_linear()
        scurve = self.forecast_scurve()
        expo = self.forecast_exponential()
        mc = self.monte_carlo_scenarios()

        report.append("SCENARIO FORECASTS (Market Size in $B):")
        report.append("-" * 80)
        report.append(f"{'Year':<8} {'Linear':<15} {'S-Curve':<15} {'Exponential':<15} {'MC Mean':<15}")
        report.append("-" * 80)

        for year in [2024, 2025, 2026, 2027, 2028, 2029, 2030]:
            idx = year - 2024
            lin = linear["forecast"].get(year, "N/A")
            sc = scurve["forecast"].get(year, "N/A")
            ex = expo["forecast"].get(year, "N/A")

            if isinstance(lin, float):
                report.append(f"{year:<8} ${lin:>13.1f}B ${sc:>13.1f}B ${ex:>13.1f}B ${mc['mean_2030']:>13.1f}B")

        report.append("-" * 80)
        report.append(f"2030 Value: Linear=${linear['2030_value']:.1f}B ({linear['cagr']*100:.1f}% CAGR)")
        report.append(f"2030 Value: S-Curve=${scurve['2030_value']:.1f}B ({scurve['implied_cagr']*100:.1f}% CAGR)")
        report.append(f"2030 Value: Exponential=${expo['2030_value']:.1f}B ({expo['implied_cagr']*100:.1f}% CAGR)")
        report.append("")

        # Monte Carlo
        report.append("MONTE CARLO SCENARIO ANALYSIS (1000 simulations):")
        report.append("-" * 80)
        report.append(f"2030 Mean Forecast: ${mc['mean_2030']:.1f}B")
        report.append(f"2030 Median: ${mc['median_2030']:.1f}B")
        report.append(f"2030 Std Dev: ${mc['std_2030']:.1f}B")
        report.append(f"2030 10th Percentile (Bear): ${mc['percentile_10']:.1f}B")
        report.append(f"2030 90th Percentile (Bull): ${mc['percentile_90']:.1f}B")
        report.append(f"P(CAGR > 25%): {mc['p_growth_gt_25pct_cagr']:.1%}")
        report.append(f"P(CAGR > 35%): {mc['p_growth_gt_35pct_cagr']:.1%}")
        report.append(f"P(CAGR < 15%): {mc['p_growth_lt_15pct_cagr']:.1%}")
        report.append("")

        # Sensitivity analysis
        report.append("SENSITIVITY ANALYSIS (50% upside/downside to each driver):")
        report.append("-" * 80)
        for driver in self.drivers:
            up_sens = self.sensitivity_analysis(driver.name, shock_pct=0.5)
            down_sens = self.sensitivity_analysis(driver.name, shock_pct=-0.5)
            report.append(f"{driver.name}:")
            report.append(f"  +50% scenario: ${up_sens['shocked_2030_value']:.1f}B 2030 ({up_sens['shocked_cagr']*100:.1f}% CAGR) [{up_sens['delta_pct']:+.1f}%]")
            report.append(f"  -50% scenario: ${down_sens['shocked_2030_value']:.1f}B 2030 ({down_sens['shocked_cagr']*100:.1f}% CAGR) [{down_sens['delta_pct']:+.1f}%]")
        report.append("")

        return "\n".join(report)

if __name__ == "__main__":
    model = AIAcceleratorGrowthModel()
    print(model.generate_report())

    # Export JSON
    output = {
        "growth_drivers": [
            {
                "name": d.name,
                "current_magnitude": d.current_magnitude,
                "growth_rate": d.growth_rate,
                "contribution_to_cagr": d.contribution_to_cagr,
            } for d in model.drivers
        ],
        "implied_sector_cagr": model.calculate_implied_cagr(),
        "forecasts": {
            "linear": model.forecast_linear(),
            "scurve": model.forecast_scurve(),
            "exponential": model.forecast_exponential(),
            "monte_carlo": model.monte_carlo_scenarios(),
        }
    }

    with open("/sessions/clever-affectionate-euler/mnt/multi-agent equity research/output/data/nvda-sector-growth-forecast.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\nJSON output saved to output/data/nvda-sector-growth-forecast.json")
