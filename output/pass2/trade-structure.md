# AMD — Trade Structure Memo
## Advanced Micro Devices, Inc. — Equity Research Swarm

**Date:** 2026-03-09
**Prepared by:** Trade Structurer
**Basis:** Editor's Draft (2026-03-09), Pass 1 DCF, Risk, Technical, Devil's Advocate, and Catalyst Analyst reports
**Rating:** HOLD | Price Target: $192 | Current: $190.40 | Conviction: [Director to assign] /5

---

## 1. Thesis and Recommendation Summary

| Input | Value | Source |
|-------|-------|--------|
| Rating | HOLD | Director / Editor Draft |
| Price Target | $192 | Blended DCF 50% / Comps 50% |
| Current Price | $190.40 | Market, 2026-03-09 |
| Expected Return (price target) | +0.8% | Derived |
| Expected Return (probability-weighted EV) | -3.4% ($184) | Kelly-scenarios tool |
| Conviction | [Director to assign] /5 | Director |
| Time Horizon | 6-12 months (MI450 ramp resolution) | Catalyst Analyst |
| Key Catalyst | MI450/Helios production ramp | Catalyst Analyst |
| Catalyst Date | Q3-Q4 2026 (H2 2026) | Catalyst Analyst |
| Sector | Semiconductors | — |
| Beta | 2.02 | Risk Analyst (5Y monthly, StockAnalysis.com, Tier 4) |
| Annualized Volatility | ~55% | Risk Analyst estimate |
| Implied Volatility (ATM, est.) | ~50-55% | Risk Analyst [ESTIMATED] |

**Thesis in one sentence:** AMD at $190.40 is approximately fairly valued with a left-skewed probability distribution (EV $184, -3.4%), a binary H2 2026 catalyst (MI450 ramp), and a confirmed technical downtrend — the optimal trade is no new capital deployment at current levels, with structured entry plans at lower levels and options overlays to exploit elevated implied volatility.

**The core trade problem:** The Kelly-scenarios tool confirms this is a **negative expected value position** at current price (Full Kelly = -10.74%; EV = $184 vs. $190.40 current). The probability-weighted expected return is -3.4%. The break-even bear probability is only 22% — meaning if bear probability exceeds 22%, the position loses money on average. Our assigned bear probability of 30% is well above this threshold. At the same time, the stock sits near major support ($185-191), RSI is approaching oversold (~32-39), and H2 2026 catalysts could generate +20-30% upside if MI450 executes. The trade structure must reconcile negative current EV with significant optionality.

**Kelly Tool Output (verbatim):**
```
Expected Value Price: $184.00
Expected Return: -3.36%
Full Kelly: -10.74% (NEGATIVE — do not take position)
Upside/Downside Ratio: 0.99x
Probability of Loss: 80% (base and bear both at or below current)
Breakeven Bear Probability: 22%
Recommendation: NEGATIVE EXPECTED VALUE — do not take this position
```

---

## 2. Primary Trade Recommendation

**Trade Type:** No New Position at Current Levels + Conditional Phased Entry + Options Income Overlay

**Rationale:** Per the trade structurer framework, when the recommendation is Hold, "the best trade is no trade." The Kelly math confirms this emphatically: at -10.74% Kelly fraction, initiating a long position at $190.40 is mathematically inadvisable. However, the binary H2 2026 catalyst creates genuine optionality that warrants an active structure for (a) existing holders seeking to optimize, (b) new entrants seeking defined entry points, and (c) options traders seeking to exploit elevated IV.

### For Existing Holders

| Parameter | Value |
|-----------|-------|
| Action | HOLD current position; do NOT add at $190.40 |
| Covered call overlay | Sell $220 calls, 4-6 month expiry (see Section 4) |
| Protective put | Buy $165 puts, 6-month expiry (see Section 4) |
| Stop-loss for traders | $165 (below structural support; -13.3% from current) |
| Hard stop (catastrophic) | $140 (61.8% Fibonacci retracement; -26.5%) |
| Max loss with discipline | -13.3% to $165 stop; -26.5% to $140 hard stop |

