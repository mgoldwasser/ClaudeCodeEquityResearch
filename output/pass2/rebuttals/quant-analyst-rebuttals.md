# Pass 2 Rebuttals — Quant Analyst
**Date:** 2026-03-09
**Subject:** Advanced Micro Devices, Inc. (AMD)

---

## Response to DCF Analyst's Critique

### 1. NTM EBITDA Margin of 27% Is Too Conservative vs. DCF's 32.5%
**Verdict: Partially Accept**

The DCF Analyst correctly identifies that using trailing EBITDA margin (27.2%) for NTM EBITDA understates forward profitability, given consensus and the DCF model project margin expansion as GPU mix increases. I accept that 27% is a floor, not a central estimate. However, I deliberately anchored to trailing margins because comps-implied valuations should use the same basis as the peer multiples — and peer multiples are calculated on consensus NTM EBITDA, which for most comps already embeds their own margin trajectories. The issue is consistency, not conservatism. I revise my approach: I will present two EV/EBITDA scenarios — one at current margins (27%, yielding $12,500M EBITDA, implied price $162) and one at the DCF's 32.5% (yielding ~$14,950M EBITDA, implied price ~$196). The blended midpoint of $179 is more defensible than either extreme, and the margin-expansion scenario at 35% ($207) remains the bull case anchor.

### 2. PEG Gets Insufficient Weight in Blended Estimate
**Verdict: Partially Accept**

The DCF Analyst notes that a 1.16x PEG at AMD's 55.9% CAGR implies $431/share, and even at 0.58x PEG implies $230. The observation that PEG-based valuations are unreliable at very high growth rates is correct — this is precisely why I assigned PEG zero explicit weight in the blended estimate (40% EV/EBITDA, 40% P/E, 20% EV/Rev). However, the suggestion to cap EPS CAGR at 30-35% and then weight PEG at 20-25% is constructive. At a capped 30% CAGR and 1.0x PEG, the implied P/E is 30x, yielding $200/share — close to my base case. I accept adding a capped-PEG cross-check at 15% weight in the blended estimate, revising the blend to 35% EV/EBITDA (margin-adjusted), 35% P/E, 15% capped PEG, 15% EV/Rev.

### 3. Warrant Dilution Should Be Scenario-Dependent, Not Flat 80M
**Verdict: Accept**

The DCF Analyst's framework of 0M (bear), 200M (base), 320M (bull) is more rigorous than my flat 80M assumption. Dilution increasing with stock price is mechanically correct — warrants vest as performance thresholds are met, meaning bull scenarios incur more dilution. I adopt the scenario-dependent framework: bear case at 1,630M shares ($140), base case at 1,830M shares (reducing $210 to ~$187), bull case at 1,950M shares (reducing $260 to ~$218). This compresses the range and reduces the probability-weighted expected value from $205 to approximately $184.

---

## Response to Competitive Analyst's Critique

### 1. PEG Uses Backward-Looking 55.9% 5Y EPS CAGR
**Verdict: Partially Accept**

The Competitive Analyst argues that AMD's 55.9% CAGR reflects the hyper-growth phase of EPYC share gains and initial AI ramp, and that forward CAGR of 25-30% is more realistic given EPYC share ceiling at 40%, CUDA constraints, and Gaming decline. The directional point is valid — the 55.9% figure is a trailing/consensus blended CAGR, not a pure forward estimate. However, the claim that EPYC gains face a "ceiling" at 40% understates the opportunity: AMD was at 33.9% server share in Q4 2025 and Intel's turnaround timeline under Lip-Bu Tan extends to 2027+, providing a multi-year runway. I accept revising the PEG analysis to present both trailing PEG (0.51x at 55.9% CAGR) and a forward PEG (0.95-1.14x at 25-30% CAGR) to give the Director both signals. The trailing PEG remains informative as a measure of what the market has already observed but not fully priced.

### 2. ROIC Depressed by Xilinx Goodwill — Present Adjusted ROIC
**Verdict: Accept**

The Competitive Analyst correctly identifies that AMD's $41.8B in Xilinx goodwill inflates the invested capital denominator, producing a misleadingly low 6.6% ROIC. On tangible invested capital (excluding goodwill), the operating ROIC is approximately 15-20%, which is mid-pack rather than worst-in-class. The Xilinx goodwill reflects acquisition price, not current operational inefficiency. I accept this critique and will present dual ROIC figures: as-reported (6.6%) and goodwill-adjusted (~18%), with the quality score recalculated to approximately 50-55/100 on the adjusted basis. This moves AMD from "worst in group" to "mid-pack," which is a material change in interpretation.

