# AMD Research Swarm — Bias, Duplication & Orthogonality Audit

**Date:** 2026-03-10
**Scope:** Full review of AMD research output, all 15 Pass 1 reports, Pass 2 critiques/rebuttals, agent definitions, and orchestration design (CLAUDE.md)

---

## Executive Summary

The AMD research note is genuinely impressive in its depth and intellectual honesty — particularly the Analyst Debate Summary, the Contrarian Analysis, and the transparent disclosure of unresolved contradictions. That said, the swarm has several structural problems that introduce systematic bias, inflate false confidence through signal duplication, and waste significant compute on work that doesn't change the output. The core finding: **the system is better at generating volume than generating orthogonal signals**, and the adversarial review process is largely performative — 79% of critiques produced no material change.

---

## 1. SYSTEMATIC BIASES

### 1.1 Anchoring Bias: The "Fairly Valued" Gravity Well

The final note lands on HOLD / $192 / 2-out-of-5 conviction — a maximally non-committal output. This isn't necessarily wrong, but the process that produced it reveals anchoring:

- The DCF Analyst produced $154 (SELL signal)
- The Quant Analyst produced $205 (BUY signal)
- The Devil's Advocate produced $178 (negative EV)
- The Editor/Director split the difference and landed on $192 — almost exactly the current price of $190.40

The probability weights (20/50/30) were chosen *after* the price targets were set, and the 50% base case conveniently equals the current market price. This is classic anchoring to the current stock price masquerading as independent analysis. A truly independent process would have the base case diverge from the current price more often than not. When four independent methodologies (DCF, comps, risk-adjusted, DA-adjusted) all "converge near $190," that's not independent confirmation — that's four teams calibrating to the same anchor.

**Structural fix:** Have the Director explicitly state the current stock price AFTER all analysts have submitted their fair value estimates. In the current design, every analyst knows the stock trades at $190.40 before they begin. Their models are unconsciously tuned to produce answers near it.

### 1.2 Recency Bias and Narrative Capture

The entire note is organized around the AI GPU mega-deal narrative — which is the dominant market narrative of early 2026. The non-AI businesses (EPYC server CPU, Client, Embedded) collectively represent 52% of FY2025 revenue and are barely analyzed:

- EPYC gets brief mentions as "gaining share" but no independent analysis of the x86 server CPU market dynamics, ARM threat timeline, or Intel recovery probability
- Client (31% of revenue) is dismissed in one sentence per scenario
- Gaming (11%) is treated as declining and irrelevant
- Embedded/Xilinx (10%) barely appears despite being a $3.5B business

The Sector Analyst, Competitive Analyst, and Macro Analyst all focus 80%+ of their analysis on Data Center / AI GPU. This means 48% of AMD's revenue consumes 80%+ of the analytical bandwidth, while 52% of revenue gets surface treatment. If the AI GPU thesis fails, the non-AI business becomes the entire valuation floor — and it's the least-analyzed part of the note.

**Structural fix:** Require each analyst to explicitly allocate analysis proportional to revenue share, not narrative salience. Or add a "Non-Thesis Business" specialist agent whose job is exclusively the non-AI segments.

### 1.3 Bear Case Asymmetry (Bearish Structural Tilt)

The system has a structural bear bias despite appearing balanced:

- The Devil's Advocate agent runs on Opus with high effort (the most capable/expensive configuration). Most other analysts run on Sonnet with medium effort.
- The Devil's Advocate produces an *independent* bear case in Pass 1 without reading other analysts — meaning it starts from a bearish prior
- There is no "Angel's Advocate" or systematic bull-case-challenger agent. The bull case must survive the Devil's Advocate; the bear case faces no symmetric challenge
- The forensic, sentiment, and risk analysts are all structurally oriented toward finding problems, not confirming strengths

This asymmetry is intentional (the CLAUDE.md explicitly wants skeptical, evidence-based analysis), but it means the probability weights are systematically pushed bearish. The final 30% bear probability vs. 20% bull probability may reflect system design more than reality.

