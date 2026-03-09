# DCF Model — [TICKER] ([Company Name])
**Date:** [YYYY-MM-DD]
**Analyst:** DCF Analyst (Equity Research Swarm)

---

## 1. Revenue Build

### Segment Revenue

| Segment | FY[Y-1]A | FY[Y]E | FY[Y+1]E | FY[Y+2]E | FY[Y+3]E | FY[Y+4]E | Driver |
|---------|----------|--------|----------|----------|----------|----------|--------|
| [Segment 1] | | | | | | | [Units × Price / Growth rate] |
| [Segment 2] | | | | | | | |
| [Segment 3] | | | | | | | |
| **Total Revenue** | | | | | | | |
| **YoY Growth** | | | | | | | |

### Revenue Driver Detail

**[Segment 1]:**
- Units/Volume: [X] → [Y] (CAGR: [Z]%)
- Price/ASP: $[X] → $[Y] (CAGR: [Z]%)
- Key assumption: `[ASSUMPTION: ...]`

**[Segment 2]:**
- [Same format]

### Revenue Scenario Assumptions

| Driver | Bear | Base | Bull |
|--------|------|------|------|
| [Seg 1] Revenue Growth | [X]% | [Y]% | [Z]% |
| [Seg 2] Revenue Growth | [X]% | [Y]% | [Z]% |
| Total Revenue FY[Y+4] | $[X]M | $[Y]M | $[Z]M |
| Total Revenue CAGR | [X]% | [Y]% | [Z]% |

---

## 2. Margin Assumptions

| Line Item | FY[Y-1]A | FY[Y]E | FY[Y+1]E | FY[Y+2]E | FY[Y+3]E | FY[Y+4]E |
|-----------|----------|--------|----------|----------|----------|----------|
| Gross Margin | | | | | | |
| R&D (% of Rev) | | | | | | |
| S&M (% of Rev) | | | | | | |
| G&A (% of Rev) | | | | | | |
| SBC (% of Rev) | | | | | | |
| **EBITDA Margin** | | | | | | |
| **EBIT Margin** | | | | | | |
| D&A (% of Rev) | | | | | | |

### Margin Assumptions Notes
- Gross margin: `[ASSUMPTION: ...]`
- OpEx leverage: `[ASSUMPTION: ...]`
- SBC treatment: Treated as real operating expense. NOT added back to FCF.

### Margin Scenario Assumptions

| Margin | Bear | Base | Bull |
|--------|------|------|------|
| Terminal Gross Margin | [X]% | [Y]% | [Z]% |
| Terminal EBITDA Margin | [X]% | [Y]% | [Z]% |

---

## 3. Free Cash Flow Bridge

| Line Item ($M) | FY[Y]E | FY[Y+1]E | FY[Y+2]E | FY[Y+3]E | FY[Y+4]E |
|----------------|--------|----------|----------|----------|----------|
| EBITDA | | | | | |
| (-) Cash Taxes | | | | | |
| (-) Change in Working Capital | | | | | |
| (-) Maintenance CapEx | | | | | |
| (-) Growth CapEx | | | | | |
| **Unlevered FCF** | | | | | |
| FCF Margin (%) | | | | | |
| FCF Conversion (FCF/EBITDA) | | | | | |

### CapEx Breakdown
- Maintenance CapEx: `[ASSUMPTION: X% of revenue, based on ...]`
- Growth CapEx: `[ASSUMPTION: ...]`
- Total CapEx as % of Revenue: [X]% → [Y]% over forecast period

### Working Capital Assumptions
- DSO: [X] days → [Y] days `[ASSUMPTION: ...]`
- DIO: [X] days → [Y] days `[ASSUMPTION: ...]`
- DPO: [X] days → [Y] days `[ASSUMPTION: ...]`
- Cash conversion cycle: [X] days → [Y] days

---

## 4. WACC Derivation

### Cost of Equity

| Component | Value | Source |
|-----------|-------|--------|
| Risk-Free Rate | [X]% | [10-year Treasury as of YYYY-MM-DD] |
| Equity Risk Premium | [X]% | [Source: Damodaran / Duff & Phelps / other] |
| Beta (levered) | [X] | [2-year weekly regression vs. S&P 500] |
| Size Premium | [X]% | [Source, or 0% if large-cap] |
| Company-Specific Risk | [X]% | [Justification] |
| **Cost of Equity (Re)** | **[X]%** | Re = Rf + β × ERP + Size + Specific |

**Calculation:** Re = [X]% + [X] × [X]% + [X]% + [X]% = **[X]%**

### Cost of Debt

| Component | Value | Source |
|-----------|-------|--------|
| Weighted Avg Interest Rate | [X]% | [From filings — specify which note] |
| Tax Rate | [X]% | [Effective or statutory, specify] |
| **After-Tax Cost of Debt (Rd)** | **[X]%** | Rd × (1 - t) |

### Capital Structure (Market Value Weights)

