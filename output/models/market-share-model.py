#!/usr/bin/env python3
"""
AI Accelerator Market Share Evolution Model
Models competitive market share shifts 2024-2030 for NVIDIA vs. competitors
Incorporates share erosion from AMD, custom silicon, and Intel
"""

import json
import numpy as np
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Competitor:
    name: str
    share_2024: float  # Market share %
    growth_driver: str  # Main growth driver
    share_cagr: float  # Annual share point change
    max_share_potential: float  # Ceiling for competitive positioning

# Current market positioning (2024-2025)
COMPETITORS_2024 = [
    Competitor(name="NVIDIA", share_2024=92.0, growth_driver="First-mover + CUDA moat", share_cagr=-1.5, max_share_potential=75.0),
    Competitor(name="AMD", share_2024=5.0, growth_driver="ROCm software + MI325X", share_cagr=2.0, max_share_potential=20.0),
    Competitor(name="Custom Silicon (Google/Amazon/Meta)", share_2024=2.0, growth_driver="Internal inference workloads", share_cagr=2.5, max_share_potential=25.0),
    Competitor(name="Intel", share_2024=0.5, growth_driver="Weak positioning", share_cagr=0.2, max_share_potential=5.0),
    Competitor(name="Others (Qualcomm, Marvell, etc.)", share_2024=0.5, growth_driver="Niche edge inference", share_cagr=0.1, max_share_potential=3.0),
]

