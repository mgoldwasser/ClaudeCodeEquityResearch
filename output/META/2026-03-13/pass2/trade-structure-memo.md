# Trade Structure Memo — META Platforms (META)
## Date: 2026-03-13 | Prepared by: Trade Structurer

---

## Section 1: Thesis and Recommendation Summary

| Input | Value | Source |
|-------|-------|--------|
| Rating | Buy (Conviction 3/5 — Moderate) | Director |
| Base Case Fair Value | $725/share | DCF/Debate consensus |
| Probability-Weighted EV | $697–701/share | Post-debate reconciliation |
| Current Price | $638.18 | Market, 2026-03-13 |
| Expected Return to EV | +9.3% | Derived |
| Expected Return to Base FV | +13.6% | Derived |
| Conviction | 3/5 | Director (CapEx ROI unresolved) |
| Time Horizon | 9–12 months | Primary catalyst: Q1 earnings + Avocado |
| Key Near-Term Catalyst | Q1 2026 earnings (late April) | Catalyst Analyst |
| Key Medium-Term Catalyst | Avocado model release (H1 2026) | Catalyst Analyst |
| Key Risk | CapEx ROI failure (P = 15–35%; central 25%) | Disagreement Map |
| Beta | 1.25 | Risk & Contrarian |
| Annualized Volatility (est.) | ~35% | Technical Analyst (30–40% range) |
| Technical Score | 2.5/5 (death cross; Fibonacci support) | Technical Analyst |

**Return Distribution (left-skewed):**

| Scenario | Probability | Price | Return |
|----------|-------------|-------|--------|
| Bull | 23% | $1,050 | +64.5% |
| Base | 49% | $725 | +13.6% |
| Bear | 28% | $400 | -37.3% |
| **Probability-Weighted EV** | | **$709** | **+11.1%** |

`[NOTE: EV calculation uses resolved consensus prices $1,050/$725/$400; probability-weighted sum = $708.75, rounded to $709.]`

**Critical structural observation:** The return distribution is materially left-skewed. The bear case loss magnitude (-37.3%) exceeds the base case gain (+13.6%) by 2.7x. A pure long-equity position at current price requires either high conviction in avoiding the bear case, or explicit structure to limit downside. Conviction is 3/5 with a key unresolved risk — this argues decisively against unhedged long equity.

**Kelly Analysis (pre-hedge):**
- Probability of positive outcome (bull + base): 72%
- Probability-weighted average win: +29.9%
- Probability-weighted average loss: -37.3%
- Kelly fraction: **~18–20% of portfolio** (full Kelly: 37%; constrained to half-Kelly = 18.5%)
- Binding constraint: CapEx ROI uncertainty caps position size — this is a 3/5 conviction trade, not 4/5

---

## Section 2: Primary Trade Recommendation

**Trade Type: Long Equity (Structured Entry) with Protective Put Collar**

**Rationale:** The thesis is company-specific (META trades at 0.74x PEG vs. peer median 1.60x; 46% growth-adjusted discount to comps). The alpha source is genuine mispricing of the CapEx normalization trajectory, not a sector call — social advertising peers trade differently. However, the left-skewed distribution (-37.3% bear vs. +13.6% base) and unresolved CapEx ROI risk (15–35% failure probability) make unhedged long equity structurally unattractive at conviction 3/5. The collar eliminates tail exposure while preserving base case participation.

**Preferred Structure: Cash Equity Long + Protective Put (scaled)**

Scale into the position in two tranches rather than all at once, using the technical setup as the guide:

### Tranche 1 (50% of intended position) — Enter Now at Current Levels

| Parameter | Value |
|-----------|-------|
| Entry Price Range | $628–$642 (current zone; 50% Fibonacci support) |
| Tranche 1 Size | 50% of full intended position |
| Entry Rationale | Precisely at 50% Fibonacci retracement ($638.03); MACD and Momentum turned positive March 9–10 |
| Stop Loss (hard) | $589 (structural 2024 year-end support; -7.7% from entry) |
| Technical Invalidation | Daily close below $610 triggers review; below $589 triggers full stop |

