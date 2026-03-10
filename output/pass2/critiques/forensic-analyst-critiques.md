# Pass 2 Cross-Critiques -- Forensic Analyst
**Date:** 2026-03-09
**Reviewing Analyst:** Forensic Analyst
**Subject:** AMD (Advanced Micro Devices, Inc.)

---

## Critique of DCF Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** Terminal gross margin of 57.5% driven by Data Center mix shift to 74% of revenue by FY2030.

**Why it's weak:** The 57.5% terminal gross margin assumes Data Center segment economics flow through at GPU-level margins, but AMD refuses to disclose Instinct GPU revenue separately from the Data Center segment. My forensic analysis of the Q4 earnings call confirms the Sentiment Analyst's finding that GPU-specific economics are opaque. The $306M inventory reserve release inflated Q4 gross margins by ~300bps (underlying ~54%, not 57%), meaning the starting point for this margin trajectory is already overstated if analysts extrapolate Q4 as run-rate.

**Quantified impact if wrong:** If terminal gross margin is 54% (current underlying) rather than 57.5%, EBITDA margins compress by ~3.5pp. On $98.5B base revenue, that is ~$3.4B less EBITDA. At the DCF's implied exit multiple, this reduces fair value by approximately $20-25/share, pushing the base case from $154.58 to ~$130-135.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** The 60/40 blend of exit multiple terminal value ($603B) vs. perpetuity growth terminal value ($242B) is a methodological choice that accounts for a ~$10-15/share swing, but the more fundamental error is that terminal value represents 72-80% of enterprise value across all scenarios.

**Why this is the most likely error:** When terminal value dominates this heavily, the DCF is effectively a disguised multiples model. The "precision" of a 5-year projection is illusory -- the valuation is driven almost entirely by the terminal assumptions (growth rate, margins, WACC). From a forensic standpoint, this means the DCF's fair value is no more reliable than a simple forward P/E analysis, yet it is presented with more apparent precision. The WACC of 16% is the binding constraint, and the DCF analyst correctly flags that lowering to 13% would justify $200+, but the choice between 13% and 16% is more impactful than all five years of revenue projections combined.

**Suggested correction:** Present the DCF as a sensitivity table with WACC on one axis and terminal growth on the other, rather than as a point estimate. Disclose that the "fair value" is essentially a terminal value estimate discounted back. This would give the Director better decision-making information.

**Severity: Medium**

---

### 3. Recommended Change

**What I'd change:** Adjust the base case revenue assumption to exclude the $306M Q4 inventory reserve release from run-rate margin calculations, and apply a 5% haircut to mega-deal revenue realization (from 75% to 70%) given that the financial data underlying these projections has significant data gaps (no segment-level GPU margins, no full 10-K text reviewed, mega-deal contract terms not public).

**Why:** From a forensic perspective, building a 5-year DCF on data that relies heavily on Tier 4 sources (StockAnalysis.com aggregated financials) without reviewing the actual 10-K introduces unquantifiable error. The GAAP/non-GAAP gap of $1.52/share is large, and while I've confirmed it is explainable, the DCF should use GAAP-basis metrics or explicitly reconcile every non-GAAP adjustment in its projections.

**Impact on conclusion:** A 70% mega-deal realization rate combined with adjusted margins would reduce the base case fair value by approximately $10-15/share (from $154.58 to ~$140-145), modestly widening the overvaluation gap.

**Severity: Low**

---

### 4. What's Strong

The DCF correctly identifies warrant dilution as a "tax on success" and explicitly models the dilution haircut across scenarios. This is rigorous and often overlooked.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*

---

## Critique of Quant Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** NTM EBITDA of ~$12,500M at ~27% margin on ~$46B revenue, marked as [ESTIMATED].

**Why it's weak:** This estimate is constructed from consensus aggregator data (Tier 4), not from AMD's own financial disclosures. My forensic analysis found that GAAP operating income ($3.69B) vs. non-GAAP operating income ($7.77B) has a $4.08B gap. The NTM EBITDA figure likely uses a non-GAAP basis without clearly stating so. If it uses GAAP EBITDA (which includes ~$2.25B in Xilinx amortization), the margin would be materially lower, making AMD appear even more expensive on EV/EBITDA.

**Quantified impact if wrong:** If GAAP EBITDA is used (~$7.8B FY2025 vs. non-GAAP ~$10B+), the EV/EBITDA multiple jumps from 24.6x to ~39x, which would flip the conclusion from "fairly valued" to "significantly overvalued."

**Severity: High**

