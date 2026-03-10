# Pass 2 Rebuttals -- Competitive Analyst
**Date:** 2026-03-09
**Subject:** Advanced Micro Devices, Inc. (AMD)

---

## Response to DCF Analyst's Critique

### 1. "Custom ASICs and GPUs are complementary" assumption is weak — ASIC growth at 44.6% vs. GPU 16.1% suggests substitution
**Verdict: Partially Accept**

The DCF Analyst makes a strong quantitative point: if ASICs and GPUs were purely complementary, growth rates should converge, not diverge. I accept that my "medium confidence" characterization of complementarity was insufficiently nuanced. However, the comparison of aggregate ASIC growth (44.6%) to aggregate GPU growth (16.1%) conflates new ASIC TAM creation with GPU substitution. Much of the ASIC growth comes from hyperscalers deploying custom silicon for workloads they never ran on merchant GPUs — Google's TPU has been internal-only since 2015, and Amazon's Trainium targets internal AWS workloads that were previously CPU-based. The substitution-relevant metric is whether OpenAI and Meta are reducing GPU purchases in favor of ASICs, and the evidence here is mixed: both signed massive AMD GPU deals while simultaneously pursuing ASIC programs. I revise my assessment to: "GPUs and ASICs are complementary in the near term (2026-2028) as ASICs mature, transitioning to partially substitutional by 2029-2030 for high-volume inference workloads. Confidence: medium-low." I also accept the DCF Analyst's point that the mega-deal realization rate should be stress-tested against this dynamic, and I lower my implied realization assumption from 75% to 65-70% for the base case.

### 2. Revenue-weighted moat score should be ~5.5/10, not 6/10 — AI GPU (5/10 moat) dominates valuation
**Verdict: Partially Accept**

The DCF Analyst correctly observes that the overall competitive score of 6/10 blends a strong but lower-value franchise (server CPU, 8/10) with a weak but high-value franchise (AI GPU, 5/10). On a FY2030 revenue-weighted basis with AI GPU at 74% of revenue, the blended score would converge toward 5.5/10. I accept the principle that a revenue-weighted score better reflects the investment thesis. However, I note two mitigating factors: (1) the server CPU business provides a durable earnings floor that reduces downside risk even if the AI GPU thesis disappoints, which a pure revenue-weighted score undervalues; (2) the moat score captures structural durability, not near-term revenue contribution — a 5/10 moat with improving trajectory is different from a 5/10 moat that is stable or declining. I will present both the simple average (6/10) and revenue-weighted (5.5/10 at FY2030 mix) competitive scores in any revision, with the revenue-weighted score flagged as the more relevant metric for equity valuation purposes.

### 3. CUDA Gap Score should be translated into quantified financial impact
**Verdict: Accept**

The DCF Analyst is right that presenting the CUDA Gap Score (28.7-99.1) without translating it into revenue or margin terms limits its utility for financial modeling. I will add the following framework: at a 30% effective CUDA gap (low end, inference workloads), AMD can compete on TCO and address ~60-70% of the AI GPU TAM; at a 65% gap (midpoint), AMD is limited to price-sensitive and second-source procurement, addressing ~30-40% of TAM; at 99% (high end, legacy CUDA-optimized training), AMD is effectively locked out. At the DCF Analyst's $140B 2025 TAM, the revenue difference between the 30% and 65% gap scenarios is approximately $42-56B in addressable market, translating to $4-6B in AMD revenue at 10% share — a meaningful swing that should be explicitly modeled.

---

## Response to Quant Analyst's Critique

### 1. CUDA Gap Score range of 28.7-99.1 is too wide to be analytically useful — Tier 6 source
**Verdict: Partially Accept**