### For New Position Entrants — Phased Entry Plan

| Tranche | Price Level | Condition | Size | Technical Justification |
|---------|-------------|-----------|------|------------------------|
| Tranche 1 | $170-175 | Retest of $165 structural support + hold | 1/3 of target | 2021 highs; 50% Fibonacci retracement ($171.78); volume support |
| Tranche 2 | Post-MI450 confirmation | MI450 ships on schedule, initial deployment data positive (Q3 2026) | 1/3 of target | Catalyst confirmation removes primary thesis risk |
| Tranche 3 | $228+ | Close above 200-day MA on expanding volume | 1/3 of target | Technical trend reversal confirmation |

**Why NOT enter at current levels?**
1. Kelly fraction is -10.74% — mathematically the position destroys expected value
2. Stock is below all major moving averages (20d $202, 200d $228, 50d $242) in confirmed downtrend
3. Risk/reward to nearest support ($185) vs. nearest resistance ($200) is only 1.2:1
4. No bullish divergence on any momentum indicator
5. Break-even bear probability of 22% is far below our assigned 30% — the math says "don't buy"
6. H2 2026 catalysts are 4-6 months away; there is no urgency to own the stock today

**When DOES this change?**
- If AMD drops to $165-175 (Tranche 1 entry): EV improves to approximately +8-15%, Kelly turns positive
- If MI450 ships on time with positive benchmarks: bear probability drops to ~15%, EV turns meaningfully positive
- If a bullish divergence forms (RSI makes higher low while price makes lower low): technical entry signal

---

## 3. Pair Trade — Long AMD / Short INTC (Intel)

**Pair Type:** Relative Value / x86 Market Share Divergence

**Rationale:** If the thesis is that AMD deserves a HOLD (not a sell), the cleanest alpha expression is relative to the weakest comparable. Intel (INTC) is the natural pair: both are x86 semiconductor companies, but AMD has been systematically gaining server CPU share (36-40% and rising) while Intel has been losing it (18 consecutive quarters of share losses). Intel trades at 17.9x EV/EBITDA and 90.7x P/E with only 7.9% revenue growth — fundamentally impaired. AMD's EPYC Turin has a 40% performance lead over Intel Xeon. Even in the AMD bear case ($130), EPYC continues gaining share; Intel's recovery thesis (Granite Rapids, foundry) faces higher execution risk than AMD's.

**Why NOT NVDA as the short?**
- NVIDIA has a fundamentally stronger competitive position (CUDA moat, 80%+ AI GPU share, higher margins)
- Shorting NVDA against AMD is a bet that the #2 AI GPU player outperforms the dominant #1 — this contradicts the CUDA gap evidence (30-99% effective advantage)
- NVDA's beta is lower (~1.4 vs. AMD's 2.02), creating adverse pair dynamics in selloffs

**Why NOT SMH/SOXX as the short?**
- AMD is 8.4% of SOX — shorting the index while long AMD creates a circular position where you're partially short your own long
- Better to isolate the specific relative value thesis (x86 share shift) with a single-name pair

### Pair Structure

| Leg | Ticker | Direction | Weight | Rationale |
|-----|--------|-----------|--------|-----------|
| Long | AMD | Buy | 50% | x86 share gains, AI GPU optionality, fortress balance sheet |
| Short | INTC | Sell | 43% (beta-adjusted) | x86 share losses, foundry execution risk, turnaround uncertainty |

**Beta Adjustment:**
```
INTC beta: ~1.40 [ESTIMATED: turnaround-stage stock with elevated vol]
AMD beta: 2.02
Hedge Ratio = AMD weight x (AMD beta / INTC beta) = 50% x (2.02 / 1.40) x 0.60 = 43%
Note: 0.60 multiplier reflects imperfect pair correlation
```

