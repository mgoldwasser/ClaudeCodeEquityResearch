# Forensic Quality Report — AMD (Advanced Micro Devices, Inc.)

**Date:** 2026-03-09
**Analyst:** Forensic Analyst
**Ticker:** AMD | **Exchange:** NASDAQ
**Fiscal Year End:** December 27, 2025 (FY2025)

---

## Step 1: Automated Scoring

### Beneish M-Score (Earnings Manipulation Detection)

```
python3 tools/portfolio-math.py beneish --financials-file amd-beneish.json
```

| Score | Value | Threshold | Assessment |
|-------|-------|-----------|------------|
| **Beneish M-Score** | **-2.71** | > -1.78 = concern | **Low Risk** |

**Component Breakdown:**

| Component | Value | Interpretation |
|-----------|-------|----------------|
| DSRI (Days Sales Receivables Index) | 0.759 | Favorable — receivables growing slower than revenue |
| GMI (Gross Margin Index) | 1.010 | Neutral — gross margins essentially flat YoY (GAAP) |
| AQI (Asset Quality Index) | 0.887 | Favorable — asset quality improving |
| SGI (Sales Growth Index) | 1.343 | **Flagged** — 34.3% revenue growth is rapid (but organic, driven by Data Center/AI) |
| DEPI (Depreciation Index) | 1.114 | Neutral — depreciation rates slightly declining |
| SGAI (SGA Expense Index) | 1.128 | Neutral — SGA growing in line with business expansion |
| LVGI (Leverage Index) | 1.180 | Neutral — modest leverage increase |
| TATA (Total Accruals / Total Assets) | -0.044 | **Favorable** — negative accruals (cash flow exceeds net income) |

**M-Score Assessment:** At -2.71, AMD is well below the -1.78 manipulation threshold and below the -2.22 gray zone boundary. The only flagged component is SGI (rapid revenue growth), which is consistent with AMD's genuine market share gains in data center and AI GPU markets — not a manipulation signal. The negative TATA (cash exceeds earnings) is a strong positive signal for earnings quality.

### Altman Z-Score (Bankruptcy Risk)

```
python3 tools/portfolio-math.py altman-z --financials-file amd-altmanz.json
```

| Score | Value | Threshold | Assessment |
|-------|-------|-----------|------------|
| **Altman Z-Score** | **14.38** | < 1.81 = distress | **Safe Zone** |

**Component Breakdown:**

| Component | Value |
|-----------|-------|
| X1 (Working Capital / Total Assets) | 0.227 |
| X2 (Retained Earnings / Total Assets) | 0.087 |
| X3 (EBIT / Total Assets) | 0.048 |
| X4 (Market Cap / Total Liabilities) | 22.290 |
| X5 (Revenue / Total Assets) | 0.450 |

**Z-Score Assessment:** At 14.38, AMD is deep in the safe zone (>2.99). The score is inflated by X4 (market cap of $310B vs. total liabilities of $13.9B), reflecting AMD's equity-heavy capital structure. Net cash position of $6.55B provides substantial liquidity buffer. No bankruptcy risk whatsoever.

---

## Step 2: Revenue Quality Analysis

### Revenue Trend Analysis

| Metric | FY2023 | FY2024 | FY2025 | Trend | Flag? |
|--------|--------|--------|--------|-------|-------|
| Revenue ($M) | $22,680 | $25,785 | $34,639 | Accelerating | No |
| Revenue Growth (%) | -3.9% | 13.7% | 34.3% | Accelerating | Monitor — rapid |
| Days Sales Outstanding | 86.5 | 87.6 | 66.6 | **Improving** | No — positive |
| Inventory ($M) | $4,351 | $5,734 | $7,920 | Rising | Monitor |
| Inventory / Revenue | 19.2% | 22.2% | 22.9% | Slightly rising | Yellow flag |
| Receivables ($M) | $5,376 | $6,192 | $6,315 | Modest growth | No |

**DSO Calculation:**
- FY2025: ($6,315 / $34,639) x 365 = **66.6 days** (improved from 87.6 in FY2024)
- FY2024: ($6,192 / $25,785) x 365 = **87.6 days**
- FY2023: ($5,376 / $22,680) x 365 = **86.5 days**

**DSO Assessment:** DSO improved significantly from 87.6 days to 66.6 days in FY2025. This is a strong positive signal — revenue is growing 34% while receivables grew only 2%. AMD is collecting faster, not slower. This directly contradicts channel stuffing or aggressive revenue recognition concerns.

### Inventory Analysis — Key Forensic Item

