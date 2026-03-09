# Equity Research Swarm

A multi-agent equity research system built on Claude Code agent teams. Twenty specialized AI analysts collaborate through a data intelligence phase and two-pass adversarial review process to produce investment-grade research notes with PDF reports, probability-weighted scenario analysis, forensic accounting checks, contrarian stress tests, trade structuring, position sizing, and executable Python models.

## How It Works

The system runs a team of twenty agents:

### Data & Research (Runs First)
| Agent | Role | Phase 0 | Pass 2 |
|-------|------|---------|--------|
| **Research Analyst** | Data intelligence | Gathers all external data before analysts | Validates data, challenges stale sources |

### Core Analysts
| Agent | Role | Pass 1 | Pass 2 |
|-------|------|--------|--------|
| **Director of Research** | Orchestrator | Dispatches analysts | Synthesizes + final call |
| **DCF Analyst** | Intrinsic valuation | Builds 5-year DCF with scenarios | Critiques + rebuttals |
| **Quant Analyst** | Relative valuation | Comparables analysis + screens | Critiques + rebuttals |
| **Competitive Analyst** | Strategic positioning | Moat + market share + cross-stock notes | Critiques + rebuttals |
| **Macro Analyst** | External risk | Macro overlay + cycle positioning | Critiques + rebuttals |
| **Editor** | Quality control | Inactive | Synthesizes final note |

### Extended Analysts
| Agent | Role | Pass 1 | Pass 2 |
|-------|------|--------|--------|
| **Risk Analyst** | Risk quantification | Stress tests, drawdowns, VaR | Critiques + rebuttals |
| **Credit Analyst** | Balance sheet / debt | Capital structure, covenants, liquidity | Critiques + rebuttals |
| **Catalyst Analyst** | Event mapping | Catalyst calendar, options-implied | Critiques + rebuttals |
| **ESG & Governance Analyst** | Governance / ESG risk | Board quality, comp alignment, ESG | Critiques + rebuttals |
| **Technical Analyst** | Price action / timing | Trend, volume, momentum, levels | Critiques + rebuttals |
| **Sector Analyst** | Sector structure / growth | TAM, market share, regulation, cross-stock notes | Critiques + rebuttals |
| **Position Sizing Analyst** | Portfolio implementation | Inactive | Sizing after all analysis |

### Deep Analysis Agents
| Agent | Role | Pass 1 | Pass 2 |
|-------|------|--------|--------|
| **Devil's Advocate** | Contrarian stress test | Independent bear case, assumption challenges | Targeted challenges to all analysts |
| **Forensic Analyst** | Accounting quality | Beneish M-Score, Altman Z, revenue quality | Critiques + rebuttals |
| **Sentiment Analyst** | Management tone | Transcript NLP, confidence scoring, red flags | Critiques + rebuttals |

### Portfolio-Level Agents
| Agent | Role | Pass 1 | Pass 2 |
|-------|------|--------|--------|
| **Model Builder** | Quantitative modeling | Generates executable Python models | Validates + updates models |
| **Portfolio Manager** | Portfolio construction | Inactive (single-stock) | Constructs multi-stock portfolio |
| **Trade Structurer** | Trade construction | Inactive | Pair trades, hedges, options overlays |

**Phase 0:** Research Analyst gathers all external data (SEC filings, transcripts, market data, insider/institutional ownership, macro data, analyst consensus, bear case evidence).
**Pass 1:** Fourteen analysts work in parallel on their specialties, working from the enriched data set.
**Pass 2:** Each analyst critiques the others' work (15 critiques + 15 rebuttals), the Editor synthesizes everything, the Trade Structurer proposes trade structures, the Position Sizing Analyst produces implementation guidance, and the Director makes the final call.
**Report Generation:** Charts, full PDF report, and standalone executive summary PDF are generated automatically.

## Quick Start

