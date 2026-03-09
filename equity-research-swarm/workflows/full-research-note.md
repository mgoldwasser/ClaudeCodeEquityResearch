# Workflow: Full Research Note

## Trigger
Initiation of coverage or deep-dive analysis on a specific ticker.

## Input Requirements
- **Ticker symbol** (required)
- **Materials in `input/`** (at least one of the following):
  - 10-K (annual filing) — strongly preferred
  - 10-Q (quarterly filing)
  - Earnings call transcript (most recent)
  - Prior research notes (if updating coverage)
  - Press releases, investor presentations
  - Industry reports

If no materials are provided in `input/`, the Research Analyst will retrieve all necessary data in Phase 0.

## Execution Steps

### Phase 0: Data Intelligence (Director + Research Analyst)
1. Create output directories:
   ```
   output/pass1/
   output/pass2/critiques/
   output/pass2/rebuttals/
   output/data/
   output/models/
   output/notes/
   ```
2. Spawn the **Research Analyst** to gather all available external data:
   ```
   Gather all available external data for [TICKER] following the framework in
   agents/research-analyst.md. Use all available tool scripts:
   - tools/edgar-enhanced.py filing [TICKER] 10-K (and 10-Q, DEF-14A)
   - tools/transcript-fetcher.py search [TICKER]
   - tools/market-data.sh summary [TICKER]
   - tools/market-data.sh history [TICKER] 3y
   - tools/alt-data.py ownership-summary [TICKER]
   - tools/alt-data.py analyst-estimates [TICKER]
   - tools/alt-data.py peers [TICKER]
   - tools/macro-data.py rates
   - tools/macro-data.py industry [SECTOR]
   Use WebSearch for: earnings transcripts, analyst commentary, podcasts,
   conference transcripts, industry reports, bear case evidence.
   Use WebFetch to retrieve full text of transcripts and key documents.
   Produce a Data Intelligence Memo. Save to output/pass1/data-intelligence-memo.md.
   Save retrieved data to output/data/. Save key filings to input/.
   ```
3. Wait for Research Analyst to complete.
4. Read ALL files in `input/` (now populated by Research Analyst).
5. Check `output/notes/` for cross-stock notes from prior research runs.
6. Write company context memo (3-5 sentences), including key data gaps flagged by Research Analyst.

### Phase 1: Parallel Research (Director spawns 14 analysts)
Spawn all fourteen analysts **in parallel** using the Task tool:

**Core Analysts:**

**Task 1 — DCF Analyst:**
```
Read the company context memo and all input materials in input/. Build a 5-year DCF model following your framework in agents/dcf-analyst.md. Use templates/dcf-model-template.md for output format. Save your work product to output/pass1/dcf-analysis.md.
```

**Task 2 — Quant Analyst:**
```
Read the company context memo and all input materials in input/. Run comparables analysis following your framework in agents/quant-analyst.md. Use templates/comp-table-template.md for output format. Use tools/screening.py if quantitative screens are needed. Save your work product to output/pass1/quant-analysis.md.
```

**Task 3 — Competitive Analyst:**
```
Read the company context memo and all input materials in input/. Map the competitive landscape following your framework in agents/competitive-analyst.md. Save your work product to output/pass1/competitive-analysis.md.
```

**Task 4 — Macro Analyst:**
```
Read the company context memo and all input materials in input/. Assess macro positioning following your framework in agents/macro-analyst.md. Save your work product to output/pass1/macro-analysis.md.
```

**Extended Analysts:**

**Task 5 — Risk Analyst:**
```
Read the company context memo and all input materials in input/. Quantify all risk dimensions following your framework in agents/risk-analyst.md. Include stress tests, drawdown analysis, volatility assessment, correlation analysis, and risk-adjusted return metrics. Save your work product to output/pass1/risk-analysis.md.
```

**Task 6 — Credit Analyst:**
```
Read the company context memo and all input materials in input/. Analyze capital structure, debt sustainability, covenant compliance, and liquidity following your framework in agents/credit-analyst.md. Save your work product to output/pass1/credit-analysis.md.
```

**Task 7 — Catalyst Analyst:**
```
Read the company context memo and all input materials in input/. Map all upcoming catalysts with probability, magnitude, and priced-in assessment following your framework in agents/catalyst-analyst.md. Save your work product to output/pass1/catalyst-analysis.md.
```

**Task 8 — ESG & Governance Analyst:**
```
Read the company context memo and all input materials in input/. Assess board quality, compensation alignment, shareholder rights, and material ESG risks following your framework in agents/esg-governance-analyst.md. Save your work product to output/pass1/esg-governance-analysis.md.
```

**Task 9 — Technical Analyst:**
```
Read the company context memo and all input materials in input/. Analyze price action, volume, momentum, relative strength, and entry/exit timing following your framework in agents/technical-analyst.md. Save your work product to output/pass1/technical-analysis.md.
```