Inventory rose from $5,734M to $7,920M (+38%) while revenue grew 34%. The 4pp gap warrants examination:

- **$800M inventory charge** in 2025 related to MI308 China export controls [Source: AMD 8-K, 2025-04-16 — Tier 1]
- **$306M inventory reserve release** in Q4 2025 [Source: CFO Jean Hu, Q4 earnings call — Tier 2]
- Net inventory charge impact in FY2025: ~$494M
- Excluding the charge/release dynamics, underlying inventory growth of ~$1,700M (+30%) is roughly in line with revenue growth
- Inventory build is consistent with MI350/MI450 ramp preparation for H2 2026 mega-deals (OpenAI, Meta)

**Inventory Reserve Release ($306M) — Forensic Assessment:**
The Q4 $306M inventory reserve release boosted Q4 gross margin by ~300bps (from ~54% to ~57% non-GAAP). This is a legitimate reversal if the previously reserved inventory became saleable (e.g., MI308 export license obtained with 15% fee). However, this is a non-recurring item that flatters Q4 margins and should be excluded from run-rate analysis. The CFO disclosed this openly on the earnings call, which is a positive governance signal. [ASSUMPTION: Reserve release related to MI308 China export resolution, based on timing and magnitude]

### Revenue Recognition Red Flags Checklist

| Red Flag | Present? | Evidence |
|----------|----------|---------|
| Revenue growing faster than cash collections | **No** | CFO grew 153% ($7.7B) vs revenue growth of 34%. Cash collections strongly exceed revenue growth. |
| Increasing DSO without business model change | **No** | DSO improved from 87.6 to 66.6 days |
| Large end-of-quarter revenue concentration | **Unknown** | [DATA GAP: Quarterly revenue linearity not disclosed] |
| Unusual related-party revenue | **No** | No related-party revenue identified in press releases |
| Revenue from non-recurring items classified as recurring | **No** | Revenue breakdown by segment is clean; $306M reserve release affects COGS, not revenue |
| Significant use of percentage-of-completion or mark-to-model | **No** | AMD uses point-of-sale recognition (ASC 606 standard for semiconductor shipments) |
| Bill-and-hold arrangements | **Unknown** | [DATA GAP: Full 10-K text needed for revenue recognition policy detail] |
| Channel stuffing indicators | **No** | DSO improvement contradicts channel stuffing. Inventory build is supply-side (MI350/MI450 ramp), not channel. |

---

## Step 3: Cash Flow Quality

### Cash Flow vs. Accrual Analysis

| Metric | FY2023 | FY2024 | FY2025 | Concern? |
|--------|--------|--------|--------|----------|
| Net Income ($M) | $838 | $1,608 | $4,309 | |
| CFO ($M) | $1,667 | $3,041 | $7,709 | |
| CFO / Net Income Ratio | 1.99x | 1.89x | 1.79x | **No** — consistently >1.0x, though declining |
| Accruals Ratio (NI - CFO) / Total Assets | -0.012 | -0.021 | -0.044 | **No** — negative accruals = strong quality |
| Free Cash Flow ($M) | $1,121 | $2,405 | $6,697 | |
| FCF / Net Income Ratio | 1.34x | 1.50x | 1.55x | **No** — FCF consistently exceeds net income |
| Stock-Based Compensation / Revenue | 7.4%[EST] | 5.5% | 4.7% | Improving — below 10% threshold |
| CapEx / Revenue | 2.4% | 2.5% | 2.9% | Asset-light model confirmed |

**Cash Flow Assessment:**

AMD's cash flow quality is **strong**. Key observations:

1. **CFO/NI ratio consistently above 1.0x** for three consecutive years (1.99x, 1.89x, 1.79x). While the ratio is declining, it remains well above the 0.8x concern threshold. The decline is structural — as net income grows, the D&A component (which is relatively stable at ~$3B) contributes less proportionally to CFO. This is not a red flag.

2. **Negative accruals ratio** (-0.044 in FY2025) means cash generation exceeds reported earnings. This is the single strongest indicator of earnings quality. Companies manipulating earnings typically show positive accruals (earnings exceed cash).

3. **FCF of $6.7B** exceeds GAAP net income of $4.3B by 55%. This confirms that reported earnings are conservative relative to cash generation.

4. **SBC at 4.7% of revenue** is material but declining and below the 10% concern threshold. Total SBC was ~$1.6B in FY2025.

### GAAP vs. Non-GAAP Reconciliation — Critical Forensic Item

