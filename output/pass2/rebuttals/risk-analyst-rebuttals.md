# Pass 2 Rebuttals -- Risk Analyst
**Date:** 2026-03-09
**Subject:** AMD (Advanced Micro Devices, Inc.)

---

## Response to DCF Analyst's Critique

### Scenario Price Divergence from DCF ($210 EV vs. $154 DCF)
**Verdict:** Partially Accept

The DCF Analyst correctly identifies the $56/share gap between my expected value ($210) and the DCF-derived fair value ($154.07) as the largest inter-analyst disagreement. I accept that the methodology behind my scenario prices should have been more transparent. My Bull ($280), Base ($220), and Bear ($120) scenarios were constructed as market-implied targets blending the DCF output, comps-implied values (Quant Analyst's $207 central estimate), and a judgment overlay on how the market would re-rate AMD under each scenario -- not as standalone DCF outputs. The Base of $220, for example, reflects a scenario where the market assigns a WACC closer to 13-14% (as multiple analysts argue is more appropriate given AMD's evolving revenue mix) rather than the DCF's 16%. That said, the critique is valid that these prices are disconnected from the DCF framework, and presenting them without reconciliation creates confusion. I revise my recommendation: the Director should use the DCF's $154 and comps' $207 as the primary valuation anchors, and treat my $210 expected value as reflecting an implicit view that the DCF's 16% WACC overstates risk. The position sizing and drawdown analysis remain valid regardless of which price target is used.

### Estimated Volatility and Correlation Data
**Verdict:** Accept

The critique that my 55% annualized volatility and all correlation figures are estimated rather than computed is acknowledged in my own report as the primary data limitation. I accept this fully. The downstream impact is real: position sizing recommendations carry false precision when built on estimated inputs. I maintain that the 55% figure is reasonable given AMD's 2.02 beta and the idiosyncratic volatility from mega-deal dependency, but I cannot defend a specific number without actual price data. I accept the suggestion to retrieve historical data and compute realized volatility, beta, and correlation from at least 3 years of daily returns before finalizing position sizing.

### Reconciliation Recommendation
**Verdict:** Accept

I accept that the $56/share divergence must be explicitly addressed for the Director. The resolution is methodological: my risk analysis is designed to answer "given a range of outcomes, how should you size the position?" while the DCF answers "what is AMD worth today?" These are complementary, not competing, frameworks. The DCF's $154 should be the valuation anchor; my contribution is the risk overlay (drawdown frequency, breakeven bear probability, Kelly sizing) applied to whatever price target the Director selects.

---

## Response to Quant Analyst's Critique

### Sharpe Ratio Internal Inconsistency
**Verdict:** Accept

The Quant Analyst identifies a genuine arithmetic inconsistency: using my stated inputs of 10.3% expected return, 4.15% risk-free rate, and 55% volatility, the Sharpe ratio should be (10.3% - 4.15%) / 55% = 0.11, not the 0.19 I reported. The 0.19 figure was derived from the portfolio-math.py output, which appears to have used the scenario-based upside/downside ratio rather than the traditional Sharpe formula. I accept this error. The corrected Sharpe of 0.11 is even worse than reported, reinforcing rather than changing the practical conclusion: AMD's risk-adjusted return is poor at current prices. The Quant Analyst's broader point about forward-looking volatility (35-40% if contracted revenue reduces uncertainty) is valid in theory, but I would not apply it until mega-deal revenue actually materializes in financial results. Using backward-looking volatility is conservative but appropriate for a pre-catalyst position.

### Bull Case Reconciliation ($280 vs. $260 Comps vs. $223 DCF)
**Verdict:** Partially Accept

