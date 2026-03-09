# Probability Distribution Output Template

All analysts producing scenario analysis MUST use this format for structured probability output.

---

## Probability Distribution — [TICKER]

### Scenario Table

| Scenario | Description | Implied Price | Probability | Expected Contribution |
|----------|-------------|--------------|-------------|----------------------|
| Bull | [1 sentence — what goes right] | $[X] | [X]% | $[X] × [X]% = $[X.XX] |
| Base | [1 sentence — continuation scenario] | $[X] | [X]% | $[X] × [X]% = $[X.XX] |
| Bear | [1 sentence — what goes wrong] | $[X] | [X]% | $[X] × [X]% = $[X.XX] |
| **Expected Value** | | | **100%** | **$[X.XX]** |

### Calculation

```
Expected Price = Σ(Scenario Price × Probability)
              = ($[Bull] × [P_bull]) + ($[Base] × [P_base]) + ($[Bear] × [P_bear])
              = $[X.XX]
```

**Verification:** Run `python tools/portfolio-math.py expected-value --scenarios '[JSON]'`

### Distribution Characteristics

| Metric | Value |
|--------|-------|
| Expected Value Price | $[X.XX] |
| Current Price | $[X.XX] |
| Expected Return | [X.X]% |
| Upside (Bull - Current) | +[X.X]% |
| Downside (Current - Bear) | -[X.X]% |
| Upside/Downside Ratio | [X.X]x |
| Probability of Loss | [X]% |
| Skew | [Left / Symmetric / Right] |

### Scenario Assumptions

**Bull Case ($[X], [X]% probability):**
- Key assumption 1: [specific, falsifiable]
- Key assumption 2: [specific, falsifiable]
- What must go right: [1 sentence]

**Base Case ($[X], [X]% probability):**
- Key assumption 1: [specific, falsifiable]
- Key assumption 2: [specific, falsifiable]
- Continuation of: [1 sentence]

**Bear Case ($[X], [X]% probability):**
- Key assumption 1: [specific, falsifiable]
- Key assumption 2: [specific, falsifiable]
- What goes wrong: [1 sentence]

### Probability Justification

[2-3 sentences explaining why these specific probabilities were chosen. Reference historical base rates, current conditions, or comparable situations. Do NOT just pick round numbers without justification.]

---

## Rules for Probability Assignment

1. **Probabilities must sum to 100%.** No exceptions.
2. **No scenario below 10% probability** unless it's truly a tail event (add a 4th scenario for tails).
3. **Bear case must represent genuine downside** — not just "base case minus 5%". Must include at least one scenario with >15% downside.
4. **Base case should be the most likely outcome** (typically 40-60% probability).
5. **Justify divergence from consensus** — if your probabilities differ materially from market-implied odds, explain why.
6. **Show the math** — every expected value calculation must be explicit, not just stated.
7. **Run portfolio-math.py** — compute Kelly fraction from your scenarios to sanity-check sizing implications.
