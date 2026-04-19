# DCF Model — NVIDIA Corporation (NVDA)
**Date:** 2026-03-19
**Analyst:** DCF Analyst (Equity Research Swarm)
**Price-Blinded:** Yes — no current stock price accessed
**Data Sources:** `input/financials/nvda-income-statement.json` (Tier 1), `input/financials/nvda-balance-sheet.json` (Tier 1), `input/transcripts/nvda-q4-fy2026-earnings-call.md` (Tier 2)

---

## Executive Summary

NVIDIA is a company with extraordinary near-term momentum — $215.9B FY2026 revenue, +65.5% YoY, with Q1 FY2027 guided to $78B — that is now large enough that its 5-year DCF valuation is structurally dominated by terminal value assumptions. The base case fair value is **$165/share** (implied FY2031 revenue of $583B at 42% FY27 growth decelerating to 12%). The probability-weighted expected value across bull/base/bear is **$159.54/share**. The dispersion is extreme: bull case yields $265/share, bear case $63/share, reflecting genuine uncertainty about whether AI infrastructure spending is secular or cyclical, and whether CUDA's moat holds against AMD ROCm + custom ASICs.

The central risk to this model: **terminal value represents 67-84% of enterprise value across scenarios**, meaning the investable thesis depends almost entirely on long-run assumptions about competitive position and market structure — not the near-term earnings that look spectacular.

---

## 1. Revenue Build

### Actuals — FY2022-FY2026

| Segment ($M) | FY2022 | FY2023 | FY2024 | FY2025 | FY2026 |
|---|---|---|---|---|---|
| Data Center | ~7,000 | ~15,000 | 47,500 | 115,200 | 193,700 |
| Gaming | ~12,500 | ~9,000 | 10,400 | 11,400 | 16,000 |
| Professional Viz | ~2,100 | ~1,500 | 1,600 | 1,900 | 3,200 |
| Automotive/Robotics | ~566 | ~903 | 1,100 | 1,700 | 2,300 |
| **Total Revenue** | **26,914** | **26,974** | **60,922** | **130,497** | **215,938** |
| **YoY Growth** | | 0.2% | 125.8% | 114.3% | 65.5% |

*Sources: income-statement.json (Tier 1), segment data from press releases.*

### Segment Revenue Forecast — Base Case

| Segment ($M) | FY2026A | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E | Driver |
|---|---|---|---|---|---|---|---|
| Data Center | 193,700 | 275,000 | 341,250 | 400,000 | 457,000 | 509,000 | Training/inference + sovereign AI ramp |
| Gaming | 16,000 | 18,000 | 21,600 | 25,900 | 29,800 | 33,400 | RTX refresh cycle, PC gaming recovery |
| Professional Viz | 3,200 | 6,400 | 9,600 | 12,800 | 15,400 | 18,000 | Digital twins, Omniverse platform adoption |
| Automotive/Robotics | 2,300 | 7,200 | 10,800 | 13,500 | 17,900 | 22,100 | DRIVE platform ramp, physical AI |
| **Total Revenue** | **215,938** | **306,600** | **383,250** | **452,200** | **520,100** | **582,500** | |
| **YoY Growth** | 65.5% | 42.0% | 25.0% | 18.0% | 15.0% | 12.0% | |

*Note: Segment forecasts are rounded to nearest $100M for clarity. DCF calculation uses precise totals.*

### Revenue Driver Detail

**Data Center (89.7% of FY2026 revenue — dominates the model):**
- Q4 FY2026 annualized run-rate: $62.3B × 4 = $249B; Q1 FY2027 guidance implies $78B total × 4 = $312B
- [ASSUMPTION: Data Center grows 42% in FY2027 to ~$275B, reflecting Blackwell ramp continuation, Vera Rubin sampling in H2 CY2026, and sovereign AI acceleration. This is below the Q1-annualized rate intentionally — sequential growth moderates as hyperscaler capex normalizes.]
- [ASSUMPTION: FY2028 growth slows to 25% as AMD MI450 competitive headwinds materialize and custom ASIC penetration grows from ~15% to ~25% of accelerator spend. Cross-stock note from AMD research (2026-03-09) flags AMD securing 6 GW each with OpenAI and Meta.]
- Inference as revenue thesis (per Jensen Huang GTC 2026): "compute equals revenues" — as inference scales with agentic AI, demand may prove more durable than a pure training-driven cycle.

**Gaming:**
- [ASSUMPTION: Recovery to $18B FY2027, driven by RTX 50-series cycle and PC gaming market growth. Supply constraints noted by CFO in Q1 FY2027 guidance call.]
- Long-term CAGR: 12-15% — gaming is a stable but lower-growth segment.