The Quant Analyst correctly identifies that a 28.7-99.1 range from a Tier 6 source (AIM Multiple) is imprecise. However, the wide range is not analytical noise — it reflects genuine workload-dependent variation. The 28.7 low end represents compute-intensive inference workloads where ROCm has achieved near-parity (consistent with AMD's MI355X benchmarks showing 20% faster than B200 on DeepSeek R1 FP4). The 99.1 high end represents legacy CUDA-optimized multi-node training workloads with deep library dependencies. I accept the recommendation to decompose the score by workload type: inference (CUDA gap ~25-35%), single-node training (~40-55%), multi-node training (~65-99%). I also accept that the Tier 6 sourcing should be more prominently flagged. However, I note that the MI355X and MI450 benchmark data from SemiAnalysis (Tier 3) provides partial first-party corroboration of the low end of the range, and the OpenAI/Meta mega-deals represent revealed preference by the world's most sophisticated GPU buyers that the gap is manageable for their workloads.

### 2. ASIC growth vs. GPU growth comparison conflates aggregate market with AMD-specific dynamics
**Verdict: Accept**

The Quant Analyst makes the important distinction that AMD's Data Center revenue grew 39% YoY in Q4 2025 while guided to >60% DC CAGR — both far exceeding the 16.1% aggregate GPU market growth. AMD is gaining share within the GPU market while ASICs grow separately. I accept that my analysis conflated aggregate market growth rates with AMD-specific competitive dynamics. The relevant question is not whether ASICs are growing faster than GPUs in aggregate, but whether AMD's specific customers are shifting incremental dollars from AMD GPUs to custom ASICs. The evidence — OpenAI signing both a 6 GW AMD deal and a 10 GW Broadcom ASIC deal — suggests at minimum 2-3 years of coexistence, with substitution risk concentrated in 2029+. I will revise the ASIC threat timeline accordingly.

### 3. Overall competitive score of 6/10 underweights server CPU position — revenue-weighted score should be 6.5-7/10
**Verdict: Partially Accept**

The Quant Analyst argues that a revenue-weighted score emphasizing server CPU (8/10 at ~40% of DC revenue) should pull the blended score to 6.5-7/10. This contradicts the DCF Analyst's critique that a revenue-weighted score should be 5.5/10 (emphasizing AI GPU at FY2030 mix). The disagreement reveals that the competitive score is time-dependent: at current revenue mix, the score is 6.5/10; at FY2030 projected mix, it converges toward 5.5/10. I accept the Quant Analyst's point that today's competitive position — anchored by server CPU dominance — is stronger than my static 6/10 suggests. I will present a time-varying competitive score: 6.5-7/10 today (strong server CPU, emerging AI GPU), declining to 5.5-6/10 by FY2030 if AI GPU moat does not widen. This framework better captures the trajectory than a single number.

---

## Response to Research Analyst's Critique

### 1. AI GPU share of ~8-12% sourced from TechNetBooks (Tier 6) — wide range, low reliability
**Verdict: Partially Accept**

The Research Analyst correctly flags that a 4-percentage-point range from a Tier 6 source is problematic for the most critical metric in the analysis. I accept that the sourcing should be upgraded. However, I note that the 8-12% range can be partially triangulated from higher-tier data: AMD's Data Center segment revenue was $16.6B in FY2025 (Tier 1), of which GPU revenue is estimated at $10-12B (based on management commentary and segment trends). Against an AI GPU TAM of ~$140B (Tier 3-6 consensus), this implies ~7-9% revenue share — consistent with the lower end of my range. I will revise to present the share as "~8-10% [ESTIMATED, triangulated from AMD Tier 1 revenue data and Tier 3-6 TAM estimates]" and drop the 12% upper bound as insufficiently supported.

### 2. CUDA Gap Score of 28.7-99.1 sourced from AIM Multiple (Tier 6) — may not reflect current ROCm performance
**Verdict: Partially Accept**

The Research Analyst raises a valid point that ROCm is evolving rapidly and the benchmark data may be stale. ROCm 7.0 launched in late 2025 with meaningful improvements (day-zero support for major models, 3.5x inference performance improvement). I accept the recommendation to date-stamp all CUDA/ROCm benchmark comparisons and note whether they are pre- or post-ROCm 7.0. I also accept that the gap is likely narrowing for inference workloads, though I note that training workloads remain CUDA-dominant and the gap may be widening in absolute terms (NVIDIA continues to invest in CUDA libraries). I will add a temporal qualifier: "CUDA Gap Score as of mid-2025 benchmarks; gap likely narrowing for inference (estimated 20-30% post-ROCm 7.0) while remaining wide for multi-node training (estimated 50-80%)."

### 3. Custom ASIC threat should be quantified by cross-referencing specific hyperscaler programs
**Verdict: Accept**

The Research Analyst correctly notes that my analysis should have cross-referenced the OpenAI-Broadcom 10 GW deal more explicitly against the AMD 6 GW deal. OpenAI committing 67% more wattage to custom ASICs than to AMD GPUs is meaningful evidence that GPUs are not the sole infrastructure strategy. I accept this critique and will add: "OpenAI's infrastructure allocation — 10 GW ASICs vs. 6 GW AMD GPUs — implies ~63% of OpenAI's compute buildout is custom silicon, suggesting GPUs serve as a flexible complement to ASIC-optimized inference rather than the primary compute platform. This weakens the 'GPUs remain core infrastructure' thesis and supports a 55-65% mega-deal realization rate rather than 75%."

---

## Response to Risk Analyst's Critique

### 1. ASIC complementarity assumption contradicted by own data — should be time-phased
**Verdict: Accept**

The Risk Analyst provides the most precise formulation of this critique: "GPUs and ASICs are complementary in the short term (next 2-3 years) while ASICs mature, then increasingly substitutional as custom silicon reaches performance parity for inference workloads." I accept this framing and adopt it as a revision to my analysis. The time-phasing is consistent with ASIC development cycles (3-5 years from design to production) and aligns with the mega-deal horizons (5-6 year terms). The implication is that AMD's mega-deal revenue is more secure through 2028-2029 than 2030+, which the Director should factor into the price target derivation.

### 2. AI GPU share Tier 6 source with 50% range (8-12%) — should segment training vs. inference
**Verdict: Accept**

The Risk Analyst's suggestion to segment AI GPU share into training vs. inference is analytically superior to my blended estimate. AMD likely has higher share in inference (where CUDA matters less and cost-per-token matters more — MI355X's "40% more tokens per dollar" is compelling) and lower share in training (where CUDA library depth is critical). I accept this decomposition and will present: "AMD AI GPU share: inference ~12-15% [ESTIMATED], training ~5-8% [ESTIMATED], blended ~8-10%. The inference share is the more relevant metric as inference grows from ~30% to ~60% of compute spend by 2028."