**Evidence:** The Devil's Advocate initially argued for 35% bear probability and $80 bear case. Multiple analysts pushed back to 30% and $120-140. The bear probability was revised *down* from the Devil's Advocate's initial estimate — but the starting point was set by the most bearish, highest-effort agent in the system.

### 1.4 Data Source Homogeneity

Despite having 15 analysts, the data source pool is surprisingly narrow. Nearly every analyst drew from the same ~5 sources:

- AMD 10-K FY2025 and Q4 press release (Tier 1)
- Q4 FY2025 earnings call transcript from Motley Fool (Tier 2)
- StockAnalysis.com for market data (Tier 4)
- Yahoo Finance for current prices (Tier 4)
- A handful of news articles (Tom's Hardware, CNBC, Bloomberg Intelligence — Tier 3-6)

The Data Intelligence Memo reports only 55-65% data completeness. Critical missing data:

- No competitor financial models (NVIDIA, Broadcom financials are "partial")
- No options chain data (market-implied probabilities are "estimated")
- No historical price data (tool failure)
- No DEF 14A proxy statement (governance analysis incomplete)
- No channel checks, supply chain contacts, or proprietary data of any kind

The result: 15 agents analyzing essentially the same 5 documents from different angles. This creates the illusion of diverse perspectives while actually being 15 interpretations of the same limited dataset.

---

## 2. SIGNAL DUPLICATION (Same Signal, Multiple Agents)

This is the most significant structural problem. Many "findings" that appear in the final note as corroborating evidence from multiple analysts are actually the same underlying signal read by different agents.

### 2.1 The "CUDA Gap" Echo Chamber

The CUDA/ROCm software gap appears in at least 8 of 15 analyst reports:

| Agent | How They Frame It |
|-------|-------------------|
| DCF Analyst | "ROCm software gap remains binding constraint" |
| Quant Analyst | "NVIDIA software moat durable" |
| Competitive Analyst | "ROCm developer ecosystem small vs. CUDA's 6M+ developers" |
| Sector Analyst | "Software ecosystem as structural barrier" |
| Devil's Advocate | "CUDA Gap Score 28.7-99.1%" |
| Risk Analyst | "CUDA gap persistence" as risk factor |
| Catalyst Analyst | ROCm 7.0 release as catalyst |
| Sentiment Analyst | Management hedges on GPU specifics |

These are NOT 8 independent signals. They are 8 agents reading the same earnings call transcript and same tech press articles, then restating the CUDA gap in their own frameworks. The final note presents this as "CUDA gap persistence: High (60%)" with implicit support from multiple independent sources — but the underlying evidence base is 2-3 data points (the SemiAnalysis benchmark, the developer count comparison, and management commentary).

### 2.2 The Mega-Deal Signal

The OpenAI/Meta mega-deal analysis appears in essentially every report:

- DCF models it as revenue input
- Quant implies it in growth rate
- Competitive frames it as customer concentration
- Credit frames it as purchase commitment risk
- Catalyst frames it as deployment milestone
- Risk frames it as execution risk
- ESG frames it as warrant governance risk
- Devil's Advocate frames it as bridge contract risk
- Forensic frames it as revenue quality concern
- Sentiment frames it as management confidence signal

This is one business development — two customer contracts — that gets counted as evidence in 10+ different analytical frameworks. Each analyst treats their framing as a "new insight," but the information content is identical: AMD signed big deals with warrant sweeteners, and execution is uncertain.

### 2.3 The Inventory Reserve Release ($306M)

This single accounting item from Q4 FY2025 appears in:

- Forensic Analyst: margin inflation concern
- Sentiment Analyst: press release vs. reality discrepancy
- DCF Analyst: gross margin assumption basis
- Quant Analyst: margin comparability issue
- Editor: featured in both the Financial Analysis warning and the Forensic Quality section

One $306M reserve release is not five independent red flags. It's one datapoint that five agents independently discovered and each presented as their own finding.

### 2.4 Quantifying the Duplication

My estimate of truly orthogonal signals in the final research note:

| Signal Category | Unique Signals | Times Presented | Inflation Factor |
|----------------|---------------|-----------------|-----------------|
| AI GPU competitive dynamics (CUDA, ASICs, mega-deals) | ~5 | ~35 | 7.0x |
| Financial/valuation (WACC, margins, multiples) | ~8 | ~20 | 2.5x |
| Management quality/credibility | ~3 | ~12 | 4.0x |
| Balance sheet/credit | ~4 | ~6 | 1.5x |
| Macro/geopolitical | ~4 | ~8 | 2.0x |
| Technical/price action | ~3 | ~4 | 1.3x |
| ESG/governance | ~3 | ~5 | 1.7x |
| **Total** | **~30** | **~90** | **3.0x average** |

The research note presents approximately 90 distinct claims/findings, but only ~30 are based on independent underlying signals. The 3x inflation factor creates a false sense of corroboration.

---

## 3. UNNECESSARY WORK AND INEFFICIENCY

### 3.1 The Critique/Rebuttal Process Is Mostly Performative

The Pass 2 critique/rebuttal phase generated 15 critique files and 15 rebuttal files — roughly 30 documents of debate. The material outcomes:

| Category | Count | % of Total |
|----------|-------|-----------|
| Critiques that changed a number or conclusion | 3-4 | ~16% |
| Critiques that were "agree but emphasize differently" | ~12 | ~50% |
| Critiques that were rejected with no change | ~8 | ~33% |

The three material changes were:

1. **WACC:** DCF Analyst adopted declining schedule (16% → 14%), shifting base case +$25-35/share. This was the single most impactful change in the entire process.
2. **Bear case floor:** Devil's Advocate revised from $80 to $120-140 after credit/sector pushback.
3. **Forward PEG:** Quant Analyst revised trailing PEG 0.51x to forward PEG 0.82-1.0x, eliminating the "deep value" signal.

Everything else was debate that didn't move the needle. The 7-analyst consensus that "WACC is the critical issue" produced exactly one change (the declining schedule compromise), and even that was a split-the-difference rather than a principled resolution.

**Cost-benefit:** The critique/rebuttal phase likely consumed 40-50% of total compute (15 agents × 2 rounds × reading all other agents' work). For 3 material changes, that's extremely expensive per insight.

### 3.2 Agents with Heavily Overlapping Mandates

Several agent pairs have 60-80% scope overlap:

**Competitive Analyst vs. Sector Analyst:** Both analyze market share dynamics, competitive structure, TAM, and industry trends. The Competitive Analyst focuses on AMD's positioning; the Sector Analyst focuses on industry-level dynamics. In practice, both produced analyses of AI GPU market share, ASIC competition, and NVIDIA's dominance. The Sector Analyst's market share model and the Competitive Analyst's moat assessment are analyzing the same competitive dynamics from slightly different angles — but using the same data.

**Risk Analyst vs. Devil's Advocate:** Both produce bear cases. The Risk Analyst quantifies downside scenarios with probabilities and stress tests. The Devil's Advocate constructs narrative bear cases with pre-mortems and assumption fragility scores. Both agents produced ~30% bear probability estimates, both identified MI450 execution and ASIC cannibalization as top risks, and both used the same supporting evidence. The differentiation (quantitative vs. narrative) is real but the information content is heavily duplicated.

**Forensic Analyst vs. Sentiment Analyst:** Both assess management credibility. The Forensic Analyst checks accounting quality and governance flags; the Sentiment Analyst analyzes earnings call tone. Both flagged the $306M reserve release, both assessed Lisa Su's credibility (8.5/10 vs. 82/100 — same conclusion on different scales), and both identified GPU revenue opacity as the top transparency concern.

**Macro Analyst vs. Risk Analyst (macro risk section):** The Macro Analyst maps macro factors to P&L impact. The Risk Analyst stress-tests macro shocks. Both produced tables of macro risks (interest rates, FX, geopolitical, AI capex cycle) with probability and magnitude estimates. The difference is framing (macro positioning vs. tail risk), but the content is 70%+ overlapping.

### 3.3 The Model Builder Agent

The Model Builder produced Python scripts for DCF, comps, risk, sector, and credit models. However:

- The DCF Analyst, Quant Analyst, Risk Analyst, Credit Analyst, and Sector Analyst all also describe their models in their markdown reports
- It's unclear whether the Model Builder's Python scripts were actually *used* to validate the analysts' calculations, or whether they were built independently and produced different numbers
- No cross-validation results appear in the output — no "Model Builder's DCF script produces $X vs. DCF Analyst's manual calculation of $Y"

The Model Builder may be producing artifacts that nobody else consumes.

---

## 4. ORTHOGONALITY FAILURES

The system has weak mechanisms for ensuring analysts produce genuinely independent signals.

### 4.1 All Agents Read the Same Input

Every analyst receives the same company context memo and the same `input/` directory (populated by the Research Analyst in Phase 0). This means all 15 agents start from identical information and apply different frameworks to it. True orthogonality would require different information sources, not just different frameworks.

What would add orthogonal signal:

- **Channel checks** (not available to LLMs, but the system could flag this gap more prominently)
- **Competitor deep-dives** (running the full swarm on NVIDIA or Broadcom, not just AMD)
- **Customer perspective analysis** (what do OpenAI/Meta actually need from AMD?)
- **Supply chain analysis** (TSMC allocation dynamics, CoWoS capacity, packaging bottleneck math)
- **Historical analogy analysis** (what happened to the #2 GPU company in prior platform shifts?)

### 4.2 The Cross-Critique Creates Herding, Not Independence

In Pass 2, every analyst reads every other analyst's summary brief. This is designed to enable cross-critique, but it also creates herding pressure:

- When 7 of 15 analysts independently flag WACC as the critical issue, the remaining 8 see that consensus and are less likely to challenge it or propose alternative critical issues
- The rebuttal process rewards "accepting critique with modification" over "rejecting critique entirely" — agents that accept critiques appear more intellectually honest, creating an incentive to converge
- The final note weights the "consensus" view heavily, so individual analysts who dissent face implicit pressure to moderate their positions

**Evidence:** The Devil's Advocate started at 35% bear probability and $80 bear case. After the cross-critique process, it was 30% and $120-140. The Quant Analyst started at $205 fair value with a BUY-leaning signal. After cross-critique, the comps-implied value was revised to $184-190 (HOLD). Both moved toward the center. Nobody moved away from it.

### 4.3 What's Missing Entirely

The research note has blind spots that no agent was designed to cover:

1. **Customer concentration risk modeling:** Two customers (OpenAI, Meta) represent ~35% of FY2028E revenue. No agent modeled what happens if one customer defects, delays, or renegotiates. The Credit Analyst notes the concentration; nobody models the scenario.

2. **Warrant game theory:** The 320M warrants create complex incentive dynamics between AMD and its customers. No agent analyzed this as a game theory problem (e.g., what's OpenAI's optimal strategy given they hold warrants AND are building competing ASICs?).

3. **TSMC dependency modeling:** AMD is 100% dependent on TSMC. No agent modeled TSMC's capacity allocation decisions, pricing power over AMD, or the strategic dynamics of AMD competing with NVIDIA for TSMC's best process nodes.

4. **Insider behavior deep-dive:** The Devil's Advocate mentions Lisa Su sold 350K shares. No agent analyzed the full Form 4 filing pattern, compared insider selling to historical patterns, or assessed whether the 10b5-1 plan timing was suspicious.

5. **Software ecosystem valuation:** The CUDA gap is flagged by 8 agents but nobody attempts to quantify the economic value of NVIDIA's software ecosystem vs. AMD's, or model the investment required for AMD to close the gap.

---

## 5. STRUCTURAL RECOMMENDATIONS

### 5.1 Reduce Agent Count, Increase Orthogonality

**Merge candidates:**
- Competitive Analyst + Sector Analyst → "Industry Analyst" (one agent, two sections)
- Risk Analyst + Devil's Advocate → "Risk & Contrarian Analyst" (quantitative bear case + narrative pre-mortem in one report)
- Forensic Analyst + Sentiment Analyst → "Quality & Credibility Analyst" (accounting quality + management assessment unified)
- Macro Analyst can be absorbed into the Risk Analyst's macro stress test section

This reduces 15 analysts to 10-11 while losing minimal orthogonal signal. The compute savings can be redirected to deeper analysis by the remaining agents.

### 5.2 Enforce Information Barriers in Pass 1

Instead of all agents reading the same input, partition the data:

- **Group A** (DCF, Quant, Model Builder): Gets financial statements only
- **Group B** (Competitive, Sector): Gets industry data and competitor info only
- **Group C** (Risk, Devil's Advocate): Gets risk factors, insider data, bear case evidence only
- **Group D** (Forensic, Sentiment): Gets transcripts and accounting detail only
- **Group E** (Macro, Credit): Gets macro data and balance sheet only

Each group produces analysis from their partition. The Editor synthesizes. This creates genuine information diversity instead of 15 agents reading the same 10-K.

### 5.3 Make the Critique Process Decision-Forcing

Replace the open-ended "identify weakest assumption" critique with structured decision gates:

- After Pass 1, the Director identifies the 3-5 most consequential disagreements
- Only those disagreements go to critique/rebuttal — not everything
- Each disagreement must produce a RESOLUTION: either a revised number both sides accept, or an explicit "Key Unresolved Risk" with competing probability ranges
- If the critique process doesn't change any numbers, it failed and shouldn't have been run

### 5.4 Track Signal Independence

Add a metadata requirement: every claim in the final note must cite its PRIMARY source (the underlying data point) and flag whether other agents used the same source. When the Editor sees that 8 agents cited the same CUDA benchmark, the note should say "CUDA gap (one signal, corroborated by zero additional independent sources)" rather than presenting it as a consensus finding.

### 5.5 Blind the Analysts to Current Price

The single most impactful change would be removing the current stock price from the input materials. If the DCF Analyst doesn't know AMD trades at $190, their model output can't unconsciously anchor to it. The Director can compare the price-blind fair value estimates to the current price *after* all analysis is complete.

---

## 6. WHAT THE SYSTEM DOES WELL

Credit where due — several aspects of this design are genuinely strong:

1. **The Analyst Debate Summary is excellent.** Most research notes bury disagreements. This one surfaces them prominently with Position A / Position B / Resolution structure. That's rare and valuable.

2. **The Data Tier system works.** Every claim is tagged with a source reliability tier (1-10). This is a meaningful quality signal that most research processes lack.

3. **The forensic and sentiment analyses add genuine alpha.** The $306M reserve release finding, the hedging language analysis, and the management credibility scoring are the kinds of non-obvious signals that justify the swarm approach.

4. **The pre-mortem is the best section in the note.** The Devil's Advocate's narrative of "It's March 2028, AMD has lost 40%" is vivid, specific, and genuinely useful for stress-testing conviction.

5. **The unresolved contradictions are honestly disclosed.** The note admits the team can't agree on WACC, capex cycle timing, bridge contract risk, or ROIC methodology. That intellectual honesty is more valuable than false consensus.

6. **The warrant dilution analysis is sophisticated.** The asymmetric dilution dynamic (maximum dilution in the bull case) is a genuinely non-obvious insight that most sell-side notes miss.

---

## 7. VERDICT

The AMD research note is a B+ product from a system that could be an A with structural improvements. The quality of individual analyses is high. The synthesis (Editor + Director) is strong. The intellectual honesty is above sell-side standard. But the system spends too much compute producing redundant signals, the adversarial review is mostly theater, and the 15-agent design creates an illusion of corroboration where there's actually 30 independent signals presented 90 times.

The single highest-ROI change: **reduce agents, increase information partitioning, and blind analysts to the current stock price.**