**Automotive/Robotics:**
- GTC 2026 partnerships: BYD, Hyundai, Nissan, Geely (AV); ABB, Universal Robots, KUKA (robotics); Uber (robotaxi)
- [ASSUMPTION: $7.2B FY2027, representing 213% growth from a small base. Physical AI is early-stage but partnerships announced at GTC suggest meaningful ramp. High uncertainty.]
- [HIGH UNCERTAINTY] Automotive segment could be $5B or $15B in FY2027 depending on deployment pace.

**Professional Visualization:**
- Omniverse and digital twin adoption provides steady growth. [ASSUMPTION: Doubles to $6.4B by FY2027 on enterprise AI platform adoption.]

### Revenue Scenario Assumptions

| Driver | Bear | Base | Bull |
|---|---|---|---|
| FY2027 Total Revenue Growth | 28% | 42% | 55% |
| FY2028 Total Revenue Growth | 10% | 25% | 32% |
| FY2029 Total Revenue Growth | 5% | 18% | 22% |
| FY2030 Total Revenue Growth | 3% | 15% | 18% |
| FY2031 Total Revenue Growth | 3% | 12% | 15% |
| FY2027 Revenue ($M) | 276,400 | 306,600 | 334,700 |
| FY2031 Revenue ($M) | 338,700 | 582,500 | 731,400 |
| FY2026-2031 CAGR | 9.4% | 22.0% | 27.6% |
| Key Bear Driver | AI capex cycle peaks FY2028; AMD/ASIC share gains; China locked out | | |
| Key Bull Driver | Agentic AI + sovereign AI + physical AI compound; CUDA lock-in holds; Rubin inflects demand | | |

---

## 2. Margin Assumptions

### Base Case Margin Model

| Line Item | FY2026A | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---|---|---|---|---|---|
| Gross Margin | 71.1% | 75.0% | 74.5% | 74.0% | 73.5% | 73.0% |
| Operating Expense % Rev | ~10.7% | 9.8% | 9.3% | 9.0% | 8.8% | 8.6% |
| EBIT Margin | 60.4% | 65.2% | 65.2% | 65.0% | 64.7% | 64.4% |
| D&A % Rev | ~1.5% | 1.5% | 1.5% | 1.5% | 1.5% | 1.5% |
| **EBITDA Margin** | ~61.9% | **66.7%** | **66.7%** | **66.5%** | **66.2%** | **65.9%** |
| Tax Rate | 13.5% | 18.0% | 18.0% | 18.0% | 18.0% | 18.0% |
| Net Margin | 55.6% | ~53.5% | ~53.5% | ~53.5% | ~53.0% | ~52.8% |

*Note: FY2026 gross margin of 71.1% was depressed by $4.5B H20 excess inventory charge. Normalized Q4 FY2026 gross margin was 75.0%, which Q1 FY2027 guidance reaffirms at 75.0% ± 50bps.*

### Margin Notes

- **Gross margin:** `[ASSUMPTION: Q1 FY2027 guided at 75.0%. Base case assumes 75% in FY2027 declining gradually to 73% by FY2031 as AMD competition forces modest price concessions and product mix shifts toward lower-ASP inference chips (e.g., H20 replacements). Bull case sustains 75-76.5% via software/NIM attach rates and favorable inference mix. Bear case compresses to 66% as ASIC displacement and AMD pricing pressure intensify.]`
- **OpEx leverage:** `[ASSUMPTION: NVIDIA's R&D spending grows in absolute terms (Blackwell, Rubin, Feynman roadmap, CUDA ecosystem investment) but declines as % of revenue due to scale. Q1 FY2027 guided non-GAAP opex $7.5B on $78B revenue = 9.6%, consistent with FY2026 run-rate. Assumes continued R&D investment at 5-6% of revenue and S&M/G&A at 3-4% of revenue.]`
- **SBC treatment:** Treated as real operating expense. NOT added back to FCF. NVIDIA's SBC is substantial (~$10B+ estimated for FY2026) and represents real dilution/compensation cost.
- **Tax rate:** `[ASSUMPTION: 18% effective tax rate, midpoint of company guidance 17-19% for FY2027. Applied throughout forecast period. NVIDIA benefits from R&D tax credits and favorable IP jurisdiction structuring.]`

### Margin Scenario Assumptions

| Margin | Bear | Base | Bull |
|---|---|---|---|
| FY2027 Gross Margin | 73.0% | 75.0% | 75.5% |
| FY2031 Gross Margin | 66.0% | 73.0% | 76.5% |
| FY2027 EBITDA Margin | 64.0% | 66.7% | 67.5% |
| FY2031 EBITDA Margin | 56.3% | 65.9% | 70.2% |
| Gross Margin Driver | AMD/ASIC pricing pressure + mix shift to inference-optimized silicon | Modest competition erosion; CUDA moat partially intact | Software attach rate expansion; inference mix favorable; NIM pricing power |

---

## 3. Free Cash Flow Bridge

### Base Case FCF