```bash
cd equity-research-swarm

# Option 1: Drop filings into input/ first
cp ~/Downloads/AAPL-10K-2024.pdf input/
cp ~/Downloads/AAPL-Q4-transcript.txt input/

claude "Run the full-research-note workflow for AAPL. All input materials are in input/. Follow the CLAUDE.md orchestration protocol."

# Option 2: Let the system fetch filings automatically
claude "Run the full-research-note workflow for MSFT. No input materials provided — retrieve the latest 10-K and earnings transcript via web search. Follow the CLAUDE.md orchestration protocol."
```

## Workflows

### Full Research Note
Deep-dive or initiation coverage. Uses all 20 agents, both passes, report generation. ~48 agent invocations across 7 sequential phases.

```bash
claude "Run the full-research-note workflow for [TICKER]. All input materials are in input/. Follow the CLAUDE.md orchestration protocol."
```

### Price Target Review
Update an existing note with new data. Only spawns agents relevant to what changed.

```bash
# Put prior note + new data in input/
cp existing-note.md input/
cp new-earnings-release.pdf input/

claude "Run the price-target-review workflow for [TICKER]. Prior research note and new earnings data are in input/. Follow the CLAUDE.md orchestration protocol."
```

### Earnings Reaction
Rapid post-earnings analysis (skips adversarial review for speed). ~6-7 agents.

```bash
cp earnings-release.pdf input/
cp earnings-transcript.txt input/

claude "Run the earnings-reaction workflow for [TICKER]. Earnings release and transcript are in input/. Follow the CLAUDE.md orchestration protocol."
```

### Batch Run
Run research on multiple stocks filtered by tag, sector, or staleness. Includes cross-stock intelligence processing between stocks.

```bash
# See what needs refreshing
python3 tools/batch-runner.py stale

# Generate a run plan for Magnificent Seven
python3 tools/batch-runner.py plan --tag mag7

# Run all stale stocks
python3 tools/batch-runner.py plan --stale

# Run a specific sector
python3 tools/batch-runner.py plan --sector Healthcare

# Execute the batch
claude "Run the batch-run workflow for all mag7 stocks. Follow the CLAUDE.md orchestration protocol and workflows/batch-run.md."
```

### Stock Universe Management

```bash
# Add a stock
python3 tools/batch-runner.py add PLTR "Palantir Technologies" --sector Technology --tags ai,software,government

# List stocks by tag
python3 tools/batch-runner.py list --tag semiconductors

# Universe dashboard
python3 tools/batch-runner.py status

# Available tags
python3 tools/batch-runner.py tags
```

### Portfolio Construction
Multi-stock portfolio optimization. Runs after individual stock analyses are complete. Constructs a concentrated portfolio (~20-40 positions) with correlation management, factor exposure limits, and risk budgets.

```bash
# After running full-research-note for multiple tickers:
claude "Run the portfolio-construction workflow. Use all completed research notes in output/. Follow the CLAUDE.md orchestration protocol."
```

## Output

All output goes to `output/`. Final deliverables per stock:
- `output/[TICKER]-research-note-[YYYY-MM-DD].md` — Full research note (Markdown)
- `output/[TICKER]-report.pdf` — Full research report (PDF with embedded charts)
- `output/[TICKER]-exec-summary.pdf` — Standalone executive summary (1-2 pages)
- `output/[TICKER]-scenarios.json` — Scenario data for programmatic use
- `output/charts/` — Probability histogram, return distribution, sensitivity heatmap, waterfall

Other workflow outputs:
- `output/[TICKER]-price-target-review-[YYYY-MM-DD].md`
- `output/[TICKER]-earnings-reaction-[YYYY-MM-DD].md`
- `output/portfolio/portfolio-[YYYY-MM-DD].md` — Multi-stock portfolio recommendation

