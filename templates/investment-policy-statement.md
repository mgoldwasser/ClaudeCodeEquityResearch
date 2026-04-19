# Investment Policy Statement (IPS)

An IPS is the mandate document that defines what the research output can and cannot recommend. Every research note is validated against the active IPS before publication. If the note's recommendation violates the IPS, the Director must either (a) revise the recommendation to fit, (b) flag the violation and downgrade to "restricted / educational," or (c) document an explicit mandate exception with rationale.

The active IPS for a run is specified by the `--ips` flag to `tools/ips-validator.py` (default: `configs/default-ips.yaml`).

---

## 1. Mandate Overview

- **Mandate name:**
- **Mandate type:** (Long-only / Long-short / Hedge / Concentrated / Diversified)
- **Investment universe:** (e.g., US large-cap equities ≥ $10B market cap)
- **Benchmark:** (e.g., S&P 500, Russell 1000, custom)
- **Style bias:** (Growth / Value / Core / GARP / Quality)
- **Investment horizon:** (e.g., 12–24 months fundamental view)
- **Effective date:**
- **Last reviewed:**

## 2. Return & Risk Objectives

- **Return target:** (e.g., benchmark + 200bps net of fees, rolling 3-year)
- **Volatility band:** (e.g., 0.9x–1.2x benchmark vol)
- **Tracking error ceiling:** (e.g., ≤ 600bps vs. benchmark)
- **Max drawdown tolerance:** (e.g., ≤ −25% peak-to-trough)
- **Information ratio target:** (e.g., ≥ 0.5 over full cycle)

## 3. Position-Level Constraints

- **Max single-name weight:** (e.g., 5% of NAV)
- **Max single-name weight vs. benchmark:** (e.g., benchmark weight + 300bps, whichever is greater)
- **Min single-name weight at initiation:** (e.g., 50bps — smaller is noise)
- **Max position in any single issuer family:** (parent + subsidiaries)
- **Max short position (long-short only):**

## 4. Sector & Factor Constraints

- **Sector caps:** per-GICS-sector max weight (often benchmark weight ± 500bps)
- **Max factor tilt:** (e.g., value / momentum / size / quality / low-vol; often expressed as max standardized exposure)
- **Country / region caps:** (for non-US inclusive mandates)
- **Industry concentration cap:** (e.g., ≤ 25% in any GICS industry)

## 5. Liquidity & Operational Constraints

- **Min 30-day ADV position limit:** (e.g., position ≤ 10% of 30-day ADV, assumes 10-day exit)
- **Min market cap floor:** (e.g., $2B)
- **Min public float:** (e.g., $1B free float)
- **Max ownership of any issuer:** (e.g., ≤ 5% of shares outstanding — passive-ownership threshold)
- **Trading venues:** (e.g., listed US exchanges only; OTC excluded)

## 6. ESG & Exclusionary Constraints

- **Controversial-weapons exclusion:** (Ottawa, Oslo, CCM signatories)
- **Tobacco / thermal-coal / civilian-firearms exclusions:**
- **Sanctions screens:** (OFAC, EU, UK HMT)
- **Issuer-level ESG score floor:** (e.g., MSCI ESG rating ≥ BBB; apply floor at portfolio level not security level)
- **Norms-based screening:** (UN Global Compact violations, etc.)
- **Governance screens:** (dual-class max, activist-target inclusion)

## 7. Quality & Accounting Constraints

- **Forensic-quality floor:** (e.g., Beneish M-Score < −1.78; Altman Z > 1.81 for non-financials)
- **Going-concern qualification:** automatic restricted list
- **Recent restatement within 24 months:** requires committee approval
- **Auditor opinion:** unqualified required

## 8. Turnover & Tax Considerations

- **Annual turnover budget:** (e.g., ≤ 60% for a core mandate)
- **Short-term gain avoidance:** (e.g., < 12-month positions require documented rationale in taxable sleeves)
- **Wash-sale discipline:** (30-day re-entry rule enforced)

## 9. Derivatives & Leverage

- **Options permitted:** (Y/N; if Y: covered-call, protective-put, collar caps)
- **Max gross / net leverage:**
- **Max single-trade notional as % of NAV:**

## 10. Governance & Review

- **Portfolio manager:**
- **Oversight committee:** (names / cadence)
- **Client / allocator sign-off cadence:** (quarterly / semi-annually)
- **Exception authority:** who can waive an IPS constraint, and for what duration
- **Review cadence:** annual minimum; interim after mandate change, governance event, or material drawdown

## 11. Reporting Requirements

- **Performance attribution cadence:**
- **Risk reporting:** (VaR, ex-ante tracking error, factor decomposition)
- **Compliance certification:** pre-trade and monthly post-trade
- **Client reporting package:** sections required

---

## How the Research System Uses the IPS

For each research note, `tools/ips-validator.py` runs the following checks against the note's recommendation and the target security's characteristics:

| Check | Source field in note | IPS field |
|-------|---------------------|-----------|
| Market-cap floor | Section 3 (Business Overview) / data | `universe.min_market_cap_usd` |
| Liquidity floor | data/market-data.json (30-day ADV) | `liquidity.min_adv_usd` |
| Sector eligibility | Section 6 (Industry) | `universe.allowed_sectors` / `exclusions.sector_exclusions` |
| Position size | Section 14 (Position Sizing) | `position.max_single_name_weight` |
| Forensic quality | Section 11 (Quality & Credibility) | `quality.min_beneish_m_score`, `quality.min_altman_z` |
| ESG exclusions | Data Intelligence Memo / Section 9 | `exclusions.*` |
| Restricted list | Data Intelligence Memo | `exclusions.restricted_list` |
| Rating eligibility | Section 1 (Executive Summary) | `mandate.allowed_ratings` (e.g., long-only excludes Sell) |

The validator emits `output/[TICKER]/[DATE]/pass2/ips-compliance.md` with one row per check and a terminal verdict: **ELIGIBLE**, **ELIGIBLE WITH EXCEPTIONS**, or **RESTRICTED**. The Director reviews the verdict in Step 2.7 before price reveal and final sign-off.