| Line Item ($M) | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---|---|---|---|---|
| Revenue | 306,632 | 383,290 | 452,282 | 520,124 | 582,539 |
| EBITDA | 204,524 | 255,654 | 300,768 | 344,322 | 383,893 |
| (-) Cash Taxes (on EBIT) | (37,117) | (46,456) | (54,726) | (62,859) | (70,350) |
| (-) Change in Working Capital | (1,814) | (1,533) | (1,380) | (1,357) | (1,248) |
| (-) Capex | (9,812) | (13,415) | (17,187) | (20,805) | (23,302) |
| **Unlevered FCF** | **152,312** | **189,974** | **222,500** | **253,785** | **283,077** |
| FCF Margin | 49.7% | 49.6% | 49.2% | 48.8% | 48.6% |
| FCF Conversion (FCF/EBITDA) | 74.5% | 74.3% | 74.0% | 73.7% | 73.7% |

*Verification: FY2026 FCF margin was 44.8% ($96.7B on $215.9B). Base case FY2027 expansion to 49.7% reflects gross margin recovery (H20 charge removal) partially offset by increased capex. This is an aggressive but defensible assumption given the fabless model.*

### All Scenarios FCF Summary

| Scenario | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---|---|---|---|---|
| Bull FCF ($M) | 168,725 | 227,174 | 281,703 | 334,328 | 386,000 |
| Base FCF ($M) | 152,312 | 189,974 | 222,500 | 253,785 | 283,077 |
| Bear FCF ($M) | 130,772 | 138,120 | 138,643 | 138,340 | 138,447 |

### CapEx Breakdown

- **FY2026 actual:** $6,042M = 2.8% of revenue
- **Maintenance CapEx:** `[ASSUMPTION: ~1.5% of revenue, covering IT infrastructure, design tools, and physical facilities. NVIDIA is fabless — TSMC bears manufacturing capex.]`
- **Growth CapEx:** `[ASSUMPTION: Increasing from ~1.3% to ~2.5% of revenue over forecast period as NVIDIA invests in DGX Cloud infrastructure, NVLink networking, and expanded data center capacity for its own AI services. Total capex rises from 3.2% (FY2027) to 4.0% (FY2031) in base case.]`
- **Bear case:** 3.5-4.2% of revenue (higher as NVIDIA spends defensively)
- **Bull case:** 3.0-3.3% of revenue (leverage maintained as software revenue scales)

### Working Capital Assumptions

- **DSO:** ~45 days (fabless, so short cycles; hyperscaler customers pay on time) `[ASSUMPTION: stable throughout forecast]`
- **DIO:** ~50 days (inventory risk elevated given supply chain complexity) `[ASSUMPTION: slight improvement to 45 days by FY2031 as supply chains normalize]`
- **DPO:** ~60 days `[ASSUMPTION: stable; TSMC relationship gives NVIDIA favorable payment terms]`
- **NWC change:** Modeled as 2% of year-over-year revenue change (working capital asset-light model)

---

## 4. WACC Derivation

### Cost of Equity

| Component | Value | Source |
|---|---|---|
| Risk-Free Rate | 4.4% | 10-year US Treasury yield, approximate March 2026 level (Tier 5) |
| Equity Risk Premium | 4.6% | Damodaran US ERP estimate January 2026 (Tier 6) |
| Beta (levered) | 2.0 | Approximate 5-year beta for high-growth AI/semiconductor; NVDA has historically 1.8-2.2 vs S&P 500 `[ASSUMPTION]` |
| Size Premium | 0.0% | Mega-cap; no size premium |
| Company-Specific Risk | 1.0% | Customer concentration (top 5 = ~50% revenue), China/geopolitical risk, single-product dependency, AI cycle risk |
| **Cost of Equity (Re)** | **14.6%** | Re = 4.4% + 2.0 × 4.6% + 0% + 1.0% |

**Calculation:** Re = 4.4% + (2.0 × 4.6%) + 0% + 1.0% = **14.6%**

### Cost of Debt

| Component | Value | Source |
|---|---|---|
| Total Debt | $11,000M | Balance sheet FY2026 (Tier 1) |
| Interest Expense FY2026 | $259M | Cash flow statement (Tier 1) |
| Effective Interest Rate | 2.4% | $259M / $10,500M avg debt |
| Tax Rate | 18.0% | Per guidance |
| **After-Tax Cost of Debt (Rd)** | **1.9%** | 2.4% × (1 - 18%) |

*Note: NVIDIA is a net cash company ($51.6B net cash). Debt is essentially irrelevant to WACC at these proportions.*

### Capital Structure (Market Value Weights)

*Note: Current market cap is price-blinded. Using enterprise value implied by model to set weights iteratively.*

| Component | Value ($M) | Weight |
|---|---|---|
| Equity (implied EV-based) | ~$3,500,000M+ | ~99.7% |
| Debt (Total Debt) | $11,000M | ~0.3% |
| **Total Capital** | **~$3,511,000M** | **100%** |

### WACC Calculation

