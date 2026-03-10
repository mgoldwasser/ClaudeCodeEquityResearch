# Pass 2 Cross-Critiques — Catalyst Analyst
**Date:** 2026-03-09
**Reviewing Analyst:** Catalyst Analyst
**Subject:** Advanced Micro Devices, Inc. (AMD)

---

## Critique of DCF Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** "MI450 production H2 2026 with ~1 quarter delay" used as the base case timing assumption.

**Why it's weak:** The DCF base case bakes in a one-quarter delay as the central scenario, but the catalyst evidence is more nuanced. AMD management has repeatedly confirmed on-track for H2 2026, Oracle's 50,000-GPU supercluster deployment is scheduled for Q3 2026, and three separate mega-deal customers have committed to H2 2026 timelines. The SemiAnalysis delay report (mass production Q2 2027) was explicitly denied by AMD as "BS." A one-quarter delay is neither the most probable outcome (on-time is more likely at ~45%) nor the bear case (full delay to 2027 at ~25%). It sits in an awkward middle ground that may systematically undervalue the base case.

**Quantified impact if wrong:** If MI450 ships on-time in Q3 2026 (no delay), FY2026 data center revenue would be $2-3B higher than the delayed scenario, adding approximately $15-20/share to the base case DCF value, moving it from $154.58 to ~$170-175.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** WACC of 16.0% using beta of 2.02 as a static input.

**Why this is the most likely error:** Beta is a backward-looking measure that includes AMD's pre-AI-pivot volatility. As AMD's revenue mix shifts toward recurring enterprise data center contracts (OpenAI, Meta, Oracle deployments with multi-year horizons), the business model stabilizes. By H2 2026 — when key catalysts resolve — AMD's beta should compress toward 1.5-1.7x as revenue visibility improves with confirmed hyperscaler deployments. Using a trailing beta of 2.02 to discount cash flows that increasingly depend on contracted revenue overstates the discount rate by 150-250bps.

**Suggested correction:** Model WACC as declining over the projection period: 16% in FY2026, 14.5% in FY2027-28, 13% in FY2029-30 as business mix matures. Or use a blended WACC of ~14% that reflects the forward-looking revenue composition. At 14% WACC, the base case fair value rises from $154.58 to approximately $190-200.

**Severity: High**

---

### 3. Recommended Change

**What I'd change:** The 25/50/25 probability weighting across bull/base/bear scenarios.

**Why:** The catalyst calendar shows an overwhelmingly positive setup for H2 2026 — MI450 ramp, three confirmed mega-deal deployments, EPYC Venice launch — with management on record confirming timelines. The bear case requires multiple simultaneous failures (MI450 delay + NVIDIA outperformance + ASIC cannibalization). I would assign 30/45/25 or even 30/50/20, reflecting that the near-term catalyst pipeline is more favorable than a symmetric distribution implies. The Q4 2025 beat-and-raise cadence, combined with the breadth of confirmed customer commitments, reduces the probability of the full bear case.

**Impact on conclusion:** Shifting to 30/45/25 would raise the probability-weighted fair value from $154.07 to approximately $167-172, narrowing the overvaluation gap from -19.1% to roughly -10 to -12%.

**Severity: Medium**

---

### 4. What's Strong

The terminal value sensitivity analysis and the warrant dilution modeling are excellent — the "tax on success" framework correctly identifies that bull case appreciation is partially offset by dilution, which most sell-side models miss.

---

## Critique of Quant Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** "Comp set of 6 companies is adequate despite AMD's rapid business mix evolution."

**Why it's weak:** AMD's business is undergoing a structural transformation — data center revenue grew 94% in FY2025 and now represents 50%+ of total revenue. By H2 2026, when MI450 ramps, data center could be 60-65% of revenue. A static comp set drawn from today's semi universe fails to capture that AMD is becoming a different company with each passing quarter. The relevant comps for the AI GPU business are not traditional semi companies but potentially cloud infrastructure providers or specialized AI hardware companies. Using today's comps to value a company whose business mix will look materially different in 12 months creates a structural mismatch.

**Quantified impact if wrong:** If AMD's forward revenue mix justifies comparison to higher-growth AI infrastructure peers rather than broad-based semis, the appropriate P/E could be 32-35x rather than 27.8x, implying fair value of $213-$233 versus the $205 central estimate — a 4-14% undervaluation.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** Quality score of 29.0/100 based on current ROIC (6.6%) and EBITDA margin (27.2%).

**Why this is the most likely error:** These metrics are backward-looking and reflect Xilinx acquisition goodwill drag on ROIC and the pre-MI450 margin profile. The catalyst timeline shows that H2 2026 brings higher-margin AI GPU revenue at scale (MI450 ASPs likely $20,000-40,000+). EBITDA margins should expand toward 35%+ as GPU mix increases. Scoring AMD's quality on trailing metrics when the single most important catalyst (MI450 ramp) is 6 months away systematically penalizes a company at an inflection point.

