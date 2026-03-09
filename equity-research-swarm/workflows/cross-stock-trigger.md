# Cross-Stock Intelligence Trigger Workflow

## Purpose
When analysts researching Stock A discover information that materially affects Stock B, they file a cross-stock note. This workflow defines how those notes are processed, especially when Stock B has already been researched.

## Who Writes Cross-Stock Notes?

The following agents are instructed to write notes when they discover cross-stock intelligence:
- **Competitive Analyst** — market share shifts, new competitive threats, pricing changes
- **Sector Analyst** — TAM changes, industry dynamics affecting multiple companies
- **Research Analyst** — data discoveries from external sources affecting peers
- **Devil's Advocate** — disconfirming evidence that reveals competitor advantages/weaknesses

## Note Format

All notes use `templates/cross-stock-note-template.md` and are saved to:
```
output/notes/[SOURCE_TICKER]-to-[TARGET_TICKER]-[DATE].md
```

Example: `output/notes/AMD-to-INTC-2025-06-15.md`

## When Notes Are Checked

### During Active Research (Standard Flow)

In the standard `workflows/full-research-note.md` flow:

1. **Phase 0 (Data Gathering):** Director checks `output/notes/` for any existing notes targeting the current stock
2. **Phase 1 (Parallel Analysis):** Director includes relevant cross-stock notes in the context memo passed to all analysts
3. **Phase 1 (During Analysis):** Analysts write NEW notes to `output/notes/` when they discover cross-stock intelligence
4. **Phase 2 (Synthesis):** Director reviews any notes written during Phase 1 and factors them into final synthesis

### After Research Completes (Trigger Flow)

When a note is filed AFTER the target stock has already been researched:

#### Step 1: Director Detects New Note

After each stock analysis completes, the Director monitors `output/notes/` for new notes targeting already-researched stocks. The Director should check:

```bash
# List all notes targeting a specific ticker
ls output/notes/*-to-[TARGET_TICKER]-*.md
```

#### Step 2: Materiality Assessment

The Director reads the new note and assesses materiality:

| Materiality Level | Criteria | Action |
|-------------------|----------|--------|
| **High** | Note suggests price target should move >5%, or rating could change | Trigger Cross-Stock Review |
| **Medium** | Note affects a key assumption but price impact <5% | Add footnote to existing note |
| **Low** | Note is informational but doesn't change thesis | Log and file, no action needed |

#### Step 3: Cross-Stock Review (High Materiality Only)

If the note is high-materiality, the Director spawns a **lightweight review** — not a full re-analysis:

**Spawn these analysts only (in parallel):**

1. **DCF Analyst** — re-run the DCF with the new information. Does the price target change?
2. **Competitive Analyst** — reassess competitive position given the new intelligence
3. **Devil's Advocate** — does this new information strengthen or weaken the bear case?

**Context for review agents:**
```
CROSS-STOCK REVIEW CONTEXT:
- Original research note: output/[TICKER]-research-note-[DATE].md
- Original rating: [Buy/Hold/Sell]
- Original price target: $[X]
- New cross-stock note: output/notes/[SOURCE]-to-[TARGET]-[DATE].md
- Question: Does this new information materially change the thesis?

YOU ARE NOT DOING A FULL ANALYSIS. Only assess the impact of the new information on:
1. Your specific area of expertise
2. The original price target
3. The original rating
```

**Do NOT re-run:** Editor, Position Sizing, Portfolio Manager, Technical Analyst, Macro Analyst, Credit Analyst, ESG Analyst, Trade Structurer, Forensic Analyst, Sentiment Analyst (unless the note specifically concerns their domain)

#### Step 4: Director Decision

After the lightweight review:

| Outcome | Action |
|---------|--------|
| Price target moves >5% AND/OR rating changes | Produce **Research Addendum** (see below) |
| Price target moves 2-5%, rating unchanged | Add **Material Update** footnote to original note |
| Price target moves <2%, no rating change | Add **Acknowledged** footnote to original note |

#### Step 5: Research Addendum (if needed)

**Save to:** `output/[TICKER]-addendum-[DATE].md`

```markdown
# [TICKER] — Research Addendum

**Original Note Date:** [Date]
**Addendum Date:** [Date]
**Triggered By:** Cross-stock note from [SOURCE TICKER] analysis

## Rating Change
- **Previous:** [Buy/Hold/Sell] | **Updated:** [Buy/Hold/Sell]
- **Previous Price Target:** $[X] | **Updated Price Target:** $[X]
- **Change Driver:** [2-3 sentences]

## New Information
[Summary of the cross-stock intelligence that triggered this review]

## Impact Assessment
[Which assumptions changed and by how much]

## Updated Probability Distribution
[Updated bull/base/bear with new probabilities]

## Conviction Adjustment
- **Previous Conviction:** [1-5] | **Updated:** [1-5]
- **Rationale:** [1 sentence]
```

## Monitoring Dashboard

Track cross-stock activity across the research universe:

```
output/notes/
├── AMD-to-INTC-2025-06-15.md        [Status: Reviewed, Low materiality]
├── AMD-to-NVDA-2025-06-15.md        [Status: Triggered review, Addendum issued]
├── AAPL-to-QCOM-2025-06-16.md       [Status: Pending review]
└── MSFT-to-GOOGL-2025-06-17.md      [Status: Acknowledged, no change]
```

## Rules

1. **Speed:** Cross-stock reviews should complete in 1/3 the time of a full analysis — they are focused, not exhaustive
2. **Bias check:** The Director should not anchor to the original thesis. Read the note fresh.
3. **Cascading notes:** If the cross-stock review reveals FURTHER cross-stock intelligence (Stock A → Stock B → Stock C), file additional notes but limit cascade depth to 2 levels to prevent infinite loops
4. **Staleness:** Cross-stock notes older than 30 days should be reviewed for continued relevance before acting on them
5. **Conflict resolution:** If a cross-stock note conflicts with the original analysis, this is a feature, not a bug — the Director should present both perspectives in the addendum