Intermediate work products (useful for debugging or deep dives):
- `output/pass1/` — Individual analyst outputs (14 files + Data Intelligence Memo)
- `output/pass2/critiques/` — Cross-analyst critiques (15 files)
- `output/pass2/rebuttals/` — Analyst rebuttals (15 files)
- `output/pass2/editor-draft.md` — Editor's synthesis before Director review
- `output/pass2/trade-structure.md` — Trade structure recommendation
- `output/pass2/position-sizing.md` — Position sizing recommendation
- `output/models/` — Executable Python models (DCF, comps, risk, sector, credit, portfolio optimizer)
- `output/models/README.md` — Model index with inputs, outputs, and validation status
- `output/notes/` — Cross-stock intelligence notes (generated when analysis reveals competitor-relevant information)
- `output/portfolio/` — Portfolio construction outputs (correlation matrix, optimization results, implementation plan)

## Project Structure

```
equity-research-swarm/
├── CLAUDE.md                          # Master orchestration config
├── README.md                          # This file
├── .claude/
│   └── settings.json                  # Permissions + agent teams enabled
├── agents/
│   ├── director-of-research.md        # Lead orchestrator
│   ├── dcf-analyst.md                 # Cash flow / valuation
│   ├── quant-analyst.md               # Comparables / quantitative
│   ├── competitive-analyst.md         # Competitive landscape
│   ├── macro-analyst.md               # Macro / sector / cycle
│   ├── risk-analyst.md                # Risk quantification / stress tests
│   ├── credit-analyst.md              # Balance sheet / debt / covenants
│   ├── catalyst-analyst.md            # Event mapping / catalyst timing
│   ├── esg-governance-analyst.md      # Governance / ESG risk
│   ├── technical-analyst.md           # Price action / entry-exit timing
│   ├── sector-analyst.md              # Sector structure / growth modeling
│   ├── research-analyst.md            # External data intelligence / web research
│   ├── position-sizing-analyst.md     # Portfolio implementation / bet sizing
│   ├── portfolio-manager.md           # Multi-stock portfolio construction
│   ├── model-builder.md               # Python model generation
│   ├── editor.md                      # Final synthesis / QC
│   ├── devils-advocate.md             # Contrarian analysis / assumption stress testing
│   ├── forensic-analyst.md            # Accounting quality / fraud detection
│   ├── sentiment-analyst.md           # Transcript tone / management credibility
│   └── trade-structurer.md            # Trade construction / hedging / options
├── workflows/
│   ├── full-research-note.md          # End-to-end deep dive
│   ├── price-target-review.md         # Update existing coverage
│   ├── earnings-reaction.md           # Rapid post-earnings
│   ├── portfolio-construction.md      # Multi-stock portfolio optimization
│   ├── cross-stock-trigger.md         # Cross-stock intelligence re-analysis
│   └── batch-run.md                   # Multi-stock batch execution
├── templates/
│   ├── research-note-template.md      # Final output format
│   ├── dcf-model-template.md          # DCF output format
│   ├── comp-table-template.md         # Comparables format
│   ├── critique-template.md           # Agent-to-agent critique
│   ├── cross-stock-note-template.md   # Inter-stock intelligence notes
│   ├── probability-output-template.md # Scenario probability distribution
│   └── executive-summary-template.md  # Standalone executive summary
├── tools/
│   ├── financial-data.sh              # Basic SEC EDGAR data retrieval
│   ├── edgar-enhanced.py              # Enhanced EDGAR (full filings, insider, 13F, search)
│   ├── transcript-fetcher.py          # Earnings call transcript retrieval
│   ├── market-data.sh                 # Market data (quotes, history, options)
│   ├── macro-data.py                  # FRED, BLS, industry-specific government data
│   ├── alt-data.py                    # Insider trades, institutional, short interest, estimates
│   ├── screening.py                   # Quantitative screening
│   ├── portfolio-math.py              # Kelly criterion, optimization, Monte Carlo, Beneish, Altman
│   ├── sentiment-analyzer.py          # Transcript NLP, tone scoring, red flag detection
│   ├── report-generator.py            # PDF reports, charts, executive summaries
│   └── batch-runner.py                # Stock universe management, batch execution
├── data/
│   └── stocks.json                    # Stock universe database with tags
├── input/                             # Drop filings here
└── output/                            # Research notes land here
    ├── models/                        # Executable Python models
    ├── charts/                        # Generated visualizations
    └── notes/                         # Cross-stock intelligence notes
```