| Pair Metric | Value |
|-------------|-------|
| Net Exposure | +7% (slight net long) |
| Gross Exposure | 93% |
| Estimated Pair Correlation | 0.35-0.45 [ESTIMATED; both are x86 semis but diverging fundamentals] |
| Expected Pair Return (12m) | +10-15% [ESTIMATED: AMD EPYC share gains vs. INTC share losses] |
| Max Pair Loss (estimate) | -20% (if INTC turnaround succeeds and AMD MI450 fails) |
| Borrow Cost (INTC short) | ~1.0-1.5% annualized [ESTIMATED; INTC has higher short interest than AMD] |

**Why this short?** Intel is not just "same sector." Intel is losing the specific market (x86 server CPU) where AMD is gaining. This is a direct competitive displacement trade. Even if the broader AI thesis disappoints, AMD takes EPYC share from Intel — the pair captures this alpha independent of market direction. Intel's turnaround under Pat Gelsinger's successor faces 18-24 months of uncertainty, and Granite Rapids benchmarks show it still trails Turin.

**Pair exit triggers:**
- Profit exit: AMD/INTC relative multiple spread compresses to 1.0x (currently AMD at 24.6x EV/EBITDA vs. INTC at 17.9x, but AMD deserves premium given growth differential); target 6-12 months
- Loss exit: INTC closes above $30 AND AMD breaks below $165 simultaneously (indicates Intel turnaround + AMD thesis failure)
- Time stop: 12 months if pair P&L is within +/-5% (thesis not expressing)

**Max loss on pair trade: -20%** (scenario: INTC rallies 25% on turnaround progress while AMD drops 15% on MI450 delays)

---

## 4. Options Overlay — Exploiting Elevated IV on Binary Catalyst

### Why Options Are Appropriate Here

Three factors make options the optimal trade expression for AMD:

1. **Binary H2 2026 catalyst:** MI450 ramp is date-specific (Q3-Q4 2026) with +20-30% upside / -25-35% downside magnitude — classic options catalyst
2. **Elevated implied volatility:** IV of ~50-55% vs. the ~45-50% option-implied suggests options are roughly fairly priced to slightly cheap [ESTIMATED]. The IV/RV ratio near 1.0 means options are not overpriced — unlike many high-IV stocks where selling premium is the only trade
3. **Left-skewed distribution:** The probability distribution favors strategies that limit downside while maintaining upside — exactly what defined-risk options structures achieve

### Structure A — Covered Call for Existing Holders (Premium Selling / Income)

**Strategy:** Sell out-of-the-money covered calls against existing long position
**Applicable to:** Existing holders who want income while waiting for H2 2026 catalyst resolution

| Leg | Option | Strike | Expiry | Estimated Premium | Delta |
|-----|--------|--------|--------|-------------------|-------|
| Sell | Call | $220 | September 2026 (~6 months) | ~$12-16/share [ESTIMATED at ~50% IV] | ~0.30 |

| Risk Profile | Value |
|-------------|-------|
| Premium Collected | ~$12-16/share (~6.3-8.4% of stock price annualized) |
| Maximum Gain | ($220 - $190.40) + premium = $41.60-45.60/share (+21.9-24.0%) |
| Upside Cap | $220 (bull case target is $250 — this sacrifices $30/share of upside above $220) |
| Downside Buffer | Premium reduces effective cost basis to ~$174-178 |
| Breakeven | ~$174-178 (vs. $190.40 unhedged) |
| Max Loss | Stock to $0 minus premium collected; practical stop at $165 limits loss to -$9 to -$13/share net of premium |

**Rationale:** The $220 strike is 15.5% above current price and sits below the bull case target of $250. At ~50% IV, 6-month ATM+15% calls generate meaningful premium. If MI450 executes and the stock reaches $250, the covered call caps gains at $220 — but this is a HOLD-rated stock where the probability-weighted EV is below current price. Sacrificing $30 of low-probability bull case upside in exchange for $12-16 of certain premium income is a rational trade for a HOLD thesis.

