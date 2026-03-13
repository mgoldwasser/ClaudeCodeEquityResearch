# Targeted Debate #2: META CapEx ROI — Will $125B Generate Adequate Returns?

**Date:** 2026-03-13
**Participants:** DCF Analyst, Industry Analyst, Risk & Contrarian Analyst
**Moderator:** Director of Research
**Status:** PARTIALLY RESOLVED — revised numbers agreed on 3 of 5 questions; 2 flagged as Key Unresolved Risk

---

## The Disagreement

META is committing $115-135B in FY2026 CapEx — the largest single-year infrastructure investment by any company in history. The three analysts disagree fundamentally on whether, when, and how this investment generates adequate returns.

| Dimension | DCF Analyst | Industry Analyst | Risk & Contrarian |
|-----------|-------------|-----------------|-------------------|
| CapEx/Revenue by 2030 | 16.3% | Implicit ~14-18% (via TAM expansion) | 22%+ (bear case: never normalizes) |
| Cloud analogy validity | Partially valid | Strongly valid (90% cost decline, 40x spending) | Invalid — Meta lacks B2B cloud revenue |
| Revenue streams justifying CapEx | Core ad improvements + gradual new monetization | $83B probability-weighted incremental TAM by 2030 | Unproven; "personal superintelligence" = metaverse 2.0 |
| P(inadequate ROI within 3 years) | ~25% (bear case probability) | ~15-20% | 25-30%, possibly higher |
| How to price the uncertainty | Elevated beta (1.25) + company-specific risk premium (0.5%) | Through terminal value range + scenario probabilities | Higher bear probability (30%) + lower base case price |

---

## Question 1: What Is the Right CapEx/Revenue Ratio by 2030?

### DCF Analyst — Position: 16.3%

**Best evidence:** Management has explicitly guided FY2026 as peak CapEx. Historical CapEx/revenue was 20-23% in FY2023-24 (pre-AI era). My 16.3% terminal assumption is actually *below* the pre-AI baseline, which I justify through two mechanisms: (1) MTIA custom silicon targeting 40-44% TCO reduction vs. merchant GPUs — this structurally lowers the cost of maintaining compute capacity, and (2) revenue grows faster than maintenance CapEx as the AI infrastructure buildout completes. The growth CapEx component ($107B in FY2026) declines to $46B by FY2030 as Phase 1 AI clusters come online. Maintenance CapEx grows modestly from $18B to $24B with the asset base.

**Weakest point in opponents' arguments:**
- *Industry Analyst:* The $83B incremental TAM by 2030 is probability-weighted, but the probabilities are generous. WhatsApp Commerce at 55% probability and Meta AI Subscription at 45% probability are pre-commercial products with no revenue base. Applying 55% probability to a $42B midpoint outcome yields $23B in "expected" revenue from a product generating ~$2B today. This is aspiration, not analysis.
- *Risk & Contrarian:* The bear case CapEx/revenue of 22%+ treats the *guidance* (peak in FY2026) as non-credible, despite management's track record of delivering on operational commitments since the 2023 "Year of Efficiency." Zuckerberg called 2023 the year of efficiency and delivered: headcount dropped from 87K to 67K, operating margin expanded from 25% to 41%. The CapEx normalization guidance deserves similar credibility weight.

**Proposed resolution:** 16-18% by FY2030. The 16.3% base case is defensible but should carry a wider confidence interval. If I concede upside to the maintenance CapEx estimate (AI infrastructure refresh cycles may be shorter than traditional server life, requiring more frequent replacement), the range is 16-18%. Below 16% requires the bull case (MTIA exceeding targets + aggressive depreciation schedule). Above 18% requires the bear case (CapEx never fully normalizes).

### Industry Analyst — Position: Implicit 14-18% (via TAM expansion)