## Agent Descriptions

### Core Analysts

**Director of Research** — Orchestrator only in Pass 1 (reads inputs, writes context memo, dispatches analysts). In Pass 2, synthesizes all findings, assigns conviction rating (1-5), writes executive summary, makes the final Buy/Hold/Sell call. Does not force false consensus — flags unresolved disagreements as Key Unresolved Risks.

**DCF Analyst** — Builds bottom-up revenue models (units x price, segments x growth), not top-down consensus. Three scenarios minimum (bull/base/bear). WACC derived from components, never assumed. Terminal value calculated via both perpetuity growth and exit multiple. Flags TV > 50% of EV.

**Quant Analyst** — Runs comparables analysis with justified comp selection. Uses median (not mean) multiples. Calculates z-scores and flags outliers > 2 standard deviations. Historical multiple analysis with mean-reversion signals. Derives implied valuation range from comps.

**Competitive Analyst** — Maps competitive landscape using Porter's Five Forces. Scores moat type and durability (1-10) across five dimensions: network effects, switching costs, cost advantages, intangible assets, efficient scale. Identifies #1 competitive threat and models its impact.

**Macro Analyst** — Default stance: contrarian. Maps every macro factor to specific P&L line items with dollar magnitudes. Identifies the >30% downside macro scenario and estimates its probability. Tracks regulatory pipeline. Quantifies FX exposure.

**Editor** — Inactive in Pass 1. Synthesizes (not summarizes) all work products into one coherent research note. Enforces template compliance. Flags internal contradictions. Ensures every claim has a citation or assumption tag. Executive summary must be readable in 60 seconds.

### Extended Analysts

**Risk Analyst** — The team's probabilistic thinker. Runs historical, factor, and multi-factor stress tests. Calculates VaR/CVaR, drawdown profiles, and risk-adjusted return metrics. Analyzes options-implied risk (skew, term structure). Assesses liquidity risk and correlation to portfolio. Provides drawdown risk score (1-10).

**Credit Analyst** — Analyzes full capital structure: every debt instrument, rate, maturity, and covenant. Builds maturity profile and identifies refinancing risk. Calculates coverage ratios and tests covenant headroom under stress. Assesses liquidity adequacy and off-balance-sheet obligations. For distressed situations: Altman Z-score and recovery analysis.

**Catalyst Analyst** — Maps all upcoming catalysts (near/medium/long-term) with probability, magnitude, and priced-in assessment. Analyzes options-implied moves vs. historical. Models impact scenarios for top catalysts. Maintains a negative catalyst watch list. Assesses information edge — what does the market know vs. not know?

**ESG & Governance Analyst** — Focuses on financially material ESG factors only (no box-ticking). Scores board quality (1-10) and shareholder rights (1-10). Analyzes executive compensation alignment, SBC dilution, and anti-takeover provisions. Assesses activist vulnerability. Quantifies material environmental/social risks through specific financial channels.

**Technical Analyst** — Supplements (never replaces) fundamental analysis. Assesses trend across timeframes, identifies key support/resistance levels, analyzes volume confirmation, relative strength, and momentum divergences. Recommends entry/exit timing. Explicitly flags when technicals diverge from the fundamental thesis.

**Research Analyst** — The team's data bloodhound. Runs before all other analysts (Phase 0) to gather every available data point from free public sources: SEC filings (10-K/10-Q/DEF 14A/Form 4/13F), earnings transcripts (Motley Fool, Finnhub), historical prices, insider trading, institutional holdings, short interest, consensus estimates, macro data (FRED, BLS), industry data, analyst commentary, podcast transcripts, and bear case evidence. Produces a Data Intelligence Memo with source quality ratings and data gap flags. Specifically searches for disconfirming evidence to prevent confirmation bias.