---

### 2. Most Likely Source of Error

**Error source identified:** The quality score of 29.0/100 (worst in comp group ex-INTC) based on ROIC of 6.6%.

**Why this is the most likely error:** AMD's ROIC is depressed by $25.1B in goodwill from the Xilinx acquisition. This is a purchase accounting artifact, not an operational deficiency. If you calculate ROIC on invested capital excluding goodwill (tangible invested capital), AMD's operational return is substantially higher. The quant analysis penalizes AMD for a 2022 acquisition price without adjusting for the accounting distortion. From a forensic standpoint, comparing AMD's ROIC to NVIDIA's (which has minimal goodwill) is comparing apples to oranges.

**Suggested correction:** Calculate and present both ROIC (as-reported, including goodwill) and ROIC-ex-goodwill. The comp table should flag that AMD's low ROIC is a Xilinx accounting artifact and adjust the quality score accordingly.

**Severity: Medium**

---

### 3. Recommended Change

**What I'd change:** Explicitly state whether all multiples are calculated on a GAAP or non-GAAP basis, and ensure the comp set uses the same basis for all companies. AMD's GAAP/non-GAAP gap ($1.52/share EPS, $4.08B operating income) is larger than most peers', so inconsistent basis inflates or deflates AMD's apparent valuation.

**Why:** Forensic analysis shows the gap is explainable (Xilinx amortization, SBC, one-time charges), but if AMD is valued on non-GAAP while peers with smaller adjustments are also valued on non-GAAP, the comparison is asymmetric. AMD's non-GAAP adjustments are ~36% of non-GAAP EPS; for NVIDIA, the gap is typically much smaller.

**Impact on conclusion:** Could shift the central comps estimate by $10-20/share in either direction depending on basis chosen.

**Severity: Medium**

---

### 4. What's Strong

The PEG ratio analysis at 0.51x is a clean, hard-to-manipulate metric that correctly captures AMD's growth discount. This is the most forensically reliable signal in the quant analysis.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*

---

## Critique of Competitive Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** AI GPU share of ~8-12%, gaining 2.6pp in Q4 2025, sourced from TechNetBooks (Tier 6).

**Why it's weak:** AMD does not disclose Instinct GPU revenue. This market share figure is an estimate from a Tier 6 source (low reliability). My forensic analysis confirms that management actively refuses to break out GPU revenue from Data Center segment revenue. Any market share figure for AMD's AI GPUs is reverse-engineered from partial data. The 2.6pp quarterly gain is particularly suspect -- quarterly share gains in semiconductors are notoriously lumpy due to large order fulfillment timing.

**Quantified impact if wrong:** If actual AI GPU share is 6-8% rather than 8-12%, the TAM capture rate in the competitive analysis is overstated by 33-50%, which would materially reduce the competitive moat score and the implied revenue trajectory.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** The CUDA Gap Score of 28.7-99.1 sourced from AIM Multiple (Tier 6).

**Why this is the most likely error:** Benchmark scores from a single Tier 6 source cannot be forensically verified. The range itself (28.7-99.1) is so wide that it is nearly meaningless as a precision metric -- it says NVIDIA's advantage is anywhere from 30% to 99%. This is presented as a quantified finding but is really a qualitative statement dressed in numbers.

**Suggested correction:** Cite the CUDA gap as a qualitative competitive risk ("NVIDIA has a substantial and likely widening software ecosystem advantage") rather than presenting a precise-looking score range from a low-tier source. Alternatively, triangulate with multiple benchmark sources.

**Severity: Low**

---

### 3. Recommended Change

**What I'd change:** Explicitly flag that the competitive moat assessment for AI GPUs is built almost entirely on Tier 3-6 data. Not a single Tier 1 source (SEC filing) is available for AMD's GPU market share, GPU-specific revenue, or GPU-specific margins.

**Why:** The competitive analysis is the most data-constrained of all analyst work products because the core thesis driver (AI GPU positioning) has no auditable financial disclosure. This is a forensic red flag -- not of manipulation, but of asymmetric information that favors management over investors.

**Impact on conclusion:** Would not change the 6/10 competitive score but would properly contextualize its reliability. The Director should weight this analysis with lower confidence.

**Severity: Low**

---

### 4. What's Strong

The identification of the dual squeeze (NVIDIA CUDA + custom ASIC cannibalization) as the #1 competitive threat is well-reasoned and not dependent on low-tier data.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*

---

## Critique of Macro Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** AI capex-to-revenue ratio of 25-28:1 ($660B+ capex vs. ~$25B AI revenue), characterized as "6-7x more speculative than telecom bubble."