**Best evidence:** The CapEx/revenue ratio is a *fraction* — both numerator and denominator matter. My analysis shows Meta's true addressable market is ~$430-480B by 2030, not the $202-306B narrow social media definition. The bottom-up application-level decomposition identifies $83B in probability-weighted incremental revenue by 2030 from five new application waves (AI creative automation, WhatsApp commerce, Meta AI subscription, AR advertising, Llama enterprise). If Meta captures even half of this incremental TAM, FY2030 revenue is $460-480B, and CapEx/revenue at $70B CapEx would be ~15%.

The cloud computing analogy is the critical framework. Cloud costs fell ~90% from 2008 to 2018 (AWS pricing cuts), yet total cloud spending grew ~40x because demand elasticity overwhelmed cost efficiency. Meta's AI CapEx follows the same pattern: better AI targeting reduces cost-per-conversion, but this *increases* advertiser willingness to spend (Jevons paradox). Evidence is already visible — FY2025 price per ad grew +9% while impressions grew +12%, meaning *both* volume and pricing expanded simultaneously. Advantage+ advertisers report 40%+ ROAS improvement. This is not speculative; the flywheel is already turning.

WhatsApp is the largest swing variable. 3.3B users with near-zero monetization vs. WeChat's ~$10B from 1B users. Click-to-WhatsApp grew +60% YoY in Q3 2025. Even at modest monetization (1/3 of WeChat's per-user revenue), WhatsApp contributes $33B by 2030. At full WeChat parity: $60B+. The range is $10-60B, and this single variable changes the CapEx/revenue ratio by 2-4 percentage points.

**Weakest point in opponents' arguments:**
- *DCF Analyst:* The revenue build shows FoA advertising decelerating from 22% to 8% by FY2030, which assumes the current Advantage+ momentum is a one-time step-function rather than a sustained re-acceleration. The historical analogue of programmatic advertising (2013-2016) showed 3-4 years of re-accelerated growth before normalization. We are only in year 2 of the AI ad re-acceleration. Using an S-curve deceleration model starting *now* is premature.
- *Risk & Contrarian:* The comparison to Google/Amazon/Microsoft B2B cloud revenue misframes Meta's AI investment thesis. Meta is not building cloud infrastructure to sell compute — it is building AI infrastructure to improve its existing $196B advertising engine. The ROI metric is not "cloud revenue generated" but "incremental ad revenue per dollar of AI CapEx." At $196B FY2025 ad revenue, even a 5% improvement in ad efficiency from AI = $10B incremental revenue annually, which at 80% gross margin generates $8B in gross profit. That alone justifies $30-40B in annual AI CapEx at a 5-year payback.

**Proposed resolution:** 15-18% by FY2030, with the range determined by WhatsApp monetization outcome. If WhatsApp reaches $25B+ by 2030 (my base case), CapEx/revenue falls to 15-16%. If WhatsApp monetization disappoints (<$10B), CapEx/revenue stays at 17-18%. Both are within the DCF Analyst's framework. The key disagreement is not the CapEx path — it is the *revenue* path.

### Risk & Contrarian Analyst — Position: 22%+ (bear case)

**Best evidence:** The "CapEx normalizes" narrative requires three assumptions that are each independently uncertain and collectively fragile:

1. **The AI compute buildout has a definable endpoint.** It does not. Unlike a factory or data center for a known workload, AI infrastructure requirements are *open-ended*. Each new model generation (Llama 5, 6, ...) requires more compute. Meta's shift from open-source to closed-source AI (post-Llama 4 benchmark scandal) suggests the competitive pressure to build bigger clusters will *intensify*, not abate. DeepSeek and other efficient-architecture competitors create an arms race dynamic: Meta must spend to avoid falling behind.

2. **MTIA custom silicon delivers 40-44% TCO reduction.** This is management's claim, unverified by independent benchmarks. The Llama 4 benchmark manipulation — confirmed by Yann LeCun himself — demonstrates that Meta's AI team has a documented pattern of overstating capabilities. Why should we take MTIA TCO claims at face value?