**Suggested correction:** Run a forward quality score using consensus FY2027 estimates (post-MI450 ramp) alongside the trailing score. Present both to show the trajectory, not just the snapshot.

**Severity: Medium**

---

### 3. Recommended Change

**What I'd change:** Include a time-adjusted valuation framework that accounts for catalyst timing.

**Why:** The comps analysis is static — it values AMD today. But the catalyst calendar shows that 70%+ of AMD's value creation is concentrated in Q3-Q4 2026. A 6-month forward comp analysis (valuing AMD at expected H2 2026 run rates) would provide a more relevant anchor. The current analysis correctly identifies AMD as fairly valued today but does not account for the impending catalyst density.

**Impact on conclusion:** A forward-looking comp analysis using H2 2026 run-rate metrics could shift the central estimate from $205 to $220-240, changing the conclusion from "modestly undervalued" to "meaningfully undervalued on a 6-12 month basis."

**Severity: Medium**

---

### 4. What's Strong

The PEG ratio analysis (0.51x vs. 1.16x median) is the most compelling quantitative signal in the entire comp framework — it correctly identifies that AMD's growth rate is dramatically underpriced relative to peers.

---

## Critique of Competitive Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** "NVIDIA's CUDA moat (6M developers, 300+ libraries, 18 years) can be narrowed by ROCm + Triton/MLIR abstraction" rated at [confidence: low].

**Why it's weak:** The competitive analysis treats the CUDA gap as a monolithic barrier, but the catalyst timeline reveals that the nature of GPU competition is shifting. The mega-deals with OpenAI, Meta, and Oracle are infrastructure-scale deployments where the software stack is controlled by the customer, not the GPU vendor. OpenAI and Meta have the engineering resources to optimize ROCm or build abstraction layers. At the hyperscale infrastructure layer, CUDA's developer ecosystem advantage matters far less than it does for enterprise adoption. The CUDA moat is real for the bottom 80% of the market but largely irrelevant for the top 20% of spend — which is where AMD's mega-deals are concentrated.

**Quantified impact if wrong:** If CUDA's relevance is diminished for hyperscale customers (representing 60%+ of AMD's AI GPU TAM by 2027), the competitive score should be 7/10, not 6/10, and the AI GPU share ceiling rises from 15-20% to 20-25%, adding $15-25/share to the bull case.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** Custom ASIC cannibalization threat rated at "60% probability in 3 years."

**Why this is the most likely error:** The 60% probability does not account for timing. Custom ASICs take 3-5 years from design to production deployment. OpenAI's Broadcom ASIC deal was announced but first production is unlikely before 2028-2029. AMD's mega-deals are structured with 5-6 year horizons that overlap with ASIC maturation timelines, but the GPU volumes come first. The more likely dynamic is sequential (GPUs now, ASICs later for specific workloads) rather than simultaneous substitution. A 60% probability of material cannibalization within 3 years is too aggressive given ASIC development cycles.

**Suggested correction:** Separate the ASIC threat into time horizons: 20% probability of meaningful cannibalization by 2028, 45% by 2029, 60% by 2030. This changes the investment calculus because AMD's mega-deal revenue peaks in 2027-2028, potentially before ASICs are ready at scale.

**Severity: Medium**

---

### 3. Recommended Change

**What I'd change:** Add a catalyst-driven competitive timeline rather than a static moat assessment.

**Why:** Competition is dynamic, not static. AMD's competitive position in Q3 2026 (when MI450 launches before Vera Rubin reaches scale) is materially different from its position in Q1 2027 (when Vera Rubin is fully deployed). The moat analysis should map competitive advantage windows to specific catalyst dates. Right now, the analysis concludes "6/10" as if competitive position is fixed, when in reality AMD has a 3-6 month window of potential hardware advantage in H2 2026.

**Impact on conclusion:** A time-varying competitive score (7-8/10 in Q3-Q4 2026, declining to 5-6/10 by mid-2027 as Vera Rubin scales) would more accurately reflect the investment opportunity and align with the phased entry strategy I recommended.

**Severity: Medium**

---

### 4. What's Strong

The identification of the "dual squeeze" (NVIDIA CUDA from above, custom ASICs from below) is the most important competitive insight — it correctly frames AMD's AI GPU position as structurally time-limited.

---

## Critique of Macro Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** "AI capex-to-revenue ratio: 25-28:1 ($660B+ capex vs. ~$25B AI revenue) — 6-7x more speculative than telecom bubble."

**Why it's weak:** The telecom bubble comparison is misleading because the revenue denominator is measured differently. The $25B "AI revenue" figure appears to capture only direct AI-specific SaaS revenue, excluding the productivity gains, cost savings, and revenue enablement that AI capex supports. If you include AI-enabled cloud revenue, enterprise automation savings, and AI-enhanced product revenues, the effective return on AI capex is considerably higher. The telecom bubble comparison also ignores that telecom capex was building physical infrastructure with 20-year depreciation cycles, while AI GPU capex depreciates in 3-5 years — the payback window is structurally different.

