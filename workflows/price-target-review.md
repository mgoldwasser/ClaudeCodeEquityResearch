# Workflow: Price Target Review

## Trigger
Updating an existing research note due to new information (earnings release, guidance change, M&A announcement, macro shift, or periodic review).

## Input Requirements
- **Ticker symbol** (required)
- **Prior research note** in `input/` (required — the note being updated)
- **New data** in `input/` (at least one of the following):
  - New earnings release / 10-Q
  - Updated guidance from management
  - Material news (M&A, restructuring, management change)
  - Macro data that changes the thesis
  - Competitive development (new entrant, pricing change, market share shift)

## Execution Steps

### Phase 0: Triage (Director)
1. Read the prior research note and the new data in `input/`.
2. Classify the change:
   - **Financial update:** New earnings beat/miss, revised guidance → spawn DCF Analyst + Quant Analyst
   - **Competitive shift:** New entrant, market share change, pricing action → spawn Competitive Analyst + DCF Analyst
   - **Macro shift:** Rate change, regulatory action, FX move → spawn Macro Analyst + DCF Analyst
   - **Multi-factor:** Multiple material changes → spawn all relevant analysts
3. Write a change memo: What changed, what hasn't, what specific questions the analysts should answer.

**Key principle: Only spawn agents relevant to what changed.** Do not re-run the full workflow for a routine quarterly update.

### Phase 1: Targeted Analysis (Director spawns relevant analysts)
Spawn only the analysts needed based on triage:

Each analyst receives:
- The prior research note
- The new data
- The change memo
- Instruction: "Update ONLY the sections relevant to the new data. Flag what changed and by how much. Preserve prior analysis that remains valid."

### Phase 2: Abbreviated Review (Director)
For price target reviews, **skip the full adversarial review** unless the change is fundamental:

- **Routine update** (beat/miss within 10% of estimates): Director reviews analyst updates directly, no cross-critique needed.
- **Material change** (>10% estimate revision, rating change consideration): Run abbreviated cross-critique — each spawned analyst reviews the others' updates (one round, no rebuttals).
- **Fundamental change** (thesis-altering event): Escalate to full research note workflow (`workflows/full-research-note.md`).

### Phase 3: Update Synthesis (Director)
1. Revise the price target:
   - Show old target vs. new target
   - Show what drove the change (revised estimates, revised multiple, revised probability weights)
   - Show the math explicitly
2. Update conviction rating if warranted.
3. Update the executive summary.
4. Add a "Change Summary" section at the top of the note.

### Phase 4: Output
Save updated note to: `output/[TICKER]-price-target-review-[YYYY-MM-DD].md`

## Output Format
The updated note should include a **Change Summary** header before the Executive Summary:

```markdown
## Change Summary
**Date:** [YYYY-MM-DD]
**Prior Target:** $[X] | **New Target:** $[Y] | **Change:** [±Z%]
**Prior Rating:** [Buy/Hold/Sell] | **New Rating:** [Buy/Hold/Sell]
**Prior Conviction:** [1-5] | **New Conviction:** [1-5]

**What Changed:**
- [Bullet 1: specific change and impact]
- [Bullet 2: specific change and impact]

**What Didn't Change:**
- [Key assumptions that remain intact]

**Key Risk Update:**
- [Any new risks or changes to existing risk assessment]
```

Then the full updated research note follows.

## Estimated Agent Calls
- Routine update: 2-3 agents (targeted analysts only)
- Material change: 3-4 agents + abbreviated review
- Fundamental change: Escalate to full workflow (13 agents)