3. **Revenue growth outpaces CapEx growth.** This requires the Jevons paradox to dominate supply-side deflation. But Meta's AI CapEx is *not* primarily about serving ads more efficiently — management's stated vision is "personal superintelligence" (Zuckerberg, Q4 2025 earnings call). This echoes the metaverse pivot framing almost exactly. In 2021, Zuckerberg described the metaverse as "the next major computing platform." In 2025-2026, he describes AI as enabling "personal superintelligence." Both are grand visions that justify unlimited CapEx with no measurable ROI timeline.

**The B2B revenue gap is real.** Google, Amazon, and Microsoft all monetize their AI infrastructure through cloud revenue (GCP, AWS, Azure). Meta has *no* equivalent B2B revenue stream. Llama open-source has no direct monetization. When Google spends $75B on AI CapEx, ~30-40% is directly monetizable through cloud compute sales. When Meta spends $125B, 100% must be justified through advertising improvements — a single, cyclical revenue stream.

**Weakest point in opponents' arguments:**
- *DCF Analyst:* The "Year of Efficiency" comparison is misleading. In 2023, Zuckerberg cut headcount — a straightforward cost reduction with immediate P&L benefit. CapEx normalization requires a *strategic* decision to slow infrastructure investment, which conflicts with the AI arms race narrative. Cutting headcount is easy; deciding to build fewer data centers while competitors build more is a fundamentally different decision with strategic risk.
- *Industry Analyst:* The Jevons paradox / cloud analogy conflates two different market structures. Cloud computing created entirely new workloads (SaaS, streaming, IoT) that did not exist before. Meta's AI CapEx primarily improves an *existing* product (ad targeting) for *existing* customers (advertisers). The incremental demand from "AI makes ads cheaper to create" is real but bounded — you cannot make an advertiser spend 10x more just because ad creation costs fell to zero. The WhatsApp $33-60B projection extrapolates WeChat's model to Western markets where users have fundamentally different relationships with messaging apps (no super-app culture, no integrated payments infrastructure, regulatory barriers to financial services).

**Proposed resolution:** Model two distinct CapEx paths, not one. Path A (60% probability): CapEx normalizes to 18-20% by FY2030 — above the DCF Analyst's 16% but reflecting ongoing AI investment. Path B (40% probability): CapEx stays at 22-25% of revenue through FY2030 as AI arms race intensifies. The blended expectation: ~20% CapEx/revenue by FY2030. This is materially different from the DCF Analyst's 16% and significantly changes the fair value calculation.

### Director's Resolution — Question 1

**PARTIALLY RESOLVED.** All three analysts agree CapEx/revenue declines from the FY2026 peak of ~49%. The disagreement is on the terminal level.

| Analyst | FY2030 CapEx/Revenue | Implied FY2030 FCF Margin |
|---------|---------------------|--------------------------|
| DCF Analyst | 16% | 34% |
| Industry Analyst | 15-18% | 30-37% |
| Risk & Contrarian | 20% (blended) | 22-28% |

**Revised consensus range: 16-20% by FY2030**, with 18% as the central estimate. This is above the DCF Analyst's 16% base case, reflecting the Risk & Contrarian's valid point that AI compute requirements are open-ended and the "Year of Efficiency" analogy is imperfect. Impact on DCF base case: using 18% instead of 16% reduces FY2030 UFCF from $146B to ~$137B, reducing base case fair value by approximately $40-50/share (from $733 to ~$685-695).

**Action for DCF Analyst:** Revise base case CapEx/revenue to 18% for FY2030. Maintain 16% as bull case and 22%+ as bear case.

---

## Question 2: Is the Cloud Computing Analogy Valid?

### Industry Analyst — The Analogy Holds