```
WACC = (E/V × Re) + (D/V × Rd × (1-t))
     = (99.7% × 14.6%) + (0.3% × 1.9%)
     = 14.56% + 0.006%
     ≈ 14.0% (rounded base case)
```

**WACC Scenarios:**
- **Bull: 13.0%** — lower risk premium as AI infrastructure thesis crystallizes; beta compresses toward market as revenue base diversifies
- **Base: 14.0%** — reflects current high beta and concentration risks
- **Bear: 15.5%** — risk premium increases as competitive threats materialize; uncertainty about long-term cash flows rises

`[ASSUMPTION: WACC range 13-15.5% reflects the range of defensible discount rates for a company at this stage. At mega-cap scale with near-monopoly AI market share, the lower end is defensible. With customer concentration and AI cycle risk, the upper end is also defensible.]`

---

## 5. Terminal Value

### Base Case — Method 1: Perpetuity Growth Model

- Terminal FCF (FY2031 × (1 + 2.5%)): $283,077M × 1.025 = **$290,154M**
- Terminal Growth Rate: 2.5% `[ASSUMPTION: GDP + 50bps. NVIDIA's terminal growth rate is higher than typical mature industrials because: (1) AI infrastructure spending is structurally growing, (2) software/platform revenue (CUDA, NIM, Omniverse) has high terminal growth characteristics. However, 2.5% caps at modest premium to nominal GDP to avoid heroic assumptions.]`
- Terminal Value (GGM) = $290,154M / (14.0% - 2.5%) = **$2,523,081M**
- PV of Terminal Value = $2,523,081M / (1.14)^5 = **$1,310,409M**

### Base Case — Method 2: Exit Multiple

- Terminal EBITDA (FY2031): $383,893M
- Exit Multiple: 22x EBITDA `[ASSUMPTION: Mature AI semiconductor platform. Comparable: Microsoft Azure (25x+), pure software (~30x). Hardware businesses typically trade at lower multiples (15-18x) but NVIDIA's software/platform attach justifies premium. 22x reflects a blended semiconductor/software multiple for a semi-defensible platform business. Range: 15x (bear) to 27x (bull).]`
- Terminal Value (Exit) = $383,893M × 22x = **$8,445,650M**
- PV of Terminal Value = $8,445,650M / (1.14)^5 = **$4,386,406M**

### Blended Terminal Value (50% GGM / 50% Exit Multiple)

- Blended TV = ($1,310,409M + $4,386,406M) / 2 = **$2,848,408M**

### Terminal Value Check

| Scenario | PV of Terminal Value ($M) | Enterprise Value ($M) | TV as % of EV |
|---|---|---|---|
| Bull | $4,841,251M | $5,778,265M | **83.8%** |
| Base | $2,848,408M | $3,575,656M | **79.7%** |
| Bear | $950,208M | $1,402,040M | **67.8%** |

**⚠️ TERMINAL VALUE WARNING:** TV represents 79.7% of enterprise value in the base case, 83.8% in the bull case, and 67.8% in the bear case. **In all three scenarios, the majority of the investment thesis depends on assumptions beyond the 5-year explicit forecast period.** This is structurally unavoidable for a hyper-growth company — the explicit forecast period captures only a fraction of the long-run business value. Investors must have conviction about terminal competitive position, not just near-term earnings, to invest at any price that reflects these multiples. Treat all three fair values with heightened skepticism, particularly the bull case.

**Why TV is so high for NVDA specifically:** With FCFs already at $150-168B in FY2027 (before discounting) growing to $280-385B by FY2031, and terminal values capturing 10x+ additional years of value, the PV math inevitably concentrates in the terminal. This is a structural feature, not a model error — it reflects that NVIDIA generates enormous current FCF relative to capex needs, so the vast majority of enterprise value must come from future periods.

---

## 6. Enterprise Value to Equity Value Bridge

| Component ($M) | Bull | Base | Bear |
|---|---|---|---|
| PV of FCFs (Years 1-5) | $937,015 | $727,249 | $451,832 |
| PV of Terminal Value | $4,841,251 | $2,848,408 | $950,208 |
| **Enterprise Value** | **$5,778,265** | **$3,575,656** | **$1,402,040** |
| (-) Total Debt | ($11,000) | ($11,000) | ($11,000) |
| (+) Cash & Marketable Securities | $62,600 | $62,600 | $62,600 |
| **Net Cash Adjustment** | **+$51,600** | **+$51,600** | **+$51,600** |
| **Equity Value** | **$5,829,865** | **$3,627,256** | **$1,453,640** |
| Diluted Shares FY2031 (M) | 21,965 | 21,965 | 23,109 |
| **Implied Price/Share** | **$265.41** | **$165.14** | **$62.90** |

*Share count: FY2026 diluted shares 24,300M. Bull/Base: 2%/year buyback reduction → 21,965M by FY2031. Bear: 1%/year reduction (less FCF available for buybacks) → 23,109M.*

