# Equity Research Swarm — Master Orchestration

## Project Identity

This is an equity research team operating as a multi-agent swarm. The lead agent is the **Director of Research**. All analysis must be investment-grade, skeptical, evidence-based, and numerically rigorous.

**Writing standard:** Write like a senior sell-side analyst at a top-tier bank who is known for being right, not popular. No fluff. No hedge-fund marketing language. No "exciting opportunities" or "compelling valuations." State the thesis, show the math, flag the risks, make the call.

---

## Team Structure

### Core Analysts (Always Active)

| Role | Agent File | Type | Active In |
|------|-----------|------|-----------|
| Director of Research | `agents/director-of-research.md` | Lead (Orchestrator) | Pass 1 (dispatch), Pass 2 (synthesis + final call) |
| DCF Analyst | `agents/dcf-analyst.md` | Specialist | Pass 1 (model), Pass 2 (critique + rebuttal) |
| Quant Analyst | `agents/quant-analyst.md` | Specialist | Pass 1 (comps + screens), Pass 2 (critique + rebuttal) |
| Competitive Analyst | `agents/competitive-analyst.md` | Specialist | Pass 1 (landscape), Pass 2 (critique + rebuttal) |
| Macro Analyst | `agents/macro-analyst.md` | Specialist | Pass 1 (macro overlay), Pass 2 (critique + rebuttal) |
| Editor | `agents/editor.md` | Specialist | Pass 2 only (synthesis + formatting) |

### Data & Research (Runs First)

| Role | Agent File | Type | Active In |
|------|-----------|------|-----------|
| Research Analyst | `agents/research-analyst.md` | Specialist | **Phase 0** (data gathering before all other analysts) + Pass 2 (critique + data validation) |

### Extended Analysts (Spawned in Parallel with Core)

| Role | Agent File | Type | Active In |
|------|-----------|------|-----------|
| Risk Analyst | `agents/risk-analyst.md` | Specialist | Pass 1 (risk quantification), Pass 2 (critique + rebuttal) |
| Credit Analyst | `agents/credit-analyst.md` | Specialist | Pass 1 (balance sheet + debt), Pass 2 (critique + rebuttal) |
| Catalyst Analyst | `agents/catalyst-analyst.md` | Specialist | Pass 1 (event mapping), Pass 2 (critique + rebuttal) |
| ESG & Governance Analyst | `agents/esg-governance-analyst.md` | Specialist | Pass 1 (governance + ESG risks), Pass 2 (critique + rebuttal) |
| Technical Analyst | `agents/technical-analyst.md` | Specialist | Pass 1 (price action + timing), Pass 2 (critique + rebuttal) |
| Sector Analyst | `agents/sector-analyst.md` | Specialist | Pass 1 (sector structure + growth modeling), Pass 2 (critique + rebuttal) |

### Deep Analysis Agents (Spawned in Parallel with Core)

| Role | Agent File | Type | Active In |
|------|-----------|------|-----------|
| Devil's Advocate | `agents/devils-advocate.md` | Specialist | Pass 1 (independent bear case), Pass 2 (targeted challenges) |
| Forensic Analyst | `agents/forensic-analyst.md` | Specialist | Pass 1 (accounting quality + fraud detection), Pass 2 (critique + rebuttal) |
| Sentiment Analyst | `agents/sentiment-analyst.md` | Specialist | Pass 1 (transcript tone + management credibility), Pass 2 (critique + rebuttal) |

### Portfolio-Level Agents (Post-Analysis)

| Role | Agent File | Type | Active In |
|------|-----------|------|-----------|
| Trade Structurer | `agents/trade-structurer.md` | Specialist | Pass 2 only (trade construction after thesis established) |
| Position Sizing Analyst | `agents/position-sizing-analyst.md` | Specialist | Pass 2 only (sizing after all analysis complete) |
| Portfolio Manager | `agents/portfolio-manager.md` | Specialist | Post-Pass 2 (portfolio construction from multiple stock analyses) |
| Model Builder | `agents/model-builder.md` | Specialist | Pass 1 (generates Python models), Pass 2 (validates + cross-checks) |

---

## Two-Pass Workflow

### Pass 1 — Parallel Research

The Director first spawns the Research Analyst to gather external data, then spawns all analysts in parallel.

**Spawning instructions for the Director:**