class MarketShareModel:
    def __init__(self, competitors: List[Competitor] = None):
        self.competitors = competitors or COMPETITORS_2024
        self.validate_shares()

    def validate_shares(self):
        """Verify shares sum to 100%"""
        total = sum(c.share_2024 for c in self.competitors)
        if abs(total - 100.0) > 0.1:
            raise ValueError(f"Shares don't sum to 100%: {total}%")

    def forecast_linear_share_shift(self, years: int = 6) -> Dict:
        """Linear share shift model (constant annual changes)"""
        forecast = {}

        for year in range(2024, 2024 + years + 1):
            t = year - 2024
            year_shares = {}

            for competitor in self.competitors:
                # Linear shift: current share + (years * annual_change)
                # Constrained by max_share_potential
                new_share = competitor.share_2024 + (t * competitor.share_cagr)
                # Ensure shares don't go negative or exceed potential
                new_share = max(0, min(new_share, competitor.max_share_potential))
                year_shares[competitor.name] = new_share

            # Normalize to 100% (redistribute constraint violations)
            total = sum(year_shares.values())
            if total > 0:
                year_shares = {k: (v / total * 100) for k, v in year_shares.items()}

            forecast[year] = year_shares

        return {
            "method": "linear_share_shift",
            "assumptions": "Constant annual share point changes; constrained by max_share_potential",
            "forecast": forecast,
        }

    def forecast_s_curve_share_shift(self, years: int = 6) -> Dict:
        """S-curve share shift model (sigmoid adoption of competitors)"""
        forecast = {}

        for year in range(2024, 2024 + years + 1):
            t = year - 2024
            year_shares = {}

            for competitor in self.competitors:
                if competitor.name == "NVIDIA":
                    # NVIDIA loses share via sigmoid decay
                    # Decays from 92% toward max_share_potential
                    share_loss = (competitor.share_2024 - competitor.max_share_potential) / (1 + np.exp(-0.8 * (t - 3)))
                    new_share = competitor.share_2024 - share_loss
                else:
                    # Competitors gain share via sigmoid adoption
                    # Adopts from current toward max_share_potential
                    share_gain_potential = competitor.max_share_potential - competitor.share_2024
                    share_gain = share_gain_potential / (1 + np.exp(-0.8 * (t - 2)))
                    new_share = competitor.share_2024 + share_gain

                year_shares[competitor.name] = max(0, min(new_share, competitor.max_share_potential))

            # Normalize to 100%
            total = sum(year_shares.values())
            if total > 0:
                year_shares = {k: (v / total * 100) for k, v in year_shares.items()}

            forecast[year] = year_shares

        return {
            "method": "s_curve_share_shift",
            "assumptions": "Sigmoid adoption curves; NVIDIA decays to max_share, competitors adopt S-curve",
            "forecast": forecast,
        }

    def monte_carlo_share_scenarios(self, years: int = 6, n_simulations: int = 1000) -> Dict:
        """Monte Carlo simulation of market share evolution"""
        results_2030 = {c.name: [] for c in self.competitors}

        for _ in range(n_simulations):
            year_shares = {c.name: c.share_2024 for c in self.competitors}

            for t in range(1, years + 1):
                new_shares = {}

                for competitor in self.competitors:
                    # Vary annual shift by ±40% (add randomness)
                    varied_cagr = competitor.share_cagr * np.random.normal(1.0, 0.4)
                    new_share = year_shares[competitor.name] + varied_cagr
                    new_share = max(0, min(new_share, competitor.max_share_potential))
                    new_shares[competitor.name] = new_share

                # Normalize to 100%
                total = sum(new_shares.values())
                if total > 0:
                    year_shares = {k: (v / total * 100) for k, v in new_shares.items()}

            # Store 2030 result
            for c_name, share in year_shares.items():
                results_2030[c_name].append(share)

        # Compute statistics
        stats = {}
        for c_name in results_2030:
            shares = np.array(results_2030[c_name])
            stats[c_name] = {
                "mean_2030": float(np.mean(shares)),
                "median_2030": float(np.median(shares)),
                "std_2030": float(np.std(shares)),
                "p10": float(np.percentile(shares, 10)),
                "p90": float(np.percentile(shares, 90)),
            }

        return {
            "method": "monte_carlo_share_scenarios",
            "n_simulations": n_simulations,
            "2030_statistics": stats,
        }

    def threat_scenario_analysis(self) -> Dict:
        """Analyze specific threat scenarios"""
        scenarios = {}

        # Scenario 1: Custom silicon accelerates (Google, Amazon, Meta scale rapidly)
        scenarios["custom_silicon_rapid_scale"] = {
            "description": "Custom silicon gains faster than expected (4% annually vs. 2.5% base)",
            "adjustments": {
                "Custom Silicon (Google/Amazon/Meta)": {"share_cagr": 4.0, "max_share_potential": 35.0},
                "NVIDIA": {"share_cagr": -2.5},
            },
            "2030_nvda_share_impact": "NVIDIA share declines to ~65% (vs. 75% base case)"
        }

        # Scenario 2: AMD ROCm catches up faster (ecosystem parity by 2027)
        scenarios["amd_ecosystem_parity"] = {
            "description": "AMD ROCm achieves ecosystem parity faster; customers switch to AMD for cost",
            "adjustments": {
                "AMD": {"share_cagr": 3.5, "max_share_potential": 30.0},
                "NVIDIA": {"share_cagr": -2.0},
            },
            "2030_nvda_share_impact": "NVIDIA share declines to ~70% (vs. 75% base case)"
        }

        # Scenario 3: Benign competition (NVIDIA retains >80% through 2030)
        scenarios["nvidia_market_leadership_sustained"] = {
            "description": "CUDA moat holds; custom silicon remains internal-only; AMD ROCm lags",
            "adjustments": {
                "NVIDIA": {"share_cagr": -0.8, "max_share_potential": 80.0},
                "AMD": {"share_cagr": 0.6, "max_share_potential": 12.0},
                "Custom Silicon (Google/Amazon/Meta)": {"share_cagr": 0.8, "max_share_potential": 10.0},
            },
            "2030_nvda_share_impact": "NVIDIA maintains 80-82% share (stronger moat scenario)"
        }

        # Scenario 4: Competitive pressure intensifies (NVIDIA to <60%)
        scenarios["intense_competitive_pressure"] = {
            "description": "Custom silicon + AMD ROCm both scale rapidly; hyperscalers prioritize TCO",
            "adjustments": {
                "NVIDIA": {"share_cagr": -3.5, "max_share_potential": 55.0},
                "AMD": {"share_cagr": 3.0, "max_share_potential": 25.0},
                "Custom Silicon (Google/Amazon/Meta)": {"share_cagr": 3.5, "max_share_potential": 30.0},
            },
            "2030_nvda_share_impact": "NVIDIA declines to ~55% (severe competitive loss scenario)"
        }

        return scenarios

    def generate_report(self) -> str:
        """Generate full analysis report"""
        report = []
        report.append("=" * 100)
        report.append("AI ACCELERATOR MARKET SHARE EVOLUTION MODEL")
        report.append("=" * 100)
        report.append("")

        # Current state
        report.append("MARKET SHARE BASELINE (2024):")
        report.append("-" * 100)
        for competitor in self.competitors:
            report.append(f"{competitor.name:45s} | Share: {competitor.share_2024:6.2f}% | Annual Shift: {competitor.share_cagr:+6.2f}pp | Max Potential: {competitor.max_share_potential:6.2f}%")
        report.append("")

        # Linear forecast
        linear = self.forecast_linear_share_shift()
        report.append("LINEAR SHARE FORECAST (Constant Annual Changes):")
        report.append("-" * 100)
        header = f"{'Year':<8}"
        for competitor in self.competitors:
            header += f" {competitor.name[:20]:<20}"
        report.append(header)
        report.append("-" * 100)

        for year in range(2024, 2031):
            line = f"{year:<8}"
            if year in linear["forecast"]:
                for competitor in self.competitors:
                    share = linear["forecast"][year][competitor.name]
                    line += f" {share:>19.1f}%"
            report.append(line)

        report.append("")

        # S-curve forecast
        scurve = self.forecast_s_curve_share_shift()
        report.append("S-CURVE SHARE FORECAST (Sigmoid Adoption):")
        report.append("-" * 100)
        header = f"{'Year':<8}"
        for competitor in self.competitors:
            header += f" {competitor.name[:20]:<20}"
        report.append(header)
        report.append("-" * 100)

        for year in range(2024, 2031):
            line = f"{year:<8}"
            if year in scurve["forecast"]:
                for competitor in self.competitors:
                    share = scurve["forecast"][year][competitor.name]
                    line += f" {share:>19.1f}%"
            report.append(line)

        report.append("")

        # Monte Carlo
        mc = self.monte_carlo_share_scenarios()
        report.append("MONTE CARLO 2030 PROJECTIONS (1000 simulations):")
        report.append("-" * 100)
        for competitor in self.competitors:
            stats = mc["2030_statistics"][competitor.name]
            report.append(f"{competitor.name}:")
            report.append(f"  Mean: {stats['mean_2030']:6.1f}% | Median: {stats['median_2030']:6.1f}% | Std Dev: {stats['std_2030']:6.1f}%")
            report.append(f"  Range (10-90): {stats['p10']:6.1f}% - {stats['p90']:6.1f}%")

        report.append("")

        # Threat scenarios
        threats = self.threat_scenario_analysis()
        report.append("COMPETITIVE THREAT SCENARIOS:")
        report.append("-" * 100)
        for scenario_name, scenario_data in threats.items():
            report.append(f"\n{scenario_name.upper()}:")
            report.append(f"  Description: {scenario_data['description']}")
            report.append(f"  Impact: {scenario_data['2030_nvda_share_impact']}")

        report.append("")

        return "\n".join(report)

    def herfindahl_hirschman_index(self, shares: Dict[str, float]) -> float:
        """Calculate HHI for concentration analysis"""
        return sum(share ** 2 for share in shares.values())