**Why $220 strike?** The $220 level sits:
- Above the 200-day MA ($228 — rounded) as a realistic resistance zone
- Below the bull case target ($250) but above the price target ($192)
- At a delta of ~0.30 — 70% probability the call expires worthless (aligns with base/bear probability of 80%)

### Structure B — Protective Put for Existing Holders (Catastrophic Insurance)

**Strategy:** Buy out-of-the-money put for portfolio protection

| Leg | Option | Strike | Expiry | Estimated Premium | Delta |
|-----|--------|--------|--------|-------------------|-------|
| Buy | Put | $165 | September 2026 (~6 months) | ~$8-12/share [ESTIMATED at ~50% IV] | ~-0.25 |

| Risk Profile | Value |
|-------------|-------|
| Premium Cost | ~$8-12/share (~4.2-6.3% of stock price for 6 months) |
| Protection Begins | Below $165 |
| Protection Level | Full protection below $165 through September 2026 |
| Max Protected Loss | ($190.40 - $165) + premium = $33.40-37.40/share (-17.6% to -19.6%) |
| Breakeven (with stock) | Stock must appreciate by premium amount (~$8-12) to break even on total position |

**Rationale:** The $165 level is the 2021 highs and the structural support identified by the Technical Analyst. A break below $165 signals thesis deterioration (MI450 failure, mega-deal restructuring). The put transforms the risk profile from open-ended downside (-32% to bear case $130, -60% to catastrophic $76) to defined max loss of ~-18-20%.

### Structure C — Combined Collar (Covered Call + Protective Put for Existing Holders)

**Strategy:** Sell call + buy put = zero-cost or low-cost collar

| Leg | Option | Strike | Expiry | Net Premium |
|-----|--------|--------|--------|-------------|
| Sell | Call | $220 | September 2026 | Collect ~$12-16 |
| Buy | Put | $165 | September 2026 | Pay ~$8-12 |
| **Net** | | | | **Collect ~$2-6/share** |

| Risk Profile | Value |
|-------------|-------|
| Net Premium | Collect ~$2-6/share (collar pays you to hedge) |
| Maximum Gain | ($220 - $190.40) + net premium = $31.60-35.60/share (+16.6-18.7%) |
| Maximum Loss | ($190.40 - $165) - net premium = $19.40-23.40/share (-10.2% to -12.3%) |
| Effective Floor | $165 (hard floor) |
| Effective Ceiling | $220 (upside cap) |
| Risk/Reward | 1.4:1 to 1.7:1 (significantly improved from unhedged 0.99:1) |

**This is the recommended options structure for existing holders.** The collar transforms the AMD risk profile from:
- Unhedged: Upside +31% / Downside -32% / R:R 0.99:1 / Max loss open-ended
- Collared: Upside +17-19% / Downside -10-12% / R:R 1.5:1 / Max loss capped at $165 / Net premium collected

The collar costs nothing (or pays a small net credit) because the elevated IV makes the call premium roughly offset the put premium. This is the key insight: **when IV is high, collars are cheap or free — the market is paying you to define your risk.**

### Structure D — Bull Call Spread (For New Entrants at Lower Levels)

**Strategy:** Defined-risk bullish options position for Tranche 1 entrants at $170-175

| Leg | Option | Strike | Expiry | Estimated Premium |
|-----|--------|--------|--------|-------------------|
| Buy | Call | $175 | January 2027 (~10 months) | ~$28-34/share [ESTIMATED] |
| Sell | Call | $230 | January 2027 (~10 months) | ~$12-16/share [ESTIMATED] |
| **Net Debit** | | | | **~$14-20/share** |

| Risk Profile | Value |
|-------------|-------|
| Maximum Gain | ($230 - $175) - net debit = $35-41/share (175-292% return on premium) |
| Maximum Loss | Net debit = $14-20/share (100% of premium) |
| Breakeven | ~$189-195 (roughly current price — need MI450 execution to profit) |
| Risk/Reward | ~2:1 to 2.5:1 |