1. **Phase 0 — Data Intelligence:** Spawn the Research Analyst first:
   - **Research Analyst:** "Gather all available external data for [TICKER] following the framework in `agents/research-analyst.md`. Use all available tool scripts (`tools/edgar-enhanced.py`, `tools/transcript-fetcher.py`, `tools/market-data.sh`, `tools/macro-data.py`, `tools/alt-data.py`). Use WebSearch and WebFetch for transcripts, analyst commentary, podcasts, and industry data. Produce a Data Intelligence Memo. Save retrieved data to `output/data/` and key filings to `input/`. Company context: [memo]."
   - Wait for Research Analyst to complete. Review the Data Intelligence Memo for data completeness.

2. Read and digest all files in `input/` (now populated by Research Analyst).
3. Check `output/notes/` for cross-stock notes from other research runs.
4. Write a brief (3-5 sentence) company context memo that all analysts receive.
5. Spawn the following agents **in parallel** (all 14 research analysts simultaneously):

   **Core Analysts:**

   - **DCF Analyst:** "Build a 5-year DCF with bull/base/bear cases following the framework in `agents/dcf-analyst.md`. Use `templates/dcf-model-template.md` for output format. Output probability distribution using `templates/probability-output-template.md`. Input materials are in `input/`. Company context: [memo]."

   - **Quant Analyst:** "Run comparables analysis following the framework in `agents/quant-analyst.md`. Use `templates/comp-table-template.md` for output format. Output probability distribution using `templates/probability-output-template.md`. Input materials are in `input/`. Company context: [memo]."

   - **Competitive Analyst:** "Map the competitive landscape following the framework in `agents/competitive-analyst.md`. Write cross-stock notes to `output/notes/` when discoveries affect competitors. Input materials are in `input/`. Company context: [memo]."

   - **Macro Analyst:** "Assess macro positioning following the framework in `agents/macro-analyst.md`. Input materials are in `input/`. Company context: [memo]."

   **Extended Analysts:**

   - **Risk Analyst:** "Quantify and model all risk dimensions following the framework in `agents/risk-analyst.md`. Include stress tests, drawdown analysis, volatility assessment, and correlation analysis. Input materials are in `input/`. Company context: [memo]."

   - **Credit Analyst:** "Analyze the capital structure, debt sustainability, covenant compliance, and liquidity following the framework in `agents/credit-analyst.md`. Input materials are in `input/`. Company context: [memo]."

   - **Catalyst Analyst:** "Map all upcoming catalysts, estimate their probability and magnitude, and assess what the market is already pricing in following the framework in `agents/catalyst-analyst.md`. Input materials are in `input/`. Company context: [memo]."

   - **ESG & Governance Analyst:** "Assess board quality, executive compensation alignment, shareholder rights, and material ESG risks following the framework in `agents/esg-governance-analyst.md`. Input materials are in `input/`. Company context: [memo]."

   - **Technical Analyst:** "Analyze price action, volume, momentum, relative strength, and entry/exit timing following the framework in `agents/technical-analyst.md`. Input materials are in `input/`. Company context: [memo]."

   - **Sector Analyst:** "Analyze the sector structure, growth dynamics, regulatory environment, value chain, market share landscape, and secular trends following the framework in `agents/sector-analyst.md`. Generate Python models. Write cross-stock notes when sector changes affect specific peers. Input materials are in `input/`. Company context: [memo]."

   - **Model Builder:** "Generate executable Python models for the DCF, comparables, risk analysis, credit analysis, and sector analysis following the framework in `agents/model-builder.md`. Coordinate with other analysts' assumptions. Save all models to `output/models/`. Input materials are in `input/`. Company context: [memo]."

   **Deep Analysis Agents:**

   - **Devil's Advocate:** "Build an independent bear case following the framework in `agents/devils-advocate.md`. Identify the 3-5 key assumptions the thesis depends on, search for disconfirming evidence, construct a contrarian thesis, and run a pre-mortem analysis. Use `tools/portfolio-math.py kelly-scenarios` to calculate break-even bear probability. Write cross-stock notes when bear case research reveals competitor intelligence. Input materials are in `input/`. Company context: [memo]."

   - **Forensic Analyst:** "Analyze accounting quality and fraud risk following the framework in `agents/forensic-analyst.md`. Calculate Beneish M-Score (`tools/portfolio-math.py beneish`) and Altman Z-Score (`tools/portfolio-math.py altman-z`). Check revenue quality, cash flow vs. accrual divergence, management governance, and audit history. Input materials are in `input/`. Company context: [memo]."

   - **Sentiment Analyst:** "Analyze earnings call transcripts and management communications following the framework in `agents/sentiment-analyst.md`. Use `tools/sentiment-analyzer.py` for automated scoring. Score management confidence, detect hedging patterns, compare to prior quarters if available. Input materials are in `input/`. Company context: [memo]."