### 3. CUDA Gap Score needs workload decomposition — 28.7-99.1 range is analytically useless as a single metric
**Verdict: Accept**

I accept this critique fully. Presenting a single range of 28.7-99.1 without workload decomposition is imprecise to the point of being misleading. I will decompose into: inference (25-35% gap), single-node training (40-55% gap), multi-node distributed training (65-99% gap), and fine-tuning (30-45% gap). This decomposition reveals that AMD is competitive in the fastest-growing segment (inference) while remaining disadvantaged in the segment with the deepest CUDA lock-in (distributed training) — a more nuanced and actionable competitive picture.

---

## Response to Macro Analyst's Critique

### 1. AI GPU TAM of $200-250B depends on hyperscaler capex continuing at $650B+ — structurally fragile if energy costs rise
**Verdict: Partially Accept**

The Macro Analyst raises a legitimate structural concern: if Hormuz-driven energy cost increases of 20-30% raise data center TCO by 5-10%, hyperscaler ROI calculations worsen and capex plans could slow. I accept that my TAM estimates should incorporate a macro-adjustment factor and present a range that accounts for energy cost inflation scenarios. However, I note two mitigating factors: (1) hyperscaler AI capex is budgeted 12-18 months in advance and is strategic competitive spending that is less elastic to near-term cost fluctuations than discretionary capex; (2) AMD's MI450 actually benefits from energy cost sensitivity if it delivers superior performance-per-watt, as customers would favor the most power-efficient GPU. I will add a macro-adjusted TAM scenario: base TAM of $200-250B assumes stable energy costs; stress TAM of $160-200B assumes 25% energy cost increase reducing hyperscaler capex by 15-20%.

### 2. Competitive score of 6/10 overweights hardware, underweights macro/demand environment — should be cycle-adjusted
**Verdict: Partially Accept**

The Macro Analyst's suggestion for a "macro-adjusted competitive score" is conceptually sound but conflates competitive position with market conditions. AMD's competitive position (product quality, ecosystem, moat) does not change based on the macro cycle — what changes is the demand environment in which that position is expressed. In a strong cycle, a 6/10 competitive position captures more revenue than in a weak cycle, but the underlying moat does not improve. I partially accept: I will add a note that "AMD's competitive position is pro-cyclical — the #2 supplier benefits disproportionately from strong markets and is disproportionately exposed in weak markets. The 6/10 score reflects structural competitive position; the effective competitive score adjusts to ~7/10 in strong markets and ~4-5/10 in cyclical downturns where procurement consolidates with the #1 vendor." This captures the Macro Analyst's insight without conflating structural moat with cyclical demand.

### 3. Energy cost inflation impact on competitive dynamics should be modeled
**Verdict: Accept**