**Why it's weak:** The $660B capex figure and the $25B AI revenue figure come from Goldman Sachs and Futurum Group (Tier 3-6). These are estimates of an entire ecosystem, not AMD-specific financials. More critically, the comparison to the telecom bubble's ~4x ratio conflates different economic structures -- telecom capex was for physical infrastructure with declining marginal returns, while AI capex includes significant software/model value that monetizes differently. The ratio is provocative but may be misleading.

**Quantified impact if wrong:** If AI monetization follows a software-like trajectory (faster revenue ramp than telecom), the ratio could compress to 10-15:1 within 2 years, which would significantly reduce the bear case probability and raise the macro-adjusted fair value from ~$190 to ~$220-240.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** Section 232 tariff impact estimated at ~$75-110M annualized, marked as [ESTIMATED] [DATA GAP].

**Why this is the most likely error:** This is a fabricated number -- there is no AMD disclosure, no analyst estimate cited, and no tariff schedule referenced. The analyst constructed it from an assumption that "33% of US revenue" is subject to tariffs. AMD's revenue geographic mix, tariff classifications for semiconductor products, and the specific Section 232 provisions are all unknown or unverified. From a forensic standpoint, this number should not appear in the analysis without heavy caveats.

**Suggested correction:** Remove the specific dollar estimate or label it explicitly as "[ILLUSTRATIVE ONLY -- no underlying data]." Replace with a qualitative statement that tariff exposure is a monitoring item pending actual trade policy developments.

**Severity: Low**

---

### 3. Recommended Change

**What I'd change:** The catastrophic scenario ($70-90, -60% downside, 10% probability) should be stress-tested against AMD's actual financial resilience. My forensic analysis shows $6.7B FCF, $10.6B cash, minimal debt, and 59.3x interest coverage. Even in a severe AI winter, AMD's non-AI business (EPYC server CPUs, embedded, client PCs) generates substantial cash flow. A -60% scenario requires not just AI capex collapse but a simultaneous semiconductor downturn affecting all segments.

**Why:** The catastrophic scenario is useful for risk budgeting but appears to be constructed top-down from macro assumptions rather than bottom-up from AMD's financial structure. A forensic bottom-up analysis would likely produce a floor price higher than $70-90.

**Impact on conclusion:** Would modestly increase the probability-weighted fair value (by reducing the tail risk drag) and could raise the macro-adjusted value from ~$190 to ~$195-200.

**Severity: Low**

---

### 4. What's Strong

The China revenue impact quantification ($5.8B annualized loss, now ~$400M/year) is well-sourced from AMD's 8-K (Tier 1) and is the most forensically reliable data point in the macro analysis.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*

---

## Critique of Risk Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** Annualized volatility of ~55% marked as [ESTIMATED], and correlation estimates also marked as [ESTIMATED].

**Why it's weak:** The Risk Analyst's own brief acknowledges this is the weakest point -- volatility and correlation figures are "from qualitative analysis, not computed from actual historical price series." From a forensic standpoint, a risk analysis built on estimated volatility is like a credit analysis built on estimated financial statements. The 55% figure may be reasonable for a high-beta semiconductor stock, but it could easily be 45% or 65%, and this range materially changes the Kelly fraction (from ~30% to ~50%) and the Sharpe ratio (from 0.15 to 0.25).

**Quantified impact if wrong:** At 45% volatility instead of 55%, the Sharpe ratio improves from 0.19 to ~0.23 and the vol-adjusted weight increases from 2.2% to ~2.7%. At 65%, Sharpe drops to ~0.16 and vol-adjusted weight to ~1.8%. The position sizing recommendation swings by ~50% across this range.

**Severity: High**

---

### 2. Most Likely Source of Error

**Error source identified:** The expected value of $210 (Bull $280/25%, Base $220/50%, Bear $120/25%).

**Why this is the most likely error:** These scenario prices and probabilities appear to be independently constructed without anchoring to the DCF analyst's scenarios ($223/$155/$84 at 25/50/25) or the Quant analyst's ($260/$210/$140). The Risk Analyst's base case of $220 is 42% higher than the DCF's $155. If the Risk Analyst used the DCF's scenarios, the expected value would be ~$154, and the risk-adjusted metrics would be dramatically worse (negative Sharpe, negative Kelly).

**Suggested correction:** Use the DCF analyst's probability-weighted scenarios as the starting point, then adjust for risk factors. The Risk Analyst should not independently construct scenario prices without reconciling to the valuation analysts.

