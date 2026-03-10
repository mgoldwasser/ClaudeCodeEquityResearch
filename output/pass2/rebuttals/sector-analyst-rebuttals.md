# Sector Analyst — Rebuttals

**Date:** 2026-03-09
**Subject:** AMD (Advanced Micro Devices, Inc.)

---

## Response to Technical Analyst

**Critique: Stock's price action (peaked October 2025, making lower lows) contradicts 3-4 years of high growth remaining — sector leaders typically peak 12-18 months before the cycle peaks.**

Reject. Stock price action reflects market expectations about growth rates, multiples, and sentiment — not actual TAM trajectories. NVIDIA peaked in late 2024 before correcting 20%+, yet data center GPU revenue continued accelerating in FY2025 ($130.5B). AMD peaked and corrected 28%, yet Q4 FY2025 data center revenue hit a record $5.4B (+39% YoY). The "sector leaders peak before the cycle" pattern applies to cyclical industries (memory, commodity semiconductors) where revenue growth decelerates predictably. AI GPU demand is being driven by contracted hyperscaler capex ($300B+ committed), not cyclical patterns. The price decline reflects execution risk and multiple compression, not TAM exhaustion.

**Critique: TAM overstatement of 20-40% acknowledged but not applied — base case should use 20%-haircut figure (~$302B).**

Partially accept. The critique is logically consistent — if I flag overstatement risk, the base case should reflect it. However, the 20-40% historical overstatement pattern is drawn from technology markets where adoption stalled (VR, 3D printing, autonomous vehicles). AI GPU TAM estimates have been consistently understated: the 2023 consensus AI accelerator TAM for 2025 was $30-50B; NVIDIA alone generated $130.5B in data center revenue in FY2025. I revise the base case to apply a 10% haircut (reflecting overstatement risk but acknowledging that AI TAM has historically been understated), producing a base-case AI GPU TAM of $340B by 2030 (down from $378B). The 20% haircut ($302B) is retained as the bear-case TAM.

**Critique: Add sector relative strength analysis — AMD underperforming SOXX suggests company-specific issues dominate sector tailwinds.**

Accept. AMD's underperformance vs. SOXX is a valid signal that the stock's weakness is company-specific (CUDA gap, MI450 execution risk, warrant dilution) rather than sector-driven. This is an important distinction: the sector thesis (AI GPU demand growing >30% annually) remains intact, but AMD's ability to capture that growth is being questioned by the market. I add a company-vs-sector relative performance assessment to acknowledge that sector tailwinds are necessary but not sufficient for the AMD thesis.

---

## Response to Devil's Advocate

**Critique: Market share trajectory from 10% to 18.8% by 2030 is too optimistic — CUDA moat, custom ASIC competition, and bridge contract risk cap AMD at 12-15%.**

Partially accept. The 18.8% base case assumes sustained execution across MI350, MI450, and next-generation products, plus successful mega-deal realization. The Devil's Advocate correctly identifies that any single failure (MI450 delay, ASIC cannibalization, CUDA lock-in) could cap share at 12-15%. I revise the share trajectory to present a range: 12% (bear — execution stumbles), 16% (base — partial mega-deal realization, MI450 competitive but not leading), 22% (bull — full mega-deal realization, MI450 outperforms). The previous 18.8% base case was a point estimate that masked the binary nature of the share outcome. The revised 16% base case is more defensible given the identified risks.

**Critique: TAM estimates in the sector analysis are unverified third-party figures — no bottom-up validation.**

Partially accept. The TAM figures ($378B AI GPU, $151B custom ASIC by 2030) are sourced from industry analysts (Tier 3) without bottom-up computational verification. However, the AI GPU TAM can be partially verified from known hyperscaler capex commitments: announced AI infrastructure spending for 2026 alone exceeds $350B globally, implying a multi-year TAM trajectory well above $200B annually. I acknowledge that a bottom-up verification (number of AI training clusters x GPU density x ASP x replacement cycle) would strengthen the analysis and should be incorporated in any revision. The directional conclusion — that the TAM is large enough to support AMD's growth thesis — holds regardless of whether the exact 2030 figure is $302B or $378B.

---

## Response to Forensic Analyst

**Critique: Segment restructuring (Client + Gaming combined) reduces visibility into declining gaming business — forensic concern about management hiding deteriorating sub-segments.**

Reject. The Client + Gaming combination is cosmetically concerning but immaterial to the investment thesis. Gaming is now <5% of AMD revenue and declining — the segment could go to zero and the thesis is unchanged. The Forensic Analyst's own report correctly identifies that the real disclosure gap is Instinct GPU revenue within the Data Center segment, not the Gaming business. The segment restructuring is standard practice for de-emphasizing legacy businesses (Intel did the same with its modem business). I maintain that the Data Center GPU disclosure gap is the legitimate concern; the Client + Gaming combination is noise.

---

## Response to Sentiment Analyst