I accept this critique. My analysis did not account for how energy cost inflation changes the competitive dynamic between AMD and NVIDIA. If MI450 delivers better performance-per-watt (AMD claims 50% more memory capacity at comparable power), energy-constrained environments would favor AMD's architecture. Conversely, if total GPU demand contracts due to higher electricity costs, the #2 vendor (AMD) gets cut first. I will add an "energy sensitivity" subsection noting this dual dynamic.

---

## Response to Catalyst Analyst's Critique

### 1. CUDA moat relevance differs by customer segment — less relevant for hyperscale (top 20% of spend), more for enterprise (bottom 80%)
**Verdict: Accept**

This is the most incisive critique of my CUDA analysis. The Catalyst Analyst correctly identifies that OpenAI and Meta — AMD's mega-deal customers — have the engineering resources to optimize ROCm or build abstraction layers. At the infrastructure layer, CUDA's developer ecosystem advantage matters far less than at the enterprise level. I accept this segmentation and revise: "The CUDA moat is structural for enterprise GPU adoption (6M developers, 300+ libraries, 18 years of lock-in) but substantially weakened at the hyperscale level where customers control the software stack. Since AMD's mega-deals concentrate revenue in the hyperscale segment, the effective CUDA constraint on AMD's near-term revenue is lower than the headline gap suggests." This adjustment would support raising the AI GPU competitive sub-score from 5/10 to 5.5-6/10 for the hyperscale-focused business.

### 2. Custom ASIC threat of 60% probability in 3 years is too aggressive — should be time-phased
**Verdict: Accept**

The Catalyst Analyst's recommendation to separate the ASIC threat into time horizons (20% by 2028, 45% by 2029, 60% by 2030) is analytically superior to my static 60% probability. Custom ASICs take 3-5 years from design to production deployment. AMD's mega-deals are structured to deliver GPU volumes before ASICs reach scale, providing a 2-3 year revenue window that my static probability obscured. I revise the ASIC cannibalization assessment to: "20% probability of meaningful GPU substitution by 2028, 40-45% by 2029, 55-60% by 2030."

### 3. Should add a catalyst-driven competitive timeline rather than a static moat assessment
**Verdict: Partially Accept**

The Catalyst Analyst proposes a time-varying competitive score (7-8/10 in Q3-Q4 2026 when MI450 may launch before Vera Rubin scales, declining to 5-6/10 by mid-2027 as Vera Rubin fully deploys). This is directionally correct but overstates AMD's H2 2026 advantage. MI450 launching 3-6 months before Vera Rubin reaches scale provides a narrow window, but hyperscaler procurement cycles are 12-18 months, meaning the orders for that window are already placed. The competitive advantage is real but already priced into existing mega-deal commitments. I accept adding temporal context but with more moderate variation: competitive score of 6.5/10 in H2 2026 (MI450 hardware advantage), returning to 5.5-6/10 by mid-2027 (Vera Rubin parity).

---

## Response to ESG & Governance Analyst's Critique

### 1. Mega-deals are framework agreements, not binding purchase orders — 40% realization if deals are bridge contracts
**Verdict: Partially Accept**

The ESG & Governance Analyst correctly flags that these are framework agreements with complex warrant structures, not binding purchase commitments. The warrant structure does create an incentive dynamic worth examining: once customers vest enough warrants, their incremental incentive to deploy AMD hardware diminishes. However, the warrant vesting is deployment-milestone-based, meaning customers must physically install and operate AMD GPUs to vest — this creates real switching costs and installed-base lock-in. I accept lowering my implied realization assumption from 75% to 60-70% to account for the framework (non-binding) nature of the agreements, but I reject 40% as too aggressive given the deployment-linked vesting structure that creates genuine lock-in.

### 2. Management incentive compensation tied to revenue/EPS, not ROCm ecosystem — misaligned with key competitive variable
**Verdict: Accept**

This is a genuinely novel and important insight. The ESG & Governance Analyst correctly identifies that AMD management's PRSU metrics (revenue, net income, FCF) do not reward closing the CUDA gap, which is the single most important competitive variable. Management is incentivized to sell hardware, not build software ecosystems. I accept this critique and will add: "Management compensation structure creates a structural bias toward hardware-driven revenue growth over software ecosystem investment. The absence of ROCm adoption KPIs in executive compensation is a governance-relevant competitive risk that could perpetuate the CUDA gap." This is a finding I should have identified independently.

