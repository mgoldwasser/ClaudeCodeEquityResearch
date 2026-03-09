# Architecture Review: Equity Research Swarm

**Date:** 2026-03-09
**Reviewer:** Meta-analysis of workflow, agents, tools, templates, and data architecture
**Scope:** Structural gaps, scalability, information sharing, temporal intelligence, duplication

---

## Executive Summary

The workflow is impressively designed for **single-stock, one-shot analysis**. The two-pass adversarial review, probability-weighted scenarios, conviction caps, and quality gates are genuinely well-engineered.

But the system has fundamental structural problems the moment you try to operate it as a **continuous, multi-stock research operation** — which is clearly the intent given the batch runner, portfolio manager, and cross-stock intelligence mechanisms.

**Seven critical issues identified:**

1. Flat file structure that overwrites intermediate work between stocks
2. No temporal intelligence layer (no awareness of "what happened today")
3. Massive duplication of macro/sector work across stocks
4. Over-engineered review process (30 agent invocations where 6 would suffice)
5. No shared state management or research memory
6. No tiered analysis depth (every stock gets the same 48-invocation treatment)
7. No cost/token budget awareness

---

## Issue 1: File Architecture Collapses at Scale

### Current State

The output directory is a **flat, single-stock workspace** with no ticker-level namespacing for intermediate work products:

```
output/
├── pass1/dcf-analysis.md          # Generic name — gets OVERWRITTEN on next stock
├── pass1/risk-analysis.md         # Same problem
├── pass2/critiques/               # Same problem
├── data/MSFT-prices-3y.json       # Ticker-specific (good)
├── models/msft-dcf-model.py       # Ticker-specific (good)
├── notes/MSFT-to-GOOGL-...md      # Ticker-specific (good)
└── MSFT-research-note-2026-03-08.md  # Final output is dated (good)
```

The final deliverables (`MSFT-research-note-2026-03-08.md`) and data files (`MSFT-*.json`) are properly namespaced. But all Pass 1 analysis, Pass 2 critiques/rebuttals, and summaries use **generic filenames** that get destroyed when the next stock runs.

### Impact

- Cannot keep historical intermediate work for audit trail
- Cannot compare how different analysts assessed the same factor across stocks
- Cannot resume a partially-completed analysis
- Cannot selectively re-run one analyst without losing all others' work

### What Happens at "All US Equities" Scale

500 stocks × daily runs × 43+ files per run = chaos. Even with dated final outputs, the intermediate work disappears.

### Recommended Structure

```
research/
├── {TICKER}/
│   ├── {YYYY-MM-DD}/                    # Each run is isolated
│   │   ├── data/                        # Retrieved data for this run
│   │   ├── pass1/                       # Analyst outputs
│   │   ├── pass2/                       # Critiques, rebuttals, synthesis
│   │   ├── summaries/                   # Compressed briefs
│   │   ├── models/                      # Python models
│   │   └── {TICKER}-research-note.md    # Final output
│   └── latest -> {YYYY-MM-DD}/          # Symlink to most recent
│
├── shared/                              # Cross-stock shared state (see Issue 3)
│   ├── macro/
│   ├── sectors/
│   ├── notes/                           # Cross-stock intelligence
│   └── market-context/
│
└── portfolios/
    └── {YYYY-MM-DD}/
```

**Key principle:** Every run is immutable and self-contained. Prior runs are preserved. A symlink or index provides "latest" access.

---

## Issue 2: No Temporal Intelligence Layer

### Current State

The system has **zero temporal awareness**. There is no mechanism for:

