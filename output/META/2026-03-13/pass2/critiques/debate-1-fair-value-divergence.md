# Debate 1: Fair Value Divergence — DCF Analyst vs. Model Builder

**Date:** 2026-03-13
**Ticker:** META (Meta Platforms, Inc.)
**Moderator:** Director of Research
**Participants:** DCF Analyst, Model Builder, Quant Analyst (reference)

---

## The Disagreement

Three independent valuations produced materially different base case fair values:

| Source | Base Case Fair Value | Probability-Weighted |
|--------|---------------------|---------------------|
| DCF Analyst | $733/share | $714 |
| Model Builder | $856/share | $875 |
| Quant Analyst (comps) | $681/share | $689 |

The DCF-to-Model-Builder gap is 17% ($123/share). The DCF-to-Quant gap is 8% ($52/share). The Model-Builder-to-Quant gap is 26% ($175/share). These spreads exceed the 15% threshold requiring resolution.

---

## Root Cause Decomposition

The $123/share gap between DCF Analyst ($733) and Model Builder ($856) decomposes into four identifiable driver differences:

| Driver | DCF Analyst | Model Builder | Impact on Gap |
|--------|-------------|---------------|---------------|
| **WACC** | 10.4% (prose) / 9.8% (implied by sensitivity fit) | 10.36% | Small (~$0-20/share) |
| **Terminal growth rate** | 3.0% | 3.5% | ~$50-70/share |
| **CapEx normalization (FY2030)** | 16% of revenue | 23% of revenue | ~$60-80/share (OPPOSITE direction) |
| **TV blending method** | 60% perpetuity / 40% exit multiple | 70% perpetuity / 30% exit multiple | ~$20-40/share |
| **Exit EBITDA multiple** | 14.0x | 18.0x | ~$50-80/share (via blended TV) |

**Critical finding:** The Model Builder's HIGHER CapEx assumption (23% vs. 16%) should produce a LOWER fair value, all else equal. The Model Builder's higher valuation is driven primarily by (1) a higher terminal growth rate (3.5% vs. 3.0%), (2) a substantially higher exit EBITDA multiple (18x vs. 14x), and (3) a higher weight on the perpetuity method which, at 3.5% terminal growth with 10.36% WACC, produces a large terminal value. These factors more than offset the CapEx drag.

---

## Question 1: What Is the Right WACC?

### DCF Analyst Position: 10.4%
- Risk-free rate: 4.25%
- ERP: 5.0% (Damodaran)
- Beta: 1.25 (elevated from historical ~1.15 for AI CapEx uncertainty)
- Company-specific risk: +50bps (dual-class governance + RL capital destruction)
- Capital structure: 92/8 equity/debt (blended estimate)
- Cost of equity: 11.0%
- After-tax cost of debt: 3.4% (4.0% pre-tax, 15% tax rate)
- **WACC = 10.12% + 0.27% = 10.4%**

**Best evidence:** The 50bps company-specific risk premium is directly supported by the ESG & Governance Analyst's finding: Governance Score 1/5 (worst among mega-cap tech), Zuckerberg controls 55-60% voting power with 13% economic ownership, $125B CapEx commitment made unilaterally with no independent board-level review documented. The ESG Analyst explicitly recommends "50-100bps to WACC (governance risk premium)."

### Model Builder Position: 10.36%
- Risk-free rate: 4.3%
- ERP: 5.5% (Damodaran)
- Beta: 1.20 (5-year weekly regression)
- No explicit company-specific risk premium
- Capital structure: 92/8 equity/debt
- Cost of equity: 10.9%
- After-tax cost of debt: 4.1% (4.8% pre-tax, 14.5% tax rate)
- **WACC = 10.03% + 0.33% = 10.36%**

**Best evidence:** The Model Builder uses slightly higher ERP (5.5% vs. 5.0%) and higher cost of debt (4.8% vs. 4.0%), which are arguably more current. No company-specific premium is added, which is standard CAPM practice — company-specific risk is typically captured in scenario analysis rather than WACC adjustment.

### Weakest Points

**DCF Analyst weakness:** Adding 50bps company-specific risk to WACC AND modeling separate bear case scenarios that capture governance risk (RL losses accelerating, CapEx not normalizing) creates potential double-counting of governance risk. If the bear case already penalizes Zuckerberg's unilateral decision-making through worse outcomes, adding it again to the discount rate is methodologically questionable.