I accept that my $280 bull case is the most aggressive of the three analyst estimates and should be reconciled. The $280 implies 33.6x NTM P/E, which the Quant Analyst correctly notes would require both margin expansion to 35%+ and flawless mega-deal execution. I would revise the bull case to $260 (consistent with the Quant Analyst's comps-derived bull) and reduce probability from 25% to 20%. This revision lowers my expected value from $210 to approximately $198, narrowing the gap with both the DCF ($154) and comps ($207) estimates. The practical impact on position sizing is modest: Quarter Kelly moves from 9.9% to approximately 8.5%.

---

## Response to Competitive Analyst's Critique

### Mega-Deal Concentration and Correlated Attrition Risk
**Verdict:** Partially Accept

The Competitive Analyst raises an important point: treating OpenAI and Meta as independent customer risks understates the true concentration exposure because both are developing custom ASICs on similar 3-5 year timelines, creating correlated attrition risk. I accept the framing that the relevant risk is not "lose one customer" but "both customers reduce purchases simultaneously as their ASIC programs mature." However, I partially reject the implied timing. The mega-deal warrant structures vest on deployment milestones, meaning customers must physically install AMD GPUs at scale before ASICs arrive. This creates a 2-3 year window (2026-2028) where GPU volumes are contractually supported even as ASIC development proceeds. The correlated attrition risk is real for FY2029-2030 but overstated for the near-term investment horizon. I revise my recommendation to explicitly model a "correlated attrition" scenario for the 2029-2030 period with 30-40% probability, separate from the near-term execution risk.

### Asymmetric Volatility (Upside ~45%, Downside ~65%)
**Verdict:** Accept

The suggestion to decompose symmetric 55% volatility into asymmetric upside (~45%) and downside (~65%) components is well-founded. AMD's upside is constrained by the CUDA ecosystem ceiling and ASIC cannibalization risk, while downside is uncapped in a mega-deal failure or AI demand correction scenario. This asymmetry is consistent with the asymmetric beta I documented (2.4x in 2022 selloffs vs. 2.02 average) and would improve the accuracy of Sortino calculations and downside-focused position sizing. I accept this framework and note it further supports conservative sizing: the vol-adjusted weight using 65% downside volatility would be approximately 1.7% rather than 2.2%.

### TSMC CoWoS Allocation as Top-5 Risk
**Verdict:** Accept

I accept that CoWoS allocation should be elevated to a top-5 risk factor. My analysis focused on demand-side risks (mega-deal execution, CUDA gap, AI demand cycle) while underweighting the supply-side constraint. The Sector Analyst's data showing AMD at 8-10% of CoWoS capacity vs. NVIDIA at 60% represents a binding physical constraint on AMD's AI GPU ramp regardless of demand. I would add this as a discrete risk with 20-30% probability and -15-25% price impact, consistent with the Competitive Analyst's recommendation.

---

## Response to Macro Analyst's Critique

### Scenario Probabilities Too Generous Given Macro Environment
**Verdict:** Partially Accept

The Macro Analyst argues that my 25/50/25 bull/base/bear distribution is too generous given the Hormuz crisis, delayed rate cuts, and the 26x AI capex-to-revenue ratio. The joint probability calculation (0.70 x 0.50 x 0.75 = 26% probability everything goes right) is a valid framework. However, I note that my bull case does not require all three factors to resolve favorably -- it requires AMD-specific execution (MI450 ramp) and continued AI demand, which are partially independent of macro factors. The Hormuz crisis and rate cuts primarily affect the multiple, not AMD's ability to ship GPUs. That said, I accept that the current macro environment tilts probabilities more bearish than my symmetric 25/50/25 distribution implies. I would revise to 20/50/30 (Bull/Base/Bear), which reduces expected value from $210 to approximately $198 and narrows the breakeven bear probability from 41% to approximately 36%. The practical sizing recommendation is unchanged: quarter-Kelly at the revised scenarios produces approximately 8% maximum allocation.

### Volatility Estimate and "Provisional" Label
**Verdict:** Accept

I accept the suggestion to label all position sizing outputs as "provisional" pending actual options data retrieval. The Macro Analyst is correct that if actual volatility is 65-70% (plausible given the Hormuz crisis and recent drawdown dynamics), the quarter-Kelly recommendation of 9.9% could be excessive. At 65% vol, quarter-Kelly drops to approximately 7%. I revise my output to present position sizing as a range (7-10% quarter-Kelly) rather than a point estimate.

### Stress-State Correlation Emphasis
**Verdict:** Accept

The critique that asymmetric beta (2.4x realized in 2022 selloffs) is buried rather than prominently featured is fair. I accept the recommendation to make stress-state correlations a headline finding. AMD functions as a leveraged market bet during macro stress periods, and the vol-adjusted weight of 2.2% already reflects this implicitly, but the rationale should be stated explicitly: AMD offers essentially zero diversification benefit in the scenarios where diversification matters most.

---

## Response to Catalyst Analyst's Critique

### MI450 Delay Probability Adjustment (20-25% to 15-20%)
**Verdict:** Partially Accept

The Catalyst Analyst argues that my 20-25% delay probability is too generic because MI450 has three specific de-risking factors: TSMC N3 maturity, pre-committed customer volumes, and the Helios rack demonstration. I accept that these factors reduce delay risk relative to a generic new-node ramp. However, the Sector Analyst's critique provides a useful counterpoint: the binding constraint is not the logic node but CoWoS advanced packaging and HBM4 supply, where delay risk may be higher (25-35%). Balancing the Catalyst Analyst's de-risking factors against the packaging-specific risk, I revise to 20% overall delay probability (down from 22.5% midpoint), decomposed as: 10% node risk, 25% packaging risk, 20% HBM4 risk, with partial overlap. This revision modestly increases expected value by $3-5/share.

### Time-Varying Sharpe Ratio
**Verdict:** Partially Accept

The suggestion to present time-conditional Sharpe ratios (poor pre-catalyst, improving post-catalyst) is theoretically sound. The Sharpe ratio does improve dramatically if MI450 confirmation resolves uncertainty and compresses volatility. However, a time-varying Sharpe framework implicitly recommends market timing, which introduces its own risk. I partially accept: I will present a pre-catalyst Sharpe (0.08-0.12, reflecting current uncertainty) and a post-catalyst Sharpe (0.20-0.30, assuming MI450 confirms and volatility compresses to 40%), but maintain that the sizing recommendation should be based on the current, pre-catalyst Sharpe to avoid anchoring to a favorable scenario that has not yet materialized.

### Breakeven Bear Probability Endorsement
**Verdict:** Noted with appreciation. The Catalyst Analyst's affirmation that the 41% breakeven bear probability is "the single most useful risk metric" validates this framework as the primary risk communication tool for the Director.

---

## Response to ESG & Governance Analyst's Critique

### Governance Tail Risk on Warrant Expansion
**Verdict:** Accept

The ESG Analyst correctly identifies that my breakeven bear probability of 41% does not incorporate the possibility of additional "equity-for-demand" deals beyond the current 320M warrants. If AMD signs additional warrant packages bringing total potential dilution to 400-500M shares (30%+ of current outstanding), the bear case severity increases and the breakeven bear probability drops from 41% to approximately 35%. I accept this as a valid risk factor that should be explicitly modeled. The precedent-setting nature of the warrant issuance -- without shareholder approval and without a disclosed cap -- creates open-ended dilution risk that traditional risk frameworks miss. I add this as a "governance tail risk" scenario with 20% probability, partially correlated with the bull case (since additional deals would likely occur only if MI450 succeeds).

### Lisa Su Key-Person Risk as Discrete Factor
**Verdict:** Accept

The ESG Analyst's suggestion to model key-person risk as a discrete event (5% annual probability, -15% impact, cumulative 23% probability over 5 years) is well-constructed. I accept this addition. The expected annual drag of approximately 0.75% from key-person risk reduces the 5-year expected return by 3-4 percentage points, pushing the Sharpe from 0.11 (corrected) to approximately 0.08. This further supports the conclusion that position sizing, not direction, is the binding constraint.

### Stress Volatility at 75% (2022 Analog)
**Verdict:** Partially Accept

The suggestion to use AMD's 2022 realized volatility (~75%) as the stress-case input rather than my estimated 55% is directionally correct but represents a tail scenario, not a base case. I accept that 55% may understate current-regime volatility and would adopt 60-65% as the stress-adjusted estimate (consistent with the Competitive Analyst's asymmetric downside vol suggestion of 65%), but 75% reflects the 2022 rate shock period which was AMD's most volatile episode in a decade. Using 75% as the base case would be overly conservative; using it as a stress scenario within the drawdown analysis is appropriate.