### 3. Comp Set Should Weight Broadcom's Custom ASIC Business
**Verdict: Partially Accept**

The suggestion to benchmark AMD's AI GPU business specifically against Broadcom's custom ASIC segment is analytically interesting but difficult to execute cleanly. Broadcom does not disclose custom ASIC segment profitability separately from its broader semiconductor segment. I accept the principle that AMD's competitive frame is broadening beyond NVIDIA to include custom ASIC alternatives, and that Broadcom's AI segment multiples are relevant. However, applying segment-level comp multiples requires segment financials that are not publicly available. I note this as a [DATA GAP] rather than making speculative adjustments.

---

## Response to Macro Analyst's Critique

### 1. PEG Uses Backward-Looking CAGR (Duplicate of Competitive/Risk Critiques)
**Verdict: Partially Accept**

Same response as the Competitive Analyst critique above. I accept presenting both trailing and forward PEG ratios. At a forward 25-30% CAGR, AMD's PEG normalizes to 0.95-1.14x, which is near the comp median of 1.16x — fair value, not deep value. The PEG signal weakens from "strongest signal" to "neutral" on a forward basis.

### 2. Quality Score Should Be Weighted More Heavily Given Higher-for-Longer Rates
**Verdict: Partially Accept**

The Macro Analyst makes a valid regime argument: in a 3.50-3.75% fed funds environment, markets reward quality and profitability over pure growth. The 2022 rotation from growth to quality is a relevant precedent. I accept that the quality-adjusted fair value ($162 at current margins on EV/EBITDA) should carry more weight in the blended estimate than I originally assigned. However, the suggested 10-15% blanket quality discount is methodologically imprecise. I revise the blended weight toward EV/EBITDA (which inherently penalizes low margins) from 35% to 40%, effectively incorporating the quality discount structurally rather than as an ad hoc haircut.

### 3. Historical 40x P/E Was in a Low-Rate Environment
**Verdict: Accept**

The Macro Analyst correctly observes that AMD's 5-year average forward P/E of ~40x was established when fed funds was 0-0.25% to 2.5%, and that using it as a reference point for undervaluation ignores the rate regime shift. At 3.50-3.75%, the equilibrium forward P/E for a 2.02-beta semiconductor stock is structurally lower. I accept that a rate-adjusted historical average of 28-32x is more appropriate. At 30x, the implied price is $200 (vs. $266 at 40x). I remove the historical 40x reference as a primary valuation anchor and reclassify it as directional context only, noting the rate regime caveat explicitly.

---

## Response to Risk Analyst's Critique

### 1. PEG Compares Structurally Different Growth Profiles
**Verdict: Partially Accept**

The Risk Analyst adds an important nuance to the PEG debate: AMD's 55.9% CAGR reflects mega-deal-dependent, execution-heavy growth, while peers' ~22% reflects diversified, lower-risk growth. PEG ratios assume linear risk-to-growth scaling, which breaks down at 2.5x growth differentials. This is a valid methodological limitation of PEG that I should have flagged. I accept the critique and add a risk-adjusted PEG note: AMD's raw PEG of 0.51x should be discounted for execution risk concentration. At a risk-adjusted CAGR of 35% (applying a 37% haircut to the 55.9% for execution risk), the PEG becomes 0.82x — still below the comp median but no longer signaling deep undervaluation.

### 2. Quality Score Noted but Overridden in Conclusion
**Verdict: Partially Accept**