### 3. Monopsony risk — two customers with 320M warrants have significant negotiating leverage
**Verdict: Partially Accept**

The ESG & Governance Analyst raises a valid concern about customer concentration and bargaining power inversion. If OpenAI and Meta represent >35% of Data Center revenue and hold $60B+ in equity optionality, AMD's negotiating position weakens. However, the dynamics are more nuanced: AMD is not solely dependent on these two customers. EPYC server CPUs serve thousands of enterprise customers, and the MI350 series is deployed at "8 of 10 top AI companies" beyond just OpenAI and Meta. The monopsony risk is concentrated in the MI450 generation, not across AMD's entire business. I accept adding a "customer concentration risk" dimension to the competitive assessment, noting that MI450-era GPU pricing power is constrained by the mega-deal structure, but I reject reducing the overall competitive score to 5/10 based on this factor alone, as it applies to one product generation within one business segment.

---

## Response to Technical Analyst's Critique

### 1. Price action (-28% from ATH, broken support) suggests CUDA gap is NOT narrowing — market is rejecting the narrative
**Verdict: Reject**

The Technical Analyst interprets the stock's breakdown as evidence that the CUDA gap is not narrowing. Price action is information, but it is not competitive analysis. The post-earnings selloff (-17% on a 23% EPS beat) is more consistent with the market repricing MI450 execution risk, warrant dilution, and macro concerns than with a verdict on CUDA vs. ROCm progress. The Q4 earnings call contained no negative ROCm data; management did not discuss ROCm deterioration. The stock decline coincides with multiple non-CUDA factors: the SemiAnalysis MI450 delay report, the 320M warrant dilution disclosure, and broader semiconductor sector rotation. Using price action to infer competitive dynamics requires isolating the competitive signal from macro, sentiment, and positioning noise — the Technical Analyst has not done this.

### 2. Custom ASIC growth of 44.6% vs. GPU 16.1% not fully integrated — "beat and fade" pattern confirms market sees structural ASIC headwind
**Verdict: Partially Accept**

I accept that my analysis should have integrated the ASIC growth differential more prominently into the competitive narrative. The 44.6% vs. 16.1% gap is a structural trend worth elevating. However, I reject the inference that the "beat and fade" pattern specifically confirms ASIC concerns — the post-earnings selloff had multiple catalysts (warrant dilution, MI455X delay questions, sector rotation) and cannot be attributed to any single competitive factor without options-implied decomposition, which was unavailable due to data gaps.

### 3. Add a "market-revealed competitive assessment" using relative underperformance vs. SOXX and NVDA
**Verdict: Reject**

The suggestion to derive a competitive score from relative stock performance conflates market sentiment with structural competitive position. AMD underperforming SOXX by 18 points over 3 months could reflect competitive concerns, macro positioning, warrant dilution repricing, technical selling, or any combination. Competitive analysis should assess product quality, ecosystem strength, market share trajectory, and structural barriers — not reverse-engineer these from stock price movements. If AMD's stock rises 30% in Q3 2026 on MI450 launch confirmation, it would not mean the CUDA gap suddenly narrowed. Stock prices are useful for checking whether the market agrees with a competitive assessment, but they should not determine the assessment itself.

---

## Response to Sector Analyst's Critique

### 1. Share plateau at 12-15% underweights structural deconcentration dynamics — HHI declining from 9,000 to 6,864
**Verdict: Partially Accept**

The Sector Analyst provides valuable historical context: AMD went from 5% to 28% server CPU unit share in 7 years, and the AI GPU market HHI is declining on the standard deconcentration curve. This is a legitimate argument for continued share gains beyond 15%. However, server CPU share gains occurred in an x86 duopoly with high switching costs — AMD only had to be better than Intel. AI GPU share gains require overcoming NVIDIA's software ecosystem, which is a qualitatively different and harder barrier than Intel's process node disadvantage. I accept that 12-15% plateau is likely too conservative for the base case given the mega-deal structural demand, but I maintain that 20-25% requires ROCm achieving near-parity with CUDA for production workloads, which remains unproven. I revise my base case AI GPU share trajectory to 15-18% by 2030 (up from 12-15%), with 20-25% requiring measurable ROCm ecosystem progress.

### 2. CUDA Gap Score treated as static — should be workload-weighted and projected forward as inference grows
**Verdict: Accept**