---

## Response to Technical Analyst's Critique

### Base Case of $220 Lacks Technical Support
**Verdict:** Partially Accept

The Technical Analyst argues that a $220 base case (+15.5%) assigns 50% probability to reclaiming the 200-day moving average ($228), for which there is no current technical evidence. This is a fair challenge. My base case reflects a 12-month fundamental view (MI450 ramp, continued EPYC share gains, data center growth) that is not yet supported by price action. I accept that in the near term (3-6 months), the technical picture makes $220 less probable than my distribution implies. However, over a 12-month horizon, the fundamental catalysts in H2 2026 could generate the reversal the Technical Analyst notes is absent today. I maintain $220 as the 12-month base case but accept the Technical Analyst's implicit point that a 3-month expected value would be materially lower. For immediate position sizing, the vol-adjusted weight of 2.2% (which the Technical Analyst considers appropriate) is the right constraint.

### Realized Volatility Higher Than Estimated
**Verdict:** Accept

The Technical Analyst's calculation that the -28% decline over 4.3 months implies approximately 47% annualized downside realized vol is a useful data point. Combined with upside moves, total realized vol is likely 60-70%, not my estimated 55%. I accept this correction and note it aligns with the Competitive Analyst's asymmetric vol framework (upside ~45%, downside ~65%) and the Sector Analyst's Parkinson estimator calculation (approximately 75% from the 52-week range). I revise my central volatility estimate to 60-65%, which reduces the vol-adjusted weight from 2.2% to approximately 1.8-2.0% and the quarter-Kelly from 9.9% to approximately 7-8%.