The Risk Analyst argues that the 29/100 quality score is flagged but then effectively dismissed in favor of the growth narrative, and that the comp set distortions (INTC pulling quality floor down, AVGO's software model inflating multiples) should be addressed. I accept that the final conclusion — "fairly valued to modestly undervalued" — gives insufficient emphasis to the quality concern. However, I reject the suggestion to remove INTC and AVGO from the comp set entirely. INTC is AMD's most direct competitor in x86 CPUs and cannot be excluded from a semiconductor comp analysis. AVGO's custom ASIC business directly competes with AMD for hyperscaler AI budgets. I accept presenting the comp analysis with and without INTC (given its outlier status), but the primary analysis retains both names.

### 3. Comp Set Needs Better Justification
**Verdict: Reject**

The suggestion to replace INTC and AVGO with MCHP (Microchip Technology) weakens the comp set. MCHP is an analog/embedded-focused company with no AI GPU exposure and minimal competitive overlap with AMD's data center business. Intel and Broadcom are AMD's two most important competitors — in server CPUs and AI accelerators respectively. Excluding direct competitors to produce cleaner statistics defeats the purpose of comparables analysis. The outlier treatment already addresses the statistical distortion from INTC's turnaround-stage metrics.

---

## Response to Credit Analyst's Critique

### 1. ROIC Distorted by Xilinx Goodwill
**Verdict: Accept**

Same response as the Competitive Analyst critique. I accept presenting dual ROIC figures (as-reported 6.6% and goodwill-adjusted ~18%) and recalculating the quality score on both bases. The Credit Analyst's additional point about tangible ROIC being relevant for debt serviceability is well-taken — at 25-35% tangible ROIC, AMD's operations easily cover the $3.3B debt load.

### 2. No Capital Structure Adjustment in Comps
**Verdict: Partially Accept**

The Credit Analyst argues that AMD's net cash position ($7.25B) should warrant a 0.5-1.0x EV/EBITDA premium versus the levered comp median (AVGO at 1.4x Net Debt/EBITDA, INTC at 0.7x). The directional argument is correct — balance sheet strength does command a premium in volatile markets. However, the EV/EBITDA metric already adjusts for capital structure differences by using enterprise value (equity + net debt), which is its primary advantage over P/E. Adding a further "balance sheet premium" on top of EV-based multiples risks double-counting the capital structure benefit. I accept noting AMD's net cash position as a qualitative positive but reject applying a numerical multiple premium on top of an EV-based framework.

### 3. Warrant Dilution Should Be Scenario-Specific
**Verdict: Accept**

Consistent with my response to the DCF Analyst, I adopt scenario-dependent dilution: 0M (bear), ~100M (base at ~$210 price), ~160M (bull at $260). The Credit Analyst's point about purchase-milestone versus stock-price-threshold tranches is a useful refinement of the vesting mechanics.

---

## Response to Catalyst Analyst's Critique

### 1. Static Comp Set vs. Evolving Business Mix
**Verdict: Partially Accept**

The Catalyst Analyst argues that AMD's business mix will look materially different in 12 months (data center at 60-65% of revenue post-MI450) and that static comps undervalue the mix shift. This is conceptually valid but practically difficult to implement — forward-looking comp sets based on projected revenue mix are inherently speculative. I accept adding a forward mix-adjusted sensitivity: if AMD's data center business (60% of FY2027 revenue) is valued at NVDA-like multiples (26x P/E) and the remaining 40% at QCOM-like multiples (12.7x P/E), the blended implied P/E is ~20.7x, yielding $138 — actually lower than the current comp approach. This illustrates that sum-of-parts comp analysis cuts both ways: AMD's non-data-center segments (Gaming, Embedded) drag the blended multiple down.

### 2. Quality Score Is Backward-Looking Pre-MI450
**Verdict: Partially Accept**

The critique that trailing quality metrics penalize a company at an inflection point is fair. I accept presenting a forward quality score alongside the trailing score, using consensus FY2027 estimates. However, the forward score is inherently less reliable because it depends on assumptions about MI450 ramp and margin expansion that are the core analytical uncertainty. I present both scores with appropriate caveats.

### 3. Need Time-Adjusted Valuation
**Verdict: Reject**

Valuing AMD on H2 2026 run-rate metrics would be a forward projection exercise, not a comparables analysis. Comps are designed to assess relative value using current or NTM consensus data — the same basis on which all peers are valued. Applying one-sided forward adjustments to AMD but not to peers (who also have their own catalysts) creates an asymmetric framework that biases toward undervaluation. The catalyst timeline is better addressed by the Catalyst Analyst and DCF Analyst's scenario analysis than by distorting the comps methodology.

---

## Response to ESG/Governance Analyst's Critique

### 1. 80M Warrant Dilution Figure Is Arbitrary
**Verdict: Accept**

The critique is correct — the 80M figure lacked rigorous derivation. I adopt scenario-dependent dilution as described in my responses to the DCF and Credit Analysts. At 160M shares (the ESG Analyst's estimate), the central estimate drops from $197 to $188, which changes the signal from "modestly undervalued" to "approximately fairly valued." This is a material revision.

### 2. Revenue Quality Discount for Warrant-Linked Revenue
**Verdict: Partially Accept**

The ESG/Governance Analyst raises a novel point: AMD is effectively "buying" revenue with equity through the warrant issuance, and this revenue is not equivalent in quality to organically won revenue. No peer in the comp set has a comparable arrangement. This is a legitimate governance concern. However, the warrant structure is performance-contingent — AMD only incurs dilution if the customer actually deploys AMD hardware, meaning the revenue and the dilution are mechanically linked. The "equity cost" of the revenue is already captured in the dilution adjustment. Applying a separate revenue quality discount on top of the dilution adjustment would double-count the economic cost. I reject the additional 5-10% discount but accept flagging the warrant revenue model as a unique comp set risk with no peer precedent.

---

## Response to Technical Analyst's Critique

### 1. Historical 40x P/E May Be Structural, Not Cyclical Compression
**Verdict: Partially Accept**

The Technical Analyst observes that AMD's P/E has compressed from ~40x to 28.6x over 5 months and that the break below $200 suggests the market no longer accepts the premium. Price action is informational — sustained compression across multiple quarters is a stronger signal than a temporary drawdown. I accept removing the 40x historical reference as a primary valuation anchor (consistent with the Macro Analyst critique) and noting that the 25-30x range may be the new equilibrium for AMD at current rates and profitability. However, I resist the conclusion that price action alone determines fundamental value — the market can be wrong for extended periods, and AMD's P/E compressed to ~20x in late 2022 before recovering 91% over the following 52 weeks.

### 2. Incorporate Relative Strength Into Comps
**Verdict: Reject**

The suggestion to incorporate AMD's underperformance versus SPX (-18pp over 3 months) into the comps framework conflates technical and fundamental analysis. Relative strength is a trading signal, not a valuation input. Comps analysis assesses what a company should be worth based on peer fundamentals; relative momentum assesses what the market is currently willing to pay. These serve different analytical purposes, and mixing them degrades both. The Technical Analyst's own work product is the appropriate vehicle for relative strength signals, not the comps framework.

---

## Response to Sector Analyst's Critique

### 1. Comp Set Doesn't Reflect AMD's Mix Shift
**Verdict: Partially Accept**

The Sector Analyst suggests weighting NVIDIA at 40-50% of the comp (rather than equal weight) to reflect AMD's GPU business transition. If the comp set is reweighted 50% NVDA / 20% AVGO / 30% others, the weighted P/E median shifts from 27.8x to approximately 30x, implying $200 — modestly above my central estimate. I accept that revenue-mix-weighted comps are a useful sensitivity but reject them as the primary methodology because they require subjective judgments about forward mix that can be gamed to produce any desired answer. I add the mix-weighted sensitivity as a cross-check.

### 2. EV/EBITDA Distorted by Xilinx Amortization (GAAP/Non-GAAP)
**Verdict: Accept**

The Sector Analyst raises a critical data quality issue: if AMD's EBITDA is calculated on a GAAP basis (including ~$2.8B/year in Xilinx amortization) while peers' EBITDA uses non-GAAP, the comparison is systematically biased against AMD. On a non-GAAP basis, AMD's EV/EBITDA drops from 24.6x to approximately 18-19x, which is below the comp median. I accept that the comps table must standardize all multiples on the same basis. I revise to use non-GAAP EBITDA consistently across the comp set, which reduces AMD's apparent EV/EBITDA premium and shifts the metric from "overvalued" to "fairly valued to modestly cheap."

### 3. Segment-Level PEG Analysis
**Verdict: Partially Accept**

A segment-level PEG decomposition (AI GPU growing >60% vs. Gaming declining) would sharpen the valuation signal. The concept is sound but data availability is limited — AMD does not disclose segment-level EPS, making a true segment PEG impossible without material assumptions. I note the suggestion as analytically valuable but impractical with available data. [DATA GAP: No segment-level EPS disclosure.]

---

## Response to Devil's Advocate's Critique

### 1. PEG Is Backward-Looking Fantasy
**Verdict: Partially Accept**

The Devil's Advocate makes the strongest version of the PEG critique: no semiconductor company has sustained 55% EPS growth for 5 years at AMD's scale, and the figure embeds unshipped products and unproven software adoption. The NVIDIA analog (50% CAGR from FY2020-FY2025) started from a smaller base ($10.9B) and with a monopoly (CUDA) that AMD does not possess. I accept that the trailing PEG of 0.51x overstates the growth signal and revise the primary PEG reference to a forward estimate: at 30% forward CAGR, the PEG is 0.95x (near comp median); at 35%, the PEG is 0.82x (modest discount). The trailing PEG is reclassified as historical context.

### 2. Quality Should Be a Binding Constraint When ROIC < WACC
**Verdict: Reject**

The Devil's Advocate proposes capping the composite score at the quality percentile when ROIC < WACC, which would reclassify AMD as a "value trap." This is an intellectually provocative framework but mechanically flawed for two reasons. First, as multiple analysts note, AMD's GAAP ROIC of 6.6% is depressed by Xilinx goodwill — the tangible ROIC is ~18%, which exceeds most reasonable WACC estimates (even the DCF's 16%). Second, ROIC < WACC is common for companies in the investment phase of a growth cycle (Amazon's ROIC was below WACC for years during its AWS buildout). The appropriate test is whether incremental ROIC on new investments exceeds WACC, not whether blended ROIC on legacy acquisitions does. AMD's incremental returns on data center investments appear well above cost of capital given 50%+ GPU gross margins.

### 3. Comp Set Needs Historical "NVIDIA Challenger" Analogs
**Verdict: Reject**

Comparing AMD to Intel Habana or Qualcomm Centriq is a false equivalence. Habana had zero market share when acquired; Centriq was a from-scratch ARM server chip with no ecosystem. AMD has 33.9% x86 server share, existing hyperscaler relationships, and $12.4B in trailing data center revenue. AMD is an incumbent semiconductor company expanding into adjacent markets, not a startup challenger. Historical failure analogs apply to companies entering from zero, not to companies leveraging existing design wins and manufacturing relationships.

---

## Response to Forensic Analyst's Critique

### 1. NTM EBITDA Unclear on GAAP vs. Non-GAAP Basis
**Verdict: Accept**

The Forensic Analyst correctly identifies that the $12,500M NTM EBITDA figure does not specify its basis, and that AMD's GAAP/non-GAAP gap ($4.08B in operating income) is larger than most peers'. This is a legitimate data quality issue. I accept this critique and will standardize all comp multiples on a non-GAAP basis, consistent with how consensus estimates are typically reported. On non-GAAP EBITDA, AMD's multiple drops materially, as noted in my response to the Sector Analyst.

### 2. ROIC Distorted by Goodwill
**Verdict: Accept**

Same response as the Competitive and Credit Analyst critiques. Dual ROIC presentation accepted.

### 3. Standardize GAAP/Non-GAAP Across Comp Set
**Verdict: Accept**

The Forensic Analyst's point that AMD's non-GAAP adjustments are ~36% of non-GAAP EPS (versus much smaller gaps for NVIDIA and peers) means that inconsistent basis inflates AMD's apparent valuation relative to peers. I accept standardizing all comp table multiples on the same basis with explicit disclosure of the chosen methodology.

---

## Response to Sentiment Analyst's Critique

### 1. Comp Set Doesn't Capture AMD's Repositioning as AI Infrastructure
**Verdict: Partially Accept**

The Sentiment Analyst argues that management's communication strategy is explicitly designed to earn a growth multiple, not a semi multiple. This is an astute observation about how management narrative shapes investor perception. However, comps analysis should be based on what a company is (by revenue, margins, end markets), not what management says it is becoming. AMD generates 50% of revenue from data center, 27% from client, and 23% from gaming/embedded — this is a diversified semiconductor company by any objective measure. I accept noting the management narrative as context for why the market may assign a premium to AMD, but reject recomposing the comp set based on aspirational positioning.

### 2. Present Comp Analysis at Both Current and Target Margins
**Verdict: Accept**

Consistent with my response to the DCF Analyst, I accept presenting dual-margin EV/EBITDA scenarios. The current-margin scenario ($162 at 27%) represents the "show me" valuation; the target-margin scenario ($196-207 at 32.5-35%) represents the "thesis works" valuation.

### 3. Weight PEG More Heavily Based on Management Confidence
**Verdict: Reject**

Weighting a quantitative metric based on qualitative management tone introduces subjectivity into a framework designed to be objective. The PEG ratio should be weighted based on the reliability of the growth input, not management enthusiasm about it. Management teams are inherently biased toward optimism; the Sentiment Analyst's own work product identifies hedging language in CFO commentary that suggests margin uncertainty. The quant framework should remain independent of management sentiment — that is the Sentiment Analyst's domain.

---

## Response to Research Analyst's Critique

### 1. 55.9% EPS CAGR Is [ESTIMATED] With No Derivation
**Verdict: Accept**

The Research Analyst correctly calls out the lack of a bottom-up derivation for the 55.9% figure. The implied FY2030 EPS of ~$37 (requiring $60B net income, a 9x increase from current levels) is aggressive by any standard. I accept that this figure should be derived transparently: FY2025 non-GAAP EPS of $4.17, consensus NTM EPS of $6.66 (60% growth), and the 5Y CAGR is a backward-looking calculation from FY2020-FY2025, not a forward projection. I revise the presentation to clearly label the 55.9% as trailing 5Y CAGR and add a forward consensus CAGR of approximately 25-35% based on analyst estimates for FY2026-FY2028.

### 2. Heavy Reliance on Tier 4 Aggregator Data
**Verdict: Partially Accept**

The Research Analyst notes that comp multiples from StockAnalysis.com (Tier 4) may vary by 1-2x turns across aggregator sites depending on fiscal year definitions and consensus sources. For the two most impactful comps (NVDA and AVGO), I accept the recommendation to cross-reference against a second source. However, for mega-cap semiconductors with broad analyst coverage, Tier 4 aggregator accuracy is generally within 0.5x turns on forward P/E — sufficient for the directional conclusions in the comps analysis. I flag the data sourcing limitation but do not expect cross-referencing to change the comp median materially.

### 3. Quality Score Disconnect With PEG Conclusion
**Verdict: Partially Accept**

The Research Analyst identifies the core analytical tension: the report simultaneously argues AMD is "significantly undervalued on PEG" and has "the weakest quality metrics." I accept that this tension must be explicitly resolved rather than left as parallel observations. My revised conclusion: AMD is undervalued on a trailing-growth-adjusted basis (PEG), but this signal is substantially weakened when (a) forward growth rates are used (PEG normalizes to ~1.0x), (b) quality discount is applied for below-comp profitability, and (c) GAAP/non-GAAP basis is standardized. The revised assessment is "approximately fairly valued with upside contingent on margin expansion."

---

## Summary of Revisions

| Item | Original | Revised | Impact |
|------|----------|---------|--------|
| PEG Ratio (primary) | 0.51x (trailing 55.9% CAGR) | 0.82-1.0x (forward 25-35% CAGR) | Signal downgrades from "deep value" to "fair to modest discount" |
| ROIC | 6.6% (as-reported only) | 6.6% (reported) + ~18% (goodwill-adjusted) | Quality score improves from 29/100 to ~50-55/100 |
| EV/EBITDA Basis | Ambiguous GAAP/non-GAAP | Standardized non-GAAP across comp set | AMD multiple drops from 24.6x to ~18-19x; moves from "overvalued" to "fairly valued" |
| Warrant Dilution | Flat 80M shares | Scenario-dependent: 0M/100M/160M | Expected value drops from $205 to ~$184 |
| Historical P/E Anchor | 40x (5Y average) | 28-32x (rate-adjusted) | Removes the $266 implied upside reference |
| Blended Estimate Weights | 40% EV/EBITDA, 40% P/E, 20% EV/Rev | 40% EV/EBITDA (non-GAAP), 30% P/E, 15% PEG (capped), 15% EV/Rev | More balanced framework |
| Primary Conclusion | "Fairly valued to modestly undervalued" | "Approximately fairly valued; upside contingent on margin expansion" | Directional shift toward neutral |
| Expected Value | $205 (+7.7% upside) | ~$184-190 (-1% to flat) | Upside signal eliminated |

The most important revisions stem from three interconnected issues raised across multiple critiques: (1) the PEG ratio's reliance on backward-looking growth that is almost certainly unsustainable at 55.9%, (2) the GAAP/non-GAAP inconsistency that overstated AMD's EV/EBITDA premium, and (3) the flat warrant dilution assumption that understated share count in positive scenarios. Correcting all three moves the comps-implied assessment from "modestly undervalued" to "approximately fairly valued," converging with the P/E median signal (28.6x vs. 27.8x) that was already indicating near-parity.

The quality score revision (dual ROIC) partially offsets these downward adjustments by showing that AMD's operational profitability is mid-pack rather than worst-in-class — an important correction that prevents over-penalization for Xilinx acquisition accounting. On balance, AMD is trading close to fair value on comps, with the margin expansion thesis representing the primary source of potential upside and the key unresolved analytical question.

---

*Rebuttals by Quant Analyst, Equity Research Swarm. Pass 2 adversarial review.*