Cloud costs fell ~90% over 10 years; total spending grew ~40x. The mechanism was demand elasticity: cheaper compute enabled workloads that previously could not exist (SaaS, streaming, mobile backends, IoT, ML training). Meta's AI CapEx triggers the same dynamic: cheaper, more effective ad targeting enables advertisers who were previously priced out (SMBs), enables new ad formats (AI-generated creative at zero marginal cost), and expands the TAM into messaging and AI-native commerce. The evidence is empirical: Advantage+ at $60B run rate, +40% ROAS improvement, price per ad +9% alongside impression growth +12%.

### Risk & Contrarian — The Analogy Is Flawed

The cloud analogy fails on three dimensions:

1. **New workload creation:** Cloud enabled *entirely new* categories of applications. Meta's AI CapEx improves *existing* applications (better ad targeting). The ceiling on advertising efficiency improvements is lower than the ceiling on new compute workloads.

2. **Revenue model:** Cloud providers monetize compute directly (sell compute hours). Meta must convert compute into advertising improvements, then into advertiser spending increases — a two-step translation with leakage at each step.

3. **Multi-customer base:** Cloud serves millions of diverse customers across industries. Meta's AI infrastructure serves one customer: Meta's own advertising platform. Single-customer infrastructure has higher stranded asset risk.

### DCF Analyst — Middle Ground

The analogy is *partially* valid. The Jevons paradox mechanism (efficiency gains drive demand expansion) is real and already operating in Meta's ad business. But the magnitude is constrained: cloud computing enabled an entirely new computing paradigm, while Meta's AI CapEx optimizes an existing business model. The appropriate analogy is not "AWS creating cloud computing" but "Google improving search quality" — real and valuable, but generating incremental improvement (10-15% annual efficiency gains) rather than paradigm shift (40x growth).

### Director's Resolution — Question 2

**RESOLVED with nuance.** The Jevons paradox mechanism is valid and already operating (evidence: simultaneous price and volume growth in FY2025). However, the *magnitude* of the cloud analogy (40x growth) overstates the applicable dynamic. Meta's AI CapEx is better analogized to Google's search quality investments: high ROI on the core product, incremental rather than transformative. WhatsApp and Meta AI represent the genuine "new workload" potential — but these are pre-commercial, not established.

**Revised framing:** AI CapEx generates measurable ROI on core advertising (high confidence, 5-15% annual efficiency improvement) AND *may* create new revenue streams (low-medium confidence, $10-83B incremental by 2030). The cloud analogy applies to the *potential* new revenue streams, not to the core ad optimization.

---

## Question 3: What Revenue Streams Justify $125B Annual CapEx?

### Quantified Revenue Bridge — All Three Analysts

| Revenue Stream | DCF Analyst FY2030E | Industry Analyst FY2030E | Risk & Contrarian View | Confidence |
|---------------|--------------------|--------------------------|-----------------------|------------|
| Core FoA Advertising (AI-enhanced) | $411,600M | $375-460B (prob-weighted) | $331,000M (bear)-$411,600M | High (existing business) |
| WhatsApp Commerce & Ads | Embedded in FoA (~$5-15B implied) | $55-80B (70% prob) → $38-56B PW | $0-5B (skeptical of WeChat analogy) | Low-Medium |
| Meta AI Subscription | $5-10B (HIGH UNCERTAINTY) | $5-15B (50% prob) → $2.5-7.5B PW | $0 (no evidence of monetization) | Very Low |
| Threads Advertising | Embedded in FoA (~$15-20B implied) | $15-25B (65% prob) → $10-16B PW | Embedded in base ad revenue | Medium |
| Llama Enterprise / API | Not modeled | $5-20B (35% prob) → $2-7B PW | $0 (open-source = no monetization) | Very Low |
| AR/Glasses Advertising | Negligible | $3-10B (30% prob) → $1-3B PW | $0 (pre-commercial) | Very Low |
| **Total FY2030** | **$428,600M** | **~$430-510B (prob-weighted ~$425-450B)** | **$345,000M (bear)** | — |