### Tranche 2 (50% of intended position) — Wait for MA50 Breakout Confirmation

| Parameter | Value |
|-----------|-------|
| Trigger | Daily close above $657 (50-day MA) on volume > 20-day average |
| Entry Price Range | $655–$665 |
| Rationale | Volume-confirmed MA50 break validates institutional conviction returning; Technical Analyst's "conservative" entry threshold |
| Miss Risk | If META runs directly through $657 without pullback, enter at market; risk/reward still acceptable to $725 |

**Combined Long Equity Risk/Reward:**

| Parameter | Value |
|-----------|-------|
| Blended Entry | ~$638–$650 |
| Target Exit (base case) | $725 (+11.5–13.6%) |
| Target Exit (bull case) | $800–$900 (partial; hold remaining for $1,050 if thesis confirmed) |
| Hard Stop Loss | $589 (-7.7% to -9.2% from entry) |
| Max Loss (unhedged, hard stop) | -7.7% to -9.2% |
| Risk/Reward (to base $725) | 1:1.5 (tight stop) to 1:2.0 (full spread) |
| Time Horizon to Base Case | 9–12 months (Q1 earnings → Avocado → H2 monetization news) |

`[NOTE: Unhedged max loss assumes stop is executed. If stop fails in a gap-down event — the most likely bear case trigger (CapEx ROI shock or Chinese advertiser cliff) — actual loss approaches -37.3%. This is why put protection is essential for this specific risk profile.]`

---

## Section 3: Protective Put Overlay (Bear Case Insurance)

**Recommended: Buy $589 Put, January 2027 Expiry**

This is not optional at conviction 3/5 with a 28% bear probability that carries -37.3% downside. The put provides a floor at the technical invalidation level.