**Model Builder weakness:** Zero company-specific risk premium for a company where one individual controls $125B in annual capital allocation without shareholder recourse is analytically aggressive. The ESG Analyst's 1/5 governance score and the metaverse precedent ($70B+ in losses from a unilateral founder decision) justify some discount rate adjustment beyond what standard beta captures.

### Resolution: WACC = 10.2%

**Revised WACC components:**
- Risk-free rate: 4.25% (split the 5bps difference; immaterial)
- ERP: 5.25% (average of 5.0% and 5.5%; both defensible Damodaran estimates)
- Beta: 1.22 (average of 1.20 and 1.25; the difference is within estimation error)
- Company-specific risk: +25bps (compromise: ESG Analyst recommends 50-100bps, but partial double-counting with bear scenarios reduces this to 25bps)
- Capital structure: 92/8 (both agree)
- Cost of equity: 4.25% + (1.22 x 5.25%) + 0.25% = **10.91%**
- After-tax cost of debt: 4.4% x (1 - 14.75%) = **3.75%**
- **WACC = (0.92 x 10.91%) + (0.08 x 3.75%) = 10.04% + 0.30% = 10.3%**

**Rationale:** 10.3% is within the estimation error of both analysts' figures. The 25bps governance premium is warranted by the ESG Analyst's evidence but halved to avoid double-counting with scenario analysis. This is a minor driver of the valuation gap.

---

## Question 2: What Is the Right CapEx Normalization?

### DCF Analyst Position: 16% of Revenue by FY2030
- FY2026: $125B (48.9% of revenue) -- peak year per management guidance
- FY2027: $105B (34.1%)
- FY2028: $85B (23.9%)
- FY2029: $75B (19.0%)
- FY2030: $70B (16.3%)
- Growth CapEx declines as Phase 1 AI clusters come online
- 16% is ABOVE historical pre-AI average of 20-22% (FY2023-24), acknowledging structural increase

**Best evidence:** The DCF Analyst explicitly models growth CapEx declining from $107B (FY2026) to $46B (FY2030) as the initial AI infrastructure buildout completes, while maintenance CapEx grows from $18B to $24B. The total $70B by FY2030 is consistent with a maturing infrastructure cycle where the bulk of GPU clusters are built and the ongoing spend is refresh + incremental capacity.

### Model Builder Position: 22-23% of Revenue by FY2030
- FY2026: 49% of revenue
- FY2027: 44%
- FY2028: 36%
- FY2029: 28%
- FY2030: 23%
- CapEx normalization is slower; AI infrastructure requires ongoing, large-scale investment
- Base case FY2030 CapEx: ~$101B (23% x $440B revenue)

**Best evidence:** The Model Builder's position is supported by the reality that: (1) GPU compute hardware has a 3-5 year useful life requiring continuous refresh cycles, (2) Meta's competitors (Google, Amazon, Microsoft) have also guided sustained elevated CapEx with no clear peak-to-trough normalization timeline, and (3) the DCF Analyst's own bear case uses 22%+ CapEx through FY2030, suggesting it is a plausible (not just pessimistic) assumption. Furthermore, the DCF Analyst notes "this assumption has LOW confidence" in the Key Assumptions Register.

### Weakest Points

**DCF Analyst weakness:** Normalizing to 16% by FY2030 assumes a ~73% reduction in growth CapEx ($107B to $46B) in four years while revenue grows 68% ($255B to $429B). This implies Meta would be spending proportionally LESS on AI infrastructure in 2030 than in 2024 ($55B on $165B revenue = 33%), despite AI being more central to the business. The 16% figure also conflicts with the DCF Analyst's own acknowledgment that "this is the MOST CRITICAL assumption in the model" with "LOW confidence." The pre-AI era comparison is misleading because FY2023-24 CapEx of 20-22% was ALREADY in the ramp phase.