**Sector Analyst** — Analyzes sector-level dynamics: TAM sizing and growth modeling, market share landscape (HHI concentration), regulatory environment (current and pending), value chain analysis, and secular trends. Generates executable Python scripts for sector growth models and market share shift simulations. Produces 5-year sector TAM forecasts with growth driver decomposition.

**Position Sizing Analyst** — Translates research into actionable portfolio weights. Calculates Kelly criterion (full/half/quarter), volatility-adjusted sizing, liquidity constraints, and drawdown-aware limits. Final position size is the minimum of all constraints. Provides entry strategy (tranche plan with triggers), exit strategy (trim/stop triggers), and portfolio context (impact on beta, sector weight, concentration).

### Deep Analysis Agents

**Devil's Advocate** — Systematic assumption challenger and contrarian thesis builder. Assumes the bull thesis is wrong and constructs the strongest possible counter-argument. Maps assumption dependency chains (confidence/fragility/verifiability ratings), searches for disconfirming evidence (insider selling, short interest, analyst downgrades, short seller theses), builds the contrarian thesis, writes a pre-mortem narrative, and calculates the break-even bear probability using `tools/portfolio-math.py`. Operates independently in Pass 1 (does not read other analysts' work), then produces targeted challenges in Pass 2.

**Forensic Analyst** — Accounting quality and fraud pattern detection specialist. Calculates Beneish M-Score (8 components) and Altman Z-Score (5 components) using `tools/portfolio-math.py`. Assesses revenue quality (DSO trends, cash conversion, channel stuffing indicators), cash flow quality (CFO/NI divergence, accruals ratio, SBC impact), balance sheet risks (goodwill, off-balance sheet items), and management/governance (auditor changes, related party transactions, board independence). Assigns a 5-point accounting quality rating: Clean / Minor Concerns / Yellow Flags / Red Flags / Avoid. If rating ≤ 2, conviction is capped at 3.

**Sentiment Analyst** — Transcript and communication tone analyst. Runs `tools/sentiment-analyzer.py` on earnings transcripts to produce quantitative scores: management tone (0-100), confidence ratio, hedging density, forward/backward orientation, and net sentiment. Identifies hedging clusters by topic, analyzes Q&A sections separately from prepared remarks, detects non-answers and evasion patterns, compares PR language to actual results, and tracks tone shifts across quarters. Always compares current transcript to prior quarter when available.

### Portfolio-Level Agents

**Model Builder** — Quantitative modeling and code generation specialist. Translates analytical frameworks into executable Python models (DCF, comps, risk, sector, credit, portfolio optimizer). Every numerical claim in the research note is traceable to a model this agent produces. All code follows strict standards: reproducibility, auditability (assumptions as named variables), modularity, and validation (execution test, boundary test, sanity check).

**Portfolio Manager** — Constructs optimized multi-stock portfolios from individual research outputs. Manages correlation (cluster analysis, effective independent bets), factor exposure (market, size, value, momentum, quality, sector), and risk budgets. Runs four optimization methods (mean-variance, risk parity, max Sharpe, max diversification) and selects the best. Generates executable Python optimizer code. Produces implementation plans with entry schedules, rebalancing triggers, and monitoring dashboards.

**Trade Structurer** — Trade construction and hedge design specialist. Runs in Pass 2 only, after the recommendation and thesis are established. Proposes long/short pair trades (with correlation checks via `tools/portfolio-math.py`), sector hedges (short ETF to isolate alpha), options overlays (calls, put spreads, collars with risk/reward profiles), relative value trades (spread + z-score analysis), and thematic baskets. Every proposed structure includes max loss, max gain, and breakeven. Never proposes naked short options or trades without specifying max loss.

## Adding New Agent Roles

1. Create a new file in `agents/` following this structure:

```markdown
# [Agent Name]

## Role
One-line description.

## Expertise
What this agent knows deeply.

## Analytical Framework
Step-by-step methodology.

## Output Format
What the work product looks like.

## Red Lines
What the agent flags or refuses to do.

## Interaction Style
How the agent communicates in Pass 2.
```