The Sector Analyst's insight that inference is growing from ~30% to ~60% of AI compute spend by 2028 — and that the CUDA gap is narrowest for inference — is the strongest rebuttal to a static CUDA moat assessment. As the mix shifts toward inference, the effective CUDA gap narrows even without ROCm improvements. I accept this framework and will add: "Workload-weighted CUDA gap (2025): ~55% (30% inference at 28.7 gap + 70% training at 65+ gap). Projected workload-weighted CUDA gap (2028): ~38% (60% inference at 25-30% gap + 40% training at 55-65% gap). The inference mix shift is a structural tailwind for AMD's competitive position that narrows the effective CUDA gap by ~15-20 percentage points over 3 years regardless of ROCm software improvements."

### 3. "Second source" procurement dynamics set AMD's share floor at 15-20% — not a product competitiveness question
**Verdict: Partially Accept**

The Sector Analyst reframes AMD's competitive position as supply chain diversification rather than product superiority — hyperscalers choose AMD not because it is better but because NVIDIA monopoly pricing is unacceptable. This is a powerful insight that explains the mega-deals better than my product-focused analysis. I accept that the structural second-source minimum sets a higher share floor (15-20%) than my competitive analysis implied (10-12%). However, second-source dynamics have limits: if the CUDA gap makes AMD GPUs substantially less productive, the cost of second-sourcing (lower throughput, higher engineering overhead) eventually exceeds the benefit (pricing leverage on NVIDIA). The floor exists but is not guaranteed to hold if the productivity gap widens.

---

## Response to Devil's Advocate's Critique

### 1. ASIC complementarity assumption is the "load-bearing pillar" — own data contradicts it
**Verdict: Partially Accept**

The Devil's Advocate provides the most aggressive version of the ASIC substitution argument, noting that inference constitutes 60-80% of compute demand and is the workload most amenable to ASIC optimization. If ASICs capture inference while GPUs retain only training and flexible compute, AMD's addressable TAM contracts by 40-50%. I accept that the substitution risk is higher than my Pass 1 analysis implied, and I revise the ASIC threat assessment upward. However, I note that ASIC optimization for inference requires workload-specific design — Google's TPU is optimized for TensorFlow, Amazon's Trainium for JAX/XLA. These are not general-purpose inference accelerators, and each hyperscaler's ASIC serves only its own workloads. AMD's GPUs offer flexibility across workloads and customers that ASICs cannot match. The substitution is real for high-volume, stable-workload inference but limited for diverse, evolving inference demands. I revise ASIC cannibalization of GPU inference to 25-35% by 2030 (up from implied 10-15%).

### 2. AI GPU share gain trajectory assumes linear growth — should model plateau or decline after mega-deal deployments
**Verdict: Partially Accept**

The Devil's Advocate correctly notes that semiconductor share gains follow S-curves, not linear trajectories. The mega-deals provide a one-time share boost that could represent a peak rather than a base. I accept adding a "share plateau" scenario where AMD GPU share peaks at 14-16% in 2027-2028 (post-mega-deal deployment) then stabilizes or declines to 12-14% by 2030 as ASIC substitution and CUDA stickiness limit further gains. However, I reject the implied probability weighting: this plateau scenario should be the bear case (25-30% probability), not the base case, given that the structural deconcentration dynamics and second-source procurement incentives both support continued gains.

### 3. Revenue-weighted competitive score should be 5.5/10, not 6/10
**Verdict: Partially Accept**

As addressed in the DCF Analyst response above, I accept that a revenue-weighted score at FY2030 mix converges toward 5.5/10. I will present both the simple average (6/10) and the FY2030 revenue-weighted score (5.5/10), with the revenue-weighted version flagged as more relevant for equity valuation. The core message — that AMD's most valuable business has its least defensible moat — is correct and should be elevated in the final research note.

---

## Response to Forensic Analyst's Critique

### 1. AI GPU share of ~8-12% from TechNetBooks (Tier 6) — unverifiable since AMD refuses to disclose Instinct GPU revenue
**Verdict: Accept**

The Forensic Analyst raises the most fundamental version of this critique: the core competitive thesis rests on a metric (AI GPU market share) that is unverifiable because AMD does not disclose GPU-specific revenue. I accept this critique fully and will add a prominent caveat: "AMD's AI GPU market share cannot be independently verified from Tier 1 sources. All share estimates are reverse-engineered from partial data (AMD total Data Center revenue minus estimated EPYC CPU revenue) against third-party TAM estimates (Tier 3-6). The Director should weight this analysis with reduced confidence accordingly." This is an honest limitation that I should have flagged more prominently in Pass 1.

