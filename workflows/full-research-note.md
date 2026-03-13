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
   ```bash
   mkdir -p output/[TICKER]/[DATE]/{pass1,pass2/critiques,pass2/debates,summaries,models,charts,data}
   mkdir -p output/notes
   ln -sfn [DATE] output/[TICKER]/latest
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
   Partition all data into input/financials/, input/transcripts/, input/filings/,
   input/market/, input/macro/, input/alt-data/, input/price-data/.
   Produce both a full Data Intelligence Memo AND a price-blinded Data Intelligence Memo
   (omit current stock price). Save to output/[TICKER]/[DATE]/pass1/data-intelligence-memo.md and
   output/[TICKER]/[DATE]/pass1/data-intelligence-memo-priceblind.md.
   Save retrieved data to output/[TICKER]/[DATE]/data/. Save key filings to input/.
   ```
3. Wait for Research Analyst to complete.
4. Read ALL files in `input/` (now populated by Research Analyst).
5. Check `output/notes/` for cross-stock notes from prior research runs.
6. Write a **price-blinded** company context memo (3-5 sentences), including key data gaps flagged by Research Analyst. Do not include current stock price. This memo goes to all analysts except Technical Analyst.

### Phase 1: Parallel Research (Director spawns 10 analysts)
Spawn all ten analysts **in parallel** using the Task tool:

**Core Analysts:**

**Task 1 — DCF Analyst:**
```
Read the price-blinded company context memo and input/financials/. Build a 5-year DCF model following your framework in agents/dcf-analyst.md. Use templates/dcf-model-template.md for output format. Save your work product to output/[TICKER]/[DATE]/pass1/dcf-analysis.md.
```

**Task 2 — Quant Analyst:**
```
Read the price-blinded company context memo and input/financials/ + input/market/. Run comparables analysis following your framework in agents/quant-analyst.md. Use templates/comp-table-template.md for output format. Use tools/screening.py if quantitative screens are needed. Save your work product to output/[TICKER]/[DATE]/pass1/quant-analysis.md.
```

**Task 3 — Industry Analyst:**
```
Read the price-blinded company context memo and input/market/ + input/macro/ (regulatory only). Map the competitive landscape, sector structure, growth dynamics, regulatory environment, value chain economics, market share landscape, and secular trends following your framework in agents/industry-analyst.md. Generate Python models for sector growth and market share evolution if relevant. Save your work product to output/[TICKER]/[DATE]/pass1/industry-analysis.md.
```

**Extended Analysts:**

**Task 4 — Credit Analyst:**
```
Read the price-blinded company context memo and input/financials/ + input/filings/. Analyze capital structure, debt sustainability, covenant compliance, and liquidity following your framework in agents/credit-analyst.md. Save your work product to output/[TICKER]/[DATE]/pass1/credit-analysis.md.
```

**Task 5 — Catalyst Analyst:**
```
Read the price-blinded company context memo and input/filings/ + input/transcripts/. Map all upcoming catalysts with probability, magnitude, and priced-in assessment following your framework in agents/catalyst-analyst.md. Save your work product to output/[TICKER]/[DATE]/pass1/catalyst-analysis.md.
```

**Task 6 — ESG & Governance Analyst:**
```
Read the price-blinded company context memo and input/filings/ + input/transcripts/. Assess board quality, compensation alignment, shareholder rights, and material ESG risks following your framework in agents/esg-governance-analyst.md. Save your work product to output/[TICKER]/[DATE]/pass1/esg-governance-analysis.md.
```

**Task 7 — Technical Analyst:**
```
Read the full company context memo (WITH current stock price) and input/price-data/. Analyze price action, volume, momentum, relative strength, and entry/exit timing following your framework in agents/technical-analyst.md. Save your work product to output/[TICKER]/[DATE]/pass1/technical-analysis.md.
```

**Deep Analysis Agents:**

**Task 8 — Quality & Credibility Analyst:**
```
Read the price-blinded company context memo and input/transcripts/ + input/filings/ + input/financials/. Perform forensic accounting analysis and management communication analysis following your framework in agents/quality-credibility-analyst.md. Calculate Beneish M-Score and Altman Z-Score using tools/portfolio-math.py beneish and tools/portfolio-math.py altman-z. Assess revenue quality, cash flow quality, balance sheet risks, management/governance, management tone, and communication patterns. Assign accounting quality rating (1-5) and management credibility score. Save your work product to output/[TICKER]/[DATE]/pass1/quality-credibility-report.md.
```

**Task 9 — Risk & Contrarian Analyst:**
```
You are the independent contrarian voice. DO NOT read the company context memo and DO NOT receive financial data.
Read input/macro/ + input/alt-data/ + input/filings/ only. Following your framework in agents/risk-contrarian-analyst.md:
1. Build an independent bear case by inverting the bull thesis. Search for disconfirming evidence.
2. Identify macro/systemic risks that could break the thesis.
3. Assess management execution risk and governance red flags.
4. Calculate the break-even bear probability using tools/portfolio-math.py kelly-scenarios.
Your Pass 1 output must be independently derived — do NOT read other analysts' work. Save your work product to output/[TICKER]/[DATE]/pass1/risk-contrarian-report.md.
```

