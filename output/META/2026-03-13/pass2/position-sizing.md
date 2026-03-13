# Position Sizing Analysis — META (Meta Platforms, Inc.)
## Date: 2026-03-13 | Analyst: Position Sizing Analyst

---

## 1. Input Collection

| Input | Source | Value |
|-------|--------|-------|
| Current price | Market data | $638.18 |
| Base case fair value | DCF + Debate consensus | $725/share |
| Probability-weighted EV | Director / Disagreement Map | $693-701/share |
| Bull case price / probability | DCF Analyst / Director | $1,032 / 23% |
| Base case price / probability | DCF Analyst / Director | $725 / 49% |
| Bear case price / probability | DCF Analyst / Director | $359 / 28% |
| Conviction rating | Director | 3 / 5 (Moderate) |
| Quality & Credibility score | Q&C Analyst | 4 / 5 |
| ESG / Governance score | ESG Analyst | 2 / 5 (Governance 1/5) |
| Technical score | Technical Analyst | 2.5 / 5 |
| Annualized volatility | Risk / Technical | ~37.5% (midpoint 35-40% range) |
| Beta | Quant / DCF | ~1.25 |
| 52-week range | Technical Analyst | $479.80 – $796.25 |
| Key technical support | Technical Analyst | $638.03 (50% Fib), $628.45, $589 |
| Key technical resistance | Technical Analyst | $657 (MA50), $689-695 (MA200), $744 |
| Key Unresolved Risk | Disagreement Map | CapEx ROI P(failure) = 15-35% (central 25%) |
| ADV estimate | Market data (META mega-cap) | ~$1,200M/day [ESTIMATED] |
| Days to liquidate (target) | Risk budget standard | 5 days |
| Reference portfolio size | [ASSUMPTION: Standard institutional mandate] | $500M |

---

## 2. Kelly Criterion Sizing

### Scenario Returns (from $638.18 current price)

| Scenario | Price | Return | Probability |
|----------|-------|--------|-------------|
| Bull | $1,032 | +61.7% | 23% |
| Base | $725 | +13.6% | 49% |
| Bear | $359 | -43.8% | 28% |

### Kelly Calculation

`[Tool used: tools/portfolio-math.py kelly-scenarios]`

| Component | Value | Derivation |
|-----------|-------|------------|
| Win probability (p) | 72.0% | P(base) + P(bull) = 49% + 23% |
| Loss probability (q) | 28.0% | P(bear) |
| Probability-weighted avg win | 28.97% | (23% × 61.7% + 49% × 13.6%) / 72% |
| Average loss | 43.75% | Bear case return (absolute) |
| Win/loss ratio (b) | 0.662x | 28.97% / 43.75% |
| **Full Kelly** | **29.7%** | (0.72 × 0.662 − 0.28) / 0.662 |
| **Half Kelly** | **14.9%** | Standard institutional practice |
| **Quarter Kelly** | **7.4%** | High-uncertainty baseline |

**WARNING: Full Kelly = 29.7% — extremely concentrated.** This is mathematically correct but practically impermissible for a diversified institutional portfolio. Full Kelly maximizes long-term geometric growth only under exact probability assumptions that cannot hold here; model uncertainty alone warrants heavy discounting.

**Distribution characteristics:**
- Expected value: $693.13/share (+8.6%)
- Skew: Right-skewed (favorable — more upside than downside in magnitude)
- Upside/downside ratio: 1.41x
- Probability of loss: 28%
- Breakeven bear probability: **40%** (current estimate: 28% — meaningful margin of safety above breakeven)

**Key insight:** The position has positive expected value (+8.6%), but with an asymmetric loss in the bear case (−43.8%) that is meaningfully larger than the base case gain (+13.6%). This means the win/loss ratio (0.66x) is below 1.0, which is why Kelly demands a larger win probability to compensate. At 28% bear probability, we are 12 percentage points below the 40% breakeven — a real but not dominant edge.

---

## 3. Volatility-Adjusted Sizing

`[Tool used: tools/portfolio-math.py vol-size — inputs: stock vol 37.5%, portfolio vol 12%, 25 positions, avg correlation 0.45]`