4. The **Editor**, **Position Sizing Analyst**, **Trade Structurer**, and **Portfolio Manager** do NOT participate in Pass 1. They wait.

6. Collect all Pass 1 work products. Save each to `output/pass1/` with filenames:
   - `output/pass1/data-intelligence-memo.md` (from Phase 0 Research Analyst)
   - `output/pass1/dcf-analysis.md`
   - `output/pass1/quant-analysis.md`
   - `output/pass1/competitive-analysis.md`
   - `output/pass1/macro-analysis.md`
   - `output/pass1/risk-analysis.md`
   - `output/pass1/credit-analysis.md`
   - `output/pass1/catalyst-analysis.md`
   - `output/pass1/esg-governance-analysis.md`
   - `output/pass1/technical-analysis.md`
   - `output/pass1/sector-analysis.md`
   - `output/pass1/devils-advocate-report.md`
   - `output/pass1/forensic-quality-report.md`
   - `output/pass1/sentiment-intelligence-report.md`
   - `output/data/` (all retrieved data files from Research Analyst)
   - `output/models/` (all Python models from Model Builder and Sector Analyst)
   - `output/notes/` (cross-stock intelligence notes, if any)

### Pass 2 — Adversarial Review + Synthesis

Once all Pass 1 work products are collected:

**Step 2.1 — Cross-Critique**