2. Update `CLAUDE.md` to include the new agent in the Team Structure table.
3. Update the relevant workflow files to spawn the new agent in Pass 1.
4. If the agent produces a new output type, add a template in `templates/`.

## Customizing for Research Styles

### Value-Oriented
- Edit `agents/dcf-analyst.md`: Increase weight on margin-of-safety analysis, normalize earnings to cycle-average.
- Edit `agents/quant-analyst.md`: Add book value and tangible book value multiples, screen for low P/B.
- Edit `agents/credit-analyst.md`: Emphasize net-net analysis, asset coverage ratios.
- Edit `agents/macro-analyst.md`: Focus on credit cycle and balance sheet risk.

### Growth-Oriented
- Edit `agents/dcf-analyst.md`: Extend forecast period to 7-10 years, add unit economics analysis.
- Edit `agents/quant-analyst.md`: Weight EV/Revenue and PEG more heavily, add Rule of 40 metric.
- Edit `agents/competitive-analyst.md`: Emphasize TAM expansion and platform dynamics.
- Edit `agents/catalyst-analyst.md`: Focus on product launch cadence and market expansion catalysts.
- Edit `agents/sector-analyst.md`: Increase weight on adoption curve modeling and TAM expansion scenarios.

### Event-Driven
- Edit `agents/catalyst-analyst.md`: Increase depth on binary events, add event probability trees.
- Edit `agents/technical-analyst.md`: Add event-day pattern analysis, implied vs. realized move history.
- Edit `agents/risk-analyst.md`: Add binary outcome modeling, options strategy analysis.
- Edit `agents/position-sizing-analyst.md`: Add event-sizing framework (Kelly for binary outcomes).

### Credit/Distressed
- Edit `agents/credit-analyst.md`: Expand recovery analysis, add waterfall model, CDS-implied default probability.
- Edit `agents/dcf-analyst.md`: Add liquidation value scenario.
- Edit `agents/risk-analyst.md`: Add default probability modeling, contagion analysis.
- Edit `agents/macro-analyst.md`: Increase focus on credit spreads and refinancing risk.

### Activist / Special Situations
- Edit `agents/esg-governance-analyst.md`: Expand activist vulnerability section, add sum-of-parts analysis.
- Edit `agents/catalyst-analyst.md`: Track 13D filings, activist campaign timelines.
- Edit `agents/position-sizing-analyst.md`: Add event-driven sizing with catalyst timing.

### Multi-Stock Portfolio
- Edit `agents/portfolio-manager.md`: Adjust concentration limits, factor constraints, optimization method preferences.
- Edit `agents/model-builder.md`: Customize which models are generated (e.g., skip credit model for non-levered companies).
- Edit `workflows/portfolio-construction.md`: Change universe size, rebalancing frequency, risk budget allocation.

## Tool Scripts

### financial-data.sh (Basic EDGAR)
Retrieves SEC EDGAR filings and XBRL financial data.

```bash
./tools/financial-data.sh ticker AAPL          # Resolve ticker to CIK
./tools/financial-data.sh filing AAPL 10-K     # Get most recent 10-K
./tools/financial-data.sh company MSFT         # Get financial facts
./tools/financial-data.sh submissions GOOGL    # List recent filings
```

### edgar-enhanced.py (Full EDGAR Suite)
Enhanced SEC EDGAR with full filing retrieval, insider trades, institutional holdings, and full-text search.

```bash
python3 tools/edgar-enhanced.py filing AAPL 10-K           # Get 10-K URL + metadata
python3 tools/edgar-enhanced.py filing AAPL DEF-14A        # Proxy statement
python3 tools/edgar-enhanced.py insider MSFT --months 12   # Insider trades (Form 4)
python3 tools/edgar-enhanced.py institutional GOOGL        # 13F holders
python3 tools/edgar-enhanced.py financials AMZN            # 25+ XBRL metrics
python3 tools/edgar-enhanced.py search "artificial intelligence" --form 10-K
python3 tools/edgar-enhanced.py company TSLA               # Company overview
```