### Technically-Adjusted Position Size
**Verdict:** Partially Accept

The suggestion to reduce the initial position from 2.2% to 1.0-1.5% with scaling rules tied to technical confirmation levels ($185 hold, $200 reclaim, $228 MA reclaim) is constructive. I accept the phased entry framework as superior to a static allocation. However, I reject 1.0% as the starting position -- at that level, the position is too small to be meaningful even if the thesis plays out. I would set the initial position at 1.5% with scaling to 2.5% on $200 reclaim and 3.5% on MI450 confirmation, consistent with the Catalyst Analyst's phased entry recommendation.

---

## Response to Sector Analyst's Critique

### MI450 Delay Risk Decomposition (Node vs. Packaging vs. HBM4)
**Verdict:** Accept

The Sector Analyst provides a superior decomposition of MI450 delay risk: 10% node risk (TSMC 3nm is mature), 25% packaging risk (CoWoS binding constraint), 20% HBM4 supply risk. This is more analytically rigorous than my generic "20-25% based on industry precedent" and correctly identifies packaging as the binding constraint. I adopt this decomposition and note it changes the risk mitigation analysis: node risk is largely resolved, but packaging and HBM4 risks require monitoring of TSMC capacity expansion announcements and Samsung/SK Hynix HBM4 qualification timelines. This also connects to the Competitive Analyst's recommendation to add CoWoS allocation as a top-5 risk factor.

### Volatility Estimate via Parkinson Estimator
**Verdict:** Partially Accept

The Sector Analyst's Parkinson estimator calculation (ln(267/76.48) / (2 x sqrt(ln(2))) = ~75% annualized) is a useful upper-bound estimate, but the 52-week range of $76.48-$267.08 includes the April 2025 tariff crash low, which was a brief tail event rather than a sustained volatility regime. Using the more recent range ($190-$267 over the last 5 months) produces a Parkinson estimate of approximately 45-50%, and using the full range including the tariff crash produces 75%. The truth is likely between these: 55-65% annualized, consistent with my revised estimate of 60-65%. I accept the Parkinson framework as a useful cross-check but would not adopt the 75% figure as the central estimate.

### Sector-Specific Risk Decomposition
**Verdict:** Accept

The recommendation to decompose AMD's risk into (1) broad market/beta, (2) semiconductor sector (SOX), and (3) AMD-specific idiosyncratic risk is analytically superior to my blended single-beta approach. This decomposition would enable the portfolio manager to hedge sector risk via SOX puts separately from AMD-specific risk, optimizing the risk budget. I accept this as an improvement to the risk framework, though implementation requires the historical price data that was not retrieved in Pass 1.