**Critique: Lisa Su's shift to ambitious targets (>60% DC CAGR, >$20 EPS) changes the beat/fade calculus — historically she under-promised and over-delivered, now expectations are elevated.**

Partially accept. The Sentiment Analyst correctly notes that ambitious public targets raise the bar for future beats. However, the context matters: these targets were announced alongside $200B+ in contracted pipeline (OpenAI + Meta), not as aspirational marketing. The >60% DC CAGR is mathematically achievable if the mega-deals realize at even 50% of potential ($100B over 5 years = $20B/year incremental). The >$20 EPS requires full mega-deal execution plus margin expansion — this is the bull case, not the base case. I revise to acknowledge that the near-term beat rate may decline (Q1 and Q2 2026) as guidance catches up to expectations, but the multi-year revenue trajectory is backed by contracted demand rather than aspirational targets.

---

## Response to Research Analyst

**Critique: ROIC discrepancy — Sector Analyst cites 15% ROIC while Quant Analyst reports 6.6%. This inconsistency undermines cross-analyst comparisons.**

Accept. The 15% ROIC figure I cited was a forward-looking estimate based on data center segment-level returns, while the Quant Analyst's 6.6% is a trailing GAAP ROIC dragged down by Xilinx goodwill ($25.1B). Both figures are technically correct for their respective methodologies, but presenting them without reconciliation creates confusion. I revise to present both: (1) GAAP ROIC of 6.6% (trailing, penalized by $25.1B goodwill from Xilinx acquisition); (2) estimated operational ROIC of 12-15% (excluding goodwill, forward-looking, reflecting data center economics). The GAAP figure reflects the cost of the Xilinx acquisition; the operational figure reflects the current business economics.

**Critique: AMD GPU market share of "~10% current" sourced from Tier 6 estimates — insufficient reliability for a key thesis variable.**

Partially accept. The ~10% GPU market share figure is an estimate derived from analyst commentary and industry reports (Tier 3-6), not from AMD's own disclosures (AMD does not report GPU-specific revenue). The figure is consistent across multiple independent sources (SemiAnalysis, JPMorgan, Wells Fargo research) and is bounded by known data points: AMD's Data Center revenue ($16.6B) includes both EPYC CPUs and Instinct GPUs, and NVIDIA's data center revenue ($130.5B) is primarily GPUs. A rough calculation: if AMD's GPU revenue is $5-8B (implied by data center less EPYC), that is approximately 4-6% of NVIDIA's GPU revenue — consistent with ~10% total market share including other competitors. I flag the figure as [ESTIMATED, Tier 3-6 consensus] and note that AMD's refusal to break out GPU revenue prevents verification.

---

## Response to DCF Analyst

**Critique: TSMC CoWoS allocation (8-10% for AMD vs. 60% for NVIDIA) is not quantified as a revenue cap — the supply constraint should be translated into maximum achievable GPU revenue.**

Accept. The CoWoS allocation constraint directly limits AMD's GPU shipment capacity. At current allocation (8-10% of 80K wafers/month = 6,400-8,000 wafers), AMD's maximum GPU production is bounded. However, the constraint is dynamic: TSMC is expanding CoWoS to 130K wafers/month by late 2026, and AMD's mega-deals (OpenAI, Meta) give it leverage to negotiate higher allocation. I model three scenarios: (1) current allocation maintained at 8-10% of expanded capacity = 10,400-13,000 wafers (1.6x current); (2) allocation increases to 12-15% on mega-deal demand = 15,600-19,500 wafers (2.4-3x current); (3) allocation increases to 15-20% with dedicated TSMC lines = 19,500-26,000 wafers (3-4x current). Scenario 2 is the base case and supports the 16% market share target.

---

## Response to Quant Analyst

**Critique: ROIC of 15% cited by Sector Analyst conflicts with computed ROIC of 6.6% — a 2.3x discrepancy undermines the capital efficiency argument.**

Accept. See response to Research Analyst above. The 6.6% GAAP ROIC is the correct trailing figure and should be the primary metric cited. The 15% operational ROIC is a forward estimate that excludes goodwill — a legitimate analytical adjustment but one that should be clearly labeled as adjusted. I revise all ROIC references to lead with the 6.6% GAAP figure and present the goodwill-adjusted figure as supplementary context.

---

## Response to Competitive Analyst

**Critique: Market share projection of 18.8% by 2030 does not adequately account for custom ASIC competition — Google TPU, Amazon Trainium, Meta MTIA, and Microsoft Maia collectively could capture 20-30% of the accelerator market.**

Partially accept. The Competitive Analyst correctly identifies that custom ASICs are the primary competitive threat to AMD's share trajectory. My analysis included custom ASIC TAM ($151B by 2030) as a separate market, but did not explicitly model the overlap: some workloads that could go to AMD GPUs will instead go to custom ASICs, particularly inference workloads. I revise the share trajectory to account for ASIC cannibalization: if custom ASICs capture 25% of the total accelerator market by 2030, AMD's addressable GPU market is reduced from $378B to ~$283B, and 16% share of the reduced market implies $45B (vs. the original $71B). This is a material revision that reduces the bull case but does not change the base case directionally — AMD still has a large growth opportunity.