| Parameter | Value |
|-----------|-------|
| Portfolio target volatility | 12% annualized |
| Number of positions | 25 |
| Average pairwise correlation | 0.45 |
| Per-position volatility budget | 0.70% annualized |
| Stock annualized volatility | 37.5% |
| **Vol-adjusted weight** | **1.9%** |

`[ASSUMPTION: 25-position diversified portfolio at 12% target volatility with 0.45 avg pairwise correlation is standard for an active large-cap growth mandate.]`

**Note:** The vol-adjusted weight (1.9%) is the equal-risk contribution weight. It is intentionally low because META's 37.5% volatility is materially above a typical portfolio stock (~20%). A strict risk-parity approach would undersize META relative to conviction. The Kelly framework (7-15%) provides the upper bound; vol-adjusted sizing provides the floor discipline.

---

## 4. Liquidity Constraint

`[Tool used: tools/portfolio-math.py liquidity — ADV $1,200M, 15% participation, 5 days, $500M portfolio]`

| Constraint | Value | Implied Max Position |
|-----------|-------|---------------------|
| Average daily volume (ADV) | $1,200M/day [ESTIMATED] | — |
| Max participation rate | 15% of ADV | — |
| Max daily liquidation | $180M | — |
| Max liquidation window | 5 days | — |
| **Max position ($)** | **$900M** | — |
| **Max position (% of $500M portfolio)** | **180%** | Effectively unconstrained |

**Liquidity constraint: NOT BINDING.** META is one of the most liquid equities globally (~$1.2B ADV). Even a $50M position (10% of $500M portfolio) can be fully liquidated in less than 1 trading day at 15% participation. For practical purposes, liquidity is not a constraint for any institutional mandate at standard sizes.

---

## 5. Drawdown-Aware Sizing

| Parameter | Value | Derivation |
|-----------|-------|------------|
| Maximum acceptable single-position drawdown contribution | 5.0% of portfolio | Standard risk budget: single position should not drive >5pp drawdown |
| Stock max drawdown (95th percentile) | ~55% | [ASSUMPTION: 37.5% annual vol × 2.5-year horizon × 1.5 tail factor; consistent with 2022 actual META peak-to-trough −76% and bear scenario −44%] |
| **Max weight (drawdown constraint)** | **9.1%** | 5.0% / 55% = 9.1% |

```
Max Weight = Max Acceptable Drawdown Contribution / Stock Max Drawdown
           = 5.0% / 55% = 9.09%
```

If the bear case fully materializes (−43.75%), a 9.1% position contributes −4.0% portfolio drawdown — within the 5% budget. At the extreme 95th-percentile tail event (−55%), the same position contributes −5.0% — exactly at the budget. This constraint is binding at the margin: positions above 9.1% would exceed the drawdown budget in a tail event.

---

## 6. Conviction-Adjusted Sizing

| Dimension | Score | Adjustment |
|-----------|-------|------------|
| Director conviction rating | 3 / 5 | 0.50× multiplier |
| ESG / Governance score | 2 / 5 | −15% additional penalty |
| Technical score | 2.5 / 5 | −10% additional penalty |
| Quality & Credibility score | 4 / 5 | No penalty (above threshold) |

**Governance note:** ESG/Governance 2/5 (driven by Governance 1/5 — Zuckerberg 55-60% voting control with no accountability mechanism) is a structural risk, not a situational one. It does NOT cap conviction below 3 (the quality/credibility score of 4/5 is the gate), but it does warrant a discounting of position size beyond the conviction multiplier.

**Conviction-adjusted sizing from Half Kelly:**

| Step | Calculation | Result |
|------|-------------|--------|
| Half Kelly base | 14.86% | Starting point |
| Conviction 3/5 (0.5× multiplier) | × 0.50 | 7.43% |
| Governance penalty (ESG 2/5, −15%) | × 0.85 | 6.32% |
| Technical penalty (2.5/5, −10%) | × 0.90 | 5.68% |
| **Conviction-adjusted weight** | | **~5.6%** |

`[ASSUMPTION: Governance penalty of 15% reflects dual-class structural risk (Zuckerberg control precedent). Technical penalty of 10% reflects death cross + volume divergence signaling uncertain near-term entry timing. Both are separate from and additive to the conviction multiplier.]`