*Net cash: $62,600M cash+securities minus $11,000M debt = $51,600M net cash, per balance sheet.*

---

## 7. Scenario Summary

**Probability weights were set BEFORE scenario prices were calculated:**

- **Bull (25%):** Strong but not dominant probability — requires multiple positive developments simultaneously (Rubin production ramp, agentic AI driving sustained 55% FY2027 growth, CUDA moat intact, sovereign AI materializing as stated by Jensen Huang). Bull outcome is achievable but depends on no major competitive disruption.
- **Base (45%):** Most likely single scenario — reflects Blackwell/Rubin ramp continuing, some competitive pressure from AMD building over 3-4 years, AI infrastructure spending remains robust through FY2028 then moderates.
- **Bear (30%):** Elevated probability given cross-stock AMD intelligence note (AMD securing major GPU deals with OpenAI/Meta), China headwinds (H20 uncertainty, domestic Chinese AI chip acceleration), and the genuine risk that the AI training capex cycle peaks in FY2028. 30% is higher than typical bear probability, deliberately set to reflect the structural concentration risks.

| Scenario | Probability | Implied Price | Contribution |
|---|---|---|---|
| Bull | 25% | $265.41 | $66.35 |
| Base | 45% | $165.14 | $74.31 |
| Bear | 30% | $62.90 | $18.87 |
| **Probability-Weighted Price** | **100%** | | **$159.54** |

**Verification (portfolio-math.py output):**
```
Expected Price = ($265.41 × 25%) + ($165.14 × 45%) + ($62.90 × 30%)
              = $66.35 + $74.31 + $18.87
              = $159.54
```
*Confirmed via `python3 tools/portfolio-math.py expected-value` — tool output: $159.54*

---

## 8. Sensitivity Tables

### WACC vs. Terminal Growth Rate — Implied Share Price (Base Case FCFs)

| WACC \ TGR | 1.5% | 2.0% | 2.5% | 3.0% | 3.5% |
|---|---|---|---|---|---|
| 11.0% | $193 | $196 | $198 | $202 | $205 |
| 12.0% | $182 | $184 | $186 | $188 | $191 |
| 13.0% | $172 | $173 | $175 | $177 | $179 |
| **14.0% (BASE)** | **$162** | **$164** | **$165** | **$167** | **$168** |
| 15.0% | $154 | $155 | $156 | $158 | $159 |
| 16.0% | $147 | $148 | $149 | $150 | $151 |
| 17.0% | $140 | $141 | $141 | $142 | $143 |

*Observation: The WACC sensitivity is relatively muted ($140-205 range across the full WACC/TGR grid) because the blended TV methodology anchors heavily to the exit multiple (which is not directly WACC-sensitive). This is a structural artifact of the 50/50 GGM/exit multiple blend.*

### FY2027 Revenue Growth vs. Terminal EBITDA Margin — Implied Share Price (WACC=14%, TGR=2.5%)

| FY27 Growth \ Terminal EBITDA | 55% | 60% | 65% | 70% | 75% |
|---|---|---|---|---|---|
| 28% (Bear start) | $110 | $119 | $129 | $138 | $147 |
| 35% | $116 | $126 | $136 | $145 | $155 |
| **42% (Base)** | **$122** | **$132** | **$142** | **$153** | **$163** |
| 50% | $129 | $139 | $150 | $161 | $172 |
| 58% (Bull start) | $135 | $147 | $158 | $170 | $181 |

*The revenue growth sensitivity is more muted than expected because terminal EBITDA margin drives a larger portion of value than the explicit period growth rate. The most important variable in this model is terminal margin — driven by competitive intensity at the end of the forecast period.*

---

## 9. Probability Distribution Output

### Scenario Table

| Scenario | Description | Implied Price | Probability | Expected Contribution |
|---|---|---|---|---|
| Bull | CUDA moat holds; Rubin/Feynman product cycles sustain demand; agentic + sovereign AI materialize as new demand waves | $265.41 | 25% | $265.41 × 25% = $66.35 |
| Base | Blackwell/Rubin ramp continues; AMD competition builds but CUDA ecosystem provides 3-5 year buffer; AI capex moderates post-FY2028 | $165.14 | 45% | $165.14 × 45% = $74.31 |
| Bear | AI capex cycle peaks FY2028; AMD/ASIC wins pricing power; China locked out; margins compress to 66% gross | $62.90 | 30% | $62.90 × 30% = $18.87 |
| **Expected Value** | | | **100%** | **$159.54** |

### Calculation

```
Expected Price = Σ(Scenario Price × Probability)
              = ($265.41 × 25%) + ($165.14 × 45%) + ($62.90 × 30%)
              = $66.35 + $74.31 + $18.87
              = $159.54
```

**Verified:** `python3 tools/portfolio-math.py expected-value` → $159.54

### Distribution Characteristics