### The CapEx Justification Test

At $70B FY2030 CapEx (DCF Analyst base case), Meta needs to generate incremental revenue vs. a "no AI CapEx" counterfactual. The question: how much of FY2030 revenue is *attributable* to the AI infrastructure buildout?

**DCF Analyst:** If AI CapEx adds 5-8% to annual ad revenue growth (through better targeting, Advantage+, new formats), that is ~$60-100B in cumulative incremental revenue by FY2030. At 80% gross margin, that is $48-80B in incremental gross profit over 5 years. Against cumulative AI growth CapEx of ~$353B (FY2026-30), the payback is 4-7 years. Marginal, but acceptable for infrastructure with 10-15 year useful life.

**Industry Analyst:** The calculation above understates ROI because it excludes new revenue streams. If WhatsApp, Meta AI, and Threads collectively add $50-80B by FY2030, the incremental gross profit rises to $88-144B over 5 years. Payback: 2.5-4 years. This is a strong ROI.

**Risk & Contrarian:** The counterfactual is impossible to measure. "What would Meta's revenue be without AI CapEx?" is unknowable. Competitors are also spending on AI — Google $75B, Amazon $100B — so Meta must spend to *maintain* position, not just to grow. If the CapEx is defensive (maintaining share) rather than offensive (gaining share), the ROI calculation is fundamentally different: ROI = avoided revenue loss, not revenue gain. Avoided revenue loss is impossible to quantify and creates an infinite CapEx justification loop ("we must spend or we lose").

### Director's Resolution — Question 3

**PARTIALLY RESOLVED.** Core advertising improvements from AI CapEx are quantifiable and positive (5-15% annual efficiency gain). New revenue streams (WhatsApp, Meta AI, Threads) are the swing variable.

**Revised revenue framework:**
- **High confidence ($400-430B FY2030):** Core advertising + Threads + modest WhatsApp. Justifies $65-75B annual CapEx at 5-6 year payback.
- **Medium confidence ($430-470B FY2030):** Above + WhatsApp at $25-40B + some Meta AI revenue. Justifies $70-80B annual CapEx at 4-5 year payback.
- **Low confidence ($470-510B FY2030):** Above + WhatsApp at $50B+ + Meta AI at $10B+ + Llama monetization. Justifies $80B+ CapEx.

**Key insight:** At the high-confidence revenue level ($400-430B), $70B CapEx is justifiable but with thin margins of safety. The bull case for CapEx ROI depends on new revenue streams that are currently pre-commercial. This is the core of the investment risk.

---

## Question 4: Probability That CapEx Does NOT Generate Adequate Returns Within 3 Years?

### Defining "Adequate Returns"

**DCF Analyst definition:** CapEx generates adequate returns if FY2028 UFCF exceeds FY2025 levels ($43.6B) — i.e., the FCF trough recovers within 3 years.

**Industry Analyst definition:** Adequate returns if AI-driven ad revenue growth exceeds what would have occurred without AI investment by >5 percentage points annually (i.e., the investment adds measurable value to ad performance).

**Risk & Contrarian definition:** Adequate returns if incremental revenue attributable to AI CapEx exceeds the annual depreciation on AI assets (~$20-30B/yr by FY2028). If AI infrastructure depreciates faster than it generates revenue, the assets are stranded.

### Probability Estimates

| Analyst | P(Inadequate ROI by FY2028) | Reasoning |
|---------|----------------------------|-----------|
| DCF Analyst | 25% | Bear case: CapEx stays at 22%+ and ad revenue growth slows to 11% CAGR. FCF in FY2028 = ~$35-45B, borderline adequate. Main risk: delayed normalization + ad recession. |
| Industry Analyst | 15-20% | Jevons paradox already operating; Advantage+ at $60B run rate with +40% ROAS is measurable ROI *today*. Risk is recession compressing the ad cycle, not AI failure per se. If ad prices grow +8% annually (below current +9%), cumulative AI ROI clears the hurdle by mid-2027. |
| Risk & Contrarian | 30-35% | Three independent failure modes: (1) AI efficiency gains are real but competitors match them (zero-sum), probability 30%; (2) recession compresses ad budgets while CapEx depreciation is fixed, probability 15%; (3) Llama/AI development underperforms (Avocado delays, benchmark manipulation history), probability 25%. Adjusted for overlap: 30-35% composite. |