**Severity: High**

---

### 3. Recommended Change

**What I'd change:** Replace all [ESTIMATED] volatility and correlation figures with computed values from actual price data, or explicitly state that the risk analysis is unreliable for position sizing purposes without this data.

**Why:** The Research Analyst's brief confirms that historical price data was NOT retrieved due to tool errors. This cascading data failure means the entire risk quantification framework is built on assumptions rather than data. A forensic analyst cannot endorse risk metrics that lack empirical foundation.

**Impact on conclusion:** The position sizing recommendation (Quarter Kelly 9.9%, vol-adjusted 2.2%) could change by 50%+ in either direction. The Director should treat these as order-of-magnitude estimates, not precision metrics.

**Severity: High**

---

### 4. What's Strong

The identification of asymmetric beta (realized beta 2.4x in 2022 selloffs vs. stated 2.02) is an important insight even if imprecisely quantified.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*

---

## Critique of Credit Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** GAAP EBITDA estimated at ~$7,768M, noted as "D&A estimated from non-GAAP reconciliation" [ASSUMPTION].

**Why it's weak:** My forensic analysis of AMD's financials shows GAAP operating income of $3.69B, which includes ~$2.25B in Xilinx intangible amortization. Adding back D&A to get GAAP EBITDA requires knowing the total D&A figure precisely. The credit analyst's estimate likely includes the non-cash Xilinx amortization in the add-back, which is standard for credit analysis but inflates the apparent coverage ratios. The 59.3x interest coverage and 0.42x Debt/EBITDA both depend on whether EBITDA is GAAP or adjusted.

**Quantified impact if wrong:** If GAAP EBITDA is $6.5B instead of $7.8B (excluding some non-cash items differently), Debt/EBITDA rises from 0.42x to 0.51x and interest coverage falls from 59.3x to ~48x. Both still indicate fortress-level creditworthiness, so the conclusion holds regardless.

**Severity: Low**

---

### 2. Most Likely Source of Error

**Error source identified:** The $12.2B purchase commitment ($8.5B FY2026) is correctly identified but may be understated.