**Quantified impact if wrong:** If the relevant capex-to-revenue ratio is 8-12:1 (including AI-enabled revenues) rather than 25-28:1, the AI spending cycle sustainability extends 2-3 years beyond the macro analyst's timeline, pushing peak risk from 2027-2028 to 2029-2030. This gives AMD's mega-deals time to fully ramp, adding 20-30% to the bull case probability.

**Severity: High**

---

### 2. Most Likely Source of Error

**Error source identified:** Hormuz crisis impact on AMD specifically.

**Why this is the most likely error:** The macro analysis models Hormuz crisis through oil prices and rate cut delays, but AMD's direct exposure is minimal — AMD is fabless (TSMC fabricates in Taiwan, not the Middle East), AMD's customers are US hyperscalers with fixed procurement budgets, and AI capex is not discretionary (it's strategic competitive spending). The primary transmission mechanism (higher rates = lower growth multiples) is real but second-order. The macro analyst correctly identifies beta of 2.02 but does not distinguish between AMD-specific risk and systematic market risk. A Hormuz crisis hurts AMD only through broad market contagion, not through any business fundamental.

**Suggested correction:** Separate the Hormuz impact into direct (near zero for AMD) and indirect (beta-driven market contagion), and weight accordingly. The net AMD-specific Hormuz impact is probably -2-4%, not the implied -8-15%.

**Severity: Medium**

---

### 3. Recommended Change

**What I'd change:** The catastrophic scenario probability of 10-12%.

**Why:** The "AI Winter + Stagflation" catastrophic scenario requires simultaneous occurrence of: (1) hyperscaler capex reversal despite committed multi-year contracts, (2) macroeconomic recession, and (3) geopolitical escalation. The probability of all three happening in the same 12-month window is the product of their individual probabilities, not their sum. Using joint probability analysis: if each has 20-25% individual probability, the joint probability is 1-3%, not 10-12%. The macro analyst is conflating individual risk probabilities with joint scenario probability.

**Impact on conclusion:** Reducing catastrophic scenario from 10% to 3% would raise the macro-adjusted fair value from ~$190 to ~$200-205, shifting the conclusion from "flat to current" to "modestly undervalued."

**Severity: Medium**

---

### 4. What's Strong

The quantified macro sensitivity framework — mapping each macro factor to specific EPS and multiple impact — is rigorous and actionable. The rate sensitivity analysis (each delayed Fed cut = 0.5-1.0x P/E compression) is directly useful for trade timing.

---

## Critique of Risk Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** "MI450 material delay probability: 20-25% based on industry precedent for new node ramps."

**Why it's weak:** The "industry precedent" baseline treats AMD's MI450 ramp as a generic semiconductor product launch. But MI450 has three specific de-risking factors that generic precedent does not capture: (1) TSMC's N3 process is already in volume production for other customers (Apple, etc.), so this is not a bleeding-edge node bring-up; (2) AMD has pre-committed customers with contracted volumes, reducing demand uncertainty; (3) AMD's Helios rack-scale architecture was publicly demonstrated and confirmed on-track at CES 2026 and the Morgan Stanley conference (March 3, 2026). A 20-25% delay probability should be adjusted down to 15-20% given these AMD-specific factors.

**Quantified impact if wrong:** Reducing delay probability from 25% to 15% shifts $10B in expected risk-adjusted revenue back to base/bull cases, increasing the expected value from $210 to approximately $220-225.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** "Correlation to SPX rises to 0.85+ in selloffs (asymmetric beta — realized beta 2.4x in 2022)."

**Why this is the most likely error:** The 2022 correlation spike reflected a pure macro event (rate shock) hitting all growth stocks. AMD's current business profile is materially different from 2022 — data center revenue was $6.0B in FY2022 vs. $16.6B in FY2025, and AMD now has $200B+ in contracted mega-deal pipeline. In a selloff driven by macro factors unrelated to AI (e.g., recession fears), AMD's contracted revenue base would provide a fundamental floor that did not exist in 2022. Using 2022 as the analog overstates drawdown risk in scenarios where AI spending remains robust.

**Suggested correction:** Model two drawdown scenarios: macro-driven (where contracted revenue provides a floor, limiting drawdown to -25-35%) and AI-specific (where the contracted revenue itself is at risk, allowing -45-55% drawdown). The blended expected max drawdown would be lower than the current -45 to -55% estimate.

**Severity: Medium**

---

### 3. Recommended Change

**What I'd change:** The Sharpe ratio of 0.19 used to characterize risk-adjusted return.

**Why:** A static Sharpe ratio does not capture the time-varying nature of AMD's risk/reward profile. Pre-catalyst (now through Q2 2026), the Sharpe ratio is indeed poor because the stock has downside exposure without near-term positive catalysts. Post-catalyst (Q3 2026 onward), if MI450 ramp confirms, the Sharpe ratio improves dramatically as uncertainty resolves and the denominator (volatility) compresses. A phased entry strategy can capture a much higher realized Sharpe than the static 0.19 implies. The risk analysis should present time-conditional Sharpe ratios to guide entry timing.

**Impact on conclusion:** A time-varying Sharpe analysis would support the conclusion that timing (entering post-MI450 confirmation in Q3 2026) is more important than sizing, which changes the risk management recommendation from "cap position size" to "phase position entry around catalysts."

**Severity: Medium**

---

### 4. What's Strong

The breakeven bear probability analysis (41% current vs. 25% assessed) is the single most useful risk metric — it quantifies exactly how much bear case probability the market can absorb before the position becomes negative expected value.

---

## Critique of Credit Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** "$875M Sep 2026 maturity will likely be repaid from cash (refinancing unnecessary)."

**Why it's weak:** The assumption is correct in isolation, but it ignores the catalyst-driven capital deployment question. If MI450 ramp succeeds in Q3 2026, AMD may choose to refinance (not repay) to preserve cash for accelerated capacity investments, potential M&A to fill software gaps (ROCm ecosystem acquisitions), or expanded CoWoS packaging commitments with TSMC. The credit analyst treats the $875M maturity as a debt management question when it is actually a capital allocation question driven by catalyst outcomes.

**Quantified impact if wrong:** This is a low-impact critique — whether AMD repays or refinances $875M is immaterial to the equity thesis given $13.6B liquidity.

**Severity: Low**

---

### 2. Most Likely Source of Error

**Error source identified:** The $8.5B FY2026 TSMC purchase commitment characterized as a "hidden liquidity risk."

**Why this is the most likely error:** The purchase commitment is not "hidden" — it is the cost of doing business as the #2 AI GPU supplier. More importantly, the risk is asymmetric: if AMD needs to honor the full $8.5B, it means demand is strong enough to sell the output, which is the bull case. If demand collapses and AMD is stuck with take-or-pay obligations, the real problem is not the $2-4B cash consumption (manageable from $13.6B liquidity) but the 40-60% stock price decline from revenue implosion. The credit analysis overweights the balance sheet risk relative to the income statement risk.

**Suggested correction:** Frame the TSMC commitment as a call option on demand rather than a liquidity risk. AMD pays $8.5B for the right to produce GPUs that generate $15-25B in revenue. The breakeven utilization rate is approximately 50-60%.

**Severity: Low**

---

### 3. Recommended Change

**What I'd change:** Add a catalyst-conditional capital allocation analysis.

**Why:** The credit analysis is a static snapshot of a strong balance sheet. But AMD's capital allocation will change dramatically based on catalyst outcomes. If MI450 succeeds: AMD likely deploys $5-10B into capacity expansion, M&A, or aggressive buybacks. If MI450 struggles: AMD conserves cash and the fortress balance sheet becomes a survival tool. The credit analysis should present two capital allocation paths aligned with the catalyst timeline.

**Impact on conclusion:** Would not change the "credit is a strength" conclusion but would make it more useful for the investment thesis by showing how balance sheet strength enables catalyst exploitation.

**Severity: Low**

---

### 4. What's Strong

The credit analysis correctly identifies that credit risk is not the binding constraint for AMD — any AMD investment failure will be an execution or competitive failure, not a credit event. This is an important baseline for position sizing.

---

## Critique of Devil's Advocate's Work Product

### 1. Weakest Assumption

**Assumption identified:** "Mega-deals are bridge contracts, not durable demand — OpenAI's Broadcom deal is 67% larger."

**Why it's weak:** The "bridge contract" thesis assumes OpenAI and Meta are using AMD GPUs temporarily while custom ASICs mature. But the catalyst evidence contradicts this: (1) the warrant structure with 5-6 year vesting horizons and $600 stock price milestones implies long-term partnership, not bridge purchasing — you do not give 160M warrants each to a temporary supplier; (2) OpenAI's Broadcom ASIC deal is for different workloads (inference optimization) than the AMD GPU deal (training and flexible compute); (3) Meta's custom MI450 variant implies deep co-engineering, not arms-length bridge procurement. The DA correctly identifies ASIC competition as a risk but overstates the "bridge contract" probability.

**Quantified impact if wrong:** If mega-deals are durable (5+ year partnerships with 70%+ realization) rather than bridge contracts (3-year transition with 40% realization), the revenue difference is $30-50B cumulative over 5 years. This changes the DA bear case from $80 to $120-140, and shifts the DA-adjusted EV from $178 (-6.5%) to $195-205 (+2.5 to +7.7%).

**Severity: High**

---

### 2. Most Likely Source of Error

**Error source identified:** DA-adjusted bear probability of 30-35% vs. consensus 15-20%.

**Why this is the most likely error:** The DA assigns 30-35% bear probability but does not adequately weight the near-term catalyst de-risking events. Each confirmed deployment (Oracle Q3 2026, OpenAI initial deployment H2 2026, Meta initial deployment H2 2026) reduces the bear probability by 5-8pp. By Q4 2026, after 2-3 deployment confirmations, the bear probability should decline to 15-20% — the DA's current estimate may be appropriate for today but is too static to project forward. A time-varying bear probability would show the thesis strengthening as catalysts confirm.

**Suggested correction:** Model bear probability as declining from 30% today to 20% by Q4 2026 (if deployments confirm) or rising to 40%+ (if deployments fail). The expected value shifts materially depending on which path materializes in the next 6 months.

**Severity: Medium**

---

### 3. Recommended Change

**What I'd change:** The pre-mortem price of $80 by March 2028.

**Why:** The $80 pre-mortem requires mega-deal failure + AI capex correction + multiple compression. But even in a scenario where mega-deals partially fail (50% realization), AMD still has a $16.6B data center business growing 20%+ organically, EPYC server CPU share approaching 50%, and $10.5B in cash. At $80, AMD would trade at approximately 12x trailing earnings on a business generating $6B+ FCF — a valuation that implies permanent impairment, not cyclical disappointment. The more realistic bear floor is $120-140 (18-22x trailing earnings), which is still a devastating outcome but more consistent with AMD's non-AI business fundamentals.

**Impact on conclusion:** A bear case of $120-140 instead of $80 raises the DA-adjusted expected value from $178 to $192-200, flipping the conclusion from negative EV to roughly neutral.

**Severity: High**

---

### 4. What's Strong

The fragility score framework (4.2/5) is a genuinely useful construct — it correctly identifies that the AMD thesis depends on multiple assumptions holding simultaneously, which is a legitimate structural vulnerability even if individual probabilities are favorable.

---

## Critique of ESG & Governance Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** "320M warrant shares issued to OpenAI and Meta at $0.01/share without shareholder approval" — the framing implies this is a governance failure.

**Why it's weak:** The warrant issuance is not a governance failure in isolation — it is a commercially rational decision to secure $200B+ in potential lifetime revenue from the two most important AI customers. The cost (potential 20% dilution at $600/share) is acceptable if the mega-deals realize even 30-40% of their potential value. From a catalyst perspective, the warrant structure actually aligns incentives: customers vest warrants only on deployment milestones and stock price targets, meaning dilution only occurs when AMD is winning. This is a feature, not a bug, of the deal structure.

**Quantified impact if wrong:** If the warrant structure is value-accretive net of dilution (mega-deal NPV exceeds dilution cost), then the 9.3% expected dilution should be treated as a cost of revenue, not a governance penalty. The ESG WACC adjustment of +10-15bps would be unnecessary, saving approximately $3-5/share in DCF valuation.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** Expected dilution of 9.3% uses probabilities (30% no vest / 45% half vest / 25% full vest) that do not account for catalyst timing.

**Why this is the most likely error:** The vesting probabilities are static, but the catalyst calendar creates a clear sequencing: deployment milestones must be achieved before stock price milestones. If MI450 ships on-time and initial deployments confirm in H2 2026, partial vesting probability rises from 45% to 60-70%. If MI450 is delayed, partial vesting drops to 20-30%. The ESG analyst should condition vesting probabilities on catalyst outcomes rather than using unconditional probabilities.

**Suggested correction:** Present two dilution scenarios: (1) MI450 succeeds, expected dilution 12-14%; (2) MI450 fails, expected dilution 3-5%. The unconditional 9.3% obscures the decision-relevant analysis.

**Severity: Low**

---

### 3. Recommended Change

**What I'd change:** Contextualize the warrant issuance against industry precedent for large customer acquisition costs.

**Why:** Cloud and enterprise companies routinely spend 20-40% of contract value on customer acquisition. AMD is effectively spending ~$60B in equity (at full vesting, 320M shares x ~$190) to secure ~$200B in potential revenue — a 30% customer acquisition cost. This is expensive but not unprecedented. Without this context, the analysis reads as pure governance criticism rather than business strategy evaluation.

**Impact on conclusion:** Would soften the governance concern from "critical issue" to "expensive but commercially justified" and potentially raise the governance score from 7/10 to 7.5/10.

**Severity: Low**

---

### 4. What's Strong

The probability-weighted dilution calculation (9.3% expected) is a genuinely useful framework that other analysts should adopt rather than using binary "fully diluted" or "undiluted" share counts.

---

## Critique of Forensic Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** "$306M Q4 inventory reserve release inflated Q4 GM by ~300bps (57% headline vs. ~54% underlying)."

**Why it's weak:** The forensic analysis flags this as a concern, but the catalyst context explains the reserve release: AMD took the original charge in Q2 2025 related to China export control inventory write-downs. The Q4 2025 release occurred after MI308 received export approval with a 15% licensing fee. This is a legitimate reversal of a legitimate charge, not earnings manipulation. Management guided Q1 2026 gross margin at 55%, which is between the "inflated" 57% and the "underlying" 54%, suggesting the true run rate is normalizing toward 55% — consistent with mix shift toward higher-margin data center revenue.

**Quantified impact if wrong:** If the 55% GM guidance is the real run-rate (not 54% "underlying"), then the forensic analyst is understating normalized margins by ~100bps, which at $40B+ revenue equals ~$400M in EBITDA, or approximately $2-3/share in DCF value.

**Severity: Low**

---

### 2. Most Likely Source of Error

**Error source identified:** "Segment restructuring (Client + Gaming combined) reduces visibility into declining gaming business."

**Why this is the most likely error:** The forensic analyst flags the Client + Gaming combination as reducing visibility, but the catalyst-relevant question is whether this matters for the investment thesis. Gaming is now <5% of revenue and declining. The segment combination is cosmetic — it does not hide anything material to the thesis, which is entirely about Data Center (50%+ of revenue) and Embedded (recovery trajectory). Flagging this as a forensic concern overstates its significance relative to the real forensic question: why does AMD not break out Instinct GPU revenue from the Data Center segment?

**Suggested correction:** De-emphasize the Client + Gaming segment restructuring and elevate the Instinct GPU revenue opacity as the primary forensic concern. The GPU revenue question directly affects whether the mega-deal thesis is working.

**Severity: Low**

---

### 3. Recommended Change

**What I'd change:** Add forward-looking forensic risk assessment tied to mega-deal revenue recognition.

**Why:** The forensic analysis scores accounting quality based on historical metrics (Beneish M-Score, Altman Z-Score, CFO/NI ratio). But the primary forensic risk for AMD going forward is how it will recognize revenue from multi-year, multi-billion-dollar mega-deals with complex warrant structures. Will GPU shipments be recognized on delivery or on deployment? How will warrant fair value adjustments flow through the income statement? These are H2 2026+ forensic risks that the current backward-looking scoring does not capture.

**Impact on conclusion:** Would not change the 4/5 accounting quality score for historical periods but would add a "forward forensic risk" flag at 3/5, signaling that accounting complexity will increase materially as mega-deals begin.

**Severity: Medium**

---

### 4. What's Strong

The Beneish M-Score (-2.71) and Altman Z-Score (14.38) calculations provide solid quantitative foundations, and the CFO/NI ratio trend (consistently >1.0x across three years) is the strongest evidence of earnings quality.

---

## Critique of Sentiment Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** "Lisa Su's shift from conservative to ambitious public targets (>60% DC CAGR, >$20 EPS) trades her historical under-promise/over-deliver credibility for elevated expectations."

**Why it's weak:** The sentiment analyst interprets the shift to ambitious targets as negative (reducing margin of safety). But from a catalyst perspective, the shift reflects changed circumstances, not changed strategy. Lisa Su now has $200B+ in contracted pipeline that she did not have 12 months ago. The >60% DC CAGR target is backed by specific customer commitments (OpenAI, Meta, Oracle), not aspirational marketing. The >$20 EPS target, while aggressive, is consistent with the math: if data center reaches $50B+ revenue at 35%+ operating margins with 1.6B diluted shares, EPS exceeds $20. The ambition reflects deal visibility, not overconfidence.

**Quantified impact if wrong:** If the targets are achievable (backed by contracted demand rather than aspirational), then the elevated expectations are correctly calibrated, not a credibility risk. This removes a ~$5-10/share discount the sentiment analysis implicitly applies through its tone-shift concern.

**Severity: Low**

---

### 2. Most Likely Source of Error

**Error source identified:** "Refusal to disclose Instinct GPU revenue (MEDIUM-HIGH severity) — core thesis driver has no disclosed revenue."

**Why this is the most likely error:** The sentiment analyst interprets non-disclosure as a red flag ("if the story were as strong, they'd disclose"). But there is a compelling competitive reason for non-disclosure: revealing exact GPU revenue would give NVIDIA, Broadcom, and custom ASIC competitors precise intelligence on AMD's market position, customer concentration, and pricing power. Intel withheld DCAI GPU revenue for similar competitive reasons. The refusal to disclose is likely competitive strategy, not obfuscation. The catalyst that would resolve this is if AMD reaches sufficient GPU scale (>$10B annual) that non-disclosure becomes untenable — likely by FY2027 earnings.

**Suggested correction:** Rate the non-disclosure as MEDIUM severity (competitive strategy) rather than MEDIUM-HIGH (red flag). Note that many growth businesses withhold segment detail until the segment reaches critical mass.

**Severity: Low**

---

### 3. Recommended Change

**What I'd change:** Add catalyst-conditional sentiment tracking.

**Why:** The current tone score (82/100) is a snapshot from Q4 FY2025 earnings. The key question is: how will management tone shift in Q1 2026 earnings (~May 5) based on MI450 progress? If management tone drops below 75 or hedging density increases materially, it would be a leading indicator of MI450 delays before formal announcement. The sentiment analysis should establish a "tone trip-wire" framework for the next 2-3 earnings calls.

**Impact on conclusion:** Would make the sentiment analysis actionable for trade timing — a Q1 2026 tone drop from 82 to below 72 could signal MI450 issues 3-6 months before they appear in revenue, creating an early exit signal.

**Severity: Medium**

---

### 4. What's Strong

The Q&A hedging density analysis (+76% increase vs. prepared remarks) is a genuinely useful signal — management is more cautious when answering unscripted questions, which is a normal but informative pattern for assessing true confidence levels.

---

## Critique of Technical Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** "Death cross (50-day below 200-day) is a realistic risk within 4-8 weeks if trajectory continues."

**Why it's weak:** The death cross projection assumes the current downtrend continues unabated, but the catalyst calendar shows multiple potential inflection points within the 4-8 week window: (1) sell-side PT revisions post-Q4 beat are still filtering through (March-April), (2) MI455X delay resolution could come any time, and (3) Q1 2026 earnings (~May 5) are within the window. Technical projections that assume trend continuation through known catalyst events are systematically unreliable. AMD's stock moves +-8-12% on earnings — a single positive catalyst can invalidate the death cross projection.

**Quantified impact if wrong:** If AMD rallies 5-10% on positive MI455X news or pre-earnings positioning (both probable in April), the death cross does not materialize, and the technical picture shifts from "confirmed downtrend" to "consolidation with improving momentum" — a fundamentally different conclusion.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** "Measured move from $200-$267 range breakdown projects to ~$133 (maximum) or ~$165 (conservative)."

**Why this is the most likely error:** Measured move projections assume no fundamental floor. But AMD at $133-165 implies 20-25x trailing P/E on a business growing 30%+ with $200B in contracted pipeline. There is a fundamental floor where long-term value investors and the company's own $9.4B buyback authorization create demand. AMD repurchased $1.3B in FY2025; at $133-165, the buyback would accelerate materially, creating a fundamental bid that technical analysis cannot capture. The measured move target is theoretically valid but practically unreachable unless fundamental assumptions simultaneously collapse.

**Suggested correction:** Overlay fundamental support levels on the technical analysis. The $165-185 zone identified as technical support aligns with fundamental value floors from the DCF bear case ($154) and comp-implied bear case ($140), making it a reinforced support zone rather than a technical target to trade through.

**Severity: Medium**

---

### 3. Recommended Change

**What I'd change:** Integrate the catalyst calendar into the technical timing recommendation.

**Why:** The technical analysis recommends $165-185 as the preferred entry zone, but the catalyst calendar may not provide that entry. If MI450 confirmation or positive Q1 earnings guidance arrests the decline in the $185-195 range, waiting for $165 means missing the position entirely. The technical recommendation should present two entry frameworks: (1) if the stock reaches $165-185, enter aggressively (technical + fundamental alignment); (2) if the stock holds $185-195 and Q1 earnings are positive, enter at current levels with a stop at $175 (catalyst-driven entry).

**Impact on conclusion:** Changes the recommendation from "wait for $165-185" (which may never come) to a conditional framework that captures both the technical and catalyst scenarios, making it actionable for the actual investment decision.

**Severity: Medium**

---

### 4. What's Strong

The observation that AMD has experienced 30%+ drawdowns ~1.5 times per year over 5 years is the most valuable statistical insight — it normalizes the current -28% decline as routine rather than alarming, which is essential context for position sizing.

---

## Critique of Sector Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** "TAM estimates have historical tendency to overstate by 20-40% in growth sectors."

**Why it's weak:** The blanket 20-40% overstatement haircut ignores that AI GPU TAM estimates have been consistently UNDERSTATED, not overstated. In 2023, the AI accelerator TAM was estimated at $30-50B by 2027. By 2025, NVIDIA alone generated $130.5B in data center revenue. The historical pattern of TAM overstatement applies to markets like 3D printing, VR, and autonomous vehicles — not markets with immediate, measurable enterprise ROI and $300B+ in committed hyperscaler capex. Applying a generic haircut to AI GPU TAM without adjusting for the unprecedented demand signals is a systematic error.

**Quantified impact if wrong:** If the AI GPU TAM of $378B by 2030 is correctly estimated (or understated), AMD's 18.8% market share implies $71B in AI GPU revenue, not the haircut-adjusted $53-60B. This adds $40-60/share to the bull case scenario.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** "TSMC CoWoS: ~80,000 wafers/month, >100% utilization; NVIDIA ~60% allocation, AMD ~8-10%."

**Why this is the most likely error:** The CoWoS allocation percentages are from mid-2025 data. The catalyst timeline shows TSMC expanding CoWoS to 130,000 wafers/month by late 2026 (the sector analyst cites this). The incremental 50,000 wafers/month are not pre-allocated — AMD's mega-deals (OpenAI, Meta, Oracle) give it the contractual basis to claim a disproportionate share of new capacity. If AMD captures 15-20% of the expanded capacity (vs. 8-10% of current), the supply constraint is substantially relaxed. The sector analysis understates AMD's ability to increase its CoWoS allocation as total capacity expands.

**Suggested correction:** Model CoWoS allocation dynamically: 8-10% of 80K wafers today, 12-15% of 130K wafers by late 2026, 15-20% of 160K+ wafers by 2027. AMD's absolute wafer allocation could triple even without dramatically increasing share.

**Severity: Medium**

---

### 3. Recommended Change

**What I'd change:** Add a catalyst-based market share trajectory model rather than a linear share gain assumption.

**Why:** The sector analysis projects AMD AI GPU share rising linearly from 10% to 18.8% by 2030. But share gains in semiconductors are lumpy and catalyst-driven. The MI450 launch in Q3 2026 is a step-function event: if it succeeds, AMD could jump from 12% to 16-18% share in 2-3 quarters as mega-deal volumes ramp. If it fails, share could stagnate at 10-12%. A catalyst-conditional share model would be more accurate than a linear projection.

**Impact on conclusion:** A step-function share model aligned with MI450 ramp would show either faster-than-expected share gains (bull: 20%+ by 2028) or stagnation (bear: 10-12% through 2028), with the current linear 18.8% by 2030 as the blended average. This would better capture the binary risk profile I identified in my own catalyst analysis.

**Severity: Medium**

---

### 4. What's Strong

The identification of TSMC CoWoS allocation as the binding supply constraint (not demand) is the most important sector insight. It correctly reframes the investment question from "can AMD sell GPUs?" to "can AMD get enough GPUs manufactured?"

---

## Critique of Research Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** "MI450 ships H2 2026 with competitive performance vs. NVIDIA Vera Rubin [confidence: medium]."

**Why it's weak:** The confidence level of "medium" is too conservative. Multiple independent sources confirm the H2 2026 timeline: AMD management (earnings call, CES 2026, Morgan Stanley conference March 3), Oracle partnership announcement (Q3 2026 deployment), and TSMC capacity planning. AMD's CEO publicly called the SemiAnalysis delay report "BS." While healthy skepticism is warranted, the convergence of multiple Tier 1-3 sources confirming the timeline warrants at least "medium-high" confidence.

**Quantified impact if wrong:** If confidence is medium-high (implying 75-80% on-time probability vs. the implied 55-65% at medium confidence), the expected value of the MI450 catalyst increases by ~$5-8/share.

**Severity: Low**

---

### 2. Most Likely Source of Error

**Error source identified:** Multiple critical data gaps — "Historical price data, options chain data, and competitor financials (NVDA, INTC) were NOT retrieved due to tool errors."

**Why this is the most likely error:** The data gaps are not errors of analysis but errors of data collection. Without historical price data, the risk, technical, and quant analysts were forced to estimate parameters that should have been calculated. Without options chain data, my own catalyst analysis had to estimate implied moves rather than measuring them. Without competitor financials, the comp table relies on aggregator data rather than primary sources. These cascading data gaps reduce confidence across multiple work products.

**Suggested correction:** Prioritize re-running the data collection tools for: (1) 3-year AMD daily price history, (2) current options chain with IV surface, (3) NVDA and INTC 10-K financial extracts. These three data sets would materially improve at least 5 other analysts' work products.

**Severity: High**

---

### 3. Recommended Change

**What I'd change:** Add a catalyst monitoring framework to the data intelligence memo.

**Why:** The research analyst's memo is a snapshot of data as of 2026-03-09. But the investment thesis depends on catalyst outcomes over the next 6-12 months. The data intelligence memo should include a "monitoring checklist" with specific data points to track: MI450 production announcements, Oracle deployment confirmation, CoWoS allocation updates, quarterly GPU revenue disclosure changes, and NVIDIA Vera Rubin benchmarks. This would make the research function ongoing rather than point-in-time.

**Impact on conclusion:** Would not change any current conclusions but would create a framework for updating the thesis as catalysts resolve, which is essential for a position with 70%+ of value concentrated in a 6-month window.

**Severity: Low**

---

### 4. What's Strong

The data source tiering system (Tier 1-6 with explicit reliability rankings) is the strongest methodological contribution — it gives every downstream analyst a consistent framework for weighting evidence quality.

---

*Critiques by Catalyst Analyst, Equity Research Swarm. Pass 2 adversarial review.*