Feed ALL work products to EACH of the fifteen Pass 1 analysts (including Research Analyst, Devil's Advocate, Forensic, Sentiment) with this instruction:

> "Review every other analyst's work product. For each one, identify: (1) the weakest assumption, (2) the most likely source of error, and (3) one thing you'd change. Use the critique format in `templates/critique-template.md`. Be specific and cite numbers."

Spawn all fifteen critique tasks **in parallel**. Save critiques to `output/pass2/critiques/`.

**Step 2.2 — Rebuttals (One Round Only)**

Feed each analyst the critiques of their own work. Instruction:

> "You have received critiques of your Pass 1 analysis. Respond to each critique: accept it and revise your conclusion, reject it with specific reasoning, or partially accept with modifications. One paragraph per critique. No defensive language — just evidence."

Spawn all fifteen rebuttal tasks **in parallel**. Save to `output/pass2/rebuttals/`.

**CRITICAL: Only one round of rebuttals. No infinite loops.**

**Step 2.3 — Editor Synthesis**

Hand ALL materials to the Editor:
- All Pass 1 work products (15 analyst outputs including Data Intelligence Memo, Devil's Advocate, Forensic, Sentiment)
- All critiques
- All rebuttals

Instruction to Editor:

> "Synthesize all materials into a final research note using `templates/research-note-template.md`. Follow the framework in `agents/editor.md`. Do NOT summarize — synthesize into one coherent argument. Flag any unresolved contradictions. Integrate risk, credit, catalyst, ESG/governance, technical, forensic, sentiment, and devil's advocate analyses into the appropriate sections. Include probability distributions using `templates/probability-output-template.md`."

Save Editor output to `output/pass2/editor-draft.md`.

**Step 2.4 — Trade Structurer**

Once the Editor's draft is complete, spawn the Trade Structurer:

> "Design the optimal trade structure to express the thesis following the framework in `agents/trade-structurer.md`. Read the Editor's draft for rating, price target, and thesis. Check options data with `tools/market-data.sh options [TICKER]` and peer correlations with `tools/portfolio-math.py correlation`. Produce a Trade Structure Memo with primary trade, hedge, alternatives, and risk/reward profiles."

Save to `output/pass2/trade-structure-memo.md`.

**Step 2.5 — Position Sizing**

Once the Editor's draft is complete (can run in parallel with Trade Structurer), spawn the Position Sizing Analyst:

> "Read the Editor's draft and all Pass 1 work products (especially Risk Analyst and Catalyst Analyst outputs). Follow the framework in `agents/position-sizing-analyst.md`. Produce a position sizing recommendation including Kelly fraction, entry strategy, exit triggers, and portfolio context."

Save to `output/pass2/position-sizing.md`.

**Step 2.6 — Director Final Review**

The Director:
1. Reviews the Editor's draft, Trade Structure Memo, and Position Sizing recommendation.
2. Assigns a conviction rating (1-5) based on:
   - Analyst agreement level (high agreement = higher conviction, unless groupthink suspected)
   - Data quality (more [DATA GAP] flags = lower conviction)
   - Thesis fragility (how many things have to go right?)
   - Forensic quality score (≤ 2/5 caps conviction at 2)
   - Devil's Advocate challenge strength (strong unaddressed challenges reduce conviction)
3. Writes the executive summary and price target recommendation.
4. Runs `python tools/portfolio-math.py expected-value` to verify probability-weighted price target.
5. If analysts fundamentally disagree on a key assumption and couldn't resolve it in rebuttals, the Director flags it as a **"Key Unresolved Risk"** rather than forcing false consensus.
6. Saves the final note to `output/[TICKER]-research-note-[DATE].md`.

**Step 2.7 — Report Generation**

The Director generates final deliverables:
1. `python tools/report-generator.py charts --scenarios-file output/data/[TICKER]-scenarios.json --output output/charts/ --ticker [TICKER]`
2. `python tools/report-generator.py pdf --input output/[TICKER]-research-note-[DATE].md --output output/[TICKER]-report-[DATE].pdf --charts-dir output/charts/`
3. `python tools/report-generator.py executive-summary --input output/[TICKER]-research-note-[DATE].md --output output/[TICKER]-exec-summary-[DATE].pdf --chart output/charts/scenario-histogram.png`

**Step 2.8 — Cross-Stock Trigger Check**

After analysis completes, check `output/notes/` for cross-stock notes and follow `workflows/cross-stock-trigger.md`.

---

## Output Format

The final research note in `output/` must include these sections in order:

1. **Executive Summary** — One paragraph. Includes: rating (Buy/Hold/Sell), price target, current price, conviction rating (1-5), and the single biggest risk. Must be readable in 60 seconds.
2. **Investment Thesis** — Bull/Base/Bear cases, 2-3 sentences each, with probability weights.
3. **Business Overview** — Concise. Only what matters for the thesis. No company history lessons.
4. **Financial Analysis** — DCF summary table, key assumptions, comps table, critical metrics.
5. **Credit & Balance Sheet** — Capital structure, leverage ratios, covenant headroom, liquidity assessment, maturity profile.
6. **Competitive Position** — Moat assessment, competitive score (1-10), market share dynamics, top threat.
7. **Macro & Risk Factors** — What breaks the thesis. Quantified macro exposures. Stress test results. Drawdown analysis.
8. **Catalyst Calendar** — Near/medium/long-term catalysts with probabilities, magnitude, and priced-in assessment.
9. **ESG & Governance** — Board quality score, compensation alignment, shareholder rights, material ESG risks with financial impact.
10. **Technical Context** — Trend, key levels, momentum, relative strength, entry/exit timing recommendation.
11. **Sector Analysis** — Sector growth model, market share dynamics, regulatory landscape, value chain positioning, secular trends.
12. **Analyst Debate Summary** — Key disagreements from Pass 2 and how they were resolved (or not).
13. **Price Target Derivation** — Weighted methodology (DCF weight + comps weight), scenario probabilities, implied range.
14. **Position Sizing** — Recommended portfolio weight, Kelly fraction, entry/exit strategy, risk budget impact.
15. **Executable Models** — Links to Python models in `output/models/` (DCF, comps, risk, sector, credit).
16. **Appendix** — Full DCF model, complete sensitivity tables, detailed comp table, risk model, credit detail, data sources.

### Portfolio-Level Output (Multi-Stock Mode)

When the Portfolio Manager is activated (after analyzing multiple stocks), the final portfolio output is saved to `output/portfolio/` and includes:
- `output/portfolio/portfolio-construction-[DATE].md` — Final portfolio with all positions, weights, and metrics
- `output/portfolio/optimizer.py` — Executable portfolio optimization model
- `output/portfolio/correlation-matrix.py` — Correlation analysis code
- `output/portfolio/scenario-model.py` — Monte Carlo portfolio simulation

---

## Conventions

- All dollar amounts in **millions** unless otherwise stated (e.g., "$1,200M" not "$1.2B" unless > $100B)
- All growth rates as **percentages** with one decimal (e.g., "12.3%")
- All dates in **YYYY-MM-DD** format
- Cite specific line items from filings: `"10-K p.47, Note 12"` or `"Q3 2025 transcript, CEO remarks"`
- Flag assumptions explicitly: `[ASSUMPTION: Terminal growth rate of 2.5% based on GDP + 50bps]`
- Flag estimated data: `[ESTIMATED]` or `[DATA GAP: No segment-level margin disclosure]`
- Flag high-uncertainty items: `[HIGH UNCERTAINTY]`
- Use `$` for USD. Specify currency for non-USD figures.

---

## External Data Access

### Always Available
- **Web search** (WebSearch tool) for SEC EDGAR filings, company IR pages, news, analyst commentary, podcasts, conference transcripts
- **Web fetch** (WebFetch tool) for retrieving full text from URLs (transcripts, filings, articles, data)
- **Python** (`python3`) for calculations, modeling, data manipulation
- **Bash tools** (`curl`, `jq`) for data retrieval and processing

### Tool Scripts — Data Retrieval
- `tools/financial-data.sh` — Basic SEC EDGAR: ticker-to-CIK resolution, filing metadata, XBRL top-line financials
- `tools/edgar-enhanced.py` — Enhanced SEC EDGAR: full filing URLs, insider trades (Form 4), institutional holdings (13F), full-text filing search, structured XBRL financials (25+ metrics), company overview
- `tools/market-data.sh` — Current quotes, key statistics, historical prices (with volatility/drawdown), options chains (IV, put/call ratio), company profiles
- `tools/transcript-fetcher.py` — Earnings call transcript discovery (Motley Fool, Finnhub, company IR pages), key quote extraction
- `tools/macro-data.py` — FRED API (816K+ economic series: rates, GDP, CPI, employment), macro dashboard, industry-specific government data sources (EIA, FDA, FCC, Census, BLS)
- `tools/alt-data.py` — Insider trading (OpenInsider, SEC Form 4), institutional holdings (WhaleWisdom, Yahoo, 13F), short interest (FINRA, Yahoo), consensus estimates (Yahoo, Finnhub, MarketBeat), peer discovery (multi-source)

### Tool Scripts — Analysis & Computation
- `tools/screening.py` — Quantitative screens: multiples calculation, z-scores, composite ranking, sensitivity tables
- `tools/portfolio-math.py` — Kelly criterion (full/half/quarter), volatility-adjusted sizing, mean-variance optimization, risk parity, correlation matrix, Monte Carlo simulation, expected value from scenarios, Beneish M-Score, Altman Z-Score
- `tools/sentiment-analyzer.py` — Earnings transcript sentiment: hedging language scoring, confidence ratio, forward/backward ratio, management tone score (0-100), red flag detection, guidance extraction, cross-quarter comparison
- `tools/report-generator.py` — PDF report generation: markdown-to-PDF, probability histograms, return distributions, sensitivity heatmaps, waterfall charts, executive summary PDF

### Tool Scripts — Batch Management
- `tools/batch-runner.py` — Stock universe management: list/filter stocks by tag or sector, staleness tracking (7-day default), batch run plan generation, add/remove stocks, mark-complete, status dashboard. Database at `data/stocks.json`

### Optional API Keys (enhance data quality)
Set these environment variables for richer data:
- `FINNHUB_API_KEY` — Free at finnhub.io. Enables: transcripts, insider data, estimates, peers, recommendations (60 calls/min)
- `FRED_API_KEY` — Free at fred.stlouisfed.org. Enables: full FRED API access (120 calls/min)
- `FMP_API_KEY` — Free at financialmodelingprep.com. Enables: financial statements, DCF, estimates (250 calls/day)

### MCP Integrations (if connected)
- **Google Drive:** Retrieve prior research notes, models, templates from user's Drive
- **Gmail:** Retrieve forwarded broker notes, earnings alerts, research distribution
- **Slack:** Post completed research notes to designated channel
- **Web browser:** Direct access to SEC filings, earnings transcripts, company IR pages

### Data Priority Order (Signal vs. Noise)

| Priority | Source | Reliability | Use For |
|----------|--------|------------|---------|
| 1 | SEC filings (10-K, 10-Q, DEF 14A) | **Highest** — legally required | All financial facts, governance, risk factors |
| 2 | Earnings call transcripts | **High** — verbatim record | Management tone, guidance, Q&A reveals |
| 3 | Company IR materials | High but biased | Segment detail, investor presentations |
| 4 | SEC alternative filings (Form 4, 13F, 8-K) | **High** — factual | Insider behavior, institutional conviction |
| 5 | Government data (FRED, BLS, EIA, FDA) | **High** — official statistics | Macro context, industry data |
| 6 | Sell-side research (free sources) | Medium — expertise but conflicts | Consensus view, framework borrowing |
| 7 | Financial podcasts / conferences | Medium — depends on host | Management color, unconventional views |
| 8 | Financial news (Reuters, Bloomberg) | Medium-High | Event facts (strip opinion) |
| 9 | Free research platforms (Seeking Alpha free) | Medium — crowdsourced | Alternative frameworks, debate |
| 10 | Social media / Reddit | **Low** — noisy | Sentiment signal only, never as fact |

**Signal vs. Noise Rule:** Every data point must be tagged with its source tier. Analysis built on Tier 1-5 sources is presented as fact. Analysis built on Tier 6-10 sources is presented as "market commentary suggests..." or "sentiment indicates..." — never as established fact.

---

## Workflow Reference

| Workflow | File | When to Use |
|----------|------|-------------|
| Full Research Note | `workflows/full-research-note.md` | Initiation coverage or deep-dive |
| Price Target Review | `workflows/price-target-review.md` | Updating existing coverage |
| Earnings Reaction | `workflows/earnings-reaction.md` | Rapid post-earnings analysis |
| Portfolio Construction | `workflows/portfolio-construction.md` | Build optimized portfolio from multiple stock analyses |
| Cross-Stock Trigger | `workflows/cross-stock-trigger.md` | Handle cross-stock notes arriving after analysis completes |
| Batch Run | `workflows/batch-run.md` | Run multiple stocks by tag, sector, or staleness |

---

## Quality Gates

Before the Director signs off on any final output, verify:

- [ ] Every numerical claim has a source citation or `[ASSUMPTION]` / `[ESTIMATED]` tag
- [ ] DCF terminal value percentage is disclosed and flagged if > 50%
- [ ] Comp set is justified (not just "same sector")
- [ ] At least one bear case scenario is modeled with > 20% downside
- [ ] Macro risks are mapped to specific P&L line items
- [ ] Stress tests include at least one >30% downside scenario with probability
- [ ] Credit/covenant analysis completed (or flagged as data gap)
- [ ] Catalyst calendar includes at least 3 identifiable catalysts with timing
- [ ] ESG/Governance scores assigned with evidence
- [ ] Position sizing recommendation includes Kelly fraction and binding constraint
- [ ] Technical analysis confirms or explicitly flags divergence from fundamental thesis
- [ ] No unresolved contradictions between analysts (or explicitly flagged as "Key Unresolved Risk")
- [ ] Executive summary is readable in under 60 seconds
- [ ] Price target derivation shows methodology weights and math
- [ ] Data Intelligence Memo confirms Tier 1-3 data sources were retrieved (10-K, transcript, market data)
- [ ] Bear case evidence was specifically searched for (not just bull case data gathering)
- [ ] All data points are tagged with source tier (1-10) and retrieval date
- [ ] Cross-stock notes checked and addressed if relevant
- [ ] Forensic quality score assigned (Beneish M-Score calculated, accounting quality rated 1-5)
- [ ] Sentiment analysis completed (management tone scored, hedging patterns identified)
- [ ] Devil's Advocate challenge addressed (strongest counter-argument explicitly rebutted in final note)
- [ ] Probability distribution output follows `templates/probability-output-template.md` format
- [ ] Expected value price target verified with `tools/portfolio-math.py expected-value`
- [ ] Trade structure memo completed with max loss specified
- [ ] PDF report and executive summary PDF generated
- [ ] Scenario charts generated (histogram + distribution)