### 2. CUDA Gap Score of 28.7-99.1 presented with false precision — qualitative statement dressed in numbers
**Verdict: Partially Accept**

The Forensic Analyst's characterization — "a qualitative statement dressed in numbers" — is harsh but partly fair. A Tier 6 sourced range spanning 3.5x is not precision measurement. However, I reject the suggestion to present the CUDA gap as purely qualitative. The benchmark numbers, even from Tier 6, provide a useful order-of-magnitude framework: AMD is not at parity (gap is not 0-10%) and not completely uncompetitive (gap is not 100%+). The range establishes that AMD faces a material but not insurmountable software disadvantage. I will qualify the presentation: "CUDA Gap Score: 28.7-99.1 across benchmarks [Tier 6, AIM Multiple, date uncertain, wide confidence interval]. Directional interpretation: AMD faces a significant software performance disadvantage in CUDA-optimized workloads, narrowing to modest disadvantage in inference-optimized workloads. Precise quantification requires updated, workload-specific benchmarking."

### 3. Flag that AI GPU competitive assessment is built almost entirely on Tier 3-6 data
**Verdict: Accept**

This is a fair and important procedural critique. The AI GPU competitive assessment — which is the most consequential section of my analysis — relies on no Tier 1 data for market share, GPU-specific revenue, or GPU-specific margins. I accept this and will add: "DATA QUALITY NOTE: The AI GPU competitive assessment (Sections 2, 5, and 7) is built primarily on Tier 3-6 data. No Tier 1 source is available for AMD's GPU market share, GPU-specific revenue, or GPU-specific margins. This represents an asymmetric information environment that favors AMD management over investors. The Director should calibrate conviction accordingly."

---

## Response to Sentiment Analyst's Critique

### 1. CUDA gap narrowing thesis contradicted by management silence on ROCm — hardware confidence, software silence is a negative signal
**Verdict: Accept**

The Sentiment Analyst provides the most compelling behavioral evidence against CUDA gap narrowing: not a single analyst on the Q4 earnings call asked about ROCm, and management never proactively discussed ROCm progress. Lisa Su's competitive framing focused exclusively on hardware specs (MI450 memory, MI355X benchmarks) while avoiding any software discussion. This asymmetry — hardware confidence, software silence — is indeed a negative signal. If ROCm were achieving meaningful gains, management would highlight it as validation of their software investment. I accept this critique and add: "Management's silence on ROCm progress during Q4 2025 earnings is a notable behavioral signal. The absence of proactive software ecosystem updates, combined with hardware-only competitive framing, suggests ROCm improvements may be incremental rather than transformational. This supports maintaining the AI GPU moat at 5/10 rather than upgrading it."

### 2. AI GPU share Tier 6, management deflection on GPU specifics — "if the story were as strong, they'd disclose"
**Verdict: Partially Accept**

The Sentiment Analyst's inference — that management's refusal to disclose Instinct GPU revenue implies the GPU-specific numbers are less compelling than the blended Data Center figure — is plausible but not the only explanation. Competitive intelligence protection is a legitimate reason for non-disclosure, particularly when AMD is negotiating additional mega-deals and does not want to reveal pricing power or concentration metrics. I accept broadening the GPU share range to 6-12% (from 8-12%) to reflect the additional uncertainty from management opacity, and I will present the non-disclosure as a "neutral to negative" signal rather than assuming competitive motivation alone.

### 3. Add management communication analysis on competitive positioning — track what Su says vs. does not say about NVIDIA
**Verdict: Accept**

The Sentiment Analyst's observation that Lisa Su references "our competitor" having "some issues" but never claims AMD products are superior on a system-level basis is a valuable behavioral insight. Management citing competitor weaknesses while avoiding head-to-head comparisons is consistent with a #2 player that knows it cannot win the aggregate comparison. I accept adding this management communication lens to the competitive assessment as a qualitative cross-check on the hardware benchmark data.

---

## Response to Credit Analyst's Critique

### 1. AI GPU share plateau at 12-15% ignores AMD's financial capacity to invest — $13.6B liquidity and $6.7B FCF enable aggressive ROCm investment
**Verdict: Partially Accept**