### transcript-fetcher.py
Earnings call transcript discovery and key quote extraction.

```bash
python3 tools/transcript-fetcher.py search AAPL            # Find latest transcript
python3 tools/transcript-fetcher.py search MSFT --count 4  # Last 4 transcripts
python3 tools/transcript-fetcher.py ir GOOGL               # Find company IR page
python3 tools/transcript-fetcher.py finnhub AMZN           # Finnhub API (needs key)
python3 tools/transcript-fetcher.py extract transcript.txt # Extract key quotes
```

### market-data.sh
Market data retrieval with historical prices and options.

```bash
./tools/market-data.sh quote AAPL              # Current quote
./tools/market-data.sh stats MSFT              # Key statistics
./tools/market-data.sh history GOOGL 1y        # 1-year price history + vol/drawdown
./tools/market-data.sh history AMZN 3y         # 3-year history
./tools/market-data.sh options TSLA            # Options chain + implied vol
./tools/market-data.sh summary META            # All-in-one
```

### macro-data.py
FRED economic data and industry-specific government data sources.

```bash
python3 tools/macro-data.py fred GDP                       # Get GDP from FRED
python3 tools/macro-data.py fred FEDFUNDS,DGS10,DGS2       # Multiple series
python3 tools/macro-data.py rates                          # Interest rate snapshot
python3 tools/macro-data.py macro-snapshot                  # Full macro dashboard
python3 tools/macro-data.py industry energy                # Energy sector data (EIA)
python3 tools/macro-data.py industry pharma                # Pharma data (FDA, ClinicalTrials)
python3 tools/macro-data.py industry tech                  # Tech data (USPTO, FCC)
python3 tools/macro-data.py list-series                    # List all FRED series
```

### alt-data.py
Alternative data: insider trades, institutional holdings, short interest, estimates, peers.

```bash
python3 tools/alt-data.py insider AAPL                     # Insider trading (Form 4 + OpenInsider)
python3 tools/alt-data.py institutional MSFT               # 13F institutional holders
python3 tools/alt-data.py short-interest TSLA              # Short interest + squeeze metrics
python3 tools/alt-data.py ownership-summary GOOGL          # Combined ownership picture
python3 tools/alt-data.py analyst-estimates AMZN            # Consensus estimates
python3 tools/alt-data.py peers NVDA                        # Peer company discovery
```

### screening.py
Quantitative screening and sensitivity analysis.

```bash
python3 tools/screening.py calc-multiples --data comps.json
python3 tools/screening.py z-scores --data comps.json
python3 tools/screening.py rank --data comps.json --method composite
python3 tools/screening.py sensitivity \
    --wacc-range 8,12 --tgr-range 1,4 \
    --base-fcf 5000 --growth 8 --shares 1500 --net-debt 10000 \
    --format table
```

### portfolio-math.py
Portfolio mathematics: Kelly criterion, position sizing, optimization, risk scores.

```bash
python3 tools/portfolio-math.py kelly --win-prob 0.65 --win-return 0.30 --loss-return 0.15
python3 tools/portfolio-math.py kelly-scenarios \
    --bull-price 200 --base-price 160 --bear-price 100 \
    --bull-prob 0.25 --base-prob 0.50 --bear-prob 0.25 \
    --current-price 150
python3 tools/portfolio-math.py vol-size --stock-vol 0.35 --portfolio-vol 0.12 --num-positions 25
python3 tools/portfolio-math.py liquidity --adv 50 --participation 0.10 --max-days 5 --portfolio 1000
python3 tools/portfolio-math.py expected-value --scenarios-file scenarios.json
python3 tools/portfolio-math.py optimize --returns-file returns.json --cov-file cov.json --method max-sharpe
python3 tools/portfolio-math.py risk-parity --cov-file cov.json
python3 tools/portfolio-math.py correlation --tickers AAPL,MSFT,GOOGL --period 3y
python3 tools/portfolio-math.py monte-carlo --portfolio-file portfolio.json --simulations 10000
python3 tools/portfolio-math.py beneish --financials-file financials.json
python3 tools/portfolio-math.py altman-z --financials-file financials.json
```