**Rationale:** This structure is ONLY appropriate if the stock drops to $170-175 (Tranche 1 entry zone). At that level, the bull call spread provides:
- Defined max loss ($14-20/share vs. open-ended stock downside)
- 2:1+ risk/reward (vs. 0.99:1 unhedged at $190)
- Sufficient time (10 months) to capture H2 2026 MI450 ramp and Q3/Q4 2026 earnings
- Less capital required than buying stock outright (~$17/share vs. $175/share)

**Why January 2027 expiry?** The MI450 ramp begins Q3 2026 (July-September) with first deployment confirmation expected Q4 2026. January 2027 expiry gives the thesis ~3-4 months post-catalyst to resolve. Shorter expiry risks theta decay killing the position before the catalyst arrives.

---

## 5. Alternative Structures for Different Conviction Levels

### Alternative 1 — Short Straddle (Neutral/Range-Bound Conviction)

For investors who believe AMD stays between $150-$230 for 6 months while the market waits for MI450:

| Parameter | Value |
|-----------|-------|
| Structure | Sell $190 call + Sell $190 put, September 2026 |
| Premium Collected | ~$38-48/share [ESTIMATED at ~50% IV, 6 months] |
| Breakeven Range | $142-238 (wide range due to high IV) |
| Max Gain | Full premium if AMD closes at exactly $190 at expiry |
| Max Loss | Unlimited above $238 or below $142 |
| **Max Loss with management** | **Stop at -1x premium ($38-48/share); manage at $150 or $230** |

**Pros:** Collects massive premium from elevated IV. AMD's price target ($192) is almost exactly the current price ($190.40) — the research team's base case IS a range-bound outcome. Time decay works in your favor while the market waits.

**Cons:** Unlimited loss if MI450 either succeeds spectacularly (stock to $250+) or fails catastrophically ($130 or below). Requires active management. Margin-intensive. **Not recommended for accounts that cannot withstand assignment risk.**

**RED LINE: This structure involves naked short options. Per the framework, all short option positions must be hedged or spread. Convert to an iron condor (see Alternative 1B) if executing.**

### Alternative 1B — Iron Condor (Range-Bound, Defined Risk)

| Leg | Option | Strike | Expiry |
|-----|--------|--------|--------|
| Buy | Put | $145 | September 2026 |
| Sell | Put | $165 | September 2026 |
| Sell | Call | $225 | September 2026 |
| Buy | Call | $250 | September 2026 |

| Risk Profile | Value |
|-------------|-------|
| Net Premium Collected | ~$8-13/share [ESTIMATED] |
| Max Gain | Premium collected (if AMD closes between $165-$225 at expiry) |
| Max Loss | $20 spread width - premium = $7-12/share |
| Breakeven Range | $153-$237 [ESTIMATED] |
| Probability of Max Gain | ~50-55% (aligns with base case probability) |
| Risk/Reward | ~1:1 |

**NOTE: This structure has 4 legs, which exceeds the 3-leg complexity maximum in the framework. Include for completeness but flag as complex for execution.**

### Alternative 2 — Cash-Secured Put Sale (Bullish at Lower Levels)

For investors who want to buy AMD cheaper and collect premium while waiting:

| Parameter | Value |
|-----------|-------|
| Structure | Sell $165 put, September 2026 |
| Premium Collected | ~$8-12/share [ESTIMATED] |
| Effective Entry Price | $153-157 if assigned (vs. $190.40 today — 17-20% cheaper) |
| Max Gain | Premium collected ($8-12/share, 4.9-7.3% return on capital reserved) |
| Max Loss | Unlimited below $153-157 (though practical floor at $130 bear case) |
| Capital Required | $16,500 per contract (cash-secured at $165 strike) |
| Breakeven | $153-157 |

**Rationale:** If you want to own AMD at a better price, sell the $165 put. You either:
(a) Collect $8-12/share and AMD never drops to $165 — 4.9-7.3% return on reserved capital over 6 months (~10-15% annualized), or
(b) Get assigned at $165 and own AMD at an effective cost of $153-157 — 18-20% below current price and near the Technical Analyst's "ideal entry" zone