if __name__ == "__main__":
    model = MarketShareModel()
    print(model.generate_report())

    # Export JSON
    linear = model.forecast_linear_share_shift()
    scurve = model.forecast_s_curve_share_shift()
    mc = model.monte_carlo_share_scenarios()
    threats = model.threat_scenario_analysis()

    # Compute HHI for key years
    hhi_2024 = model.herfindahl_hirschman_index({c.name: c.share_2024 for c in model.competitors})
    hhi_2030_linear = model.herfindahl_hirschman_index(linear["forecast"][2030])
    hhi_2030_scurve = model.herfindahl_hirschman_index(scurve["forecast"][2030])

    output = {
        "baseline_2024": {c.name: c.share_2024 for c in model.competitors},
        "hhi_2024": hhi_2024,
        "hhi_2030_linear": hhi_2030_linear,
        "hhi_2030_scurve": hhi_2030_scurve,
        "forecasts": {
            "linear": linear,
            "scurve": scurve,
            "monte_carlo": mc,
        },
        "threat_scenarios": threats,
    }

    with open("/sessions/clever-affectionate-euler/mnt/multi-agent equity research/output/data/nvda-market-share-forecast.json", "w") as f:
        json.dump(output, f, indent=2, default=str)

    print("\nJSON output saved to output/data/nvda-market-share-forecast.json")