### Director's Resolution — Question 4

**UNRESOLVED — Key Unresolved Risk.**

The analysts converge on 15-35% probability of inadequate ROI within 3 years, with the gap driven by different assessments of competitive dynamics (zero-sum vs. TAM-expanding).

**Competing ranges for final note:**
- Optimistic: 15-20% (Industry Analyst — Jevons paradox dominates; ROI already visible)
- Central: 25% (DCF Analyst — matches bear case probability)
- Pessimistic: 30-35% (Risk & Contrarian — competitive zero-sum + recession risk + execution risk)

**Director's recommendation:** Use 25% as the base probability, consistent with the DCF Analyst's bear case weighting. Flag the Risk & Contrarian's 30-35% estimate as the upper bound. The difference between 25% and 30% changes the expected value by approximately $25-35/share — material but not thesis-changing.

**Flag for final note:** "CapEx ROI uncertainty is the single largest source of valuation dispersion. The probability of inadequate returns within 3 years ranges from 15% (if Jevons paradox dominates and no recession) to 35% (if competitive dynamics are zero-sum and macro deteriorates). This 20-percentage-point range represents ~$70/share in valuation uncertainty."

---

## Question 5: How Should CapEx ROI Uncertainty Be Priced?

### DCF Analyst — Through WACC and Scenario Probabilities

Already priced via: elevated beta (1.25 vs. historical 1.15), company-specific risk premium (0.5% for governance + CapEx risk), and 25% bear case probability. Combined effect: WACC at 10.4% (vs. ~9.5% without adjustments) reduces base case fair value by ~$100/share. The 25% bear probability reduces expected value by ~$95/share vs. a 15% bear weighting. Total CapEx uncertainty discount: ~$195/share embedded in the model.

### Industry Analyst — Through Terminal Value Range