---

## Response to Devil's Advocate's Critique

### Bear Probability Underestimate (25% vs. DA's 30-35%)
**Verdict:** Partially Accept

The Devil's Advocate makes the strongest argument against my 25% bear probability using a joint probability framework: if each of five critical assumptions has 60% confidence, the probability of all five holding is only 7.8%. This is mathematically correct under independence, but the assumptions are not independent -- EPYC server share gains, for example, do not depend on MI450 success. I partially accept: the bear probability should be higher than 25% to reflect the fragility of a thesis requiring multiple assumptions to hold simultaneously. However, 30-35% is the DA's explicitly contrarian estimate. I revise to 28-30%, which reduces expected value from $210 to approximately $195-200 (before the bull case revision noted above). Combined with the bull case reduction ($260 at 20%), my revised expected value is approximately $190-195, essentially flat to the current price. This changes my assessment from "modestly favorable risk-reward" to "roughly neutral risk-reward with significant volatility."

### Warrant Dilution Asymmetry (Revenue Loss + Permanent Dilution)
**Verdict:** Accept

The Devil's Advocate's insight that AMD faces asymmetric downside -- revenue loss from failed mega-deals PLUS permanent dilution from warrants that vested on early deployment milestones -- is a risk factor I did not adequately model. In the bear case, AMD could lose $50-100B in potential revenue while retaining 5-10% dilution from early vesting, meaning shareholders suffer both the revenue shortfall and the equity dilution. I accept this and revise my bear case target from $120 to $110-115 to account for the dilution overhang in a failed-thesis scenario. This worsens the breakeven bear probability from the revised ~36% to approximately 33%.

### Position Sizing as the Critical Lever
**Verdict:** Noted with appreciation. The DA's endorsement of "position sizing, not stock selection, is the critical risk lever" as the most pragmatic insight validates the core contribution of the risk analysis.

---

## Response to Forensic Analyst's Critique

### Estimated Volatility Built on Sand
**Verdict:** Accept

The Forensic Analyst's critique that a risk analysis built on estimated volatility is "like a credit analysis built on estimated financial statements" is apt. I fully accept the characterization and the recommendation to present all risk metrics as ranges rather than point estimates. My revised presentation: Quarter Kelly 6-10% (estimated, pending actual vol data); vol-adjusted weight 1.5-2.5%; Sharpe 0.06-0.15. The Forensic Analyst is correct that the precision of figures like "39.52% Full Kelly" is illusory when the underlying volatility input has a 20pp uncertainty range.

### Expected Value Divergence from DCF
**Verdict:** Accept

The Forensic Analyst independently raises the same $210 vs. $154 divergence flagged by the DCF and Research Analysts. I accept this critique in full, as addressed in my DCF Analyst response above. The recommendation that the Director should average both models (producing approximately $182, or -4.4%) is a reasonable synthesis approach, and I note it aligns closely with the Devil's Advocate's $178 (-6.5%) estimate.

### Scenario Prices as Ranges, Not Points
**Verdict:** Accept

I accept the recommendation to present scenarios as ranges. Revised framework: Bull $240-280 (20% probability), Base $190-220 (50%), Bear $100-130 (30%). This produces an expected value range of $175-210, with a central estimate of approximately $192 -- essentially flat to the current price. This is a more honest representation of the analytical uncertainty than my original point estimates.

---

## Response to Sentiment Analyst's Critique

### MI450 Delay Probability and Management Tone
**Verdict:** Partially Accept

The Sentiment Analyst argues that Lisa Su's confidence on MI450 ("on track," "very doable ramp") should be tempered by the observation that she pivoted to assertion rather than evidence when questioned, and that her uncharacteristic "BS" response to SemiAnalysis reveals discomfort. I accept that management tone analysis is a legitimate input to delay probability assessment. The Sentiment Analyst's suggestion to push delay probability to the higher end (25-30%) based on the confidence-without-evidence pattern is reasonable. Combined with the Sector Analyst's decomposition (packaging is the binding constraint, not the node), I maintain my revised estimate of 20-22% overall delay probability, which already reflects the de-risking factors while acknowledging packaging-specific risk. The "BS" response is ambiguous -- it could indicate the report is genuinely wrong or that it hit a nerve -- and I would not shift the estimate based on a single word choice.