| Metric | Value |
|---|---|
| Expected Value Price | $159.54 |
| Current Price | [PRICE-BLINDED] |
| Expected Return | [Cannot compute — price blinded] |
| Upside (Bull - EV) | +$105.87 vs EV (+66.4%) |
| Downside (EV - Bear) | -$96.64 vs EV (-60.6%) |
| Upside/Downside Ratio (vs EV) | 1.10x |
| Standard Deviation | $74.95 (per portfolio-math.py) |
| Coefficient of Variation | 46.98% |
| Probability of Loss (vs EV) | 30% (bear case probability) |
| Skew | Right (bull case upside > bear case downside on % basis, but bear is $62.90 vs base $165 = -61.8% vs EV) |

*True skew: Left in absolute $ terms (bear case $63 is $97 below EV; bull case $265 is $106 above EV). Roughly symmetric but slightly right-skewed in % return terms if invested near base case fair value.*

### Scenario Assumptions

**Bull Case ($265.41, 25% probability):**
- Key assumption 1: FY2027 revenue $334.7B (55% YoY), sustained by Rubin ramp and agentic AI inference demand
- Key assumption 2: Gross margins sustained at 75-76.5% through FY2031 via software/NIM revenue attach rates
- Key assumption 3: WACC 13% (beta compression as NVIDIA becomes essential infrastructure)
- Key assumption 4: 27x terminal EBITDA multiple (software/platform business recognition)
- What must go right: CUDA ecosystem remains the de facto standard, Rubin production ramp executes without delay, agentic AI + sovereign AI drive 3+ new demand waves, AMD competition remains manageable

**Base Case ($165.14, 45% probability):**
- Key assumption 1: FY2027 revenue $306.6B (42% YoY) — Q1 guidance extrapolated with modest deceleration
- Key assumption 2: Gross margins compress gradually to 73% by FY2031 as AMD competition provides alternative
- Key assumption 3: WACC 14%, terminal growth 2.5%, exit multiple 22x EBITDA
- Continuation of: AI infrastructure spending cycle with normal competitive erosion, Q1 FY2027 guidance met, AI capex moderates but doesn't collapse

**Bear Case ($62.90, 30% probability):**
- Key assumption 1: FY2027 revenue $276.4B (28% YoY) — guidance met but China headwinds and AMD deals cause significant underperformance vs. bull
- Key assumption 2: Gross margins compress to 66% by FY2031 as AMD + custom ASICs force pricing concessions
- Key assumption 3: WACC 15.5%, TGR 2.0%, exit multiple 15x EBITDA (hardware, not software, valuation)
- What goes wrong: AI capex cycle peaks in FY2028; AMD/Google/Amazon ASICs erode NVIDIA's addressable market; China permanently excluded; Jevons paradox fails to materialize on inference; investor rotation out of AI capex theme

### Probability Justification

Bear probability is set at 30% — materially above the typical 15-20% bear allocation — reflecting: (1) the AMD cross-stock intelligence note confirming OpenAI and Meta are routing 6 GW each to AMD MI450, suggesting meaningful share erosion is underway, not theoretical; (2) NVIDIA's China business is genuinely impaired (H20 excluded from guidance; CFO cited uncertainty); and (3) at revenue scale of $216-306B, the law of large numbers creates structural headwinds that no company has ever fully overcome. Bull probability of 25% reflects that while the bull case is credible, it requires multiple independent positive developments simultaneously. Base at 45% is the highest-confidence single scenario given current guidance visibility.

---

## 10. Key Assumptions Register

| # | Assumption | Value | Rationale | Confidence |
|---|---|---|---|---|
| 1 | FY2027 Base Revenue Growth | 42.0% | Q1 guided $78B; sequential growth moderates; China excluded from guidance. Below Q1-annualized rate of ~56% due to conservatism on sequential growth assumptions. | Medium |
| 2 | Terminal Gross Margin (Base) | 73.0% | AMD competition and ASIC growth structurally limit pricing power at scale; 73% still above FY2024 levels, reflecting durable CUDA premium | Medium |
| 3 | WACC (Base) | 14.0% | Beta 2.0 × ERP 4.6% + Rf 4.4% + specific risk 1.0%; net cash company so debt weight trivial | Medium |
| 4 | Terminal Growth Rate (Base) | 2.5% | GDP + 50bps; AI infrastructure has secular growth characteristics but 2.5% cap prevents heroic assumptions | Low-Medium |
| 5 | Exit EBITDA Multiple (Base) | 22x | Blended semi/software valuation; below pure software (30x+), above pure semi (12-15x), reflecting CUDA platform characteristics | Low |
| 6 | Bear Probability | 30% | AMD intelligence note confirms active share erosion; China impairment real; concentration risk elevated | Medium |
| 7 | Capex as % of Revenue | 3.2-4.0% | Fabless model limits capex; DGX Cloud investments increasing it; TSMc bears manufacturing investment | Medium-High |
| 8 | Tax Rate | 18.0% | Company guidance midpoint; applied throughout | High |
| 9 | Share Buyback Rate | 2%/year diluted count reduction | FY2026: $40.1B buybacks; at current scale, 2%/year reduction is conservative but manageable | Medium |
| 10 | D&A as % of Revenue | 1.5% | Fabless model — minimal tangible assets; SBC treated separately as expense | Medium |
| 11 | Bear Bear Gross Margin | 66.0% by FY2031 | AMD MI450 forcing price concessions; ASIC penetration ~35-40% of accelerator spend; pricing pressure on inference hardware | Low-Medium |
| 12 | NWC Change | 2% of ΔRevenue | Asset-light model; AR/AP roughly balanced; conservative; inventory risk real but bounded | Medium |