**Why this is the most likely error:** The OpenAI and Meta mega-deals (12 GW combined) will require massive TSMC wafer purchases that may not yet be reflected in the disclosed $12.2B commitment figure, which is from the FY2024 10-K/A. If AMD secures additional CoWoS capacity for MI450 production (as the Sector Analyst's brief suggests is the binding constraint), future purchase commitments could be $20B+ annually. The credit analysis should model forward commitments, not just disclosed ones.

**Suggested correction:** Include a forward-looking sensitivity analysis showing how purchase commitments evolve if mega-deals proceed at various realization rates (40%/75%/95%).

**Severity: Low**

---

### 3. Recommended Change

**What I'd change:** Add a section on the accounting treatment of the 320M warrant shares. While the credit analyst correctly notes "warrants are equity dilution risk, not credit risk," the warrant issuance could trigger mark-to-market charges through the P&L if classified as liability instruments under ASC 815. If AMD's stock price rises significantly, the warrant liability could create large non-cash losses that distort GAAP metrics and potentially affect covenant calculations.

**Why:** Warrant accounting is a known area of complexity (as demonstrated by the SPAC warrant reclassification wave in 2021-2022). AMD's warrants at $0.01 exercise price with performance vesting conditions may not qualify for equity classification under ASC 815-40, potentially requiring liability treatment with quarterly fair value adjustments.

**Impact on conclusion:** Would not change the overall credit assessment (fortress balance sheet regardless) but would alert the Director to potential GAAP earnings volatility from warrant mark-to-market.

**Severity: Low**

---

### 4. What's Strong

The M&A capacity analysis ($15-23B before exceeding 1.0-2.0x leverage) is well-constructed and directly useful for assessing AMD's strategic optionality.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*

---

## Critique of Catalyst Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** MI450 ramp expected value of +5.9%, based on 30% probability of on-time strong delivery (+25%), 45% on-time limited (+7.5%), and 25% delay (-20%).

**Why it's weak:** These probabilities are constructed without disclosed financial data on MI450 production status. The SemiAnalysis delay report (mass production Q2 2027) directly contradicts AMD's timeline, and the catalyst analyst acknowledges "the truth likely lies between Q3 2026 and Q2 2027." A forensic review of AMD's disclosures finds no quantitative production commitment for MI450 -- management has used qualitative language ("on track") without binding timeline commitments. Assigning 75% probability to on-time delivery when the company has not made a verifiable commitment is aggressive.

**Quantified impact if wrong:** If MI450 delay probability is 40% (not 25%), the expected value drops from +5.9% to approximately +2.5%, and the H2 2026 catalyst concentration becomes riskier.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** The "beat and fade" pattern interpretation (Q4 2025: +1.8% AH after 23% EPS beat).

**Why this is the most likely error:** The catalyst analyst notes the beat-and-fade but does not connect it to the forensic finding that $306M inventory reserve release inflated Q4 results. If sophisticated investors recognized the reserve release was non-recurring and adjusted Q4 margins down ~300bps, the "beat" was smaller than headline numbers suggest. The fade may have been fundamentally justified, not just a market pattern.

**Suggested correction:** Adjust the earnings beat magnitude for the reserve release. The "true" beat (excluding $306M reserve release) was approximately 15-18% on EPS, not 23%. This changes the interpretation of the beat-and-fade from a behavioral pattern to a fundamentally justified repricing.

**Severity: Low**

---

### 3. Recommended Change

**What I'd change:** The phased entry strategy (1/3 now, 1/3 post-Q1 earnings, 1/3 on MI450 confirmation) should include a forensic checkpoint -- specifically, require that Q1 2026 results show organic gross margin improvement (excluding any reserve releases or one-time items) before deploying the second tranche.

**Why:** The Q4 margin was flattered by ~300bps from the reserve release. If Q1 gross margins revert to ~54% (which I expect), the market reaction could be negative even on a revenue beat. The entry strategy should be conditioned on verifiable, clean financial performance, not headline numbers.

**Impact on conclusion:** Would not change the catalyst mapping but would add risk discipline to the implementation timeline.

**Severity: Low**

---

### 4. What's Strong

The sell-side PT range spread ($120-$358, $238 spread) is a genuinely useful metric for assessing market disagreement and is sourced from verifiable data.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*

---

## Critique of ESG & Governance Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** Warrant issuance relied on "inducement grant" exception or commercial arrangement classification under NASDAQ rules [DATA GAP: exact rule not confirmed].

**Why it's weak:** This is not an assumption but an acknowledged data gap on a critical governance question. My forensic review confirms that issuing 320M shares (~20% dilution) without shareholder approval is unusual for a company of AMD's size. If the NASDAQ exception does not apply, AMD may face regulatory scrutiny or shareholder litigation. The ESG analyst rates this as a concern but cannot assess the legal risk because the underlying rule has not been confirmed.

**Quantified impact if wrong:** If the warrant issuance is challenged and unwound (unlikely but possible), the bull case improves by ~$45/share (removing dilution). If additional warrant commitments are made under the same precedent, dilution could expand beyond 20%.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** Expected dilution calculation: (0.30 x 0%) + (0.45 x 9.8%) + (0.25 x 19.6%) = 9.3%.

**Why this is the most likely error:** The 30% probability of 0% vesting assumes mega-deals completely fail. But the warrants vest on deployment milestones, not stock price (though full vesting requires $600/share). If OpenAI and Meta deploy even modest AMD GPU capacity, partial vesting occurs. The 30% probability of zero vesting may be too high -- a 15-20% probability is more consistent with the fact that both deals have been publicly announced and preliminary deployment planning is underway.

**Suggested correction:** Adjust zero-vest probability to 15-20%, increase partial-vest to 50-55%, yielding expected dilution of ~10.5-11.5% (vs. 9.3%).

**Severity: Low**

---

### 3. Recommended Change

**What I'd change:** Include the accounting treatment of warrant instruments. Under ASC 815-40, these warrants may need to be classified as derivative liabilities (not equity) if they contain price-contingent vesting conditions ($600 stock price). If liability-classified, AMD would record quarterly mark-to-market gains/losses that flow through the income statement, creating GAAP earnings volatility that other analysts' models do not account for.

**Why:** This is a direct forensic concern. The 2021-2022 SPAC warrant reclassification precedent showed that instruments assumed to be equity often require liability treatment under ASC 815-40, and the resulting P&L volatility surprised markets.

**Impact on conclusion:** Would not change the governance assessment but would add a material financial reporting risk that the DCF and Quant analysts should model.

**Severity: Medium**

---

### 4. What's Strong

The board diversity and independence metrics (87.5% independent, 37.5% female, 50% racially diverse) are well-sourced from the DEF 14A (Tier 1) and represent some of the most reliable data in the entire research process.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*

---

## Critique of Technical Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** Measured move from $200-$267 range breakdown projects to ~$133 (maximum) or ~$165 (conservative).

**Why it's weak:** Measured move targets are pattern-based projections with no financial statement anchor. From a forensic standpoint, a $133 target implies a ~$215B market cap, at which point AMD would trade at roughly 12-13x non-GAAP EPS on FY2026E numbers -- a valuation that assumes negative growth. The technical projection ignores that AMD's $6.7B FCF and $10.6B cash balance provide a fundamental floor well above $133.

**Quantified impact if wrong:** The difference between a $133 measured move target and a forensically-supported floor (likely $140-150 based on trough multiples on trough earnings) is ~$10-17/share, which would affect entry timing recommendations.

**Severity: Low**

---

### 2. Most Likely Source of Error

**Error source identified:** All technical analysis sourced from WebSearch (Tier 4) because historical price data was NOT retrieved via Research Analyst tools.

**Why this is the most likely error:** The Technical Analyst had to reconstruct price levels, moving averages, and RSI from free websites rather than computing them from actual price data. This means the analyst could not perform independent calculations of moving averages, volume patterns, or momentum oscillators. The data may be current but cannot be verified or cross-checked. For a forensic review, this is the equivalent of analyzing financials from a blog post rather than from SEC filings.

**Suggested correction:** The Director should note that technical analysis reliability is significantly degraded by the data gap and weight it accordingly in the final synthesis.

**Severity: Medium**

---

### 3. Recommended Change

**What I'd change:** Incorporate the Feb 4 earnings breakdown (-17% on high volume) alongside the forensic finding that the $306M inventory reserve release inflated Q4 margins. The high-volume selloff may have been driven by institutional recognition of the non-recurring nature of the margin beat, not just general market sentiment. This reframes the technical breakdown as fundamentally informed rather than purely technical.

**Why:** Connecting the technical event (high-volume institutional distribution) to the forensic finding (non-recurring margin boost) strengthens both analyses and provides the Director with a more integrated view.

**Impact on conclusion:** Would reinforce the technical analyst's cautious stance and support the $165-$185 entry zone recommendation.

**Severity: Low**

---

### 4. What's Strong

The identification of the fundamental/technical divergence (sell-side Buy consensus at $261 vs. confirmed downtrend) is an important signal for timing.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*

---

## Critique of Sector Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** AI GPU TAM of $140B (2025) growing to $378B (2030 base, 22% CAGR), marked as [ESTIMATED].

**Why it's weak:** The sector analyst's own brief acknowledges that "TAM estimates have historical tendency to overstate by 20-40% in growth sectors." Applying the analyst's own correction factor, the 2030 TAM could be $225-300B rather than $378B. Every downstream analysis (AMD share capture, revenue projections, margin expansion) is built on this potentially overstated denominator. From a forensic standpoint, unauditable third-party TAM estimates are Tier 5-6 data being used as the foundation for Tier 1-level conclusions.

**Quantified impact if wrong:** A 30% TAM overstatement at constant AMD market share (18.8%) reduces AMD's implied 2030 AI GPU revenue from ~$71B to ~$50B -- a $21B revenue gap that flows directly through to the DCF and price target.

**Severity: High**

---

### 2. Most Likely Source of Error

**Error source identified:** AMD ROIC of ~15% [ESTIMATED] vs. WACC ~11%.

**Why this is the most likely error:** The ROIC estimate appears inconsistent with the Quant Analyst's figure of 6.6%. The difference is likely methodological -- the Sector Analyst may be using non-GAAP operating income and/or excluding goodwill from invested capital, while the Quant Analyst uses GAAP figures. A 15% ROIC characterizes AMD as a solid value creator; a 6.6% ROIC characterizes it as barely earning its cost of capital. These cannot both be correct without explicit reconciliation.

**Suggested correction:** Reconcile with the Quant Analyst. Report both GAAP ROIC (including goodwill, likely ~6-7%) and operational ROIC (excluding goodwill, likely ~15-18%). The gap between them is the ongoing "cost" of the Xilinx acquisition premium.

**Severity: Medium**

---

### 3. Recommended Change

**What I'd change:** The TSMC CoWoS capacity constraint (AMD at ~8-10% allocation vs. NVIDIA at ~60%) should include a financial impact analysis. If AMD cannot secure sufficient CoWoS capacity, the mega-deal revenue is supply-constrained regardless of demand. The sector analysis identifies this constraint qualitatively but does not quantify the revenue cap it implies.

**Why:** From a forensic standpoint, the $12.2B purchase commitment to TSMC (from the Credit Analyst's brief) should be cross-referenced with the CoWoS allocation estimate to determine whether AMD has sufficient contracted capacity to fulfill mega-deal obligations.

**Impact on conclusion:** Could establish a hard ceiling on AMD's AI GPU revenue growth that is lower than demand-based projections.

**Severity: Medium**

---

### 4. What's Strong

The HHI concentration analysis (AI GPU 6,864 / Server CPU 4,609) is a well-chosen structural metric that provides objective context for competitive dynamics.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*

---

## Critique of Devil's Advocate's Work Product

### 1. Weakest Assumption

**Assumption identified:** DA-adjusted bear probability of 30-35%, producing a negative expected value of -6.5%.

**Why it's weak:** The Devil's Advocate assigns LOW confidence to all five critical assumptions simultaneously, which is methodologically aggressive. The probability that ALL five assumptions fail is much lower than the probability that ANY ONE fails. The 30-35% bear probability implicitly assumes high correlation among failure modes. My forensic analysis shows AMD's accounting quality is 4/5, cash flow is strong, and the balance sheet is clean -- this limits the severity of the bear case even if several assumptions fail. AMD does not face existential risk; it faces growth disappointment risk.

**Quantified impact if wrong:** If bear probability is 20-25% (which I find more defensible given the financial resilience), the DA-adjusted EV rises from $178 to ~$192-198, flipping the conclusion from negative to roughly neutral.

**Severity: Medium**

---

### 2. Most Likely Source of Error

**Error source identified:** "Pre-mortem price: $80 by March 2028 if mega-deals are bridge contracts + AI capex correction."

**Why this is the most likely error:** $80 implies a ~$130B market cap. At that level, AMD would trade at approximately 12x trailing earnings (assuming $6.66 NTM EPS) or 1.5x FY2025 revenue. My forensic analysis shows AMD generates $6.7B in FCF. An $80 stock price implies a 5.2% FCF yield, which would make AMD a value stock that attracts buyback-driven support (AMD has $9.4B in buyback authorization). The financial structure creates a floor well above $80 absent an actual bankruptcy scenario, which the Altman Z-Score of 14.38 rules out.

**Suggested correction:** Set the pre-mortem floor at $100-120, which is more consistent with trough multiples on trough (but still positive) cash flows.

**Severity: Low**

---

### 3. Recommended Change

**What I'd change:** The bridge contract thesis should be tested against AMD's actual disclosed purchase commitments. If mega-deals were truly bridge contracts (temporary demand), AMD would not be committing $8.5B in FY2026 TSMC purchase obligations. The magnitude of AMD's supply-side commitments is real financial evidence that management believes the demand is durable, not transitory. This does not prove the bear case wrong, but it does require the Devil's Advocate to explain why management is making irreversible financial commitments for supposedly transient demand.

**Why:** Forensic analysis prioritizes financial actions over verbal statements. AMD's $8.5B purchase commitment is a verifiable action; hyperscaler "intent" is unverifiable.

**Impact on conclusion:** Would not eliminate the bear case but would raise the burden of proof and potentially reduce the DA-adjusted bear probability by 3-5pp.

**Severity: Low**

---

### 4. What's Strong

The "equity-for-demand" framing of the warrant structure (permanent dilution for potentially transient revenue) is the most incisive observation across all analyst work products.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*

---

## Critique of Sentiment Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** CEO credibility score of 8.5/10, based on "6+ consecutive quarters" of guidance beats.

**Why it's weak:** The 8.5/10 credibility score is backward-looking. The sentiment analyst correctly identifies that Lisa Su has shifted from conservative to ambitious targets (>60% DC CAGR, >$20 EPS), which means the historical beat rate is less predictive of future beats. From a forensic standpoint, management credibility should be assessed not just on past accuracy but on the gap between current guidance and verifiable financial capacity. The >$20 EPS target requires roughly 5x current non-GAAP EPS -- an unprecedented trajectory that my forensic analysis cannot verify from current financials.

**Quantified impact if wrong:** If the credibility score should be 6.5-7/10 (reflecting the shift to aspirational targets), the overall tone score drops from 82/100 to approximately 75/100, which would reduce the positive sentiment overlay on the investment thesis.

**Severity: Low**

---

### 2. Most Likely Source of Error

**Error source identified:** GAAP vs. Non-GAAP operating income gap cited as 63% ($1,752M vs. $2,854M) -- this appears to be a quarterly figure.

**Why this is the most likely error:** The sentiment analyst uses a single-quarter GAAP/non-GAAP gap (63%) without context. My forensic analysis shows the full-year gap is $3.69B vs $7.77B GAAP-to-non-GAAP operating income (a 52% gap). Using a single quarter's gap overstates the issue because quarterly amortization and SBC can be lumpy. The annual figure is more forensically appropriate for assessing structural earnings quality.

**Suggested correction:** Use full-year GAAP/non-GAAP reconciliation rather than a single quarter to assess the structural gap.

**Severity: Low**

---

### 3. Recommended Change

**What I'd change:** The refusal to disclose Instinct GPU revenue (Red Flag #1, rated MEDIUM-HIGH severity) should be escalated. My forensic analysis independently confirms this is the single most significant transparency concern. The core investment thesis rests on AI GPU growth, yet the financial metric most relevant to that thesis (GPU-specific revenue and margins) is deliberately withheld. I would rate this HIGH severity, not MEDIUM-HIGH.

**Why:** In forensic analysis, when management selectively withholds data on the thesis's most important driver, it typically means the undisclosed data is less favorable than the blended disclosure. This pattern (disclose aggregate when the hidden component is weak, break out when it is strong) is a well-documented investor relations tactic.

**Impact on conclusion:** Would strengthen the bear case for AI GPU economics and support the Devil's Advocate's thesis about GPU-specific margins being less compelling than the blended Data Center segment suggests.

**Severity: Medium**

---

### 4. What's Strong

The Q&A hedging density analysis (+76% increase vs. prepared remarks) is a genuinely useful forensic signal. Management is more guarded under questioning, which is consistent with prepared remarks being optimized messaging while Q&A reveals actual confidence levels.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*

---

## Critique of Research Analyst's Work Product

### 1. Weakest Assumption

**Assumption identified:** AMD AI GPU share of ~8-12%, gained 2.6pp in Q4 2025, sourced from TechNetBooks (Tier 6).

**Why it's weak:** This is a critical data point that flows into nearly every other analyst's work (Competitive, Sector, DCF, Risk), yet it comes from a Tier 6 source. The Research Analyst should have triangulated this figure with at least 2-3 independent sources or explicitly flagged the low reliability. My forensic analysis confirms AMD does not disclose GPU-specific revenue, making this an unverifiable third-party estimate.

**Quantified impact if wrong:** If actual share is 6% rather than 10% (midpoint), every downstream revenue projection based on GPU share capture is overstated by ~40%.

**Severity: High**

---

### 2. Most Likely Source of Error

**Error source identified:** Multiple critical tool failures -- historical price data, options chain data, competitor financials, full 10-K text all NOT retrieved.

**Why this is the most likely error:** The Research Analyst's data gathering failures cascaded through every downstream analyst. The Technical Analyst had to use WebSearch instead of actual price data. The Risk Analyst estimated volatility qualitatively. The Quant Analyst used aggregated competitor data. The Forensic Analyst (me) could not review the full 10-K for revenue recognition policies, off-balance-sheet items, and risk factors. This is not one error -- it is a systematic data quality failure that degrades the reliability of the entire research process.

**Suggested correction:** The Director should flag the tool failures as a systemic issue and either (a) rerun the Research Analyst with fixed tools, or (b) explicitly discount the conviction rating by 1 point due to data quality limitations.

**Severity: High**

---

### 3. Recommended Change

**What I'd change:** Prioritize retrieving the full 10-K text above all other data. The 10-K is a Tier 1 source that contains: (1) revenue recognition policy detail, (2) off-balance-sheet obligations, (3) risk factor changes year-over-year, (4) related-party transactions, (5) segment-level disclosures, and (6) contingent liabilities. No other single document provides this breadth of forensically verifiable information. The fact that the EDGAR CIK resolution failed should have been resolved via alternative approaches (direct SEC EDGAR URL, company IR page, WebSearch for the filing).

**Why:** Without the 10-K, multiple analysts (Forensic, Credit, ESG, DCF) are operating with incomplete Tier 1 data while relying on Tier 4-6 sources as substitutes.

**Impact on conclusion:** Would fill multiple [DATA GAP] flags across all analyst work products and potentially change assessments in areas where Tier 4-6 data proved inaccurate.

**Severity: High**

---

### 4. What's Strong

The comprehensive identification of the mega-deal structure (12 GW, ~$200B potential revenue, 320M warrants at $0.01) and its dilution implications was essential context for every downstream analyst.

---

*Critique by Forensic Analyst, Equity Research Swarm. Pass 2 adversarial review.*