### sentiment-analyzer.py
NLP-based transcript and communication analysis.

```bash
python3 tools/sentiment-analyzer.py analyze --file transcript.txt        # Full analysis
python3 tools/sentiment-analyzer.py compare --file1 q1.txt --file2 q2.txt # Cross-quarter comparison
python3 tools/sentiment-analyzer.py score --file transcript.txt           # Composite tone score (0-100)
python3 tools/sentiment-analyzer.py red-flags --file transcript.txt       # Evasion/non-answer detection
python3 tools/sentiment-analyzer.py guidance --file transcript.txt        # Extract quantitative guidance
```

### report-generator.py
PDF report and chart generation.

```bash
python3 tools/report-generator.py pdf --input note.md --output report.pdf
python3 tools/report-generator.py charts --scenarios-file scenarios.json --output charts/
python3 tools/report-generator.py executive-summary --input note.md --output exec-summary.pdf
python3 tools/report-generator.py histogram --scenarios-file scenarios.json --output hist.png
python3 tools/report-generator.py distribution --scenarios-file scenarios.json --output dist.png
python3 tools/report-generator.py sensitivity --data-file sensitivity.json --output heatmap.png
python3 tools/report-generator.py waterfall --data-file components.json --output waterfall.png
```

### batch-runner.py
Stock universe management and batch execution planning.

```bash
python3 tools/batch-runner.py list                             # List all stocks
python3 tools/batch-runner.py list --tag mag7                  # Filter by tag
python3 tools/batch-runner.py list --sector Technology          # Filter by sector
python3 tools/batch-runner.py stale                            # Show stocks needing refresh (>7 days)
python3 tools/batch-runner.py stale --days 14                  # Custom staleness threshold
python3 tools/batch-runner.py plan --tag mag7                  # Generate batch run plan
python3 tools/batch-runner.py plan --stale                     # Plan for stale stocks only
python3 tools/batch-runner.py plan --all                       # Plan for entire universe
python3 tools/batch-runner.py add TICKER "Name" --sector X --tags a,b,c
python3 tools/batch-runner.py remove TICKER
python3 tools/batch-runner.py mark-complete TICKER             # Mark as researched today
python3 tools/batch-runner.py tags                             # List all tags with counts
python3 tools/batch-runner.py status                           # Universe dashboard
python3 tools/batch-runner.py update-db                        # Sync with output files
```

## Cross-Stock Intelligence

When an analyst researching Stock A discovers information materially affecting Stock B, they write a cross-stock note to `output/notes/`. Four agents are equipped to write notes: Competitive Analyst, Sector Analyst, Research Analyst, and Devil's Advocate.

After any analysis completes, the Director checks `output/notes/` for notes targeting previously researched stocks. High-priority notes (>5% price target impact or rating change) trigger a lightweight Cross-Stock Review — 3 analysts (DCF, Competitive, Devil's Advocate) reassess the target stock with the new information.

See `workflows/cross-stock-trigger.md` for the full protocol.

## Requirements

- Claude Code with agent teams enabled
- `python3` with packages: `numpy`, `scipy` (portfolio math), `matplotlib` (charts), `reportlab` (PDF generation)
- `curl` and `jq` (for data retrieval)
- Internet access (for SEC EDGAR, market data, web search)

## Conventions

- Dollar amounts in millions ($M) unless > $100B
- Growth rates as percentages with one decimal (12.3%)
- Dates in YYYY-MM-DD format
- Assumptions flagged: `[ASSUMPTION: ...]`
- Missing data flagged: `[DATA GAP: ...]` or `[ESTIMATED]`
- Specific filing citations: `"10-K p.47, Note 12"`