| Component | Value ($M) | Weight |
|-----------|-----------|--------|
| Equity (Market Cap) | $[X]M | [X]% |
| Debt (Total Debt) | $[X]M | [X]% |
| **Total Capital** | **$[X]M** | **100%** |

### WACC Calculation
```
WACC = (E/V × Re) + (D/V × Rd × (1-t))
     = ([X]% × [X]%) + ([X]% × [X]%)
     = [X]% + [X]%
     = [X]%
```

---

## 5. Terminal Value

### Method 1: Perpetuity Growth
- Terminal FCF (Year 5 × (1+g)): $[X]M
- Terminal Growth Rate: [X]% `[ASSUMPTION: Based on ... ]`
- Terminal Value = FCF / (WACC - g) = $[X]M / ([X]% - [X]%) = $[X]M

### Method 2: Exit Multiple
- Terminal EBITDA: $[X]M
- Exit Multiple: [X]x `[ASSUMPTION: Based on mature comp range of [X-Y]x]`
- Terminal Value = EBITDA × Multiple = $[X]M × [X]x = $[X]M

### Averaged Terminal Value
- Perpetuity Growth TV: $[X]M
- Exit Multiple TV: $[X]M
- **Averaged TV: $[X]M**

### ⚠️ Terminal Value Check
| Scenario | Terminal Value ($M) | Enterprise Value ($M) | TV as % of EV |
|----------|--------------------|-----------------------|---------------|
| Bull | $[X]M | $[X]M | [X]% |
| Base | $[X]M | $[X]M | [X]% |
| Bear | $[X]M | $[X]M | [X]% |

[If any scenario shows TV > 50% of EV, insert warning:]
`⚠️ TERMINAL VALUE WARNING: TV represents [X]% of enterprise value in the [scenario] case. More than half the valuation depends on assumptions beyond the explicit forecast period. Treat this scenario's valuation with additional skepticism.`

---

## 6. Enterprise Value to Equity Value Bridge

| Component ($M) | Bull | Base | Bear |
|----------------|------|------|------|
| PV of FCFs (Years 1-5) | $[X]M | $[X]M | $[X]M |
| PV of Terminal Value | $[X]M | $[X]M | $[X]M |
| **Enterprise Value** | **$[X]M** | **$[X]M** | **$[X]M** |
| (-) Total Debt | ($[X]M) | ($[X]M) | ($[X]M) |
| (+) Cash & Equivalents | $[X]M | $[X]M | $[X]M |
| (-) Minority Interest | ($[X]M) | ($[X]M) | ($[X]M) |
| (+) Equity Investments | $[X]M | $[X]M | $[X]M |
| (-) Pension Deficit | ($[X]M) | ($[X]M) | ($[X]M) |
| **Equity Value** | **$[X]M** | **$[X]M** | **$[X]M** |
| Diluted Shares (M) | [X]M | [X]M | [X]M |
| **Implied Price/Share** | **$[X]** | **$[X]** | **$[X]** |

---

## 7. Scenario Summary

| Scenario | Probability | Implied Price | Contribution |
|----------|-------------|--------------|--------------|
| Bull | [X]% | $[X] | $[X] |
| Base | [X]% | $[X] | $[X] |
| Bear | [X]% | $[X] | $[X] |
| **Probability-Weighted Price** | **100%** | | **$[X]** |

---

## 8. Sensitivity Tables

### WACC vs. Terminal Growth Rate — Implied Share Price (Base Case)

| | TGR 1.0% | TGR 1.5% | TGR 2.0% | TGR 2.5% | TGR 3.0% | TGR 3.5% |
|---|----------|----------|----------|----------|----------|----------|
| WACC [X-2]% | | | | | | |
| WACC [X-1]% | | | | | | |
| **WACC [X]%** | | | **$[BASE]** | | | |
| WACC [X+1]% | | | | | | |
| WACC [X+2]% | | | | | | |

### Revenue Growth vs. Terminal Margin — Implied Share Price (Base Case)

| | Margin [X-2]% | Margin [X-1]% | Margin [X]% | Margin [X+1]% | Margin [X+2]% |
|---|-------------|-------------|------------|-------------|-------------|
| Growth [X-2]% | | | | | |
| Growth [X-1]% | | | | | |
| **Growth [X]%** | | | **$[BASE]** | | |
| Growth [X+1]% | | | | | |
| Growth [X+2]% | | | | | |

---

## 9. Key Assumptions Register

| # | Assumption | Value | Rationale | Confidence |
|---|-----------|-------|-----------|------------|
| 1 | | | | [High/Med/Low] |
| 2 | | | | |
| 3 | | | | |

---

## 10. Data Gaps

| # | Data Gap | Impact | Mitigation |
|---|---------|--------|------------|
| 1 | | | |

---

*Model built by DCF Analyst, Equity Research Swarm. All assumptions flagged explicitly. Verify independently.*