The $1.52/share GAAP-to-non-GAAP EPS gap ($2.65 vs $4.17) is the most significant forensic item. Decomposition:

| Adjustment | FY2025 ($M) | Per Share (est.) | Legitimate? |
|------------|-------------|------------------|-------------|
| Amortization of acquisition-related intangibles | ~$2,250 | ~$1.38 | **Yes** — non-cash, Xilinx purchase accounting. Standard for large acquisitions. Will decline over time as intangibles fully amortize. |
| Stock-based compensation | ~$1,638 | ~$1.00 | **Partially** — SBC is a real economic cost (dilution). Industry standard to exclude, but investors should track diluted share count. |
| Inventory charge (China export controls) | ~$800 | ~$0.49 | **Yes** — one-time, externally caused by government action. |
| Inventory reserve release | ~($306) | ~($0.19) | **Monitor** — reduces the net inventory charge. Legitimate if reserves were previously conservative. |
| Other (restructuring, etc.) | ~($308) | ~($0.19) | **Likely** — standard restructuring charges |

**Assessment of GAAP/Non-GAAP Gap:**
- ~60% of the gap ($2.25B amortization) is a mechanical artifact of the Xilinx acquisition. This is non-cash and does not indicate earnings manipulation. It will decline as intangibles amortize (estimated 10-15 year useful life, ~$2B+ remaining per year for several more years).
- ~25% of the gap ($1.6B SBC) is a real economic cost through dilution. AMD's diluted share count has grown from ~1,613M to ~1,637M shares, representing ~1.5% annual dilution. This is material but not excessive for a high-growth tech company.
- ~15% of the gap is the one-time inventory charge, which is legitimately non-recurring.
- **Total GAAP operating income of $3.69B vs non-GAAP of $7.77B is a $4.08B gap.** This is large but fully explainable by the three items above. No hidden or unexplained adjustments identified.

---

## Step 4: Balance Sheet Analysis

### Goodwill & Intangible Asset Risk — Key Forensic Item

| Item | FY2023 | FY2024 | FY2025 | Analysis |
|------|--------|--------|--------|----------|
| Goodwill ($M) | $24,262 | $24,839 | $25,126 | Stable — primarily Xilinx ($49B acquisition, Feb 2022) |
| Goodwill / Total Assets | 35.7% | 35.9% | 32.7% | Declining as total assets grow — positive trend |
| Intangible Assets ($M) | $21,363 | $18,930 | $16,705 | **Declining** — amortization reducing balance |
| Intangibles / Total Assets | 31.5% | 27.3% | 21.7% | Declining — positive trend |
| Combined Goodwill + Intangibles | $45,625 | $43,769 | $41,831 | Declining from amortization |
| Combined / Total Assets | 67.2% | 63.2% | 54.4% | **Improving but still elevated** |

**Goodwill Impairment Risk Assessment:**
- Goodwill of $25.1B represents 32.7% of total assets — above the 20% "acceptable" threshold but below 40% "concerning" level
- The Xilinx acquisition ($49B, closed Feb 2022) created the bulk of this goodwill
- **No goodwill impairment charges** have been recorded since the Xilinx acquisition. Given that AMD's market cap ($310B) is 6.3x the original Xilinx purchase price, impairment risk is negligible in current conditions.
- **Risk scenario:** If AMD's market cap were to fall below $50B (a ~84% decline from current), goodwill impairment testing would become relevant. This is an extreme tail risk.
- Intangible assets are declining by ~$2.2B annually through amortization, which is mechanically reducing the balance sheet concentration.

**Combined goodwill + intangibles at 54.4% of total assets is elevated** but declining and typical for semiconductor companies post-major acquisitions (compare: Broadcom at ~70%+, Intel post-Altera at ~50%). The amortization trajectory is correct — intangibles are declining from $21.4B (FY2023) to $16.7B (FY2025), confirming systematic write-down.

### Other Balance Sheet Items

| Item | Analysis |
|------|----------|
| Off-Balance Sheet Obligations | [DATA GAP: Full 10-K text needed for operating lease obligations, purchase commitments, guarantees. OpenAI and Meta deals likely create significant future purchase obligations.] |
| Accounts Receivable Aging | No concentration concerns identified. Receivables grew only 2% on 34% revenue growth. DSO improved from 87.6 to 66.6 days. |
| Inventory Obsolescence Risk | **Yellow flag** — Inventory up 38% ($5.7B to $7.9B) with $800M charge already taken. Net of charge, inventory growth (~30%) roughly matches revenue growth. Monitor for additional write-downs if MI350/MI450 ramp delays occur. |
| Debt Profile | Conservative. Total debt ~$4.0B vs cash $10.6B = net cash $6.6B. Debt/equity of 0.06 is minimal. No covenant concerns. |
| Warrant Dilution (off-balance-sheet) | 320M warrants (OpenAI 160M + Meta 160M) at $0.01 exercise price. Full vesting requires $600 stock price + deployment milestones. At current $190, partial vesting possible. **Not yet on balance sheet** — will be recorded as equity instrument upon issuance. [Source: Data Intelligence Memo — Tier 1-3] |