**Max loss: $153-157/share if AMD goes to zero. Practical max loss: ~$23-27/share if AMD reaches bear case of $130.**

### Alternative 3 — Do Nothing (Benchmark)

| Parameter | Value |
|-----------|-------|
| Structure | Hold current position unhedged; take no action |
| Expected Return | -3.4% (probability-weighted EV of $184 vs. $190.40) |
| Max Loss | -32% to bear case $130; -60% to catastrophic $76 |
| Max Gain | +31% to bull case $250 |
| Risk/Reward | 0.99:1 |

This is the default HOLD outcome. Acceptable for passive investors but suboptimal given available options structures that improve risk/reward at no net cost (collar).

---

## 6. Sector Hedge (Beta Reduction for Portfolio Context)

If AMD is held in a broader portfolio, the 2.02 beta creates outsized market sensitivity. To isolate company-specific alpha from market beta:

### Hedge Calculation

```
Hedge Vehicle: Short SMH (VanEck Semiconductor ETF)
AMD Position Size: $100 (illustrative)
Hedge Weight = AMD Position x AMD Beta x (1 / SMH Beta)
             = $100 x 2.02 x (1 / 1.50)
             = $134.67

For PARTIAL hedge (50% beta reduction):
Hedge Weight = $134.67 x 50% = $67.33
```

| Parameter | Value |
|-----------|-------|
| Hedge Vehicle | SMH (Semiconductor ETF) |
| Direction | Short |
| Weight (full hedge) | 135% of AMD long position |
| Weight (half hedge) | 67% of AMD long position |
| Estimated Borrow Cost | ~0.3-0.5% annualized (highly liquid ETF) |
| Residual Exposure | Company-specific alpha (EPYC share gains, MI450 optionality) |

**Residual After Hedge:**
- Market beta: ~0 (fully hedged) or ~1.0 (half hedged)
- Sector exposure: ~0 (AMD-specific factors only)
- What you keep: EPYC vs. Intel share gain alpha, MI450 catalyst optionality, mega-deal execution premium
- What you remove: Broad semiconductor cycle risk, AI capex cycle risk, rate sensitivity

**Caveat:** AMD is 8.4% of SOX — shorting SMH creates a circular position where ~8.4% of your short is your own long. This dilutes hedge effectiveness by ~8%. Acceptable for a rough hedge but not precise.

---

## 7. Implementation Notes

| Parameter | Recommendation |
|-----------|---------------|
| **Entry Timing** | Do NOT initiate new long positions at $190.40. Wait for Tranche 1 entry at $170-175 or catalyst confirmation in Q3 2026 |
| **Position Building** | Phased entry over 4-7 months: Tranche 1 at $170-175 (support retest), Tranche 2 on MI450 confirmation (Q3 2026), Tranche 3 on technical reversal ($228+) |
| **Collar Timing** | For existing holders, execute the September 2026 collar ($165 put / $220 call) immediately — IV is elevated, making the collar cheap or free. Do not wait for further IV expansion |
| **Pre-Q1 Earnings** | Q1 2026 earnings ~May 5. Historical average AMD earnings move: +/-7-9%. Implied move: +/-8-10%. Do NOT build new unhedged positions ahead of this event. If entering at Tranche 1, use bull call spread rather than stock |
| **MI450 Monitoring** | Q3 2026 MI450 shipment confirmation is the make-or-break event. Watch for: (1) Oracle 50K GPU supercluster deployment confirmation, (2) OpenAI/Meta deployment commentary, (3) NVIDIA Vera Rubin competitive benchmarks. Any of these three data points resolves the primary uncertainty |
| **Exit Trigger (profit)** | Bull case: $250 (full exit of stock + roll or close collar). Partial trim at $220 if covered call is in place |
| **Exit Trigger (loss)** | Break below $165 on closing basis with volume: exit entire position. This level is the 2021 highs, the put strike, and the structural support — a break below invalidates the HOLD thesis |
| **Time Stop** | If AMD is between $170-$210 by January 2027 with MI450 ramp data available, reassess thesis completely. By that point, the primary uncertainty (can AMD execute at hyperscale?) will have a definitive answer |
| **Transaction Costs** | Stock: ~2-5 bps round-trip. Options spreads: ~20-40 bps round-trip. Pair trade short (INTC): ~1.0-1.5% annualized borrow. Total all-in: ~100-200 bps for full structure |
| **Portfolio Correlation** | AMD's 2.02 beta and 0.70-0.75 SPX correlation mean this position amplifies all portfolio drawdowns. At stress-state correlation of 0.85+, AMD falls 2.4x the market (asymmetric beta). Monitor total semi/tech exposure. Do not exceed 5% portfolio weight in AMD even at Tranche 1 entry levels |