The Credit Analyst makes an important point: AMD's balance sheet provides the financial capacity to invest aggressively in closing the CUDA gap. NVIDIA's software moat was built over 18 years of cumulative R&D; AMD has the resources to compress that timeline. However, financial capacity and execution capability are different constraints. AMD has had the financial resources to invest in ROCm for 5+ years and the gap remains wide. The constraint is not capital but engineering talent, ecosystem network effects, and the chicken-and-egg problem of developer adoption. I accept adding a "financial moat" dimension noting AMD's balance sheet as a competitive asset, but I maintain that financial capacity alone does not guarantee moat-building and should not raise the competitive score without evidence of accelerating ROCm adoption.

### 2. CUDA Gap Score from Tier 6 with 3.5x range is noise — mega-deals are first-party evidence of manageable gap
**Verdict: Partially Accept**

The Credit Analyst makes a strong point: if the CUDA gap were truly 99%, sophisticated customers like OpenAI and Meta would not commit 12 GW to AMD infrastructure. The mega-deals are revealed preference evidence that the CUDA gap is manageable for hyperscale workloads. I accept this as a valuable corroborating data point and will note: "The OpenAI and Meta mega-deals constitute first-party evidence (Tier 1) that the CUDA gap is manageable for hyperscale AI workloads, partially validating the lower end of the 28.7-99.1 range. This revealed preference should be weighted more heavily than third-party benchmarks for assessing the AI GPU competitive position at the hyperscale tier." However, I note that the mega-deals include substantial equity inducements ($0.01 warrants for 320M shares), which means the purchasing decision reflects both product competitiveness and financial incentives — the deals do not prove CUDA parity.

### 3. Add a "financial moat" dimension — balance sheet as competitive weapon
**Verdict: Partially Accept**

The Credit Analyst proposes adding a balance sheet dimension to the competitive framework. AMD's warrant-backed mega-deals are indeed a balance-sheet-enabled competitive strategy that Intel (with $50B debt) and Broadcom (with $70B debt) cannot easily replicate. I accept adding a financial capacity note to the competitive assessment but will not incorporate it into the moat scoring framework, as financial resources are an enabling factor rather than a structural competitive advantage. A company with a strong balance sheet but weak products still loses to a company with great products and moderate finances.

---

## Summary of Revisions

| Item | Original | Revised | Impact |
|------|----------|---------|--------|
| Overall Competitive Score | 6/10 (static) | 6/10 simple average; 5.5/10 FY2030 revenue-weighted | More nuanced signal |
| AI GPU Moat | 5/10 (static) | 5/10 overall, 5.5-6/10 for hyperscale segment | Segmented assessment |
| CUDA Gap Score | 28.7-99.1 (undifferentiated) | Inference: 25-35%; Training: 55-80%; Workload-weighted: ~55% (2025), ~38% (2028) | Actionable decomposition |
| AI GPU Share | ~8-12% (Tier 6) | ~8-10% blended; inference ~12-15%, training ~5-8% | Narrower, segmented, better sourced |
| ASIC Substitution Timeline | 60% probability in 3 years (static) | 20% by 2028, 40-45% by 2029, 55-60% by 2030 | Time-phased risk |
| Mega-deal Realization | Implied 75% | Revised to 60-70% base case | Lower revenue assumption |
| ASIC Complementarity | Medium confidence | Medium-low; complementary through 2028, partially substitutional 2029+ | Time-dependent |
| Data Quality Flag | Not prominently flagged | Explicit note that AI GPU assessment relies on Tier 3-6 data | Honest limitation |
| Management Comp Misalignment | Not addressed | Flagged: no ROCm KPIs in executive compensation | New governance-relevant finding |
| Customer Concentration Risk | Not addressed | Added: mega-deal structure constrains MI450 pricing power | New risk dimension |

The overall competitive score of 6/10 survives the adversarial review, though the supporting analysis is substantially more nuanced. The most important revisions are: (1) the CUDA gap is workload-dependent and narrowing on a weighted basis as inference grows; (2) ASIC substitution risk is real but time-phased, with AMD's mega-deal revenue window preceding ASIC maturity; (3) the analysis rests on Tier 3-6 data with no independently verifiable GPU-specific financials, which should reduce conviction; and (4) management compensation structure does not incentivize closing the CUDA gap, a governance-relevant competitive risk. The fundamental conclusion — AMD holds a strong position in server CPUs with a narrow and unproven moat in AI GPUs — is reinforced by the adversarial process.

---

*Rebuttals by Competitive Analyst, Equity Research Swarm. Pass 2 adversarial review.*