**Task 10 — Model Builder:**
```
Read the price-blinded company context memo and input/financials/ + input/market/. Generate executable Python models for DCF, comparables, credit analysis, and risk analysis following your framework in agents/model-builder.md. All assumptions must be named variables. All models must execute with python3. Save all models to output/[TICKER]/[DATE]/models/. Generate output/[TICKER]/[DATE]/models/README.md listing all models.
```

**Wait for all ten tasks to complete before proceeding.**

### Phase 2: Targeted Debates (Director manages)

**Step 2.1 — Director Identifies Key Disagreements**
Read all ten Pass 1 work products. Identify the 3-5 most consequential disagreements:
- Revenue growth assumptions (DCF vs. Quant vs. Industry)
- Competitive positioning (Industry Analyst vs. Risk & Contrarian view)
- Key risks or thesis fragility (Risk & Contrarian vs. bull case defense)
- Credit/covenant headroom (Credit Analyst vs. macro stress scenarios)
- Catalyst timing and probability (Catalyst Analyst vs. Risk & Contrarian skepticism)

Write a brief memo identifying these disagreements and the analysts who should debate them.

**Step 2.2 — Targeted Critique Debates (parallel)**
Spawn ONLY the relevant analysts for each disagreement (not all-vs-all). Each debate pair/trio receives:
- Both analysts' full Pass 1 work products
- The disagreement framing
- Instructions from templates/critique-template.md

Example debate setup:
```
DCF Analyst vs. Quant Analyst vs. Industry Analyst debate: What is the realistic revenue CAGR?
[Each analyst reviews the others' revenue assumptions, points out weakest assumptions, cites evidence]
Save to output/[TICKER]/[DATE]/pass2/debates/revenue-growth-debate.md
```

Run 3-5 targeted debates in parallel (not 15 all-vs-all critiques).

**Wait for all debates to complete.**

**Step 2.2.5 — Bull Case Defense**
Spawn ONE analyst to defend the bull case against the Risk & Contrarian report:

```
You have read the Risk & Contrarian Analyst's bear case in output/[TICKER]/[DATE]/pass1/risk-contrarian-report.md.
For each major challenge to the bull thesis:
1. Identify the assumption the bear case questions
2. Present the evidence supporting the bull case
3. Assess the probability the bear case scenario occurs
Do NOT be defensive. Present the counterevidence dispassionately.
Save to output/[TICKER]/[DATE]/pass2/debates/bull-case-defense.md
```

**Step 2.3 — Summarize Debates**
Before handing materials to the Editor, run the Summarizer to compress the debate phase:

```
Read all debates in output/[TICKER]/[DATE]/pass2/debates/ and the bull case defense. Produce a single Disagreement Map following the format in agents/summarizer.md. For each disagreement: (1) What is the core question, (2) Position A, (3) Position B, (4) resolution or unresolved status. Maximum 600 words. Save to output/[TICKER]/[DATE]/summaries/disagreement-map.md
```

### Phase 3: Synthesis (Director → Editor → Trade Structurer → Position Sizing → Director)

**Step 3.1 — Editor Synthesis**
```
Read ALL materials: all 10 Pass 1 work products, all debates in output/[TICKER]/[DATE]/pass2/debates/, the Disagreement Map in output/[TICKER]/[DATE]/summaries/disagreement-map.md, the Data Intelligence Memo, and any cross-stock notes in output/notes/. Synthesize into a complete research note using templates/research-note-template.md. Follow your framework in agents/editor.md. Integrate credit, catalyst, ESG/governance, technical, quality & credibility, and risk & contrarian analyses into the appropriate sections. Use the Disagreement Map to identify key disputes and how they were (or weren't) resolved. Include probability distribution using templates/probability-output-template.md. Flag any unresolved contradictions. Save to output/[TICKER]/[DATE]/pass2/editor-draft.md.
```

**Step 3.2 — Trade Structurer**
Once the Editor's draft is ready, spawn the Trade Structurer:
```
Read the Editor's draft in output/[TICKER]/[DATE]/pass2/editor-draft.md and key Pass 1 work products (especially dcf-analysis.md, risk-contrarian-report.md, industry-analysis.md, and technical-analysis.md). Follow your framework in agents/trade-structurer.md. Propose the primary trade, pair trade / hedge, options overlay, and alternative structures. Calculate risk/reward for each. Use tools/portfolio-math.py correlation for pair trades. Save to output/[TICKER]/[DATE]/pass2/trade-structure.md.
```

**Step 3.3 — Position Sizing**
Once the Editor's draft is ready, spawn the Position Sizing Analyst (can run in parallel with Trade Structurer):
```
Read the Editor's draft in output/[TICKER]/[DATE]/pass2/editor-draft.md and all Pass 1 work products (especially risk-contrarian-report.md, catalyst-analysis.md, and quality-credibility-report.md). Follow your framework in agents/position-sizing-analyst.md. Use tools/portfolio-math.py kelly-scenarios and tools/portfolio-math.py vol-size for calculations. Produce a complete position sizing recommendation. Save to output/[TICKER]/[DATE]/pass2/position-sizing.md.
```