- A daily macro briefing generated once and shared across all stocks
- A news event log tracking what happened and when
- Temporal decay (knowing a 10-K from 3 months ago is still valid but yesterday's earnings need immediate integration)
- Event-driven triggers ("the Fed raised rates 2 hours ago — every rate-sensitive stock needs its macro overlay refreshed")
- Time-horizon context ("what changed in the last hour / day / week / month")

The Research Analyst gathers data from scratch each time. Each stock's Macro Analyst independently re-discovers the same macro environment. There's no concept of "the current state of the world."

### What's Needed: A Context Layer

```
context/
├── realtime/                            # Updated continuously during session
│   ├── market-pulse.md                  # Current indices, VIX, sector rotation, breadth
│   └── breaking-events.md              # Material events in last few hours
│
├── daily/
│   └── {YYYY-MM-DD}/
│       ├── morning-briefing.md          # Generated once per day, shared by ALL stocks
│       ├── macro-snapshot.md            # Rates, yields, FX, commodities, credit spreads
│       ├── market-summary.md            # Index performance, breadth, leadership
│       ├── news-digest.md              # Material events tagged by ticker/sector
│       ├── earnings-calendar.md         # What reported today, what reports this week
│       ├── economic-releases.md         # Data releases (CPI, jobs, GDP, etc.)
│       └── policy-update.md             # Fed, regulation, trade policy, geopolitics
│
├── weekly/
│   └── {YYYY}-W{NN}/
│       ├── sector-rotation.md           # Weekly sector performance and flows
│       ├── macro-trends.md              # Week-over-week changes
│       ├── earnings-season-tracker.md   # Aggregate beat/miss rates, guidance trends
│       └── cross-stock-digest.md        # Aggregated cross-stock notes
│
├── monthly/
│   └── {YYYY-MM}/
│       ├── economic-regime.md           # Cycle positioning (expansion/contraction)
│       ├── policy-landscape.md          # Tariffs, regulation, fiscal, monetary
│       └── sector-fundamentals.md       # Sector-level earnings growth, margins
│
└── persistent/
    ├── economic-regime.md               # Current regime classification (updated monthly)
    ├── rate-environment.md              # Current rate regime and forward curve
    └── geopolitical-risks.md            # Standing geopolitical risk factors
```

### Required: A "Morning Briefing" Agent

A new **Market Intelligence Agent** should run once at the start of each session/day:

- Overnight market moves and drivers
- Economic data releases from last 24 hours
- Earnings reports from last 24 hours
- Policy/regulatory developments
- Geopolitical events with market relevance
- Fed/central bank communications

This produces the daily context files that feed into **every** stock analysis that day, eliminating per-stock duplication.

---

## Issue 3: Massive Duplication Across Stocks

### The Problem

When analyzing MSFT, GOOGL, AMZN, and META in sequence:

| Duplicated Work | Per-Stock Cost | What Should Happen |
|----------------|---------------|-------------------|
| Macro Analyst assesses the macro environment | Full macro analysis × 4 | Run once, share across all 4 |
| Sector Analyst analyzes cloud/AI sector | Full sector analysis × 4 | Run once for the sector |
| Research Analyst fetches FRED data | Same FRED series × 4 | Cache with TTL |
| Technical Analyst assesses market conditions | Market-level analysis × 4 | Separate market vs. stock-specific analysis |
| Competitive Analyst maps the landscape | Overlapping landscape work × 4 | Build one landscape, stock-specific positioning within it |

### Recommended: Pre-Computed Shared Inputs

**Macro Analysis** should be a **daily shared briefing**, not a per-stock exercise:

```
shared/macro/2026-03-09/
├── macro-environment.md             # The macro picture (rates, GDP, inflation, employment)
├── rate-sensitivity-framework.md    # How rate changes flow to different business models
├── sector-cycle-positioning.md      # Where each sector sits in the cycle
└── policy-risk-register.md          # Active policy risks (tariffs, regulation, etc.)
```

Per-stock Macro Analyst work should be reduced to: "Given the shared macro environment, what are the stock-specific macro exposures and P&L impacts?"

**Sector Analysis** should run once per sector:

```
shared/sectors/
├── cloud-infrastructure/
│   └── 2026-03-09/
│       ├── sector-structure.md      # TAM, growth, competitive dynamics
│       ├── market-share-model.py    # Shared across all cloud stocks
│       └── regulatory-landscape.md
├── semiconductors/
│   └── ...
└── enterprise-software/
    └── ...
```

Per-stock Sector Analyst work should be: "Given the shared sector analysis, where does this specific company sit?"

**Estimated duplication reduction:** 30-40% of total agent work for multi-stock batches.

---

## Issue 4: Over-Engineered Review Process

### Current State: 30 Agent Invocations for Cross-Review

Pass 2 currently runs:
- **15 critique tasks** (each analyst critiques all 14 others)
- **15 rebuttal tasks** (each analyst responds to critiques received)
- **1 Summarizer** to compress critiques into a Disagreement Map
- **Total: 31 additional invocations** beyond the 15 Pass 1 analysts

This produces a **15×14 = 210 individual critiques**. Most are low-value. The Sentiment Analyst's critique of the Technical Analyst's work rarely produces actionable insight. The Credit Analyst and the ESG Analyst have almost no meaningful overlap to critique.

### What Actually Matters

The high-value disagreements are **structural**, not blanket:

| Cross-Check | Why It Matters | Current Approach |
|-------------|---------------|-----------------|
| DCF vs. Quant | Do intrinsic and relative valuations converge? | Both critique each other among 13 other critiques |
| DCF vs. Competitive | Does revenue build match competitive reality? | Lost in the noise of 210 critiques |
| Bull case vs. Devil's Advocate | Strongest challenge to the core thesis | Devil's Advocate critiques everyone, not just the thesis |
| Credit vs. Risk | Do stress tests and balance sheet analysis align? | Separate critiques, not directly compared |
| Forensic + Sentiment | Quality gate (binary pass/fail) | Given same weight as valuation debates |
| Macro vs. DCF | Does macro overlay invalidate key assumptions? | One of 14 critiques each writes |

### Recommended: Targeted Cross-Review (6-8 directed pairs)

Replace the 15×15 blanket review with **6-8 targeted cross-checks**:

1. **Valuation Convergence:** DCF Analyst ↔ Quant Analyst (do the numbers agree?)
2. **Revenue Reality Check:** DCF Analyst ← Competitive Analyst (is the revenue build credible?)
3. **Thesis Challenge:** Investment thesis ← Devil's Advocate (strongest counter-argument)
4. **Downside Alignment:** Risk Analyst ↔ Credit Analyst (do stress tests and balance sheet agree?)
5. **Quality Gate:** Forensic Analyst + Sentiment Analyst → Director (pass/fail, not full critique)
6. **Macro Validity:** Macro Analyst → DCF Analyst (do macro assumptions invalidate the DCF?)
7. **Catalyst vs. Technical:** Catalyst Analyst ↔ Technical Analyst (do catalysts align with price action?)
8. **Sector vs. Competitive:** Sector Analyst ↔ Competitive Analyst (do sector and company-level analyses agree?)

**Result:** 8-16 targeted critiques + 8-16 rebuttals = **16-32 invocations** (vs. 210 critiques + 210 rebuttals in the current blanket approach). Higher signal-to-noise ratio. The Editor gets 8 focused disagreements instead of trying to synthesize 210 mostly-redundant observations.

---

## Issue 5: No Shared State Management or Research Memory

### Current State

State sharing is entirely file-based and manual:
- Director writes a 3-5 sentence context memo
- `data/stocks.json` tracks only `last_researched` date
- Cross-stock notes sit in `output/notes/` and require manual scanning
- Prior research must be manually copied to `input/` for update workflows

### What's Missing

**A. Research Memory**

When you re-analyze MSFT a week later, the system starts from scratch. It doesn't know:
- Prior conviction rating and why
- Which assumptions proved right/wrong since last analysis
- What the prior price target was and what drove changes
- What critiques were raised last time
- How the stock performed vs. the thesis since last coverage

**Needed:** A `research-state.json` per ticker:

```json
{
  "ticker": "MSFT",
  "coverage_history": [
    {
      "date": "2026-03-09",
      "type": "full-research-note",
      "rating": "Hold",
      "price_target": 450,
      "conviction": 3,
      "current_price_at_time": 409,
      "key_assumptions": [
        "Azure growth 28% FY2026",
        "Operating margin expansion to 47%"
      ],
      "key_risks": ["AI capex sustainability", "PC market softness"],
      "unresolved_disputes": ["Terminal growth rate: DCF says 3%, Macro says 2%"],
      "forensic_score": 4,
      "output_path": "research/MSFT/2026-03-09/"
    }
  ],
  "cross_stock_notes_received": [...],
  "cross_stock_notes_written": [...],
  "assumption_changes": [...]  // Track how assumptions evolve
}
```

**B. Assumption Registry**

Shared assumptions that apply across stocks:
- Risk-free rate (set once per day, used by every DCF)
- Equity risk premium (set once, debatable but should be consistent)
- GDP growth assumption
- Sector growth rates

Currently, each stock's DCF Analyst independently estimates WACC components. They should use shared market parameters and only derive stock-specific inputs (beta, capital structure, size premium).

**C. Finding Deduplication**

The Competitive Analyst for MSFT discovers Azure is gaining share from AWS. This should be **immediately** available as structured input to AMZN analysis — not just a markdown note that gets scanned later. The cross-stock notes mechanism is directional and reactive. It needs to be:
- Structured (parseable, not just prose)
- Indexed (queryable by target ticker, sector, topic)
- Prioritized (materiality assessment at write time, not just read time)

---

## Issue 6: No Tiered Analysis Depth

### Current State

Every stock gets the same treatment:
- Phase 0: Research Analyst data gathering
- Pass 1: 14 parallel analysts (including Forensic, Sentiment, ESG/Governance, Technical)
- Pass 1.5: Summarizer
- Pass 2: 15 cross-critiques + 15 rebuttals + Disagreement Map + Editor synthesis
- Post-Pass 2: Trade Structurer + Position Sizing + Director review + Report generation

That's ~48 agent invocations regardless of whether the stock is a high-conviction thesis-driven idea or a routine maintenance update.

### Recommended Tiers

| Tier | When | Agents | Estimated Invocations |
|------|------|--------|----------------------|
| **Tier 1: Full Initiation** | New coverage, fundamental thesis change | All 21 agents, full two-pass | ~48 |
| **Tier 2: Standard Update** | Quarterly refresh, earnings reaction | Core 5 + Risk + Credit + Catalyst, abbreviated review | ~18-22 |
| **Tier 3: Maintenance** | Weekly monitoring, no material change | DCF + Quant + Risk, no cross-review | ~8-10 |
| **Tier 4: Pulse Check** | Daily monitoring | Market data + Technical + quick thesis validation | ~3-4 |

The batch runner should assign tiers based on:
- Coverage priority (portfolio weight, watchlist status)
- Time since last full analysis
- Whether material events have occurred
- Available budget

---

## Issue 7: Missing Cost/Token Budget Awareness

### Current State

No awareness of API costs. A full research note with 48 agent invocations, each using Opus or Sonnet with 10-50K token contexts, could cost $20-100+ per stock depending on model selection and output length.

### What's Needed

- **Budget ceiling per stock** that adapts the workflow tier
- **Cost tracking** — actual tokens consumed per agent, per phase, per stock
- **Model selection optimization** — not every agent needs Opus. The current agent definitions specify models (Opus for Director/DCF/Devil's Advocate, Sonnet for most others, Haiku for Summarizer/Sentiment), but there's no dynamic adjustment based on budget.
- **Early termination** — if Phase 0 reveals severe data gaps (no 10-K available, no transcripts), don't run a full 14-analyst swarm on limited data. Scale down.

---

## Issue 8: Smaller But Material Gaps

### 8a. No Data Cache

Every run re-fetches everything. No caching of:
- FRED macro data (same for all stocks analyzed that day)
- SEC EDGAR company metadata
- Market data (same market conditions for all stocks)
- Sector data

**Fix:** TTL-based cache. Macro data = 24hr TTL. Market data = 1hr TTL. SEC filings = 7 day TTL (unless new filing detected).

### 8b. No Incremental Update Logic

Binary choice: full research note or nothing (with limited lighter workflows). Cannot:
- Re-run just the Macro Analyst and update only that section
- Refresh the Technical Analyst view without touching fundamentals
- Update position sizing after a price move without re-running the full analysis

**Fix:** Each section of the final note should be independently refreshable. This requires the ticker-namespaced directory structure (Issue 1) so that you can read existing analyst outputs and selectively replace one.

### 8c. No Automated Cross-Stock Intelligence Integration

Cross-stock notes must be manually detected by the Director scanning `output/notes/`. There's no:
- Automatic notification when a note targets a stock currently under coverage
- Priority queue for high-materiality cross-stock notes
- Automatic triggering of follow-up reviews

**Fix:** The batch runner should check for new cross-stock notes after each stock completes and automatically queue cross-stock reviews for high-materiality notes.

### 8d. Forensic Quality Not Revisited in Updates

The full research note assigns a forensic quality score (1-5) and calculates Beneish M-Score. The Price Target Review and Earnings Reaction workflows don't re-run forensic analysis. But new quarterly filings could reveal accounting deterioration.

**Fix:** Forensic should be a lightweight check in every update workflow, not just initiations.

### 8e. No Analyst Track Record

No mechanism to track which analysts' predictions were most accurate over time. If the Devil's Advocate is consistently right and the DCF Analyst consistently too optimistic, the Director should weight their inputs differently.

**Fix:** Post-hoc validation workflow that compares prior predictions to actual outcomes and maintains analyst accuracy scores.

---

## Complexity Reduction Opportunities

### Things That Are More Complicated Than They Need to Be

1. **21 separate agent files** when several agents have near-identical structures. The Risk Analyst, Credit Analyst, and Macro Analyst could share a common framework with role-specific overlays. Currently each is a ~2000-word standalone document with significant boilerplate overlap.

2. **7 template files** with overlapping structure. The research-note-template, executive-summary-template, and probability-output-template have duplicated formatting conventions. These could be modular sections composed into templates rather than standalone documents.

3. **The CLAUDE.md file is ~30K tokens** and contains the entire workflow specification. The Director of Research agent is supposed to orchestrate everything, but all the orchestration logic lives in CLAUDE.md, not in the Director's agent file. This creates ambiguity about what the Director "knows" vs. what CLAUDE.md instructs.

4. **Two bash scripts (`financial-data.sh` and `market-data.sh`) alongside Python equivalents** (`edgar-enhanced.py`). The bash scripts are a legacy artifact — `edgar-enhanced.py` supersedes `financial-data.sh` with better parsing, more endpoints, and structured output. The bash market-data script should similarly be consolidated into Python for consistency and better error handling.

5. **The cross-stock note template** defines a full structured format, but the actual notes in `output/notes/` are free-form markdown. The template isn't being enforced, which means notes vary in quality and parseability.

---

## Priority Matrix

| Priority | Issue | Impact | Effort | Risk of Not Fixing |
|----------|-------|--------|--------|-------------------|
| **P0** | #1 Directory restructure | Blocks all multi-stock operations | Medium | System breaks at >1 stock |
| **P0** | #2 Temporal intelligence layer | Eliminates blind spot on current events | High | Analyses miss material events |
| **P0** | #3 Shared macro/sector pre-computation | Eliminates 30-40% duplication | Medium | Massive cost waste at scale |
| **P1** | #5 Research memory / state DB | Enables continuous coverage | Medium | Every run starts from zero |
| **P1** | #6 Tiered analysis depth | Cost control, throughput | Low | Every stock costs the same |
| **P2** | #4 Targeted cross-review | Reduces noise, saves 50%+ on Pass 2 | Low | Works but wasteful |
| **P2** | #7 Cost/token budgeting | Operational sustainability | Medium | Unbounded API costs |
| **P3** | #8a-e Smaller gaps | Quality improvements | Varies | Manageable individually |

---

## Conclusion

The intellectual design of this system — adversarial review, probability weighting, conviction caps, quality gates — is excellent. These are the right concepts for institutional-quality equity research.

The infrastructure needs to evolve from a "single-stock workbench" to a "continuous research operation." The three highest-leverage changes are:

1. **Ticker-namespaced, date-versioned directory structure** — makes multi-stock and historical analysis possible
2. **Shared context layer with temporal intelligence** — eliminates duplication and adds awareness of "the current state of the world"
3. **Pre-computed shared inputs (macro + sector)** — run once, share across all stocks in a session

These three changes alone would make the system viable for continuous multi-stock operations and eliminate roughly 40% of redundant work.