| Parameter | Value |
|-----------|-------|
| Put Strike | $589 (2024 year-end structural support; Technical Analyst's major support) |
| Expiry | January 2027 (~10 months) |
| Estimated Premium | ~$46/share (7.2% of stock price) `[ESTIMATED: BSM at 35% IV; verify against live chain]` |
| Protected From | Gap-down bear case: CapEx ROI shock, Chinese advertiser cliff ($7–23B), youth litigation adverse verdict |
| Floor Price (net of premium) | $589 - $46 = $543 (total downside from $638 entry: -14.9%) |
| Max Loss with Put | **-14.9%** (capped; replaces unbounded bear case -37.3%) |

**Why $589?** The Technical Analyst identifies $589 as the 2024 year-end structural support level — the break of this level signals structural breakdown, not just a cyclical pullback. Purchasing protection at this level creates a floor exactly where fundamental thesis invalidation begins.

**Why January 2027?** Covers all identifiable catalysts: Q1 earnings (April), Avocado release (H1), youth mental health trial (June), EU DMA decision (2026). If thesis is validated by Q3 2026 earnings, puts can be sold back with significant time value remaining.

**Put Cost Economics:**
- Annual cost: ~7.2% of position value
- Breakeven CapEx ROI failure probability needed to justify put cost: ~19% (put makes economic sense if P(bear) > 19%; consensus is 28%)
- At 28% bear probability with -37.3% bear return, expected bear case loss = 28% × 37.3% = 10.4% — put at 7.2% is **actuarially cheap**

---

## Section 4: Full Collar Structure (Alternative to Standalone Put)

For capital-constrained accounts or investors who want to reduce the put cost, pair the put with a covered call to create a zero-cost or low-cost collar.

**Collar: Buy $589P / Sell $720C, January 2027**

| Leg | Option | Strike | Expiry | Est. Premium | Direction |
|-----|--------|--------|--------|--------------|-----------|
| 1 | Put | $589 | Jan 2027 | ~$46/share | Buy (pay) |
| 2 | Call | $720 | Jan 2027 | ~$60/share | Sell (receive) |

| Risk Profile | Value |
|-------------|-------|
| Net Premium Received | ~$14/share (net credit) `[ESTIMATED]` |
| Effective Entry (net of credit) | $638 - $14 = $624 |
| Downside Floor | $589 (after credit: effective floor $603) |
| Upside Cap | $720 |
| Max Loss (collar) | $638 + $14 net credit - $589 floor = **-$25/share (-3.9%)** |
| Max Gain (collar) | $720 - $638 + $14 = **+$96/share (+15.0%)** |
| Risk/Reward | **1:3.8** |

**Collar Assessment:**
- Pros: Near-zero net cost, max loss -3.9%, risk/reward 1:3.8 to the cap
- Cons: $720 cap forfeits bull case upside above $720 (+64.5% in bull scenario foregone above $720)
- Verdict: **Prefer for investors with lower conviction or portfolio risk budget constraints.** The standalone put is preferred for investors who want full participation in the bull case (23% probability; $1,050 target)

`[NOTE: Covered call against long equity is NOT a naked call. No more than 2 legs total. Compliant with framework red lines.]`

---

## Section 5: Relative Value Trade — META Long / GOOGL Short

**This is the preferred structure for market-neutral investors or those concerned about broad tech selloff risk.**

### Rationale

META trades at a 23% P/E discount to GOOGL (21.1x vs. 27.5x) despite growing 138% faster (28.5% vs. 12%). PEG discount is 54% (0.74x vs. 2.29x median). The spread is not justified by CapEx compression risk alone — if CapEx normalizes per base case, META's NTM P/E should converge toward 27–28x within 12–18 months.

GOOGL is not a "short thesis" in isolation — it is the correct hedge because:
1. Highest correlation to META among peers (0.72) — removes market/sector beta effectively
2. GOOGL itself faces AI investment cycle uncertainty (similar CapEx narrative), but at a higher multiple — making it the right relative-value short if sector de-rates
3. Both companies compete directly for the same ad dollar pool — a META share gain (via Advantage+, Threads) is frequently a GOOGL share loss

### Pair Construction

| Leg | Ticker | Direction | Weight | Rationale |
|-----|--------|-----------|--------|-----------|
| Long | META | Buy | 100% | Primary thesis: PEG discount, CapEx normalization, Advantage+ ROI |
| Short | GOOGL | Sell | 82% | Hedge: Beta-adjusted, highest correlation (0.72), relative overvaluation |

**Hedge Ratio Calculation:**
```
Hedge Weight = META Beta × Correlation(META,GOOGL) / GOOGL Beta
             = 1.25 × 0.72 / 1.10
             = 0.82 (82% of long notional)
```

| Pair Metric | Value |
|-------------|-------|
| Net Exposure | 18% (long weight - short weight) |
| Gross Exposure | 182% (100% long + 82% short) |
| Pair Correlation (META/GOOGL) | 0.72 (3-year estimate; source: industry knowledge) |
| Residual Pair Beta | ~0.46 (materially below market) |
| Expected Pair Return | +11–14% (base case P/E convergence) |
| Expected Pair Return (EV-weighted) | ~+9% |
| Max Pair Loss (estimate) | -15% (if META de-rates while GOOGL outperforms — governance shock scenario) |

**Pair Risk/Reward:**
- Target: META P/E expands from 21.1x to 25–27x as CapEx normalization visible; GOOGL holds or contracts. +6–8x P/E expansion on $30 EPS = +$180–240/share gain META; GOOGL short neutral/positive.
- Stop: META closes below $589 AND GOOGL holds above $180 (structural divergence signals company-specific failure, not sector event)
- Timeline: 9–12 months (CapEx normalization evidence Q2–Q3 2026 earnings)

**Why NOT SNAP or PINS as the short?**
SNAP (0.55 correlation) and PINS (0.50 correlation) are too loosely correlated to META to function as effective beta hedges. Low correlation pairs provide poor sector hedges — they introduce basis risk that can generate losses even when the long leg performs correctly. GOOGL's 0.72 correlation is the right hedge instrument.

---

## Section 6: Sector Hedge (Standalone — For Long-Only Investors)

If the investor cannot execute the long-short pair (restrictions, borrow cost), hedge META-specific sector beta via a broad tech ETF.

**Note on XLC (Communication Services) ETF:** META constitutes ~21% of XLC — purchasing protection via XLC creates circular exposure (META effectively hedging itself through XLC). **XLC is NOT a suitable sector hedge for META.**

**Recommended: Short XLK (Technology Select Sector ETF) as partial hedge**

| Hedge Vehicle | Ticker | Direction | Weight | Est. Annual Borrow Cost |
|---------------|--------|-----------|--------|------------------------|
| Tech Sector ETF | XLK | Short | 85% of long position | ~0.1% annualized (liquid) |

**Hedge Ratio Calculation:**
```
Hedge Weight = META Beta × Correlation(META,XLK) / XLK Beta
             = 1.25 × 0.75 / 1.10
             = 85%
```

**Residual Exposure After Hedge:**
- Market beta: ~0.25 (residual; captures only company-specific risk)
- Sector exposure: ~15% (incomplete hedge by design; avoids over-hedging)
- Company-specific alpha preserved: Yes — the META/CapEx normalization thesis is idiosyncratic

**Sector hedge cost:** XLK borrow is cheap (~10 bps/year); primary cost is opportunity cost if broad tech rallies. This is a full thesis hedge, not a partial position — use only if conviction 2/5 or below.

---

## Section 7: Options Overlay for Q1 Earnings Catalyst

**Catalyst:** Q1 2026 earnings (late April 2026; ~45 days from 2026-03-13)
**Catalyst probability:** 75% upside beat probability (Catalyst Analyst; conservative guidance track record)
**Options rationale:** Known date, asymmetric payoff desired, limits downside if miss on CapEx guidance

`[NOTE: Options chain not directly available. Premium estimates derived from BSM approximation at 35% annualized IV (midpoint of Technical Analyst's 30–40% estimate). Verify against live chain before execution. IV may differ materially — especially into earnings, where IV typically expands 5–15 points.]`

**Recommended Options Structure: Bull Call Spread (Earnings Play)**

**Strategy: Buy $640 Call / Sell $700 Call, ~45-day expiry (targeting April 2026 earnings)**

| Leg | Option | Strike | Expiry | Est. Premium | Delta (approx.) |
|-----|--------|--------|--------|--------------|-----------------|
| 1 (buy) | Call | $640 | Late April 2026 | ~$32/share | ~0.52 |
| 2 (sell) | Call | $700 | Late April 2026 | ~$12/share | ~0.30 |

| Risk Profile | Value |
|-------------|-------|
| Net Debit | ~$20/share (3.1% of stock price) `[ESTIMATED]` |
| Max Gain | ~$40/share (if META > $700 at expiry) |
| Max Loss | ~$20/share (premium paid; 100% of debit) |
| Breakeven | ~$660 (+3.4% from current) |
| Risk/Reward | **2.0:1** |
| Days to Expiry | ~45 days |
| IV Expansion Risk (into earnings) | IV likely expands 5–15 pts before earnings — buy early or after IV normalizes post-print |

**Why a spread (not naked call)?** A bull call spread captures the earnings move (guidance beat to $700 is plausible; 75% upside prob × median beat ~$5–8B = stock to $660–680 minimum) while containing max loss to premium paid. Naked calls at 35%+ IV carry excessive theta decay over 45 days. The $700 cap is appropriate — this trade is sized for the earnings event, not the full thesis.

**Integration with primary trade:**
- If primary long equity position already established: this spread adds leveraged exposure to Q1 catalyst specifically
- If position not yet established: use this spread as a "low cost of entry" before tranche 1 equity purchase

**Why NOT a straddle?** The asymmetric catalyst probability (75% upside vs. 25% downside) argues against paying for symmetric volatility. A straddle would require a +/-5% move just to break even — appropriate only if outcome is genuinely binary. A bull call spread is the right expression of directional asymmetry.

---

## Section 8: Alternative Structures

### Alternative A: LEAPS Bull Call Spread (Lower Capital at Risk, Full Thesis Horizon)

**Structure: Buy $640C / Sell $800C, January 2027 (~10 months)**

| Parameter | Value |
|-----------|-------|
| Net Debit | ~$53/share (~8.3% of stock price) `[ESTIMATED]` |
| Max Gain | ~$107/share (at $800; 2.0:1 R/R) |
| Breakeven | ~$693 (+8.6% from current) |
| Max Loss | $53/share (options premium only; 8.3% vs. 9.2% stop loss on equity) |
| Upside Cap | $800 (captures most of base case + lower bull scenario) |
| Timeline | 10 months |

**Pros:** Defined max loss (8.3%); participates in full thesis timeline; no stop-loss management required
**Cons:** $800 cap foregoes bull case upside $800–$1,050; no dividend participation; requires 8.6% move to break even; loses full premium if META at $639 at January 2027 expiry
**Best for:** Investors who want to limit capital at risk to less than the equity stop loss but still participate in the multi-catalyst thesis horizon

---

### Alternative B: Long Only (No Hedge) for High-Conviction Accounts

**For accounts with explicit constraints on options or short selling:**

| Parameter | Value |
|-----------|-------|
| Entry | $628–$642 (current zone; aggressive) or $655–$665 (MA50 breakout; conservative) |
| Full Position Size | Based on Director / Position Sizing Analyst's recommendation |
| Stop Loss | $589 (-7.7% from aggressive entry; -9.8% from conservative) |
| Target | $725 base / $1,050 bull |
| Max Loss (if stop honored) | -7.7% to -9.8% |
| Max Loss (if stop fails on gap down) | Up to -37.3% (bear case) |
| Risk/Reward (to base FV) | 1:1.8 (conservative entry) |

**Critical caveat:** At conviction 3/5 with 28% bear probability carrying -37.3% tail, unhedged long equity is NOT the recommended primary structure. This alternative is only appropriate for accounts where: (a) position size is limited to 2–3% of portfolio (self-hedged via position sizing), or (b) options/short selling are unavailable.

---

### Alternative C: Minimal Starter Position, Wait for Catalyst Confirmation

**For investors who want to establish a beachhead but maintain optionality:**

| Parameter | Value |
|-----------|-------|
| Initial Size | 25–33% of full intended position |
| Entry | $628–$642 (current) |
| Trigger to Add | Q1 earnings beat with CapEx guidance maintained (late April) |
| Trigger to Add Further | Avocado strong reception OR CapEx ROI evidence (H1 2026) |
| Risk | Missing the run if catalyst hits before full position established |
| Reward | Preserves dry powder for adding at better price (e.g., $589–$610 dip) or confirmed thesis |

**Best for:** Fund managers with position sizing constraints or tracking-error budget concerns who cannot tolerate the full position before the April earnings catalyst.

---

## Section 9: Implementation Notes

| Parameter | Recommendation |
|-----------|---------------|
| Entry Timing — Tranche 1 | Immediate ($628–$642 zone) — Fibonacci support is NOW; delay risks missing the entry |
| Entry Timing — Tranche 2 | Wait for $657 MA50 break with volume confirmation |
| Position Building | 50%/50% tranche plan (described above); do NOT all-in at current levels given death cross |
| Protective Put Timing | Purchase simultaneously with Tranche 1; do NOT defer — bear case risks are live (April earnings, June trial) |
| Options IV Timing | For earnings spread: buy BEFORE IV expansion (2–3 weeks before earnings); selling post-expansion is too expensive |
| Collar Call Sale Timing | If using collar: sell the $720 call AFTER the next rally leg (above $657 MA50); sell into strength |
| Rebalancing | Threshold-based: if META runs >30% from entry, consider trimming Tranche 2 and rolling protection |
| Exit Trigger (profit — base case) | $725 (base case FV) — exit 50% of position; hold remaining for potential bull case |
| Exit Trigger (profit — bull case) | $900–$1,000; reassess thesis against actual CapEx ROI data at that point |
| Exit Trigger (loss — primary) | Daily close below $589 with volume; execute without delay |
| Exit Trigger (loss — secondary) | Management raises CapEx guidance above $135B without commensurate revenue evidence — thesis deterioration, not price stop |
| Catalyst-Driven Exit | Youth mental health adverse verdict ($2–15B fine) — reduce 50% immediately pending settlement terms |
| Estimated Transaction Costs | 5–10 bps round-trip (equity; high liquidity); 20–30 bps options (bid-ask spread at these strikes and expirations) |
| Estimated Carry Cost | 0% (long equity); options time decay per structure above |
| Borrow Cost (GOOGL short leg) | ~0.1–0.25% annualized (large cap; ample borrow) |
| Monitoring Cadence | Weekly review of CapEx tracking signals; real-time on earnings and regulatory developments |

**Key Monitoring Checklist (per Catalyst Analyst):**
1. **Q1 2026 earnings (late April):** Revenue vs. $55B midpoint; CapEx guidance maintained vs. revised upward; any Meta AI monetization revenue disclosure
2. **Avocado release reception:** Benchmark reception vs. OpenAI/Google frontier — if strong, upgrade bull probability
3. **Youth mental health trial (June 2026):** Track pretrial motions for settlement signals (settlement = -2–5% vs. adverse verdict = -8–15%)
4. **CapEx quarterly tracking:** Actual quarterly spend vs. $28–34B/quarter implied by $115–135B annual guidance

---

## Section 10: One-Paragraph Trade Summary

The recommended trade is a two-tranche long equity position in META (50% at current $628–$642; 50% on MA50 breakout at $655–$665), paired with a protective $589 put expiring January 2027 (estimated cost ~$46/share, 7.2% of position) as the primary structure. The put converts an unbounded bear case loss of -37.3% into a defined max loss of approximately **-14.9%** from entry — appropriate for conviction 3/5 with a 28% bear probability whose key risks (CapEx ROI failure, Chinese advertiser cliff, youth litigation) are all capable of gap-down events that would defeat a stop-loss order. For market-neutral accounts, the preferred alternative is a **META long / GOOGL short** pair (100% long / 82% short, adjusted for beta and correlation), targeting P/E convergence over 9–12 months with an estimated max pair loss of -15% in a META-specific failure scenario. An earnings-specific bull call spread ($640/$700, April 2026 expiry; ~$20 net debit; 2.0:1 R/R) can be layered on top of either structure to capture the Q1 earnings catalyst with defined risk. Max loss on the primary structure is **-14.9%** (put-floored) or **-7.7%** (hard stop, no put). Risk/reward to base case fair value ($725): approximately **1:1.9** (protected structure). The single most important entry trigger is Q1 earnings (late April): a beat with maintained CapEx guidance is the most near-term validation event and likely causes the stock to recapture the 50-day MA, upgrading the technical score and enabling Tranche 2 addition.

---

*Trade Structure Memo | META / 2026-03-13*
*Options premiums are BSM approximations at 35% IV; verify against live options chain before execution*
*Correlations estimated from industry knowledge; run `output/models/correlation-matrix.py` for empirical verification*
*SIGNAL-IDs referenced: TECH-FIBONACCI-INFLECTION, TECH-DEATH-CROSS-CONFIRMED, RISK-CAPEX-ROI-STRANDED, RISK-CHINESE-ADVERTISER-CLIFF, CAT-001 Q1-EARNINGS-BEAT, QUANT-PEG-UNDERVALUED*