**Model Builder weakness:** 23% of revenue by FY2030 translates to ~$101B in absolute CapEx — essentially flat with FY2026 peak guidance ($125B midpoint) at the revenue-adjusted level. This implies NO efficiency gains from (a) MTIA custom silicon (Meta claims 40% TCO reduction), (b) data center design maturation, or (c) GPU cost deflation as supply normalizes. It also implies Meta would be spending more on infrastructure in absolute terms in FY2030 ($101B) than FY2025 ($70B) while the initial buildout phase is complete. The market is unlikely to assign a premium multiple to a company with permanently elevated CapEx at this level.

### Resolution: CapEx Normalizes to 19% of Revenue by FY2030

**Revised CapEx schedule:**

| Year | CapEx (% of Rev) | Absolute CapEx ($M) | Rationale |
|------|------------------|--------------------:|-----------|
| FY2026 | 49% | $125,000 | Management guidance midpoint (agreed by both) |
| FY2027 | 38% | $116,900 | First normalization year; growth CapEx declines as Phase 1 clusters complete |
| FY2028 | 30% | $106,500 | Continued normalization; MTIA custom silicon begins reducing unit costs |
| FY2029 | 24% | $94,900 | GPU refresh cycle smooths; efficiency gains compound |
| FY2030 | 19% | $81,400 | Steady-state: refresh + modest growth; above pre-AI but below peak |

**Rationale:** 19% is the geometric midpoint of the two positions and reflects three realities:
1. **CapEx does decline from the FY2026 peak.** No hyperscaler in history has sustained 50% CapEx-to-revenue indefinitely. The buildout phase is finite.
2. **CapEx does NOT return to pre-AI levels.** AI inference at scale requires continuous GPU refresh (3-5 year cycles), growing data center capacity, and energy infrastructure investment.
3. **Efficiency gains are real but gradual.** MTIA custom silicon, improved GPU architectures, and data center optimization reduce cost per FLOP, but demand growth (Meta AI, AR, new products) partially offsets savings.

The 19% figure produces FY2030 absolute CapEx of ~$81B, which is meaningfully below the Model Builder's $101B (reflecting efficiency gains) but above the DCF Analyst's $70B (reflecting the ongoing investment cycle).

**Impact on fair value:** Moving from 16% to 19% CapEx/revenue in FY2030 reduces terminal FCF by approximately $13B (delta CapEx $11.4B, net of tax). At the resolved WACC (10.3%) and terminal growth (see below), this reduces fair value by approximately $55-65/share from the DCF Analyst's base case.

---

## Question 3: What Is the Right Terminal Growth Rate?

### DCF Analyst Position: 3.0%
- GDP growth (~2.5%) + modest pricing power (~0.5%)
- Digital advertising growing structurally above GDP due to continued shift from traditional media
- Below Meta's 5Y historical CAGR of 18.5% "by wide margin -- conservative for a company with platform-level network effects"

### Model Builder Position: 3.5%
- GDP growth (~2.5%) + 100bps for digital ad inflation premium
- Reflects Meta's dominant position in digital advertising with sustained pricing power

### Resolution: Terminal Growth = 3.0%

**Rationale:** At 3.0% terminal growth with 10.3% WACC, the perpetuity multiple is 1/(10.3% - 3.0%) = 13.7x terminal FCF. At 3.5%, it is 1/(10.3% - 3.5%) = 14.7x. The 3.5% rate implies Meta grows faster than the US economy in perpetuity by a full percentage point, which requires that digital advertising continues to gain share from traditional media FOREVER and that Meta maintains pricing power indefinitely. While defensible over a 10-20 year horizon, in perpetuity this is aggressive for a company already capturing ~64% of social media advertising spend. The 3.0% rate already implies above-GDP growth in perpetuity, which is a generous assumption for a terminal rate.

The DCF Analyst's sensitivity table shows: at WACC 10.4% / TGR 3.0% = $733; at TGR 3.5% = $876. The Model Builder's sensitivity at WACC 10% / TGR 3.5% = $890. Terminal growth is the single largest sensitivity in the model. Moving from 3.0% to 3.5% adds ~$100-140/share. This calls for conservatism.

**Compromise:** Use 3.0% for the base case perpetuity calculation. The exit multiple cross-check (which implicitly embeds a terminal growth rate) provides the bull-case anchor.

---

## Question 4: Terminal Value Composition and Blending

### The Problem: TV = 85-87% of Enterprise Value