---

## 8. Recommended Trade Priority Ranking

| Priority | Structure | Action | Timing | Max Loss |
|----------|-----------|--------|--------|----------|
| 1 | **Collar for existing holders** ($165P / $220C, Sep 2026) | Execute immediately | Immediate | -10.2% to -12.3% (capped at $165) |
| 2 | **Cash-secured put sale** ($165, Sep 2026) | Sell put to establish Tranche 1 entry at discount | Immediate | ~$23-27/share to bear case $130 |
| 3 | **Pair trade** (Long AMD / Short INTC, beta-adjusted) | Execute if seeking market-neutral x86 exposure | Within 1 week | -20% on pair |
| 4 | **Tranche 1 stock entry** at $170-175 | Wait for support retest | Conditional | -13% to $148 bear floor (stop at $148) |
| 5 | **Bull call spread** ($175/$230, Jan 2027) | Execute only at Tranche 1 levels | Conditional on price | $14-20/share (100% of premium) |
| 6 | **Tranche 2 stock entry** on MI450 confirmation | Wait for Q3 2026 catalyst | Conditional on execution | Reassess based on new data |

---

## 9. Risk Summary by Structure

| Structure | Max Gain | Max Loss | Risk/Reward | Break-even | Probability of Profit |
|-----------|----------|----------|-------------|-----------|----------------------|
| Unhedged long at $190.40 | +31% ($250) | -32% ($130) / -60% ($76) | 0.99:1 | $190.40 | ~20% (bull case only) |
| Collar ($165P/$220C) | +17-19% | -10-12% | 1.5:1 | ~$188 (net of credit) | ~25-30% |
| Cash-secured $165 put | ~$8-12/share (5-7%) | -$23-27/share to $130 | ~0.4:1 | $153-157 | ~70-75% (OTM expiry) |
| Pair (AMD/INTC) | +10-15% | -20% | ~0.7:1 | Relative spread neutral | ~55-60% |
| Bull call spread at $175 | +175-292% on premium | -100% of premium ($14-20) | 2:1 to 2.5:1 | $189-195 | ~25-30% |
| Iron condor | ~$8-13/share | -$7-12/share | ~1:1 | $153-237 range | ~50-55% |

---

## 10. Summary — One-Paragraph Trade Recommendation

The recommended trade for AMD is **no new capital deployment at $190.40**, consistent with the HOLD rating, negative expected value (Kelly = -10.74%, EV = $184), and confirmed technical downtrend. For existing holders, the optimal structure is a **September 2026 collar** (sell $220 call / buy $165 put) that costs nothing or generates a small net credit, caps upside at +17-19%, and defines maximum downside at -10-12% — transforming the risk/reward from 0.99:1 to 1.5:1 while the H2 2026 MI450 ramp resolves the primary uncertainty. For new entrants, the highest-EV trade is a **cash-secured $165 put sale** (September 2026) that either generates 5-7% income over 6 months or establishes a position at $153-157 — 18-20% below current price, near the Technical Analyst's ideal entry zone, where the Kelly math turns positive. Separately, a **beta-adjusted long AMD / short INTC pair trade** captures the x86 server CPU share displacement alpha with limited market exposure. **Max loss on the collar is -$19-23/share (~-10-12%) from current price, capped at $165. Max loss on the cash-secured put is $23-27/share to bear case $130. Max loss on the pair trade is ~-20%.** The primary catalyst trigger is the MI450 production ramp in Q3 2026; the thesis resolution event is OpenAI/Meta initial deployment confirmation in Q4 2026. Do not initiate unhedged long positions until either (a) price reaches $170-175 or (b) MI450 execution risk is substantively reduced by shipping confirmation.

