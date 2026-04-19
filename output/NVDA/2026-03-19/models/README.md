# NVDA Model Index
**Generated:** 2026-03-19 | **Equity Research Swarm — Model Builder**

All models are self-contained Python 3 scripts. Run with `python3 <model_name>`.
Dependencies: standard library only (+ numpy optional; pure-Python fallbacks provided).

---

## Models

### 1. `nvda_dcf_model.py` → `nvda_dcf_results.json`
**Purpose:** 5-year DCF (FY2027-FY2031) with bull/base/bear scenarios

**Key Inputs:**
- Base revenue: $215,938M (FY2026 actual)
- Q1 FY2027 guidance: $78B ±2%
- WACC: 13.86% (RF 4.5% + ERP 5.5% × beta 1.75 + 0.5% specific risk)
- Net cash: $51,600M

**Key Outputs:**
| Scenario | Prob | FY2027 Rev | FY2031 Rev | Price |
|----------|------|-----------|-----------|-------|
| Bull     | 25%  | $356,298M  | $838,760M  | $274.52 |
| Base     | 50%  | $313,110M  | $534,714M  | $139.43 |
| Bear     | 25%  | $259,126M  | $287,686M  | $52.00  |
| **EV**   |      |            |            | **$151.34** |

**Flags:** All scenarios have TV > 50% of EV — standard for high-growth compounders; documented.

---

### 2. `nvda_comps_model.py` → `nvda_comps_results.json`
**Purpose:** Peer comparable analysis; implied valuation at peer multiples

**Peer set:** AMD, AVGO, QCOM, MRVL, ASML
**Data quality:** Peer EV/market cap data is [ESTIMATED] — requires live market feed for precision

**Key Outputs:**
- NVDA EV/EBITDA: 16.9x vs peer median 26.5x → z-score -1.19 (DISCOUNT on earnings basis)
- NVDA EV/Revenue: 10.2x vs peer median 8.5x → z-score +0.17
- Implied price at peer EV/EBITDA median: $144.32 (P25-P75: $72.95–$168.46)
- Implied price at peer EV/FCF median: $214.17
- Composite ranking: NVDA #1 on value+quality composite

---

### 3. `nvda_risk_model.py` → `nvda_risk_results.json`
**Purpose:** Monte Carlo (5,000 iterations), factor stress tests, VaR/CVaR, drawdown analysis

**Key Outputs:**
- Monte Carlo P50: $207.00 | P5–P95: $84.96–$521.33
- Highest-probability stress: AMD share capture (25% prob, -18.8% price impact)
- Tail risk: Combined stress scenario (-56.2% at 5% probability)
- Sharpe: 0.282 | Kelly quarter: 12.8% (practical sizing max)
- Historical max drawdown: -70% (GFC); average recovery: 15 months

---

### 4. `nvda_credit_model.py` → `nvda_credit_results.json`
**Purpose:** Capital structure analysis, covenant headroom, Altman Z-Score, liquidity

**Key Outputs:**
- Net cash: $51,600M (net leverage -0.39x EBITDA)
- Interest coverage: 515x EBITDA/interest
- Altman Z': 12.85 (SAFE zone; threshold 2.6)
- Debt repaid in 0.11 years from FCF
- Even at -70% revenue decline: no covenant breach
- Data gap: Debt maturity profile [ESTIMATED]; full 10-K Note 12 required for precision

---

### 5. `nvda_scenarios.json`
**Purpose:** Structured scenario data for `report-generator.py charts`

Format compatible with `tools/report-generator.py --scenarios-file` parameter.

| Field | Bull | Base | Bear |
|-------|------|------|------|
| probability | 0.25 | 0.50 | 0.25 |
| price_target | $274.52 | $139.43 | $52.00 |
| EV price | $151.34 | — | — |

---

## Validation Status

| Model | Execution | Boundary Test | Sanity Check |
|-------|-----------|---------------|--------------|
| nvda_dcf_model.py | PASS | PASS (clipped growth rates) | PASS (higher growth → higher price) |
| nvda_comps_model.py | PASS | PASS (None handling) | PASS (premium to low-growth peers) |
| nvda_risk_model.py | PASS | PASS (clipped MC draws) | PASS (higher vol → wider distribution) |
| nvda_credit_model.py | PASS | PASS (zero-division checks) | PASS (more revenue → better coverage) |

---

## Key Assumptions Requiring Analyst Validation

1. **WACC 13.86%**: Beta of 1.75 drives this high; if NVDA transitions to infrastructure-like
   stability, beta could compress to 1.2-1.4, implying WACC of 11-12% and significantly
   higher fair values. Sensitivity table in DCF shows ~$157-$168 at 11-12% WACC.

2. **Bear case revenue growth +20% FY2027**: Calibrated to Q1 guidance floor but assumes
   capex digestion slows Q2-Q3. Cross-stock AMD note provides evidence for this being
   a reasonable downside (not tail) scenario.

3. **Terminal growth 3.5% (base)**: Above historical GDP. Justified by AI infrastructure
   becoming utility-like essential infrastructure, but fragile if AI adoption plateaus earlier.

4. **Peer data [ESTIMATED]**: Comps model z-scores and implied valuations require live
   market data for precision. Direction of findings (NVDA at discount on earnings/FCF
   basis, premium on revenue) is directionally correct but magnitudes are approximate.

5. **Altman Z'-Score**: EBITDA uses operating income as proxy (D&A not separately extracted
   — DATA GAP). Actual Z' would be marginally different but conclusion (SAFE zone) is robust.