---

## 7. Final Position Size — Sizing Waterfall

**The final size is the minimum of all binding constraints:**

| Method | Suggested Weight | Binding? |
|--------|-----------------|----------|
| Full Kelly | 29.7% | No — never use |
| Half Kelly | 14.9% | No — starting ceiling |
| Quarter Kelly | 7.4% | Near-binding from above |
| Volatility-adjusted (equal risk) | 1.9% | No — floor discipline, too conservative given conviction |
| Liquidity-constrained | >100% | No — not relevant |
| Drawdown-aware | 9.1% | Constrains from above |
| Conviction-adjusted (3/5 + governance + technical) | 5.6% | **YES — BINDING CONSTRAINT** |
| Portfolio max single position | 10.0% | Hard cap; not reached |

**RECOMMENDED POSITION SIZE: 5.0–5.5% of portfolio**

_Rounded from 5.6% to 5.0-5.5% for practical implementation and rounding buffer._

| Portfolio Size | Position ($M) | Shares (at $638.18) |
|----------------|--------------|---------------------|
| $250M | $12.5–13.8M | 19,600–21,600 |
| $500M | $25.0–27.5M | 39,200–43,100 |
| $1,000M | $50.0–55.0M | 78,300–86,200 |

**Bound by:** Conviction adjustment (3/5 conviction × governance penalty × technical penalty). The pure Kelly math supports 7-15%, but the combination of: (1) moderate conviction on an unresolved CapEx ROI thesis, (2) structurally flawed governance preventing shareholder correction, and (3) technically damaged chart with confirmed death cross reduces the implementable size to 5-5.5%.

**Maximum position size (under any circumstances): 7.5%** — this is the Quarter Kelly ceiling; do not exceed without Director approval and specific catalyst trigger.

---

## 8. Entry Strategy

The entry strategy must navigate the tension between:
- Technical positioning: currently at 50% Fibonacci support ($638.03); death cross overhead
- Catalyst calendar: Q1 earnings (late April) as the next major binary event
- Thesis fragility: CapEx ROI P(failure) 15-35% — a high bar for full commitment now

### Position Building Plan

| Phase | Action | Size (% of target) | Trigger | Cumulative |
|-------|--------|--------------------|---------|------------|
| **Tranche 1 — Initial** | Establish position | 33% | Immediately (current zone $628-640; 50% Fib support holds) | 33% |
| **Tranche 2 — Build** | Add to position | 33% | Either: (a) Q1 earnings beat + CapEx reiteration [aggressive] or (b) Pullback to $589-610 structural support zone [defensive] | 67% |
| **Tranche 3 — Complete** | Full position | 34% | MA50 ($657) breakout with volume confirmation OR Llama Avocado strong reception (H1 2026) | 100% |

**In dollars ($500M portfolio at 5.5% target = $27.5M):**

| Tranche | Amount | Shares | Avg Price | Timing |
|---------|--------|--------|-----------|--------|
| T1 | ~$9.1M | ~14,250 | ~$638.18 | Immediately post-research |
| T2 | ~$9.1M | ~14,900–15,500 | ~$589-610 or earnings beat | Late April (earnings) or dip |
| T3 | ~$9.3M | ~14,100 | ~$657-665 | MA50 breakout with volume |
| **Total** | **~$27.5M** | **~43,250** | **~$632-638 blended** | Over 6-8 weeks |

**Scaling rules:**
- Build in 3 tranches over 4–8 weeks; do not accelerate beyond T1 before Q1 earnings
- Each tranche requires: (1) no material thesis deterioration (CapEx guidance stable), (2) price within entry range, (3) no new litigation adverse events
- **If price drops >10% before T2** (below $574): PAUSE — reassess whether CapEx guidance changed or Chinese advertiser headwind accelerated; do not average down blindly
- **If price rises >15% before T2** (above $734, near base fair value): Accept T1 partial position; do not chase into or above fair value
- **Q1 earnings (late April):** If beat on revenue AND CapEx guidance reiterated: build T2 immediately post-print (75% probability of this outcome per Catalyst Analyst). If miss or CapEx guide raised: hold at T1 only, reassess for T3 with new data.