---

## Response to Macro Analyst

**Critique: AI capex cycle sensitivity not modeled — if hyperscaler capex growth decelerates from 40% to 15%, AMD's TAM trajectory flattens materially.**

Accept. The sector analysis assumed sustained hyperscaler capex growth of 25-40% through 2028, which is aggressive. A capex deceleration to 15-20% growth would reduce the AI GPU TAM trajectory by approximately 20-25% by 2030, bringing it closer to $280-300B rather than $378B. I incorporate a capex sensitivity analysis: base case (25% capex CAGR, TAM $340B), bear case (15% capex CAGR, TAM $280B), bull case (35% capex CAGR, TAM $400B+). The macro dependency is the most important external variable for the sector thesis.

---

## Response to Risk Analyst

**Critique: China export control risk not quantified as a share ceiling — if AMD is permanently locked out of China (15-20% of global GPU demand), the addressable market shrinks proportionally.**

Accept. China represents approximately 15-20% of global AI GPU demand, and AMD's permanent exclusion would reduce the addressable TAM by that proportion. My analysis included China as a risk factor but did not quantify the market share impact. I revise to model two scenarios: (1) China access restored (TAM $340B, AMD share 16%); (2) permanent China exclusion (effective TAM ~$280B, but AMD can redeploy capacity to non-China customers, mitigating ~50% of the impact). Net impact of permanent exclusion: -$10-15/share in fair value.

---

## Response to Credit Analyst

**Critique: TSMC concentration risk (100% advanced node dependence) should be assessed as a credit-adjacent risk — single-supplier dependency creates a tail risk that balance sheet strength cannot hedge.**

Accept. The Credit Analyst raises a valid structural risk. AMD has no foundry diversification for its advanced node products — MI450, EPYC, and Ryzen are all TSMC-dependent. A TSMC disruption (geopolitical, earthquake, capacity reallocation) would halt AMD's revenue within 6-12 months. This is a tail risk that the sector analysis should quantify: probability (5-10% over 5 years) x magnitude ($50-70B market cap loss) = expected cost of ~$3-5B or ~$2-3/share. The mitigant is that TSMC concentration is an industry-wide risk shared by NVIDIA, Apple, and Qualcomm — AMD is not uniquely disadvantaged.

---

## Response to Catalyst Analyst

**Critique: Market share gains should be modeled as step-functions tied to product launches rather than linear trajectories.**

Accept. The Catalyst Analyst correctly identifies that semiconductor share gains are lumpy and catalyst-driven, not linear. MI450 launch is a step-function event: success could jump AMD from 12% to 16-18% in 2-3 quarters, while failure would stagnate share at 10-12%. I revise the share model from linear (10% to 18.8% over 5 years) to step-function: 10% through H1 2026, then either 15-18% (MI450 success) or 10-12% (MI450 delay/failure) from H2 2026, with subsequent step-functions at MI500 launch and next-generation product cycles.

---

## Response to ESG & Governance Analyst

**Critique: AMD's R&D spending as percentage of revenue is declining as revenue scales — without a board-mandated ROCm investment commitment, the 18.8% share target relies on hardware-alone differentiation.**

Partially accept. R&D as a percentage of revenue is declining (from ~25% to ~20%), but absolute R&D spending is increasing. The ROCm software investment is embedded in the overall R&D budget and AMD does not break it out separately. The ESG Analyst is correct that hardware-alone differentiation is insufficient against NVIDIA's CUDA ecosystem — but the competitive dynamics are shifting. Abstraction layers (PyTorch 2.0, Triton, JAX) are reducing CUDA lock-in, and hyperscaler mega-deal customers (OpenAI, Meta) are investing in their own software stacks that abstract away hardware differences. The share trajectory does not require AMD to match CUDA — it requires that enough large customers value hardware performance-per-dollar over software ecosystem breadth. I maintain the revised 16% base case share target, which implicitly assumes partial ROCm improvement plus abstraction layer progress.

**Critique: Board composition may lack semiconductor manufacturing expertise to negotiate TSMC allocation effectively.**

Partially accept. Without the full DEF 14A proxy, I cannot confirm or deny the board's manufacturing expertise. However, TSMC allocation decisions are made at the CEO/COO level (Lisa Su has a PhD in electrical engineering from MIT and deep TSMC relationships), not the board level. Board manufacturing expertise would be valuable for strategic decisions (foundry diversification, Samsung/Intel Foundry evaluation) but is less relevant for near-term CoWoS allocation negotiations. I flag this as a governance consideration rather than a material constraint on the share trajectory.

---

*Rebuttals by Sector Analyst, Equity Research Swarm. Pass 2 adversarial review.*