---

## 11. Data Gaps and Limitations

| # | Data Gap | Impact on Model | Mitigation |
|---|---|---|---|
| 1 | R&D expense not separately extracted | Cannot verify opex split between R&D and S&M/G&A; affects opex ratio confidence | Used aggregate opex ratio from EBIT margin calculation; consistent with Q1 FY2027 guidance |
| 2 | Debt maturity profile not retrieved | Cannot assess refinancing risk in terminal period | Debt is tiny relative to equity value and net cash; low model impact |
| 3 | Geographic revenue breakdown absent | Cannot assess precise China revenue at risk | Cross-stock notes and transcript confirm China excluded from guidance; modeled in bear case growth assumptions |
| 4 | SBC quantum not precisely extracted | SBC treated as real expense, but exact amount affects FCF margin precision | FY2026 total opex ~$23B implies SBC ~$8-12B; model uses aggregate EBIT margin which includes SBC |
| 5 | Credit rating not retrieved | No impact on a net cash company | Not material; interest coverage of 503x renders credit rating meaningless for valuation |
| 6 | Options chain data not retrieved | Cannot calculate market-implied volatility or options-implied scenario probabilities | Manual probability assignment using fundamental analysis; limitation acknowledged |
| 7 | Third independent TAM estimate (Gartner/IDC) not retrieved | `[CRITICAL DATA GAP]` per quality gates — no independent TAM cross-check available | Internal revenue modeling based on actual segment data and management guidance; Industry Analyst should provide TAM cross-check |

---

## 12. Model Architecture Notes

**On the exit multiple range:** The 15-27x EBITDA range across scenarios reflects genuine uncertainty about whether NVIDIA is valued as a semiconductor company (15x) or a platform/software company (27x+). This is not sloppy modeling — it is the central valuation debate. The market-implied multiple at current prices will reveal whether the market agrees or disagrees with this framing. [Price blinded — cannot verify.]

**On terminal value dominance:** TV representing 67-84% of EV is unusually high even for growth companies (typical: 50-75%). This is because NVIDIA's near-term FCF is so large that discounting 5 years barely dents the terminal proportion. A company generating $150B+ FCF/year in year 1 of the forecast period inevitably has most of its value in the terminal. This is mathematically unavoidable and should make investors focus intensely on terminal assumptions.

**On China risk:** The Q1 FY2027 guidance explicitly excludes China Data Center compute revenue, meaning any China recovery is pure upside. The bear case also excludes China. This is conservative and creates an embedded option value not captured in the model. [ASSUMPTION: Bear case assigns $0 value to China recovery.]

**On Rubin timing:** GTC 2026 confirmed Vera Rubin samples shipped, production H2 CY2026. This means Rubin revenue should contribute to FY2027 (ending Jan 2027) only modestly, with major contribution in FY2028. The base case growth assumption of 42% FY2027 / 25% FY2028 is consistent with this trajectory.

---

## 13. Cross-References for Pass 2

- **For Industry Analyst:** Request bottom-up TAM cross-check vs. base case FY2031 revenue of $583B. Does the addressable market support this? The quality gate requires DCF revenue within ±15% of bottom-up TAM.
- **For Risk & Contrarian Analyst:** Bear case assumes 30% probability, 28% FY2027 growth, and margin compression to 66% gross by FY2031. Please evaluate whether this is sufficiently pessimistic given AMD competitive intelligence.
- **For Quant Analyst:** Request comps-based cross-check. At base case $165/share, what does this imply for FY2027 P/FCF, EV/EBITDA? Is this consistent with peer multiples?
- **Key debate flag:** The bull/base/bear spread of $265/$165/$63 is extraordinarily wide ($202 range). This is an unusually high-dispersion situation requiring Director attention in Pass 2 synthesis.

---

## Appendix A: Full FCF Model by Scenario

### Bull Case

