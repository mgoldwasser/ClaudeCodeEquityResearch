# Equity Research Swarm — Master Orchestration

## Project Identity

This is an equity research team operating as a multi-agent swarm. The lead agent is the **Director of Research**. All analysis must be investment-grade, skeptical, evidence-based, and numerically rigorous.

**Writing standard:** Write like a senior sell-side analyst at a top-tier bank who is known for being right, not popular. No fluff. No hedge-fund marketing language. No "exciting opportunities" or "compelling valuations." State the thesis, show the math, flag the risks, make the call.

---

## Team Structure

### Design Principles

1. **Signal Independence:** Each analyst accesses partitioned data to produce genuinely orthogonal signals. See `agents/research-analyst.md` for the partition map.
2. **Price Blinding:** No analyst (except Technical) sees the current stock price during Pass 1. The Director reveals price only after all fair value estimates are submitted. This eliminates anchoring bias.
3. **Decision-Forcing Critiques:** Pass 2 targets only the 3-5 most consequential disagreements, not all-vs-all review. Each critique must change a number or become a "Key Unresolved Risk."
4. **Anti-Herding:** The Risk & Contrarian Analyst works independently in Pass 1 (no access to other analysts' work or company context memo). In Pass 2, the Director assigns a bull-case defender to create symmetric adversarial pressure.

### Data & Research (Runs First)

| Role | Agent File | Type | Active In |
|------|-----------|------|-----------|
| Research Analyst | `agents/research-analyst.md` | Specialist | **Phase 0** (data gathering + partitioning before all other analysts) + Pass 2 (data validation) |

### Core Analysts (Spawned in Parallel)

| Role | Agent File | Type | Active In | Data Partition |
|------|-----------|------|-----------|----------------|
| Director of Research | `agents/director-of-research.md` | Lead (Orchestrator) | Pass 1 (dispatch), Pass 2 (synthesis + final call) | All (reads full memo, passes blinded version) |
| DCF Analyst | `agents/dcf-analyst.md` | Specialist | Pass 1 (model), Pass 2 (targeted critique) | `input/financials/`, `input/transcripts/` (guidance only) |
| Quant Analyst | `agents/quant-analyst.md` | Specialist | Pass 1 (comps + screens), Pass 2 (targeted critique) | `input/financials/`, `input/market/` |
| Industry Analyst | `agents/industry-analyst.md` | Specialist | Pass 1 (sector + competitive landscape), Pass 2 (targeted critique) | `input/market/`, `input/macro/` (regulatory only) |
| Editor | `agents/editor.md` | Specialist | Pass 2 only (synthesis + formatting) | All Pass 1 outputs |

### Extended Analysts (Spawned in Parallel with Core)

| Role | Agent File | Type | Active In | Data Partition |
|------|-----------|------|-----------|----------------|
| Risk & Contrarian Analyst | `agents/risk-contrarian-analyst.md` | Specialist (INDEPENDENT) | Pass 1 (independent risk + bear case), Pass 2 (targeted challenges) | `input/macro/`, `input/alt-data/`, `input/filings/` — NO financials, NO context memo |
| Credit Analyst | `agents/credit-analyst.md` | Specialist | Pass 1 (balance sheet + debt), Pass 2 (targeted critique) | `input/financials/` (debt detail), `input/filings/` |
| Catalyst Analyst | `agents/catalyst-analyst.md` | Specialist | Pass 1 (event mapping), Pass 2 (targeted critique) | `input/transcripts/`, `input/market/`, `input/filings/` |
| ESG & Governance Analyst | `agents/esg-governance-analyst.md` | Specialist | Pass 1 (governance + ESG risks), Pass 2 (targeted critique) | `input/filings/`, `input/transcripts/` |
| Technical Analyst | `agents/technical-analyst.md` | Specialist | Pass 1 (price action + timing), Pass 2 (targeted critique) | `input/price-data/` ONLY |
| Quality & Credibility Analyst | `agents/quality-credibility-analyst.md` | Specialist | Pass 1 (accounting quality + management credibility), Pass 2 (targeted critique) | `input/transcripts/`, `input/filings/`, `input/financials/` |
| Model Builder | `agents/model-builder.md` | Specialist | Pass 1 (generates Python models), Pass 2 (validates + cross-checks) | `input/financials/` |

### Portfolio-Level Agents (Post-Analysis)

| Role | Agent File | Type | Active In |
|------|-----------|------|-----------|
| Trade Structurer | `agents/trade-structurer.md` | Specialist | Pass 2 only (trade construction after thesis established) |
| Position Sizing Analyst | `agents/position-sizing-analyst.md` | Specialist | Pass 2 only (sizing after all analysis complete) |
| Arithmetic Auditor | `agents/arithmetic-auditor.md` | Specialist (blocking gate) | Pass 2 Step 2.6.5 (after Editor/Trade/Sizing, before Director final review) |
| Portfolio Manager | `agents/portfolio-manager.md` | Specialist | Post-Pass 2 (portfolio construction from multiple stock analyses) |

### Utility Agents

| Role | Agent File | Type | Active In |
|------|-----------|------|-----------|
| Summarizer | `agents/summarizer.md` | Utility (haiku) | Between Pass 1 and Pass 2 (context compression) |

---

## Two-Pass Workflow

### Run Setup — Directory Structure + Telemetry

Before beginning any research, the Director creates the run directory and starts telemetry:

```bash
# Create per-ticker, per-date output directory
TICKER="[TICKER]"
DATE="$(date +%Y-%m-%d)"
RUN_DIR="output/${TICKER}/${DATE}"
mkdir -p "${RUN_DIR}"/{pass1,pass2/critiques,summaries,models,charts,data}

# Update the "latest" symlink for this ticker
ln -sfn "${DATE}" "output/${TICKER}/latest"

# Record run start time
date -u +"%Y-%m-%dT%H:%M:%SZ"
```

Save the start timestamp in `output/[TICKER]/[DATE]/data/telemetry.json`. Record timestamps at each phase boundary (start and end of each phase below). After each subagent returns, record its token usage (input/output tokens, model) from the response metadata. If exact token counts are unavailable, estimate from content length (1 token ≈ 4 chars English) and mark with `[EST]`.

**All output paths below use `output/[TICKER]/[DATE]/` as the run root.** The `latest` symlink always points to the most recent run date for that ticker.

### Pass 1 — Parallel Research (Price-Blinded)

The Director first spawns the Research Analyst to gather and PARTITION external data, then spawns all analysts in parallel with partitioned data access. **No analyst except Technical sees the current stock price.**

**Spawning instructions for the Director:**

1. **Phase 0 — Data Intelligence + Partitioning:** Spawn the Research Analyst first:
   - **Research Analyst:** "Gather all available external data for [TICKER] following the framework in `agents/research-analyst.md`. Use all available tool scripts. Produce a Data Intelligence Memo AND a price-blinded version. Partition all data into the directory structure defined in your agent file (`input/financials/`, `input/transcripts/`, `input/filings/`, `input/market/`, `input/macro/`, `input/alt-data/`, `input/price-data/`). Save retrieved data to `output/[TICKER]/[DATE]/data/` and partitioned inputs to `input/`."
   - Wait for Research Analyst to complete. Review the FULL Data Intelligence Memo (Director only).

2. Read and digest all files in `input/` (Director sees everything).
3. Check `output/notes/` for cross-stock notes from other research runs.
4. Write a **price-blinded** company context memo (see `agents/director-of-research.md` for blinding rules).
5. Spawn the following agents **in parallel** (all 10 research analysts simultaneously). For each, the spawn prompt is: *"Follow `agents/<agent-file>.md`. Input partitions: <partitions>. Context: [blinded memo]."* Full role definitions (including mandatory steps, templates to use, and outputs) live in the agent files — do not duplicate them inline.

   | Agent | Agent file | Input partitions |
   |-------|-----------|------------------|
   | DCF Analyst | `agents/dcf-analyst.md` | `input/financials/`, `input/transcripts/` (guidance only) |
   | Quant Analyst | `agents/quant-analyst.md` | `input/financials/`, `input/market/` |
   | Industry Analyst | `agents/industry-analyst.md` | `input/market/`, `input/macro/` (regulatory only) |
   | Risk & Contrarian | `agents/risk-contrarian-analyst.md` | `input/macro/`, `input/alt-data/`, `input/filings/` (risk factors only) — **NO context memo, NO financials** |
   | Credit Analyst | `agents/credit-analyst.md` | `input/financials/` (debt), `input/filings/` (covenants) |
   | Catalyst Analyst | `agents/catalyst-analyst.md` | `input/transcripts/`, `input/market/`, `input/filings/` (8-K) |
   | ESG & Governance | `agents/esg-governance-analyst.md` | `input/filings/` (proxy, DEF 14A), `input/transcripts/` |
   | Technical Analyst | `agents/technical-analyst.md` | `input/price-data/` ONLY |
   | Quality & Credibility | `agents/quality-credibility-analyst.md` | `input/transcripts/`, `input/filings/`, `input/financials/` |
   | Model Builder | `agents/model-builder.md` | `input/financials/` → saves to `output/[TICKER]/[DATE]/models/` |

6. The **Editor**, **Position Sizing Analyst**, **Trade Structurer**, and **Portfolio Manager** do NOT participate in Pass 1.

7. Collect all Pass 1 work products. Save each to `output/[TICKER]/[DATE]/pass1/` with filenames:
   - `output/[TICKER]/[DATE]/pass1/data-intelligence-memo.md` (from Phase 0 Research Analyst)
   - `output/[TICKER]/[DATE]/pass1/dcf-analysis.md`
   - `output/[TICKER]/[DATE]/pass1/quant-analysis.md`
   - `output/[TICKER]/[DATE]/pass1/industry-analysis.md`
   - `output/[TICKER]/[DATE]/pass1/risk-contrarian-report.md`
   - `output/[TICKER]/[DATE]/pass1/credit-analysis.md`
   - `output/[TICKER]/[DATE]/pass1/catalyst-analysis.md`
   - `output/[TICKER]/[DATE]/pass1/esg-governance-analysis.md`
   - `output/[TICKER]/[DATE]/pass1/technical-analysis.md`
   - `output/[TICKER]/[DATE]/pass1/quality-credibility-report.md`
   - `output/[TICKER]/[DATE]/data/` (all retrieved data files from Research Analyst)
   - `output/[TICKER]/[DATE]/models/` (all Python models from Model Builder and Industry Analyst)
   - `output/notes/` (cross-stock intelligence notes — shared across tickers, not per-run)

### Pass 1.5 — Context Compression

Before starting Pass 2, run the Summarizer to reduce context size.

**Step 1.5 — Summarize Pass 1 Work Products**

Spawn the Summarizer (runs on Haiku with low effort):

> "Read all 10 work products in `output/[TICKER]/[DATE]/pass1/`. For each one, produce a structured brief following the Standard Brief Format in `agents/summarizer.md`. Save all briefs to `output/[TICKER]/[DATE]/summaries/`. Each brief must be under 400 words while preserving all numbers, assumptions, source citations, and data gap flags."

Save briefs to `output/[TICKER]/[DATE]/summaries/[analyst-name]-brief.md`.

### Pass 2 — Decision-Forcing Review + Synthesis

Once all Pass 1 work products are collected and summarized:

**Step 2.1 — Identify Key Disagreements (Director)**

The Director reads all summary briefs and identifies the **3-5 most consequential disagreements** by comparing analyst conclusions. Examples:
- DCF fair value vs. Quant fair value (if >15% divergence)
- Risk & Contrarian bear probability vs. other analysts' implied probability
- Growth rate assumptions that differ by >5 percentage points
- Any assumption where two analysts reach opposite conclusions

For each disagreement, the Director defines:
- The specific question to resolve (e.g., "What is the appropriate WACC: 14% or 16%?")
- Which 2-3 analysts are the relevant parties
- What evidence would resolve it

**Step 2.2 — Targeted Critiques (3-5 Focused Debates)**

For EACH identified disagreement, spawn ONLY the relevant analysts:

> "[Analyst A] and [Analyst B]: You disagree on [specific issue]. [A] argues [position with number]. [B] argues [position with number]. Each of you: (1) state your best evidence, (2) identify the weakest point in the other's argument, (3) propose a resolution with a specific revised number. If no resolution is possible, state your competing probability ranges for the final note's 'Key Unresolved Risk' section."

Spawn all 3-5 targeted critique tasks **in parallel**. Save to `output/[TICKER]/[DATE]/pass2/critiques/`.

**Step 2.2.5 — Bull Case Defense (Anti-Herding)**

The Director assigns ONE analyst (not the Risk & Contrarian) to explicitly defend the bull case against the Risk & Contrarian's bear case. This creates symmetric adversarial pressure:

> "[Assigned Analyst]: The Risk & Contrarian Analyst has constructed a bear case arguing [summary]. Your job is to defend the bull case with specific evidence. What is the strongest counter-argument to each of the Risk & Contrarian's key concerns? Where does the bear case overstate risk or underweight positive catalysts?"

Save to `output/[TICKER]/[DATE]/pass2/bull-defense.md`.

**Step 2.3 — Summarize Debates**

Run the Summarizer to compress the critique phase:

> "Read all critiques in `output/[TICKER]/[DATE]/pass2/critiques/` and the bull defense in `output/[TICKER]/[DATE]/pass2/bull-defense.md`. Produce a single Disagreement Map following the format in `agents/summarizer.md`. For each debate: state the resolution (revised number) or flag as 'Key Unresolved Risk' with competing ranges. Save to `output/[TICKER]/[DATE]/summaries/disagreement-map.md`. Maximum 600 words."

**Step 2.4 — Editor Synthesis**

Hand materials to the Editor in this priority order:
1. **Full** Pass 1 work products (10 analyst outputs) — the Editor needs complete detail for synthesis
2. **Disagreement Map** (from `output/[TICKER]/[DATE]/summaries/disagreement-map.md`) — compressed view of targeted critiques and bull defense
3. The Editor may read individual critiques from `output/[TICKER]/[DATE]/pass2/` only if the Disagreement Map flags an unresolved contradiction that needs full context

Instruction to Editor:

> "Synthesize all materials into a final research note using `templates/research-note-template.md`. Follow the framework in `agents/editor.md`. Do NOT summarize — synthesize into one coherent argument. Use the Disagreement Map in `output/[TICKER]/[DATE]/summaries/disagreement-map.md` to identify key disputes and resolutions. Read full critiques only for unresolved contradictions. Integrate the Risk & Contrarian report, Quality & Credibility report, Industry analysis, credit, catalyst, ESG/governance, and technical analyses into the appropriate sections. Include probability distributions using `templates/probability-output-template.md`. Run `python tools/signal-independence.py report --run-dir output/[TICKER]/[DATE]` and paste the output verbatim as Appendix F — Signal Independence Audit. The Director will separately enforce the hard gate (R_hard ≥ 0.5) as a blocking pre-publication check."

Save Editor output to `output/[TICKER]/[DATE]/pass2/editor-draft.md`.

**Step 2.5 — Trade Structurer**

Once the Editor's draft is complete, spawn the Trade Structurer:

> "Design the optimal trade structure to express the thesis following the framework in `agents/trade-structurer.md`. Read the Editor's draft for rating, price target, and thesis. Check options data with `tools/market-data.sh options [TICKER]` and peer correlations with `tools/portfolio-math.py correlation`. Produce a Trade Structure Memo with primary trade, hedge, alternatives, and risk/reward profiles."

Save to `output/[TICKER]/[DATE]/pass2/trade-structure-memo.md`.

**Step 2.6 — Position Sizing**

Once the Editor's draft is complete (can run in parallel with Trade Structurer), spawn the Position Sizing Analyst:

> "Read the Editor's draft and all Pass 1 work products (especially Risk & Contrarian and Catalyst Analyst outputs). Follow the framework in `agents/position-sizing-analyst.md`. Produce a position sizing recommendation including Kelly fraction, entry strategy, exit triggers, and portfolio context."

Save to `output/[TICKER]/[DATE]/pass2/position-sizing.md`.

**Step 2.6.5 — Arithmetic Auditor (Blocking Gate)**

After Trade Structurer and Position Sizing complete, spawn the Arithmetic Auditor:

> "Read the Editor's draft at `output/[TICKER]/[DATE]/pass2/editor-draft.md`, the Pass 1 source outputs in `output/[TICKER]/[DATE]/pass1/`, and the structured data at `output/[TICKER]/[DATE]/data/`. Run all 12 mandatory checks in `agents/arithmetic-auditor.md`. Save the Arithmetic Audit Report to `output/[TICKER]/[DATE]/pass2/arithmetic-audit.md`. Return a GREEN / YELLOW / RED verdict."

**Gate behavior:**
- **GREEN:** proceed to Step 2.7.
- **YELLOW (unauditable items, no failures):** Director reviews the unauditable list; if acceptable, proceed with the unauditable count recorded in telemetry. Otherwise re-dispatch the responsible analyst.
- **RED (any FAIL):** Director **must not** proceed to Step 2.7. Re-dispatch the Editor or the responsible Pass 1 analyst with the specific failing check and the corrected value. After fix, re-run the Auditor. Only GREEN or accepted-YELLOW clears the gate.

**Step 2.7 — Director Final Review (Price Reveal)**

The Director:
1. Reviews the Editor's draft, Trade Structure Memo, and Position Sizing recommendation.
2. **PRICE REVEAL:** Now (and only now) reveal the current stock price. Record each analyst's price-blind fair value estimate BEFORE comparing to market price. The gap between analyst fair values and market price IS the investment signal.
3. Assigns a conviction rating (1-5) based on:
   - Analyst agreement level (high agreement = higher conviction, unless groupthink suspected)
   - Data quality (more [DATA GAP] flags = lower conviction)
   - Thesis fragility (how many things have to go right?)
   - Quality & Credibility score (≤ 2/5 caps conviction at 2)
   - Risk & Contrarian challenge strength (strong unaddressed challenges reduce conviction)
4. Writes the executive summary and price target recommendation.
5. Derives price target: set probability weights (bull/base/bear) BEFORE calculating scenario prices. The expected value vs. current price gap is the signal — do NOT adjust weights to close it.
6. Runs `python tools/portfolio-math.py expected-value` to verify probability-weighted price target.
7. If analysts fundamentally disagree on a key assumption and the targeted debates didn't resolve it, the Director flags it as a **"Key Unresolved Risk"** rather than forcing false consensus.
8. Shows the analyst-blind fair values vs. market price table in the final note appendix.
9. Saves the final note to `output/[TICKER]/[DATE]/[TICKER]-research-note-[DATE].md`.

**Step 2.8 — Report Generation**

The Director generates final deliverables:
1. `python tools/report-generator.py charts --scenarios-file output/[TICKER]/[DATE]/data/[TICKER]-scenarios.json --output output/[TICKER]/[DATE]/charts/ --ticker [TICKER] --current-price [PRICE]`
2. `python tools/report-generator.py pdf --input output/[TICKER]/[DATE]/[TICKER]-research-note-[DATE].md --output output/[TICKER]/[DATE]/[TICKER]-report-[DATE].pdf --charts-dir output/[TICKER]/[DATE]/charts/`
3. `python tools/report-generator.py executive-summary --input output/[TICKER]/[DATE]/[TICKER]-research-note-[DATE].md --output output/[TICKER]/[DATE]/[TICKER]-exec-summary-[DATE].pdf --chart output/[TICKER]/[DATE]/charts/scenario-histogram.png`

**Step 2.9 — Cross-Stock Trigger Check**

After analysis completes, check `output/notes/` for cross-stock notes and follow `workflows/cross-stock-trigger.md`.

**Step 2.10 — Telemetry Finalization**

Record the run end time. Compile all phase timestamps and agent token usage into `output/[TICKER]/[DATE]/data/telemetry.json`. Include:
- Wall-clock time per phase and total
- Token usage per agent (input, output, total, model)
- Total tokens (input + output) across all agents
- Estimated cost based on published API pricing (Opus input: $15/MTok, output: $75/MTok; Sonnet input: $3/MTok, output: $15/MTok; Haiku input: $0.25/MTok, output: $1.25/MTok — update rates if pricing has changed)
- Include the telemetry summary as Section 17 of the final research note

---

## Output Format

The final research note in `output/[TICKER]/[DATE]/[TICKER]-research-note-[DATE].md` follows `templates/research-note-template.md` (17 sections: Executive Summary → Investment Thesis → Business Overview → Financial Analysis → Credit & Balance Sheet → Industry & Competitive Position → Risk/Macro/Contrarian → Catalyst Calendar → ESG & Governance → Technical Context → Quality & Credibility → Analyst Debate Summary → Price Target Derivation → Position Sizing → Executable Models → Appendix → Research Run Telemetry). See the template for per-section content requirements.

### Portfolio-Level Output (Multi-Stock Mode)

When the Portfolio Manager is activated (after analyzing multiple stocks), the final portfolio output is saved to `output/portfolio/` and includes:
- `output/portfolio/portfolio-construction-[DATE].md` — Final portfolio with all positions, weights, and metrics
- `output/portfolio/optimizer.py` — Executable portfolio optimization model
- `output/portfolio/correlation-matrix.py` — Correlation analysis code
- `output/portfolio/scenario-model.py` — Monte Carlo portfolio simulation

### Directory Structure — Key Conventions

- Run root is `output/[TICKER]/[DATE]/` with subdirs `pass1/`, `pass2/` (+ `critiques/`), `summaries/`, `models/`, `charts/`, `data/`. Exact filenames are listed in the Pass 1 / Pass 2 steps above.
- `output/[TICKER]/latest/` symlinks to the most recent run — use for quick access. Updated at the START of each run, so it may point to an incomplete run if one failed (check `telemetry.json` for completion).
- Previous runs are preserved indefinitely.
- `output/notes/` holds cross-stock intelligence (shared across tickers, not per-run).
- `output/portfolio/` holds portfolio-level output (shared).

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

## Token Efficiency & Data Formats

### Inter-Agent Data Passing

Choose the format that minimizes tokens for the data type:

| Data Type | Best Format | Why | Example |
|-----------|------------|-----|---------|
| Structured numerical data (prices, financials, ratios) | **JSON** | Compact, parseable, no prose overhead | `output/[TICKER]/[DATE]/data/*.json` |
| Analyst prose (reports, memos, critiques) | **Markdown** | More token-dense than JSON for text; no key/value wrapper overhead | `output/[TICKER]/[DATE]/pass1/*.md` |
| Tabular data (comp tables, sensitivity matrices) | **Markdown tables** or **CSV** | Markdown tables are readable; CSV is smallest for large datasets | Inline tables or `output/[TICKER]/[DATE]/data/*.csv` |
| Scenario parameters (bull/base/bear inputs) | **JSON** | Agents can parse directly; avoids ambiguity | `output/[TICKER]/[DATE]/data/*-scenarios.json` |
| Cross-agent summaries | **Structured markdown** (brief format) | Fixed headings + bullet points = high info density, low tokens | `output/[TICKER]/[DATE]/summaries/*.md` |

**Rules:**
- Never wrap prose in JSON. A 2,000-word analyst report as a JSON string with escaped newlines costs ~30% more tokens than plain markdown.
- Never pass raw API responses between agents. Extract only the fields needed and save structured data to `output/[TICKER]/[DATE]/data/`.
- For numerical results that downstream agents need to parse, use JSON with flat keys (avoid deep nesting).
- For human-readable output that agents also consume, use markdown with consistent heading structure.
- When an agent only needs 3 numbers from a 5,000-token report, use the Summarizer or have the upstream agent save a separate small file with just those numbers.

### Context Budget Guidelines

| Phase | What gets loaded | Target context size |
|-------|-----------------|-------------------|
| Pass 1 (each analyst) | Partitioned input data + blinded context memo | ~10-20K tokens |
| Pass 2 Targeted Critiques (2-3 analysts each) | Own full report + counterpart's brief + Director's framing | ~8-15K tokens per debate |
| Pass 2 Bull Defense (1 analyst) | Risk & Contrarian report + own analysis | ~10-15K tokens |
| Pass 2 Editor | 10 full reports + disagreement map | ~45K tokens (vs ~120K+ with old all-vs-all) |
| Portfolio Manager | Per-stock portfolio briefs (not full notes) | ~5-10K tokens per stock |

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

**Data & Sources:**
- [ ] Every numerical claim has a source citation or `[ASSUMPTION]` / `[ESTIMATED]` tag
- [ ] All data points are tagged with source tier (1-10) and retrieval date
- [ ] Data Intelligence Memo confirms Tier 1-3 data sources were retrieved (10-K, transcript, market data)
- [ ] Bear case evidence was specifically searched for (not just bull case data gathering)
- [ ] Cross-stock notes checked and addressed if relevant
- [ ] At least 2 independent TAM estimates retrieved (or gap flagged as `[CRITICAL DATA GAP]`)
- [ ] Historical CAGRs calculated (1-year, 3-year, 5-year) for subject company and sector
- [ ] Actual diluted share count retrieved from latest 10-K/10-Q (not estimated)

**Price Blinding & Anti-Anchoring:**
- [ ] No analyst (except Technical) received the current stock price during Pass 1
- [ ] Analyst fair value estimates were recorded BEFORE price reveal in Step 2.7
- [ ] Probability weights (bull/base/bear) were set BEFORE scenario prices were calculated
- [ ] Analyst-blind fair values vs. market price table included in appendix
- [ ] If all fair values cluster within ±5% of market price, residual anchoring investigated

**Demand & TAM Analysis:**
- [ ] Application-level demand decomposition completed (at least 5 workload types with adoption stage, growth model, compute intensity)
- [ ] Technology adoption framework positions sector on maturity curve with at least 2 historical analogues (cloud, mobile, internet, etc.)
- [ ] Demand multiplier scenarios model at least 3 potential new application waves (agents, robotics, video AI, sovereign AI, etc.)
- [ ] Top-down TAM vs bottom-up application-level TAM reconciled (or gap >20% explained)
- [ ] Algorithm efficiency modeled for both supply-side (cost reduction) AND demand-side (Jevons paradox / usage increase)
- [ ] Forward CAGR explicitly compared to historical CAGR with divergence justified
- [ ] Growth deceleration (if assumed) has specific mechanism identified — "growth always decelerates" is not analysis

**Financial Analysis:**
- [ ] DCF terminal value percentage is disclosed and flagged if > 50%
- [ ] Comp set is justified (not just "same sector")
- [ ] Credit/covenant analysis completed (or flagged as data gap)
- [ ] Price target derivation shows methodology weights and math
- [ ] Expected value price target verified with `tools/portfolio-math.py expected-value`
- [ ] Probability distribution output follows `templates/probability-output-template.md` format
- [ ] DCF revenue projections cross-checked against Industry Analyst bottom-up TAM (within ±15%)

**Risk & Contrarian:**
- [ ] At least one bear case scenario is modeled with > 20% downside
- [ ] Stress tests include at least one >30% downside scenario with probability
- [ ] Risk & Contrarian Analyst's strongest challenge explicitly addressed in final note
- [ ] Bull case defense completed (symmetric adversarial pressure)
- [ ] Macro risks are mapped to specific P&L line items

**Quality & Credibility:**
- [ ] Quality & Credibility score assigned (Beneish M-Score calculated, accounting quality rated 1-5)
- [ ] Management tone scored, hedging patterns identified, credibility trend assessed
- [ ] If quality score ≤ 2/5, conviction capped at 2

**Other Analysts:**
- [ ] Catalyst calendar includes at least 3 identifiable catalysts with timing
- [ ] ESG/Governance scores assigned with evidence
- [ ] Technical analysis confirms or explicitly flags divergence from fundamental thesis
- [ ] Strategic Power Assessment completed using Helmer 7 Powers framework with 1-10 scores and quantified evidence
- [ ] Financial Translation Matrix maps each Power to specific DCF assumptions (margin, growth, retention, share, pricing, WACC)
- [ ] Power Durability Timeline shows half-life for each Power; cliff risk flagged if >3 Powers erode within same 2-year window
- [ ] Competitive Vulnerability Map scores top 2-3 competitors on same 7 Powers
- [ ] DCF Analyst has validated key assumptions against Financial Translation Matrix; fragile assumptions flagged

**Synthesis & Output:**
- [ ] No unresolved contradictions between analysts (or explicitly flagged as "Key Unresolved Risk")
- [ ] Executive summary is readable in under 60 seconds
- [ ] Position sizing recommendation includes Kelly fraction and binding constraint
- [ ] Trade structure memo completed with max loss specified
- [ ] Arithmetic Audit (Step 2.6.5) returned GREEN or accepted-YELLOW verdict; report saved to `output/[TICKER]/[DATE]/pass2/arithmetic-audit.md`
- [ ] Signal Independence gate passed: `python tools/signal-independence.py gate --run-dir output/[TICKER]/[DATE]` returned exit 0 (R_hard ≥ 0.5); `pass2/signal-audit.json` saved; report pasted verbatim into Appendix F
- [ ] IPS compliance gate passed: `python tools/ips-validator.py --run-dir output/[TICKER]/[DATE] --ips <active-ips>` returned exit 0 (ELIGIBLE or ELIGIBLE_WITH_EXCEPTIONS); `pass2/ips-compliance.md` saved; any UNVERIFIED exceptions documented in Section 16
- [ ] Benchmark Comparison block generated via `tools/benchmark-compare.py` and pasted into Section 12; `N/A` baselines (if any) traced back to a specific upstream data gap, not a silent omission
- [ ] Chain-of-custody snapshotted: `tools/reproducibility.py snapshot --run-dir output/[TICKER]/[DATE] --seed <seed>` executed after Phase 0 and before parallel analyst dispatch; `inputs-snapshot/` populated; `reproducibility.json` records seed/as_of/tool-versions/file-hashes
- [ ] Chain-of-custody verified: `tools/reproducibility.py verify --run-dir output/[TICKER]/[DATE]` returned exit 0 (no drift); manifest block rendered into Appendix K
- [ ] PDF report and executive summary PDF generated
- [ ] Scenario charts generated (histogram + distribution)
- [ ] Telemetry JSON saved to `output/[TICKER]/[DATE]/data/telemetry.json` with timing and token usage
- [ ] Research Run Telemetry section included in final research note (Section 17)