**Step 3.4 — Director Final Review**
The Director:
1. REVEAL current stock price to yourself (now that all research is complete)
2. Reviews `output/[TICKER]/[DATE]/pass2/editor-draft.md`, `output/[TICKER]/[DATE]/pass2/position-sizing.md`, and `output/[TICKER]/[DATE]/pass2/trade-structure.md`
3. Reviews quality & credibility report — if accounting quality ≤ 2, caps conviction at 3
4. Reviews risk & contrarian report — ensures key challenges are addressed; if strong unaddressed challenges, note as "Key Unresolved Risk"
5. Assigns conviction rating (1-5) based on analyst agreement, data quality, thesis fragility, and forensic quality
6. Calculates probability-weighted expected price using `tools/portfolio-math.py expected-value`
7. Writes executive summary and price target recommendation
8. Integrates position sizing and trade structure into the final note
9. Resolves any flagged contradictions or marks them as "Key Unresolved Risk"
10. Saves final note to `output/[TICKER]/[DATE]/[TICKER]-research-note-[DATE].md`
11. Saves scenario data to `output/[TICKER]/[DATE]/[TICKER]-scenarios.json`

### Phase 4: Report Generation

**Step 4.1 — Generate Charts**
```
python tools/report-generator.py charts --scenarios-file output/[TICKER]/[DATE]/[TICKER]-scenarios.json --output output/[TICKER]/[DATE]/charts/ --ticker [TICKER]
```

**Step 4.2 — Generate Full Research PDF**
```
python tools/report-generator.py pdf --input output/[TICKER]/[DATE]/[TICKER]-research-note-[DATE].md --output output/[TICKER]/[DATE]/[TICKER]-report-[DATE].pdf
```

**Step 4.3 — Generate Executive Summary PDF**
```
python tools/report-generator.py executive-summary --input output/[TICKER]/[DATE]/[TICKER]-research-note-[DATE].md --output output/[TICKER]/[DATE]/[TICKER]-exec-summary-[DATE].pdf
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
- [ ] Quality & credibility rating assigned (Beneish + Altman + 5-point accounting scale + management credibility score)
- [ ] Risk & Contrarian report addresses key assumptions with break-even probability
- [ ] Probability distribution uses templates/probability-output-template.md format
- [ ] Expected value calculated via tools/portfolio-math.py expected-value
- [ ] Trade structure includes max loss for every proposed trade
- [ ] PDF report and charts generated in output/
- [ ] Executive summary PDF generated
- [ ] Cross-stock notes checked and processed
- [ ] No unresolved contradictions (or explicitly flagged)
- [ ] Executive summary readable in <60 seconds
- [ ] Price target derivation shows math
- [ ] All 10 analysts represented in synthesis (or gaps explained)
- [ ] Targeted debates document 3-5 key disagreements and resolutions

## Output

Final outputs:
- `output/[TICKER]/[DATE]/[TICKER]-research-note-[YYYY-MM-DD].md` — Full research note (Markdown)
- `output/[TICKER]/[DATE]/[TICKER]-report-[DATE].pdf` — Full research report (PDF with embedded charts)
- `output/[TICKER]/[DATE]/[TICKER]-exec-summary-[DATE].pdf` — Standalone executive summary (1-2 pages)
- `output/[TICKER]/[DATE]/[TICKER]-scenarios.json` — Scenario data for programmatic use
- `output/[TICKER]/[DATE]/charts/` — Generated visualizations (probability histogram, return distribution, sensitivity heatmap, waterfall)

Intermediate work products:
- `output/[TICKER]/[DATE]/pass1/` — 10 individual analyst outputs + Data Intelligence Memos (full + price-blinded)
- `output/[TICKER]/[DATE]/pass2/debates/` — Targeted disagreement debates (3-5 files)
- `output/[TICKER]/[DATE]/pass2/debates/bull-case-defense.md` — Bull case defense against bear case
- `output/[TICKER]/[DATE]/pass2/editor-draft.md` — Editor's synthesis
- `output/[TICKER]/[DATE]/pass2/trade-structure.md` — Trade structure recommendation
- `output/[TICKER]/[DATE]/pass2/position-sizing.md` — Position sizing recommendation
- `output/[TICKER]/[DATE]/summaries/` — Compressed briefs and disagreement map
- `output/[TICKER]/[DATE]/models/` — Executable Python models
- `output/notes/` — Cross-stock intelligence notes (shared across tickers)

## Estimated Agent Calls
- Phase 0 (Data): 1 agent (Research Analyst)
- Phase 1 (Research): 10 parallel agents
- Phase 2 debates: 3-5 targeted debates (5-6 analysts involved)
- Phase 2 summarization: 1 agent (Summarizer)
- Phase 3 (Synthesis): Editor + Trade Structurer + Position Sizing = 3 agents
- Total: ~20-24 agent invocations (but only 6 sequential phases due to parallelism)