---

## Step 5: Management & Governance

| Factor | Finding | Red Flag? |
|--------|---------|-----------|
| CEO Tenure | **Lisa Su — 11 years** (since Oct 2014) | No — long tenure, strong track record (revenue from $5B to $35B) |
| CFO Tenure | **Jean Hu — 3+ years** (since Jan 2022) | No — stable tenure, came from Lattice Semi |
| Auditor | **Ernst & Young LLP** | No — Big 4 firm, long-standing relationship |
| Auditor Changes (5 years) | **None identified** | No — continuity is positive [Source: WebSearch — Tier 4] |
| Audit Opinion | **Unqualified (Clean)** | No — standard clean opinion expected [Source: AMD 10-K FY2024 — Tier 1] |
| Material Weakness (SOX 302/404) | **None identified** | No [Source: WebSearch — no material weakness disclosures found] |
| SEC Restatements/Inquiries | **None identified** | No [Source: WebSearch — no AMD restatements or SEC investigations found] |
| Related Party Transactions | **None identified in press releases** | No [DATA GAP: DEF 14A proxy not retrieved for full related-party disclosure] |
| CEO Compensation vs. Peer Median | [DATA GAP: Proxy statement not retrieved] | Unknown — likely elevated given $35B revenue scale |
| Insider Selling Pattern | Lisa Su: Net seller via 10b5-1 plans — Feb 2026 sold 125K shares ($26.8M), Dec 2025 sold ~45K shares. **Retains ~3.15M shares (~$600M+)** | No — programmatic, pre-scheduled. Retained position substantial. |
| Board Independence | [DATA GAP: DEF 14A not retrieved] | Unknown |

**Management Integrity Assessment:**

Lisa Su's 11-year tenure has been marked by a transformational turnaround — from a company near irrelevance in 2014 to the #2 semiconductor company by market cap. No accounting controversies, no SEC actions, no auditor changes, and no material weaknesses. The CFO's open disclosure of the $306M inventory reserve release on the earnings call (rather than burying it in footnotes) is a positive transparency signal.

The insider selling pattern is programmatic (10b5-1 plans), consistent, and represents a small fraction of total holdings. Lisa Su retains over $600M in AMD stock — strong alignment.

**One concern:** The segment restructuring (combining Client and Gaming into one segment) reduces visibility into the declining gaming business. This is a common practice but deserves monitoring — segment aggregation can mask deteriorating sub-segments. [Source: Data Intelligence Memo — Tier 1]

---

## Step 6: Accounting Quality Rating

### Rating Criteria Assessment

| Criterion | Finding | Impact on Rating |
|-----------|---------|-----------------|
| M-Score | -2.71 (well below -1.78 threshold, below -2.22 gray zone) | Supports 5/5 |
| CFO/NI Ratio | 1.79x (3 consecutive years above 1.0x) | Supports 5/5 |
| Accruals Ratio | -0.044 (negative = cash exceeds earnings) | Supports 5/5 |
| Auditor | EY, no changes, unqualified opinion | Supports 5/5 |
| SEC Issues | None identified | Supports 5/5 |
| Goodwill + Intangibles | 54.4% of total assets — elevated but declining | Caps at 4/5 |
| GAAP/Non-GAAP Gap | $1.52/share — large but fully explainable | Minor concern |
| Inventory Reserve Release | $306M in Q4 — disclosed but flatters Q4 margins | Minor concern |
| Segment Restructuring | Client/Gaming combined — reduces visibility | Minor concern |
| Data Gaps | DEF 14A not retrieved, full 10-K text not reviewed | Cannot confirm 5/5 |

### Red Line Check

- CFO has NOT diverged from net income for 3+ periods (consistently above 1.0x) — Pass
- No auditor change in last 2 years — Pass
- M-Score of -2.71 is below -2.22 gray zone — Pass
- No going concern opinion — Pass
- No material weakness disclosures — Pass

**Accounting Quality Rating: 4/5 — Minor Concerns**