### Management Credibility Risk Factor
**Verdict:** Accept

The suggestion to add a "management credibility risk" factor reflecting Lisa Su's shift from conservative to ambitious guidance is valid. The shift to >60% DC CAGR and >$20 EPS targets raises the bar for future beats, creating asymmetric downside if any target is missed. I accept this as an additional risk factor that increases the expected drawdown in the base case by 5-10 percentage points. This is consistent with the Technical Analyst's observation that the market has stopped rewarding beats (Q4: +23% EPS beat, -17% stock reaction).

### Post-Earnings "Beat and Fade" as Volatility Calibration
**Verdict:** Accept

Using the -17% post-earnings reaction to a 23% EPS beat as a calibration point for asymmetric downside risk is a valuable insight. If AMD drops 17% on good news, the implied reaction to bad news (MI450 delay, mega-deal disappointment) could be 25-35%. I accept this as supporting higher downside volatility estimates (65%+) and note it reinforces the phased entry strategy over a static allocation.

---

## Response to Research Analyst's Critique

### Estimated Volatility and Historical Data Gap
**Verdict:** Accept

The Research Analyst echoes the universal critique about estimated volatility and correlation data, noting that the data gap cascaded from the Research Analyst's own tool failures. I accept fully and note that the Research Analyst's suggestion to retrieve data via WebSearch (Yahoo Finance downloadable CSV) should be prioritized for any revision. The Parkinson estimator and limited price points ($267 ATH, $190 current, $76.48 52-week low) provide some cross-validation, but computed realized volatility from daily returns would materially improve all downstream risk metrics.

### Reconciliation with DCF Expected Value
**Verdict:** Accept

As addressed in multiple rebuttals above, I accept the need to reconcile my $210 expected value with the DCF's $154. My revised expected value range of $175-210 (central ~$192) largely resolves this divergence and aligns with the consensus view across analysts.

---

## Response to Model Builder's Critique

Note: The Model Builder's critique file addressed MSFT, not AMD. No AMD-specific critique of the Risk Analyst was identified from the Model Builder. If critiques were intended for AMD, they were not available in the critique files reviewed.

---

## Summary of Revisions

Based on the cross-critique process, I revise the following:

| Parameter | Original | Revised | Driver |
|-----------|----------|---------|--------|
| Bull case price | $280 | $240-260 | Quant Analyst comp reconciliation |
| Bull probability | 25% | 20% | Macro, DA adjustments |
| Base case price | $220 | $190-220 | Technical Analyst, Forensic realism check |
| Bear case price | $120 | $100-130 | DA warrant dilution asymmetry |
| Bear probability | 25% | 28-30% | DA fragility framework, macro headwinds |
| Annualized volatility | ~55% | 60-65% | Technical, Sector, Competitive analysts |
| Expected value | $210 | ~$192 (range $175-210) | Multiple reconciliation |
| Sharpe ratio | 0.19 | 0.06-0.12 (corrected formula) | Quant Analyst arithmetic check |
| Quarter Kelly | 9.9% | 6-10% (range) | Volatility revision, range presentation |
| Vol-adjusted weight | 2.2% | 1.5-2.0% | Volatility revision, asymmetric vol |
| Drawdown Risk Score | 8/10 | 8/10 (unchanged) | Still appropriate given history |
| Breakeven bear probability | 41% | 33-36% | DA, ESG governance tail risk |
| MI450 delay probability | 20-25% | 20-22% | Sector decomposition, Catalyst de-risking |

**Revised Risk Assessment:** AMD moves from "modestly favorable risk-reward" to "approximately neutral risk-reward with extreme volatility." The position remains positive expected value at the revised central estimate, but the Sharpe ratio of 0.06-0.12 means investors are very poorly compensated for the volatility they absorb. Position sizing constraint is the dominant recommendation: 1.5-2.0% initial allocation with phased scaling tied to MI450 confirmation and technical reversal signals.

---

*Rebuttals by Risk Analyst, Equity Research Swarm. Pass 2 adversarial review.*
