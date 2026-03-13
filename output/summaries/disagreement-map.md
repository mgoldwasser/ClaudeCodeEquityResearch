# NVDA — Disagreement Map (Pass 2)
**Date:** 2026-03-10

## Debate 1: Bear Case Probability
**Parties:** DCF Analyst (15%) vs Risk & Contrarian (30-35%)
**Resolution:** 17-18% combined bear probability when properly tiered:
- Mild bear (7-8%): -20-25% impact
- Base bear (8-9%): -30-35% impact
- Severe tail (2-3%): -55-65% impact
**Key insight:** Risk & Contrarian conflated probability with severity. Their 30-35% reflects chance of ANY adverse scenario, not the severe tail.
**Position sizing:** Negative Kelly is correct at current market price if overvalued. Expected return depends on price reveal (Step 2.7).
**Status:** PARTIALLY RESOLVED — probability tiered, but Kelly reconciliation depends on price reveal.

## Debate 2: NVIDIA Data Center Market Share 2030
**Parties:** DCF Analyst (75%) vs Industry Analyst (62-63% S-curve modal)
**Resolution:** 70% base case (revised from both positions)
- Hyperscaler inference (2030E $280B TAM): Custom silicon reaches 40-50%; NVIDIA holds 60% = $168B
- Enterprise/non-hyperscaler (2030E $200B TAM): CUDA stickier; NVIDIA holds 80% = $160B
- Blended: 68-70% share = $328-336B revenue
**Fair value impact:** DCF revised down ~$20-30/share (from $668.62 to ~$640-650)
**Status:** RESOLVED — 70% base case adopted. Key Unresolved Risk: external monetization timing of custom silicon.

## Debate 3: Terminal Gross Margin (2030-2031)
**Parties:** DCF (68%) vs Industry (72%) vs Quant (75%)
**Resolution:** 71.0% terminal gross margin
- Training (~55% of revenue by 2031): 74-76% margin
- Inference (~45% of revenue): 68-71% margin
- Blended: 71.0-71.5%
**Weaknesses addressed:** DCF double-counted ASP decline; Quant provided no compression mechanism; Industry's math didn't reconcile with share loss narrative.
**Fair value convergence:** DCF up to $720-740; Quant down to $665-680. Convergence band: $700-740.
**Status:** RESOLVED — 71% adopted.

## Debate 4A: Diluted Share Count (FY2027E)
**Parties:** DCF (2,450M) vs Quant (2,640M)
**Resolution:** 2,530M shares (provisional)
- Neither analyst retrieved actual FY2026A count from filings [DATA GAP]
- ESG data: SBC $19B annualized, 6.6x jump from FY2023; $15B unearned balance
- Math: ~2,520M FY2026A base x 0.5% net dilution = 2,533M FY2027E
**Fair value impact:** Using 2,530M instead of DCF's 2,450M reduces fair value ~$21/share
**Status:** RESOLVED (provisional pending 10-K verification)

## Debate 4B: Moat Durability & CUDA Switching Costs
**Parties:** DCF (implied 8/10, holds through FY2031) vs Industry (6/10, eroding)
**Resolution:** Moat erodes over 5 years: 82% share FY2027 → 70% FY2030 → 68% FY2031
- CUDA stickiness bifurcated: 80% for training, 50% for inference
- WACC increased from 11.8% to 12.3% (+50bps) for moat erosion
- Pricing elasticity trajectory -0.2 (today) → -1.2 (2029) acknowledged
**Fair value impact:** -$57/share from moat erosion (base from $646.73 to ~$612)
**Status:** RESOLVED — erosion trajectory adopted. Key Unresolved Risk: PyTorch vendor-neutrality timing.

## Bull Defense Summary
Bull Case Defender countered Risk & Contrarian on 5 points:
1. Capex cycle is capacity-constrained (not demand-constrained) — strongest counter
2. Kelly fraction recalculated positive at +0.08-0.15 with corrected inputs
3. Insider selling = diversification/tax; CEO holds 5-10% of company
4. Custom silicon has 24-36 month structural lag; CUDA worth $50-200M per workload to abandon
5. 92% buy consensus is rational given real earnings/demand
**Bear case genuinely strong on:** Peak-cycle valuation vulnerability (40-50% probability)

## Revised Consensus Numbers (Post-Debate)
| Parameter | Pre-Debate | Post-Debate | Impact |
|-----------|-----------|-------------|--------|
| Bear probability | 15% (DCF) / 30-35% (R&C) | 17-18% tiered | Moderate |
| Market share 2030 | 75% (DCF) / 63% (Industry) | 70% | -$20-30/share |
| Terminal gross margin | 68% (DCF) / 72% (Ind) / 75% (Quant) | 71% | +$50-70 vs DCF |
| Diluted shares FY2027E | 2,450M (DCF) / 2,640M (Quant) | 2,530M | -$21/share |
| WACC | 11.8% | 12.3% | -$57/share |

## Key Unresolved Risks (for Final Note)
1. Custom silicon external monetization timing (2027 vs 2030) — high materiality
2. PyTorch vendor-neutrality timeline — could collapse CUDA switching costs
3. Actual diluted share count (FY2026A 10-K not retrieved) — data gap
4. Kelly fraction sign depends on current market price vs fair value — resolved at price reveal