---

## Appendix: Tool Outputs

### Kelly-Scenarios Tool (portfolio-math.py)

```
Scenarios:
  Bull: $250 (+31.30%, 20% probability)
  Base: $190 (-0.21%, 50% probability)
  Bear: $130 (-31.72%, 30% probability)

Expected Value Price: $184.00
Expected Return: -3.36%

Kelly Fractions:
  Full Kelly:    -10.74% (NEGATIVE — do not take position)
  Half Kelly:    -5.37%
  Quarter Kelly: -2.68%

Distribution:
  Skew: Approximately symmetric
  Upside/Downside Ratio: 0.99x
  Probability of Loss: 80%
  Breakeven Bear Probability: 22%

RECOMMENDATION: NEGATIVE EXPECTED VALUE — do not take this position.
```

### Options Premium Estimates

All premium estimates are derived at ~50% implied volatility for September 2026 expiry (~6 months). Actual premiums should be verified with live options chain data via `bash tools/market-data.sh options AMD` before execution. At current IV levels:

| Option | Strike | Expiry | Estimated Premium | Source |
|--------|--------|--------|-------------------|--------|
| Call | $220 | Sep 2026 | ~$12-16/share | Black-Scholes at 50% IV [ESTIMATED] |
| Put | $165 | Sep 2026 | ~$8-12/share | Black-Scholes at 50% IV [ESTIMATED] |
| Call | $175 | Jan 2027 | ~$28-34/share | Black-Scholes at 50% IV [ESTIMATED] |
| Call | $230 | Jan 2027 | ~$12-16/share | Black-Scholes at 50% IV [ESTIMATED] |

### Correlation Estimates

| Pair | Estimated Correlation | Source |
|------|----------------------|--------|
| AMD–SPX | 0.70-0.75 | Risk Analyst [ESTIMATED] |
| AMD–QQQ | 0.80-0.85 | Risk Analyst [ESTIMATED] |
| AMD–SOX | 0.85-0.90 | Risk Analyst [ESTIMATED] |
| AMD–NVDA | 0.75-0.80 | Risk Analyst [ESTIMATED] |
| AMD–INTC | 0.35-0.45 | Sector overlap but diverging fundamentals [ESTIMATED] |

[DATA GAP: Correlation matrix tool generated script but could not execute (output directory not found). Estimates derived from Risk Analyst report and sector relationships. Verify with `python tools/portfolio-math.py correlation --tickers AMD,INTC --period 3y` before executing pair trade.]

---

## Data Gaps and Limitations

| Data Gap | Impact | Mitigation |
|----------|--------|------------|
| Options chain data not retrieved via tools | Premium estimates are modeled, not market-observed | Flagged all premiums as [ESTIMATED]; verify live before execution |
| Correlation matrix not computed | Pair trade hedge ratio is approximate | Used estimated correlations; verify before execution |
| INTC borrow cost not verified | Short leg cost could differ from estimate | INTC is liquid large-cap; borrow should be available |
| IV surface not available | Cannot verify put/call skew or term structure | Used flat ~50% IV assumption; actual skew may affect collar pricing |

---

*Trade Structure Memo by Trade Structurer, Equity Research Swarm. All options premiums are estimated and must be verified with live market data before execution. Data as of 2026-03-09.*

*Key Sources: Editor's Draft (2026-03-09), DCF Analyst, Risk Analyst, Technical Analyst, Devil's Advocate, Catalyst Analyst Pass 1 reports. Kelly-scenarios tool output (portfolio-math.py). Options estimates at ~50% IV.*