**Task 10 — Sector Analyst:**
```
Read the company context memo and all input materials in input/. Analyze sector structure, growth dynamics, regulatory environment, value chain economics, market share landscape, and secular trends following your framework in agents/sector-analyst.md. Generate Python models for sector growth and market share evolution. Save your work product to output/pass1/sector-analysis.md. Save Python models to output/pass1/sector-growth-model.py and output/pass1/sector-share-model.py.
```

**Task 11 — Model Builder:**
```
Read the company context memo and all input materials in input/. Generate executable Python models for DCF, comparables, risk analysis, and credit analysis following your framework in agents/model-builder.md. All assumptions must be named variables. All models must execute with python3. Save all models to output/models/. Generate output/models/README.md listing all models.
```

**Deep Analysis Agents:**

**Task 12 — Devil's Advocate:**
```
Read the company context memo and all input materials in input/. Build an independent bear case following your framework in agents/devils-advocate.md. Identify the 3-5 key assumptions the bull thesis depends on, invert each, search for disconfirming evidence, construct the contrarian thesis, write the pre-mortem, and calculate the break-even bear probability using tools/portfolio-math.py kelly-scenarios. Do NOT read other analysts' work — your Pass 1 output must be independently derived. Save your work product to output/pass1/devils-advocate-report.md.
```

**Task 13 — Forensic Analyst:**
```
Read the company context memo and all input materials in input/. Perform forensic accounting analysis following your framework in agents/forensic-analyst.md. Calculate Beneish M-Score and Altman Z-Score using tools/portfolio-math.py beneish and tools/portfolio-math.py altman-z. Assess revenue quality, cash flow quality, balance sheet risks, and management/governance. Assign an accounting quality rating (1-5). Save your work product to output/pass1/forensic-analysis.md.
```

**Task 14 — Sentiment Analyst:**
```
Read the company context memo and all input materials in input/. Analyze management tone and communication patterns following your framework in agents/sentiment-analyst.md. Run tools/sentiment-analyzer.py analyze on the latest earnings transcript. If prior quarter transcript is available, run tools/sentiment-analyzer.py compare. Score management confidence, identify hedging clusters, analyze Q&A section, and flag red flags. Save your work product to output/pass1/sentiment-analysis.md.
```

**Wait for all fourteen tasks to complete before proceeding.**

### Phase 2: Adversarial Review (Director manages)