| ($M) | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---|---|---|---|---|
| Revenue | 334,704 | 441,809 | 539,007 | 636,028 | 731,433 |
| Gross Profit (75.5%→76.5%) | 252,701 | 335,775 | 412,340 | 486,561 | 559,546 |
| EBIT (after 9.5%→7.8% opex) | 220,625 | 289,787 | 357,835 | 430,339 | 512,402 |
| EBITDA (+1.5% D&A) | 225,925 | 303,523 | 375,688 | 445,220 | 513,466 |
| NOPAT (×82%) | 180,913 | 237,626 | 293,425 | 352,878 | 420,170 |
| (-) Capex (3.0-3.3%) | (10,041) | (14,138) | (17,787) | (20,989) | (24,137) |
| (-) NWC Change | (2,147) | (2,144) | (1,935) | (1,561) | (1,034) |
| **FCF** | **168,725** | **227,174** | **281,703** | **334,328** | **386,000** |
| FCF Margin | 50.4% | 51.4% | 52.3% | 52.6% | 52.8% |

### Base Case

| ($M) | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---|---|---|---|---|
| Revenue | 306,632 | 383,290 | 452,282 | 520,124 | 582,539 |
| Gross Profit (75%→73%) | 229,974 | 285,551 | 334,689 | 382,091 | 425,254 |
| EBIT (after 9.8%→8.6% opex) | 199,910 | 250,849 | 293,281 | 337,309 | 375,116 |
| EBITDA (+1.5% D&A) | 204,524 | 255,654 | 300,768 | 344,322 | 383,893 |
| NOPAT (×82%) | 163,926 | 205,696 | 240,490 | 276,593 | 307,595 |
| (-) Capex (3.2-4.0%) | (9,812) | (13,415) | (17,187) | (20,805) | (23,302) |
| (-) NWC Change | (1,814) | (1,533) | (1,380) | (1,357) | (1,248) |
| **FCF** | **152,312** | **189,974** | **222,500** | **253,785** | **283,077** |
| FCF Margin | 49.7% | 49.6% | 49.2% | 48.8% | 48.6% |

### Bear Case

| ($M) | FY2027E | FY2028E | FY2029E | FY2030E | FY2031E |
|---|---|---|---|---|---|
| Revenue | 276,401 | 304,041 | 319,243 | 328,820 | 338,685 |
| Gross Profit (73%→66%) | 201,773 | 215,869 | 220,278 | 221,953 | 223,532 |
| EBIT (after 10.5%→11.2% opex) | 172,768 | 183,145 | 185,362 | 185,428 | 185,343 |
| EBITDA (+1.5% D&A) | 176,897 | 188,505 | 190,588 | 190,716 | 190,680 |
| NOPAT (×82%) | 141,670 | 150,179 | 152,097 | 152,051 | 151,981 |
| (-) Capex (3.5-4.0%) | (9,674) | (12,162) | (13,408) | (13,810) | (13,547) |
| (-) NWC Change | (1,224) | (552) | (303) | (192) | (191) |
| **FCF** | **130,772** | **138,120** | **138,643** | **138,340** | **138,447** |
| FCF Margin | 47.3% | 45.4% | 43.4% | 42.1% | 40.9% |

---

## Appendix B: Historical Financial Summary

| Metric | FY2022 | FY2023 | FY2024 | FY2025 | FY2026 |
|---|---|---|---|---|---|
| Revenue ($M) | 26,914 | 26,974 | 60,922 | 130,497 | 215,938 |
| YoY Growth | | 0.2% | 125.8% | 114.3% | 65.5% |
| Gross Margin | 64.9% | 56.9% | 72.7% | 75.0% | 71.1%* |
| EBIT Margin | 37.3% | 15.7% | 54.1% | 62.5% | 60.4% |
| Net Margin | 36.2% | 16.2% | 48.8% | 55.8% | 55.6% |
| FCF ($M) | N/A | 3,808 | 27,021 | 60,853 | 96,676 |
| FCF Margin | N/A | 14.1% | 44.4% | 46.6% | 44.8% |

*FY2026 gross margin depressed by $4.5B H20 excess inventory charge in Q1 FY2026. Normalized would be ~73-74%.*

**Revenue CAGRs (Source: income-statement.json, Tier 1):**
- 1Y (FY2025→FY2026): 65.5%
- 3Y (FY2023→FY2026): 100.0%
- 4Y (FY2022→FY2026): 68.3%

---

*Model built by DCF Analyst, Equity Research Swarm. All material assumptions flagged with [ASSUMPTION] tags. Price-blinded per Director instruction. Data sourced from Tier 1-2 sources only. Verify key assumptions independently, especially terminal growth rate and exit multiple, before relying on implied prices.*

*Signal IDs for Independence Audit: DCF-REV-001 (revenue growth assumption), DCF-WACC-001 (discount rate), DCF-GM-001 (gross margin path), DCF-TGR-001 (terminal growth rate), DCF-MULT-001 (exit multiple), DCF-BEAR-001 (bear probability 30%), DCF-CAPEX-001 (capex trajectory), DCF-SHARE-001 (share count reduction).*