**Entry zone validation:**
- Aggressive entry: $628-640 (current zone) — 50% Fibonacci retracement holds as support
- Preferred T2 entry: $589-628 — structural support zone with favorable risk/reward
- Do NOT enter T3 below MA50 ($657) — death cross makes momentum unfavorable above T1 without MA50 recapture

---

## 9. Exit / Trim Strategy

| Trigger | Action | Size Reduction | Price Level |
|---------|--------|---------------|-------------|
| Price reaches base fair value | Begin trimming | Reduce by 40% | $725/share |
| Price reaches bull-case range | Reduce aggressively | Reduce to 15-20% core | $950-1,032/share |
| Price > bull case ($1,032) | Sell to minimal holding | Reduce to 10% core | Above $1,032 |
| **Bear case trigger event (any ONE of below):** | Immediate full exit | 100% exit | — |
| — CapEx guidance raised above $145B | Exit | 100% | — |
| — Q2 2026 ad revenue growth <5% | Exit | 100% | — |
| — Chinese advertiser revenue decline >$10B annualized | Exit | 100% | — |
| — Youth litigation adverse verdict (>$10B settlement) | Exit 50-75% | 50-75% | — |
| **Hard stop-loss** | Full exit | 100% | **$589/share** |
| Thesis degradation (fundamental, not price) | Trim over 5 trading days | 50-100% depending on severity | — |
| Better opportunity (rebalance trigger) | Trim to fund | Reduce by 2-3% portfolio weight | — |

**Hard stop-loss: $589** (7.7% below current price of $638.18; major 2024 structural support per Technical Analyst)

`[ASSUMPTION: Stop set at $589 — the 2024 year-end structural support level identified by the Technical Analyst, which is below the $628-640 Fibonacci support zone by sufficient margin to avoid being triggered by noise. Closing below $589 would represent a breakdown of all near-term technical support and suggest fundamentals-driven selling.]`

**Price target-based trim schedule:**

| Price Level | Implied Return | Action | Position Size After |
|-------------|---------------|--------|---------------------|
| $657 (MA50) | +2.9% | No action — just a moving average; reassess T3 trigger | 67-100% |
| $695 (MA200) | +8.9% | No action — monitor quality of breakout (volume) | 100% |
| $725 (base FV) | +13.6% | Trim 40% of position | ~60% |
| $850 | +33.2% | Trim another 20% | ~40% |
| $950 | +48.9% | Trim to minimal core position | 15-20% |
| $1,032 (bull FV) | +61.7% | Sell to 10% core | 10% |

**Fundamental exit triggers (thesis-based, price-independent):**
1. CapEx normalized rate doesn't show improvement toward 20% of revenue by Q4 2026 (original bear scenario: stays 22%+)
2. Advantage+ revenue contribution stops growing (stalls < $65B annual run rate) — suggests AI ROI failure
3. Zuckerberg announces major new capital commitment (third bet scenario) unrelated to current AI infrastructure program
4. WhatsApp monetization explicitly delayed past FY2027 in any management commentary

---

## 10. Portfolio Context

### Before vs. After Adding META (5.5% position)

| Metric | Before META | After META (5.5%) | Delta |
|--------|-------------|-------------------|-------|
| Number of positions | 24 | 25 | +1 |
| Portfolio beta | ~1.15 | ~1.22 | +0.07 |
| Communication Services weight | 5% | 10.5% | +5.5% |
| Tech + Comm Services combined | 20% | 25.5% | +5.5% |
| Top 5 concentration (estimated) | ~30% | ~35% | +5% |
| Portfolio vol (estimated) | ~14.0% | ~15.3% | +1.3pp |
| Marginal contribution to risk | — | ~1.25% | — |

`[ASSUMPTION: Pre-META portfolio has 24 positions with 18% tech weight, 5% Communication Services weight, 14% baseline portfolio vol, and portfolio beta of 1.15. These are reference assumptions — actual portfolio context will vary.]`