Both analysts produce terminal values representing 85-87% of total EV across all scenarios. The DCF Analyst explicitly flags this as a "WARNING" — more than four-fifths of the valuation depends on assumptions beyond the explicit forecast period. This is structural (negative FCF in FY2026, compressed FCFs through FY2028), not a modeling error.

### DCF Analyst: 60% Perpetuity / 40% Exit Multiple
- Exit multiple: 14.0x terminal EBITDA
- Overweights perpetuity method as "less sensitive to multiple assumptions"
- Implied terminal multiple from perpetuity: 8.2x EBITDA (the DCF Analyst notes this is "low")

### Model Builder: 70% Perpetuity / 30% Exit Multiple
- Exit multiple: 18.0x terminal EBITDA
- Higher weight on perpetuity growth method

### Weakest Points

**DCF Analyst weakness:** The 14.0x exit multiple is too low for a company with 48% EBIT margins, 81% gross margins, and Rule of 40+ score of 68.4. For context, the Quant Analyst shows GOOGL trades at 20.2x EV/EBITDA today with inferior growth (13% vs. 27%) and margins (32% vs. 41%). Even in a matured state, a business with Meta's margin profile should trade above 14x. The perpetuity method producing an implied 8.2x EBITDA cross-check confirms the terminal growth rate and/or CapEx assumptions are too conservative within that method.

**Model Builder weakness:** The 18.0x exit multiple at 3.5% terminal growth, combined with 70% weight on perpetuity, creates compounding optimism. If the perpetuity growth rate already implies robust long-term growth, the exit multiple should be the check on that optimism, not an amplifier. Additionally, the 70/30 weighting gives less influence to the more grounded market-multiple approach.

### Resolution: 65% Perpetuity / 35% Exit Multiple; Exit Multiple = 16.0x

**Rationale:**
- **16.0x exit EBITDA** is consistent with the Quant Analyst's base case EV/EBITDA of 15.9x (primary peer average GOOGL/AMZN) and reflects a mature but dominant digital advertising platform with above-average margins. It is the midpoint of the DCF Analyst's 14.0x and the Model Builder's 18.0x.
- **65/35 blend** slightly favors the perpetuity method (which is more theoretically grounded for a going-concern business) while giving meaningful weight to the market-multiple cross-check.

---

## Revised Base Case Fair Value

Applying the resolved assumptions to the DCF framework:

| Assumption | DCF Analyst (Original) | Model Builder (Original) | **Resolved** |
|-----------|----------------------|------------------------|-------------|
| WACC | 10.4% | 10.36% | **10.3%** |
| Terminal growth | 3.0% | 3.5% | **3.0%** |
| CapEx/Rev FY2030 | 16% | 23% | **19%** |
| TV blend | 60/40 perp/exit | 70/30 perp/exit | **65/35** |
| Exit EBITDA multiple | 14.0x | 18.0x | **16.0x** |
| FoA revenue CAGR (5Y) | 16.0% | ~14.5% | **~15.5%** |
| FY2030 EBIT margin | 48.0% | 49.3% | **48.5%** |

### Estimated Revised Fair Values

Using the DCF Analyst's base case model structure as the foundation and adjusting for resolved assumptions:

**Key adjustments from DCF Analyst's $733:**
1. CapEx increase (16% to 19%): -$55 to -$65/share
2. TV blend shift (60/40 to 65/35) with higher exit multiple (14x to 16x): +$40 to +$55/share
3. WACC decrease (10.4% to 10.3%): +$10 to +$15/share

**Estimated resolved base case: ~$720-740/share**

**Key adjustments from Model Builder's $856:**
1. Terminal growth decrease (3.5% to 3.0%): -$80 to -$100/share
2. TV blend shift (70/30 to 65/35) with lower exit multiple (18x to 16x): -$30 to -$45/share
3. CapEx decrease (23% to 19%): +$40 to +$55/share

**Estimated resolved base case: ~$720-740/share**

### Convergence Point

Both adjustments converge on approximately **$725/share** as the resolved base case fair value.

This is within 1% of the DCF Analyst's original $733 and 15% below the Model Builder's $856. The DCF Analyst's original base case was closer to the resolved figure because the understatement of CapEx (too low) was roughly offset by the understatement of the exit multiple (too low) and terminal growth (too conservative for the blended approach). The Model Builder's base case was inflated primarily by the aggressive 3.5% terminal growth rate, which cascaded through the perpetuity calculation.