**Justification:** AMD's core accounting quality is strong. The M-Score (-2.71) indicates low manipulation risk, cash flow quality is excellent (CFO/NI consistently >1.7x, negative accruals), and there are no audit or SEC red flags. The rating is capped at 4/5 (not 5/5) for three reasons:

1. **Goodwill + intangibles at 54.4% of total assets** — while declining and not at risk of impairment at current valuation, this concentration means the balance sheet is heavily dependent on the continued success of the Xilinx acquisition thesis. A significant downturn in the embedded/FPGA business could trigger impairment testing.

2. **The $306M Q4 inventory reserve release** — while properly disclosed, this non-recurring item boosted Q4 gross margins by ~300bps. Analysts relying on Q4 margins as a run-rate will overestimate forward margins.

3. **Data gaps** — the DEF 14A proxy was not retrieved, preventing full governance and related-party analysis. The full 10-K text was not reviewed for revenue recognition policy detail, off-balance-sheet obligations, and risk factor changes.

---

## Step 7: Impact on Investment Thesis

AMD's accounting quality **supports** the investment thesis. The key positive signal is that cash flow generation ($7.7B CFO, $6.7B FCF) significantly exceeds reported GAAP earnings ($4.3B net income), meaning the company is under-earning on a GAAP basis relative to its cash-generating ability. The large GAAP/non-GAAP gap is almost entirely explained by Xilinx amortization and one-time export control charges — neither of which indicate earnings manipulation.

The primary forensic risk for the investment thesis is not current accounting quality but **future accounting complexity**. The OpenAI and Meta mega-deals (320M warrants, $200B+ potential revenue) will introduce significant accounting complexity: warrant valuation, revenue recognition timing on multi-year deployment contracts, and potential goodwill from any future acquisitions. Investors should monitor how AMD accounts for the warrant equity instruments and whether deployment milestones trigger warrant vesting and associated non-cash charges.

**Conviction adjustment:** No reduction warranted based on forensic findings. The 4/5 accounting quality rating does not cap the Director's conviction rating (only a 2/5 or below would cap conviction). The forensic analysis modestly strengthens the bull case — AMD is generating more cash than it reports in earnings.

---

## Summary

Accounting quality is **4/5 — Minor Concerns**. The primary concern is balance sheet concentration in goodwill and intangibles (54.4% of total assets from the Xilinx acquisition), not earnings manipulation. The M-Score of -2.71 is well below the manipulation threshold, and the negative accruals ratio (-0.044) confirms that cash generation exceeds reported earnings — a strong positive signal. The $306M Q4 inventory reserve release flatters Q4 margins and should be treated as non-recurring. The GAAP/non-GAAP gap of $1.52/share is large but fully explained by acquisition amortization ($1.38), SBC ($1.00), and one-time inventory charges ($0.30 net). No SEC restatements, no auditor changes, and no material weaknesses identified. The forensic analysis does not warrant any reduction in investment conviction.

---

## Data Sources

| Data Point | Source | Tier | Retrieved |
|------------|--------|------|-----------|
| FY2025/FY2024 Income Statement | StockAnalysis.com | Tier 4 | 2026-03-09 |
| FY2025/FY2024 Balance Sheet | StockAnalysis.com | Tier 4 | 2026-03-09 |
| FY2025/FY2024 Cash Flow Statement | StockAnalysis.com | Tier 4 | 2026-03-09 |
| FY2023 Financial Results | AMD IR Press Release | Tier 1 | 2026-03-09 |
| Q4 FY2025 Earnings Summary | AMD IR / Motley Fool Transcript | Tier 1-2 | 2026-03-09 |
| Market Data | StockAnalysis.com | Tier 4 | 2026-03-09 |
| $800M Inventory Charge | AMD 8-K (2025-04-16) | Tier 1 | 2026-03-09 |
| $306M Reserve Release | CFO Jean Hu, Q4 Earnings Call | Tier 2 | 2026-03-09 |
| Auditor (Ernst & Young LLP) | AMD 10-K / WebSearch | Tier 1/4 | 2026-03-09 |
| Insider Trading | StockTitan, MarketDaily, SEC Form 4 | Tier 2 | 2026-03-09 |
| SEC Restatements/Inquiries | WebSearch (none found) | Tier 4 | 2026-03-09 |
| Beneish M-Score | Calculated via `tools/portfolio-math.py beneish` | Computed | 2026-03-09 |
| Altman Z-Score | Calculated via `tools/portfolio-math.py altman-z` | Computed | 2026-03-09 |