**Sector concentration:** Adding META brings Tech + Communication Services combined to ~25.5% — marginally above the 25% guideline for tech sector exposure. This is manageable given META's advertising business model is partially distinct from hardware/semiconductor tech, but warrants monitoring.

`[CONCENTRATION NOTE: Combined tech/comms weight of ~25.5% is near the 25% sector limit. Do not add additional mega-cap tech names without trimming other tech exposures first.]`

**Correlation considerations:**
- META correlation to FAANG/mega-cap tech: ~0.60 estimated
- META correlation to advertising cycle: High (positive economic exposure)
- META correlation to interest rate sensitivity: Moderate negative (longer duration given CapEx cycle)
- **If portfolio already holds GOOGL/SNAP/PINS/RDDT:** These are highly correlated advertising-cycle plays. A portfolio with both META and GOOGL effectively doubles the advertising-cycle bet. In a recession scenario, correlations spike toward 1.0, amplifying drawdown.

`[CORRELATION WARNING: If GOOGL or other digital advertising names (SNAP, PINS, RDDT, TTD) already exceed 5% combined weight, META position amplifies advertising-cycle concentration. Recommend capping combined META + digital ad exposure to 10% of portfolio.]`

**Macro sensitivity:**
- A +100bps rate shock reduces fair value by approximately $40-60/share (elevated CapEx cycle = longer duration)
- A 20% advertising recession reduces operating income to ~$57B, pressing stock toward $400-450 near-term
- A 1% USD appreciation vs. EUR/GBP reduces revenue by ~$2-3B (Europe is ~20% of revenue)

---

## 11. Scenario Stress Test on Position

**How does the position perform under each scenario?**

| Scenario | Probability | Stock Return | Position Return ($27.5M) | Portfolio Impact |
|----------|-------------|-------------|--------------------------|-----------------|
| Bull | 23% | +61.7% | +$17.0M | +3.4pp |
| Base | 49% | +13.6% | +$3.7M | +0.75pp |
| Bear | 28% | −43.8% | −$12.0M | −2.4pp |
| Hard stop triggered | ~5% | −7.7% | −$2.1M | −0.42pp |
| Stress (recession + CapEx overrun) | ~3-5% | −68% | −$18.7M | −3.7pp |

**Expected contribution to portfolio return:** +8.6% × 5.5% = **+0.47pp expected return contribution**

The risk-adjusted contribution is modest — this is a moderate-conviction position, not a portfolio anchor.

---

## 12. Position Sizing Summary

META warrants a **5.0–5.5% portfolio allocation** (reference: $25-27.5M in a $500M portfolio), built in three tranches over 4–8 weeks. The recommended weight is **bound by conviction adjustment**: the Director's Conviction 3/5 rating, combined with an ESG/Governance penalty (1/5 governance — Zuckerberg dual-class control with zero shareholder recourse) and a technical penalty (death cross confirmed; chart damaged), reduces the Half Kelly ceiling (14.9%) to an implementable 5.5% position. The Kelly math is technically supportive — breakeven bear probability is 40% against a current 28% estimate — but the unresolved CapEx ROI risk (P(failure) = 15-35%, central 25%) means the probability inputs carry meaningful model uncertainty that demands conservative sizing.

**The binding condition for resizing is CapEx ROI evidence.** If Q1 2026 (late April) and Q2 2026 earnings show: (a) CapEx tracking within $115-135B guidance, (b) Advantage+ revenue per impression inflecting above 12% growth, and (c) Meta AI monetization timeline announced, the position should be upgraded to 7-7.5% (Quarter Kelly ceiling). Conversely, if CapEx guidance is raised above $145B or ad revenue growth falls below 8%, exit to 0% immediately. The hard stop is $589 (7.7% below current price); the maximum loss from the recommended position to the stop is approximately $2.1M (0.42% of a $500M portfolio) — within a tightly managed risk budget.

---

*Position Sizing Analyst | META / 2026-03-13 / Pass 2*
*Tools used: tools/portfolio-math.py kelly-scenarios, vol-size, liquidity*
*Input sources: DCF Analyst brief, Risk & Contrarian brief, Technical Analyst brief, Catalyst Analyst brief, Credit Analyst brief, Quant Analyst brief, Disagreement Map*