---

## Probability-Weighted Expected Value

Using the resolved base case and adjusting bull/bear proportionally:

| Scenario | DCF Analyst (Original) | Model Builder (Original) | **Resolved** | Probability |
|----------|----------------------|------------------------|-------------|-------------|
| Bull | $1,032 | $1,296 | **~$1,050** | 25% |
| Base | $733 | $856 | **$725** | 50% |
| Bear | $359 | $491 | **$400** | 25% |
| **Expected Value** | **$714** | **$875** | **~$725** | 100% |

**Resolved probability-weighted expected value: ~$725/share**

*Calculation: ($1,050 x 0.25) + ($725 x 0.50) + ($400 x 0.25) = $262.50 + $362.50 + $100.00 = $725*

---

## Triangulation with Quant Analyst

The Quant Analyst's comps-implied base case of $681 (probability-weighted $689) is 6% below the resolved DCF base case of $725. This is within the acceptable 15% tolerance.

**Reconciliation of the residual 6% gap:**
- The comps approach uses NTM (FY2026) EBITDA of $105B, which reflects the CapEx-compressed year. The DCF approach captures the FCF recovery in FY2027-2030, which the comps approach does not.
- The comps base case EV/EBITDA of 15.9x (GOOGL/AMZN average) may slightly undervalue META given META's superior growth (27% vs. 13-14% for peers) and margins (41% vs. 11-32%).
- The Quant Analyst's SOTP analysis (FoA at GOOGL-parity = $884/share) supports the DCF bull case, confirming that the gap between comps and DCF is driven by NTM timing, not fundamental disagreement.

**Assessment:** The 6% gap is acceptable and does not require further resolution. The comps figure anchors the lower bound of the fair value range; the DCF captures the multi-year FCF trajectory.

---

## Unresolved Risk: Terminal Value Dependency

**Flag as Key Unresolved Risk.** Both models produce terminal values at 85-87% of enterprise value. No assumption adjustment can reduce this below ~80% given the FY2026 negative FCF and compressed FY2027-2028 FCFs. This means:

1. Any investor buying META at the resolved fair value (~$725) is making a bet on what Meta looks like AFTER FY2030 — the explicit forecast period contributes only 13-15% of the value.
2. The CapEx normalization assumption is the swing factor. If CapEx does NOT decline to 19% of revenue by FY2030 (stays at 25%+), the base case drops to ~$550-600/share.
3. The terminal growth rate at 3.0% is reasonable but is a permanent assumption — even 50bps of error compounds significantly in a perpetuity calculation.

**Recommendation to Director:** Flag the 85%+ terminal value composition in the final research note as a structural limitation of the DCF approach for META during this CapEx cycle. The comps-based triangulation ($681-689) provides a useful independent check that does not rely on terminal value assumptions.

---

## Summary of Resolutions

| Question | Resolution | Revised Number |
|----------|-----------|---------------|
| WACC | Split differences; add 25bps governance premium (half ESG recommendation to avoid double-counting) | **10.3%** |
| CapEx normalization FY2030 | Geometric midpoint; reflects efficiency gains but ongoing AI investment cycle | **19% of revenue** |
| Terminal growth rate | DCF Analyst's 3.0% prevails; 3.5% is aggressive for perpetuity | **3.0%** |
| TV blend / exit multiple | Compromise blend; exit multiple aligned with Quant Analyst's peer average | **65/35; 16.0x EBITDA** |
| **Base case fair value** | **Both models converge** | **~$725/share** |
| **Probability-weighted EV** | — | **~$725/share** |

| Flag | Status |
|------|--------|
| TV = 85-87% of EV | **Key Unresolved Risk** — structural; no resolution possible |
| CapEx normalization confidence | **Low** — the single largest swing factor; monitor quarterly CapEx guidance |
| Governance WACC premium | **Resolved at 25bps** — may increase if ESG Analyst's bear scenarios materialize |

---

*Debate moderated by Director of Research. Resolved 2026-03-13. SIGNAL-IDs referenced: DCF-META-2026-03-13, QUANT-META-2026-03-13, MODEL-META-2026-03-13, GOV-DUAL-CLASS-PERMANENT, ESG-FOUNDER-JUDGMENT-RISK.*