**Step 2.1 — Cross-Critique (parallel)**
Feed all fourteen Pass 1 work products + Data Intelligence Memo to each analyst. Spawn 15 critique tasks in parallel (14 original analysts + the Devil's Advocate produces targeted challenges):

```
You have received the work products from all fourteen analysts and the Data Intelligence Memo. Review each OTHER analyst's work (not your own). For each, identify:
1. The weakest assumption
2. The most likely source of error
3. One thing you'd change
Use the critique format in templates/critique-template.md. Be specific and cite numbers.
Save critiques to output/pass2/critiques/[your-role]-critiques.md.
```

The Devil's Advocate also produces Pass 2 targeted challenges after reading all analyst work — this is in addition to the standard critique format.

**Wait for all critiques to complete.**

**Step 2.2 — Rebuttals (parallel)**
Feed each analyst the critiques OF THEIR work. Spawn 15 rebuttal tasks in parallel:

```
You have received critiques of your Pass 1 analysis from the other analysts. Respond to each critique:
- Accept and revise your conclusion, OR
- Reject with specific reasoning, OR
- Partially accept with modifications
One paragraph per critique. No defensive language — just evidence.
Save rebuttals to output/pass2/rebuttals/[your-role]-rebuttals.md.
```

**Wait for all rebuttals to complete. ONE ROUND ONLY — no further iteration.**

### Phase 3: Synthesis (Director → Editor → Trade Structurer → Position Sizing → Director)

**Step 3.1 — Editor Synthesis**
```
Read ALL materials: all 14 Pass 1 work products, all critiques, all rebuttals, the Data Intelligence Memo, and any cross-stock notes in output/notes/. Synthesize into a complete research note using templates/research-note-template.md. Follow your framework in agents/editor.md. Integrate risk, credit, catalyst, ESG/governance, technical, forensic, sentiment, and contrarian analyses into the appropriate sections. Include probability distribution using templates/probability-output-template.md. Flag any unresolved contradictions. Save to output/pass2/editor-draft.md.
```

**Step 3.2 — Trade Structurer**
Once the Editor's draft is ready, spawn the Trade Structurer:
```
Read the Editor's draft in output/pass2/editor-draft.md and key Pass 1 work products (especially dcf-analysis.md, risk-analysis.md, competitive-analysis.md, technical-analysis.md, and devils-advocate-report.md). Follow your framework in agents/trade-structurer.md. Propose the primary trade, pair trade / hedge, options overlay, and alternative structures. Calculate risk/reward for each. Use tools/portfolio-math.py correlation for pair trades. Save to output/pass2/trade-structure.md.
```

**Step 3.3 — Position Sizing**
Once the Editor's draft is ready, spawn the Position Sizing Analyst (can run in parallel with Trade Structurer):
```
Read the Editor's draft in output/pass2/editor-draft.md and all Pass 1 work products (especially risk-analysis.md, catalyst-analysis.md, and forensic-analysis.md). Follow your framework in agents/position-sizing-analyst.md. Use tools/portfolio-math.py kelly-scenarios and tools/portfolio-math.py vol-size for calculations. Produce a complete position sizing recommendation. Save to output/pass2/position-sizing.md.
```

**Step 3.4 — Director Final Review**
The Director:
1. Reviews `output/pass2/editor-draft.md`, `output/pass2/position-sizing.md`, and `output/pass2/trade-structure.md`
2. Reviews forensic analysis — if accounting quality ≤ 2, caps conviction at 3
3. Reviews devil's advocate report — ensures key challenges are addressed
4. Assigns conviction rating (1-5)
5. Calculates probability-weighted expected price using `tools/portfolio-math.py expected-value`
6. Writes executive summary and price target recommendation
7. Integrates position sizing and trade structure into the final note
8. Resolves any flagged contradictions or marks them as "Key Unresolved Risk"
9. Saves final note to `output/[TICKER]-research-note-[DATE].md`
10. Saves scenario data to `output/[TICKER]-scenarios.json`

### Phase 4: Report Generation

**Step 4.1 — Generate Charts**
```
python tools/report-generator.py charts --scenarios-file output/[TICKER]-scenarios.json --output output/charts/ --ticker [TICKER]
```

**Step 4.2 — Generate Full Research PDF**
```
python tools/report-generator.py pdf --input output/[TICKER]-research-note-[DATE].md --output output/[TICKER]-report.pdf
```

**Step 4.3 — Generate Executive Summary PDF**
```
python tools/report-generator.py executive-summary --input output/[TICKER]-research-note-[DATE].md --output output/[TICKER]-exec-summary.pdf
```

### Phase 5: Cross-Stock Intelligence Check

After report generation:
1. Check `output/notes/` for any cross-stock notes generated during this analysis
2. Check if any notes target stocks that have already been researched
3. If a note targets a previously researched stock and is High priority, trigger the Cross-Stock Review workflow (see `workflows/cross-stock-trigger.md`)
4. Log all notes generated to `output/notes/index.md`

### Phase 6: Quality Gate
Before saving the final output, the Director checks:
- [ ] Every numerical claim has a source or assumption tag
- [ ] DCF terminal value % is disclosed
- [ ] Comp set is justified
- [ ] Bear case has >20% downside modeled
- [ ] Macro risks mapped to P&L line items
- [ ] Stress tests include >30% downside scenario with probability
- [ ] Credit/covenant analysis completed
- [ ] Catalyst calendar populated with timing
- [ ] ESG/governance scores assigned
- [ ] Position sizing recommendation with Kelly fraction
- [ ] Technical analysis confirms or flags divergence
- [ ] Forensic quality rating assigned (Beneish + Altman + 5-point scale)
- [ ] Sentiment analysis completed with confidence score
- [ ] Devil's advocate report addresses key assumptions with break-even probability
- [ ] Probability distribution uses templates/probability-output-template.md format
- [ ] Expected value calculated via tools/portfolio-math.py expected-value
- [ ] Trade structure includes max loss for every proposed trade
- [ ] PDF report and charts generated in output/
- [ ] Executive summary PDF generated
- [ ] Cross-stock notes checked and processed
- [ ] No unresolved contradictions (or explicitly flagged)
- [ ] Executive summary readable in <60 seconds
- [ ] Price target derivation shows math

## Output

Final outputs:
- `output/[TICKER]-research-note-[YYYY-MM-DD].md` — Full research note (Markdown)
- `output/[TICKER]-report.pdf` — Full research report (PDF with embedded charts)
- `output/[TICKER]-exec-summary.pdf` — Standalone executive summary (1-2 pages)
- `output/[TICKER]-scenarios.json` — Scenario data for programmatic use
- `output/charts/` — Generated visualizations (probability histogram, return distribution, sensitivity heatmap, waterfall)

Intermediate work products:
- `output/pass1/` — 14 individual analyst outputs + Data Intelligence Memo
- `output/pass2/critiques/` — Cross-analyst critiques (15 files)
- `output/pass2/rebuttals/` — Analyst rebuttals (15 files)
- `output/pass2/editor-draft.md` — Editor's synthesis
- `output/pass2/trade-structure.md` — Trade structure recommendation
- `output/pass2/position-sizing.md` — Position sizing recommendation
- `output/models/` — Executable Python models
- `output/notes/` — Cross-stock intelligence notes

## Estimated Agent Calls
- Phase 0 (Data): 1 agent (Research Analyst)
- Phase 1 (Research): 14 parallel agents
- Phase 2 critiques: 15 parallel agents
- Phase 2 rebuttals: 15 parallel agents
- Phase 3 (Synthesis): Editor + Trade Structurer + Position Sizing = 3 agents
- Total: ~48 agent invocations (but only 7 sequential phases due to parallelism)