CapEx ROI uncertainty should be priced through the terminal revenue and margin assumptions, not WACC. WACC is a blunt instrument that penalizes all future cash flows equally. The real risk is concentrated in FY2026-28 (the investment period), not in the terminal value. I recommend a wider bull/bear spread on FY2030 operating margins (35-52% vs. DCF Analyst's current range) and explicit modeling of the WhatsApp monetization outcome as a discrete scenario.

### Risk & Contrarian — Through Higher Bear Probability AND Lower Base Case

The current model underprices CapEx risk because: (1) the bear case at $359 may be too generous — my catastrophic scenario at $205 has 8-10% probability, and the more moderate bear ($420) has 20-25% probability; (2) the base case assumes CapEx normalizes to 16%, which I have argued should be 18-20%. The correct pricing is: higher bear probability (30% not 25%), lower base case (reflecting 18-20% CapEx/revenue), AND a wider distribution acknowledging the extreme uncertainty.

**The expected value calculation at ~$640 is instructive:** My independent scenario set (Bull $900 at 25%, Base $700 at 45%, Bear $420 at 30%) yields expected value of $666 — a +4.1% return with ~38% annualized volatility. The Sharpe ratio is essentially zero. At these levels, an investor is taking significant risk for near-zero excess return. CapEx uncertainty is the primary reason.

### Director's Resolution — Question 5

**RESOLVED — Implement via multiple mechanisms.**

The three approaches are not mutually exclusive. The revised model should incorporate:

1. **Revised CapEx/revenue (from Question 1):** Base case 18% (up from 16%). Impact: ~-$40-50/share on base case fair value.

2. **Maintained WACC adjustments (DCF Analyst):** Beta 1.25 and 0.5% company-specific risk premium. No change needed — these appropriately reflect the governance + CapEx execution risk.

3. **Revised bear probability (partial concession to Risk & Contrarian):** Move from 25/50/25 to **25/47/28** weighting. The 3-percentage-point shift toward bear reflects the valid points about competitive zero-sum dynamics and the Llama 4 credibility issue. Impact: ~-$10-15/share on expected value.

4. **Flagged in final note:** CapEx ROI is designated as the "Key Swing Variable" with sensitivity table showing fair value at 14%, 16%, 18%, 20%, 22%, and 25% CapEx/revenue ratios.

---

## Summary of Resolutions and Revisions

| Question | Status | Resolution | Impact on Base Case |
|----------|--------|------------|-------------------|
| Q1: CapEx/Revenue by 2030 | **PARTIALLY RESOLVED** | Revised to 18% (from 16%) | -$40-50/share |
| Q2: Cloud analogy validity | **RESOLVED** | Valid for mechanism (Jevons), overstated for magnitude (40x). Better analogy: Google search quality investment | Qualitative — frames thesis |
| Q3: Revenue justification | **PARTIALLY RESOLVED** | $400-430B high confidence; $430-470B medium confidence; new streams are swing variable | WhatsApp outcome = $50-100/share swing |
| Q4: P(inadequate ROI in 3yr) | **UNRESOLVED — Key Unresolved Risk** | Range: 15-35%, central estimate 25% | $70/share valuation uncertainty |
| Q5: How to price uncertainty | **RESOLVED** | CapEx/rev to 18%, bear probability to 28%, maintain WACC adjustments, flag in sensitivity tables | Combined: -$55-70/share from original DCF base case |

### Revised Expected Value Estimate

Applying all debate resolutions:

| Scenario | Original Price | Revised Price | Original Prob | Revised Prob | Revised Contribution |
|----------|---------------|---------------|---------------|-------------|---------------------|
| Bull | $1,032 | $1,000 (slightly lower on 18% CapEx) | 25% | 25% | $250.00 |
| Base | $733 | $685 (18% CapEx/rev) | 50% | 47% | $321.95 |
| Bear | $359 | $359 (unchanged) | 25% | 28% | $100.52 |
| **Expected Value** | **$714** | **$672** | — | — | **$672.47** |

**Net impact of debate: -$42/share on expected value** (from $714 to $672). At a ~$640 current price, this reduces the implied upside from +11.6% to +5.1%. The Risk & Contrarian's concern about marginal risk-reward is partially validated.

---

## Key Unresolved Risks for Final Note

1. **CapEx ROI probability range (15-35%):** The 20-percentage-point spread between the Industry Analyst's optimistic view and the Risk & Contrarian's pessimistic view cannot be resolved with available evidence. It requires 2-3 quarters of observable data (FY2026 ad pricing trends, WhatsApp revenue disclosure, Avocado model reception). Flag as the primary source of valuation uncertainty.

2. **WhatsApp monetization ($10-60B by 2030):** This single variable accounts for $50-100/share of valuation dispersion. No analyst can credibly narrow this range without WhatsApp standalone revenue disclosure from Meta. Flag as the largest data gap affecting the investment thesis.

3. **Competitive dynamics (TAM-expanding vs. zero-sum):** If Meta's AI CapEx primarily improves its competitive position (zero-sum with Google/Amazon), the ROI calculus is fundamentally different from the Industry Analyst's TAM-expanding view. This is an empirical question that will be answered by industry-level ad spending data over the next 12-18 months.

---

*Debate moderated by Director of Research. All positions documented with evidence. Revised numbers reflect consensus where achievable; competing ranges preserved where not.*

*SIGNAL-ID: DEBATE-2-CAPEX-ROI-META-2026-03-13*
