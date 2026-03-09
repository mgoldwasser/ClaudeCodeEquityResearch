# Workflow: Earnings Reaction

## Trigger
Rapid post-earnings analysis. Time-constrained — prioritize speed over depth.

## Input Requirements
- **Ticker symbol** (required)
- **Earnings release / press release** in `input/` (required)
- **Earnings call transcript** in `input/` (strongly preferred)
- **Prior research note** in `input/` (preferred — for comparison to expectations)
- **Prior estimates** (if available — consensus or internal)

## Execution Steps

### Phase 0: Rapid Assessment (Director)
1. Read the earnings release and transcript.
2. Identify the 3-5 most important data points (revenue beat/miss, EPS beat/miss, guidance change, margin surprise, one-time items).
3. Write a rapid context memo: "Here's what happened and here's what matters."

### Phase 1: Parallel Sprint (Director spawns 4 analysts)
Spawn all four analysts **in parallel** with time-constrained instructions:

**DCF Analyst:**
```
Rapid update only. Read the earnings release and prior research note. Update revenue and margin estimates for the current and next fiscal year based on reported results and new guidance. Recalculate implied fair value using the existing DCF framework — do not rebuild from scratch. Focus on: (1) estimate revisions, (2) whether guidance changed, (3) impact on fair value. Keep output to 1 page.
```

**Quant Analyst:**
```
Rapid update only. Assess whether the earnings result changes the company's relative position vs. comps. Has the valuation gap widened or narrowed? Any comp companies that reported recently with contrasting results? Focus on: (1) post-earnings multiple vs. comp group, (2) estimate revision direction. Keep output to 1 page.
```

**Competitive Analyst:**
```
Rapid update only. From the earnings call, identify any competitive commentary — market share claims, competitive wins/losses, pricing actions, new product launches, competitive threats mentioned. Focus on: (1) any change to competitive position, (2) management tone on competition. Keep output to half a page.
```

**Macro Analyst:**
```
Rapid update only. From the earnings call, identify any macro commentary — demand environment, input costs, FX impact, regulatory mentions, guidance assumptions about the macro environment. Focus on: (1) management's macro read, (2) whether it contradicts or confirms your prior macro view. Keep output to half a page.
```

**Catalyst Analyst:**
```
Rapid update only. From the earnings results: (1) which anticipated catalysts were confirmed or disconfirmed? (2) any new catalysts surfaced from the call? (3) updated catalyst timeline. Keep output to half a page.
```

**Technical Analyst:**
```
Rapid update only. Assess the post-earnings price action: (1) gap direction and magnitude, (2) volume vs. average, (3) key support/resistance levels now in play, (4) whether the move is technically significant (breakout, breakdown, or noise). Keep output to half a page.
```

**Credit Analyst (spawn only if material balance sheet changes disclosed):**
```
Rapid update only. If the earnings release disclosed material changes to debt, liquidity, or capital allocation: (1) updated leverage ratios, (2) covenant impact, (3) any new debt issuance or repayment. Keep output to half a page. If no material balance sheet changes, skip.
```

### Phase 2: Skip Adversarial Review
**For earnings reactions, SKIP Pass 2 entirely.** No cross-critique, no rebuttals. Speed matters more than adversarial rigor for a rapid reaction note.

### Phase 3: Direct Synthesis (Director)
The Director synthesizes directly from Pass 1 outputs:

1. **Beat/Miss Assessment:**
   - Revenue: actual vs. estimate, delta in $ and %
   - EPS: actual vs. estimate, delta in $ and %
   - Key segment performance vs. expectations
   - Quality of beat/miss (sustainable vs. one-time)

2. **Guidance Delta:**
   - Prior guidance vs. new guidance (if changed)
   - Implied growth rate change
   - Management tone (confident, cautious, defensive)

3. **Thesis Check:**
   - Is the investment thesis intact?
   - What changed about the thesis (if anything)?
   - Does this earnings report change the conviction level?

4. **Price Target Update:**
   - Quick recalculation based on estimate revisions
   - State whether the target changes and by how much
   - If insufficient data for a formal update: "Maintaining target pending full model update"

5. **Action Item:**
   - What should the PM do NOW? (Add, hold, trim, do nothing)
   - Is a full model update warranted? (triggers `workflows/price-target-review.md`)

### Phase 4: Output
Save to: `output/[TICKER]-earnings-reaction-[YYYY-MM-DD].md`

## Output Format (1-Page Earnings Reaction)

```markdown
# [TICKER] — Q[X] FY[YYYY] Earnings Reaction
**Date:** [YYYY-MM-DD] | **Rating:** [Buy/Hold/Sell] | **Target:** $[X] | **Close:** $[Y]

## Beat/Miss Summary
| Metric | Estimate | Actual | Delta | Quality |
|--------|----------|--------|-------|---------|
| Revenue | $[X]M | $[Y]M | [±Z%] | [Sustainable/One-time] |
| EPS | $[X] | $[Y] | [±Z%] | [Sustainable/One-time] |
| [Key Segment] | $[X]M | $[Y]M | [±Z%] | |

## Guidance Update
- Prior FY guidance: revenue $[X]M, EPS $[X]
- New FY guidance: revenue $[Y]M, EPS $[Y]
- Delta: [±Z%] revenue, [±Z%] EPS
- Management tone: [Confident / Cautious / Defensive]

## Key Takeaways
1. [Most important insight from the quarter]
2. [Second most important]
3. [Third most important]

## Thesis Status: [INTACT / STRENGTHENED / WEAKENED / BROKEN]
[2-3 sentences on why]

## Action
- **Near-term:** [Add / Hold / Trim / Exit]
- **Target update:** [Maintaining $X / Revising to $Y / Pending full review]
- **Full model update needed:** [Yes / No]

## Risks Surfaced This Quarter
- [Any new risks from the earnings call]
```

## Estimated Agent Calls
- Pass 1: 6-7 parallel agents (time-constrained; Credit Analyst optional)
- Pass 2: SKIPPED
- Synthesis: Director only
- Total: 6-7 agent invocations, 1 sequential phase + Director synthesis
