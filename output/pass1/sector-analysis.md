# Sector Analysis: Advanced Micro Devices (AMD)

**Analyst:** Sector Analyst
**Date:** 2026-03-09
**Sectors Covered:** AI Accelerators, Server CPUs, Client PC Processors, FPGA/Embedded, Gaming Semiconductors

---

## 1. Sector Definition and Scope

AMD operates across five distinct semiconductor sub-sectors. Analyzing "semiconductors" as a monolith is useless — each sub-sector has fundamentally different growth dynamics, competitive structures, and value chain economics.

| Dimension | AI Accelerators | Server CPU | Client PC | FPGA/Embedded | Gaming Semi |
|-----------|----------------|-----------|-----------|---------------|-------------|
| **GICS Classification** | 4530 (Semiconductors) | 4530 (Semiconductors) | 4530 (Semiconductors) | 4530 (Semiconductors) | 4530 (Semiconductors) |
| **Geographic Scope** | Global | Global | Global | Global | Global |
| **TAM 2025 ($M)** | $140,000M (GPU only) `[Source: Bloomberg Intelligence/ESTIMATED, Tier 6]` | $42,000M `[Source: Mercury Research/ESTIMATED, Tier 6]` | $85,000M `[Source: IDC/ESTIMATED, Tier 6]` | $12,000M `[Source: ESTIMATED]` | $18,000M `[Source: ESTIMATED]` |
| **TAM CAGR (5Y, base)** | 22.0% `[ESTIMATED]` | 8.0% `[ESTIMATED]` | 5.0% `[ESTIMATED]` | 7.0% `[ESTIMATED]` | 4.0% `[ESTIMATED]` |
| **AMD Revenue Exposure** | ~$12,000M (MI-series GPU) | ~$10,000M (EPYC) | ~$10,640M (Ryzen) | ~$3,454M (Xilinx) | ~$3,910M (semi-custom + Radeon) |
| **AMD Share** | ~10% | ~37% (revenue ~41%) | ~27% | ~28% | ~12% |

`[ASSUMPTION: TAM sourced from WSTS, Bloomberg Intelligence, Mercury Research, IDC. Third-party TAM estimates have a historical tendency to overstate by 20-40% in growth sectors and understate by 10-20% in mature sectors.]`

**Total global semiconductor market:** $772B in 2025, projected to approach $975B in 2026 (+25%) per WSTS. The industry is approaching $1T driven primarily by AI-related applications. `[Source: WSTS — Tier 5, retrieved 2026-03-09]`

---

## 2. Sector Growth Model

### Growth Driver Decomposition

#### AI Accelerator Market (AMD's highest-growth segment)

| Growth Driver | Current Contribution | 5-Year Trend | Sensitivity |
|--------------|---------------------|-------------|-------------|
| Volume / unit growth | 40% of total growth | Accelerating | High |
| Pricing / ASP growth | 25% of total growth | Stable (HBM, advanced node inflation) | Medium |
| Mix shift (training → inference) | 20% of total growth | Accelerating | High |
| Geographic expansion (sovereign AI) | 5% of total growth | Accelerating | Medium |
| New use cases (edge AI, agents) | 8% of total growth | Accelerating | High |
| M&A / consolidation | 2% of total growth | Stable | Low |

**Key observation:** Volume and mix shift are the dominant drivers. The shift from training to inference workloads materially benefits AMD — MI350/MI450 compete more effectively on inference (40% better tokens-per-dollar vs NVIDIA B200) than training where CUDA's software optimization creates a wider gap.

#### Server CPU Market

| Growth Driver | Current Contribution | 5-Year Trend | Sensitivity |
|--------------|---------------------|-------------|-------------|
| Volume / unit growth | 30% of total growth | Stable | Medium |
| Pricing / ASP growth | 20% of total growth | Stable (higher core counts) | Medium |
| Mix shift (higher-core, multi-socket) | 25% of total growth | Accelerating | Medium |
| Geographic expansion (India, SE Asia DC) | 10% of total growth | Accelerating | Medium |
| New use cases (AI-adjacent CPU workloads) | 10% of total growth | Accelerating | High |
| M&A / consolidation | 5% of total growth | Stable | Low |

#### Client PC Market

| Growth Driver | Current Contribution | 5-Year Trend | Sensitivity |
|--------------|---------------------|-------------|-------------|
| Volume / unit growth | 35% of total growth | Accelerating (Win10 EOL refresh) | Medium |
| Pricing / ASP growth | 15% of total growth | Stable | Low |
| Mix shift (AI PCs with NPUs) | 30% of total growth | Accelerating | High |
| Geographic expansion | 10% of total growth | Stable | Low |
| New use cases (on-device AI) | 8% of total growth | Accelerating | Medium |
| M&A / consolidation | 2% of total growth | Stable | Low |

### Adoption Curve Analysis — AI Accelerators

| Stage | Description | Current Penetration | Implied Remaining Runway |
|-------|------------|--------------------:|--------------------------|
| Innovators (0-2.5%) | Research labs, early hyperscaler testing | Completed (2018-2021) | -- |
| Early Adopters (2.5-16%) | Hyperscaler training buildout | Completed (2021-2024) | -- |
| Early Majority (16-50%) | Enterprise AI, inference at scale | **~30% penetration** | 3-4 years |
| Late Majority (50-84%) | Mid-market enterprise, edge deployment | Not yet | 5-8 years |
| Laggards (84-100%) | SMB, legacy replacement | Not yet | 8+ years |

**Current position on S-curve:** Early Majority phase, ~30% enterprise penetration. The market is past the uncertainty phase but well before saturation. This is the highest-growth phase of the adoption curve.

`[ASSUMPTION: Penetration rate of 30% based on hyperscaler capex growth trajectory and enterprise survey data. TAM denominator defined as Fortune 2000 companies with compute budgets >$10M annually. Enterprise penetration estimates vary widely — Gartner estimates 25%, McKinsey estimates 35%.]`

**Inflection risk:** Training compute scaling laws may plateau (as suggested by DeepSeek's efficiency breakthroughs), which would shift value from training GPUs to inference chips. This is a **net positive for AMD** — inference is where AMD's price-performance advantage is strongest.

### Python Growth Model

Executable model saved to: `output/models/amd-sector-growth-model.py`

Key outputs:
- AI GPU TAM: $140B (2025) → $378B (2030, base case, 22% CAGR)
- Custom ASIC TAM: $28B (2025) → $151B (2030, base case, 40% CAGR)
- Server CPU TAM: $42B (2025) → $62B (2030, base case, 8% CAGR)
- Total semi TAM: $772B (2025) → $1,361B (2030, base case, 12% CAGR)

---

## 3. Competitive Structure

### 3.1 AI GPU Market Share Landscape

| Rank | Company | Market Share (2025) | Share Trend (3Y) | Revenue ($M, est.) | Margin vs. Sector |
|------|---------|:-------------------:|:---------------:|:-------------------:|:-----------------:|
| 1 | NVIDIA | ~82% | -5pp (from 92%) | ~$114,800M | Far above (75% GM) |
| 2 | AMD | ~10% | +5pp (from 5%) | ~$14,000M | Above (57% GM) |
| 3 | Custom ASICs (aggregate) | ~6% | +4pp (from 2%) | ~$8,400M | N/A (internal) |
| 4 | Others (Intel Gaudi, startups) | ~2% | +1pp | ~$2,800M | Below |
| **Total** | | **100%** | | **~$140,000M** | |

`[ESTIMATED from Bloomberg Intelligence, TrendForce, TechNetBooks Q4 2025. Revenue-weighted shares. Unit shares differ.]`

**NVIDIA's moat:** CUDA ecosystem (6M developers, 300+ libraries, 600+ AI models). Software lock-in creates a 30-99% effective performance advantage across benchmarks even where AMD hardware matches or exceeds specs. `[Source: AIM Multiple — Tier 6]`

**AMD's wedge:** Price-performance in inference. MI355X delivers 40% more tokens per dollar than B200. The MI450/Helios architecture targets rack-scale economics with 50% more memory than NVIDIA Vera Rubin. The OpenAI and Meta mega-deals (12 GW combined) validate AMD as a credible second source.

### 3.2 Server CPU Market Share Landscape

| Rank | Company | Market Share (2025) | Share Trend (3Y) | Revenue ($M, est.) | Margin vs. Sector |
|------|---------|:-------------------:|:---------------:|:-------------------:|:-----------------:|
| 1 | Intel Xeon | ~58% (unit: 71%) | -16pp (from 78%) | ~$24,335M | Below (30% GM) |
| 2 | AMD EPYC | ~35% (unit: 29%) | +15pp (from 20%) | ~$14,524M | Above (57% GM) |
| 3 | Arm-based (Graviton, Ampere) | ~8% (unit: ~21%) | +6pp (from 2%) | ~$3,142M | Varies |
| **Total** | | **100%** | | **~$42,000M** | |

`[ESTIMATED: Blended from Mercury Research (unit share) and revenue-based estimates. AMD revenue share exceeds unit share because EPYC commands higher ASPs than Xeon. Arm unit share inflated by NVIDIA DGX Grace systems counted as Arm server CPUs. Source: Mercury Research Q4 2025, The Register, Fusion Worldwide — Tier 3-6]`

**Note on unit vs. revenue share:** Mercury Research reports AMD at 28.8% unit share (Q4 2025), but AMD's revenue share in servers was 41% in Q2 2025. The discrepancy reflects EPYC Turin's premium pricing — higher core counts and advanced node advantage command 30-50% ASP premiums over comparable Xeon.

### 3.3 Concentration Analysis

| Metric | AI GPU Market | Server CPU Market | Client PC CPU |
|--------|:------------:|:-----------------:|:-------------:|
| HHI (Herfindahl-Hirschman) | 6,864 | 4,609 | 5,378 |
| CR2 (top 2 share) | 92% | 93% | 95% |
| Material players (>5% share) | 2 | 2 | 2 |
| New entrants (last 3Y) | Custom ASICs, Intel Gaudi | Arm (Graviton, Ampere) | Qualcomm Snapdragon X |
| Exits / M&A (last 3Y) | -- | -- | -- |
| **Trend** | Moderating concentration | Moderating concentration | Beginning to fragment |

All three key markets are **highly concentrated** (HHI > 2,500). The AI GPU market is a near-duopoly but concentration is declining as custom ASICs gain ground. Server CPU is transitioning from Intel monopoly to AMD-led duopoly with Arm as an emerging third force.

**Key dynamic:** In concentrated markets with falling HHI, the share gainer (AMD) typically benefits from both market growth and share gains — a double tailwind. This is AMD's current structural position in all three of its largest addressable markets.

### Market Share Shift Model

Executable model saved to: `output/models/amd-sector-share-model.py`

**Projected share evolution (base case):**

| Market | AMD 2025 | AMD 2027 | AMD 2030 | Direction |
|--------|:--------:|:--------:|:--------:|:---------:|
| AI GPU | 10.0% | 13.9% | 18.8% | Gaining ~2.5pp/year |
| Server CPU | 34.6% | 42.0% | 48.9% | Gaining ~5pp/year, decelerating at ~50% |
| Client PC | 27.0% | 31.1% | 36.7% | Gaining ~2.5pp/year |

**AMD combined revenue projection (base case):** $34.6B (FY2025 actual) → $170B by 2030. Model output exceeds management's >35% CAGR target of ~$155B.

`[ASSUMPTION: Share gains assume current product cadence continues (EPYC Turin → Venice, MI350 → MI450 → MI500). Delays or execution failures would materially slow share gains. Ceiling applied at 55% for any single market.]`

---

## 4. Regulatory Environment

### Current Regulatory Framework

| Regulation | Jurisdiction | Impact on Sector | Affected Companies | Status |
|-----------|:------------|:----------------|:-------------------|:-------|
| U.S. CHIPS Act ($52.7B) | U.S. | Positive — subsidizes domestic fab construction | Intel, TSMC (AZ), Samsung (TX), GlobalFoundries | Enacted 2022, funds deploying through 2027 |
| EU Chips Act (€86B target) | EU | Positive — subsidizes EU fab expansion | TSMC (Dresden), Intel (Magdeburg), GlobalFoundries | Enacted 2023, Chips Act 2.0 proposed Q1 2026 |
| U.S. Export Controls (AI chips to China) | U.S. | **Negative for AMD** — $1.5-1.8B FY2025 revenue impact | AMD, NVIDIA, Intel | Evolving — Jan 2026 rule shift to case-by-case licensing |
| 25% Semiconductor Tariff (Section 232) | U.S. | Negative — increases import costs | All fabless companies (AMD, NVIDIA, Qualcomm) relying on TSMC | Announced Jan 2026 |
| Japan/Korea chip equipment restrictions | Japan, S. Korea | Neutral for AMD | Equipment makers (Tokyo Electron, ASML) | Implemented 2024-2025 |

### Pending Regulatory Actions

| Action | Status | Expected Timeline | Probability | Impact if Enacted |
|--------|:-------|:------------------|:------------|:-----------------|
| SAFE Chips Act (tighter China controls) | Proposed in Congress | 2026-Q3 | 40% | Revenue: -$2-5B for AMD; blocks all AI chip exports to China |
| EU Chips Act 2.0 revision | Commission proposal | 2026-Q1 | 70% | Neutral — targets EU fab capacity, not design |
| TSMC tariff exemption (advanced packaging) | Under review | 2026-H1 | 50% | Positive if exempted — reduces cost for AMD/NVIDIA |
| China retaliatory restrictions (rare earths) | Escalation risk | Ongoing | 25% | Negative — gallium/germanium supply disruption |

### Regulatory Trend Assessment

| Dimension | Direction | Evidence |
|-----------|:---------:|---------|
| Overall regulatory intensity | **Increasing** | Three new export control rules in 18 months; Section 232 tariffs |
| Compliance cost trend | **Rising** | AMD took $800M inventory charge; 15% revenue fee on MI308 China exports |
| Barrier-to-entry impact | **Rising barriers** | CHIPS Act subsidies favor incumbents; export controls limit market access for new entrants |
| Antitrust scrutiny | Stable | No significant antitrust actions in AI chips |
| Cross-border regulatory convergence | **Diverging** | U.S., EU, Japan imposing unilateral restrictions; China building parallel ecosystem |

**Net regulatory assessment for AMD: Net Negative.** AMD's fabless model means it cannot directly benefit from CHIPS Act manufacturing subsidies (which flow to Intel and TSMC). Meanwhile, export controls have already cost AMD $1.5-1.8B in FY2025 revenue and could worsen. The January 2026 shift to case-by-case licensing offers marginal relief (MI325X exports now possible) but uncertainty remains high. China was 24% of AMD's FY2024 revenue — now guided at ~$100M/quarter. The 25% Section 232 semiconductor tariff directly raises AMD's input costs since all AMD chips are manufactured at TSMC (Taiwan, which is a tariff target). AMD bears regulatory cost without receiving regulatory subsidy.

---

## 5. Value Chain Analysis

### Semiconductor Value Chain (AI Accelerator Focus)

```
[IP/Design]  →  [Foundry/Fab]  →  [Packaging]  →  [System Integration]  →  [Cloud/End User]
  35-75% GM       50-60% GM        25-40% GM         15-25% GM              Varies
  $200B+ pool     $120B+ pool      $40B+ pool        $80B+ pool             N/A
```

| Value Chain Position | Gross Margin Range | Key Players | Margin Trend | AMD Position |
|---------------------|:-----------------:|:-----------|:------------|:------------|
| IP / Chip Design (fabless) | 55-75% | NVIDIA, AMD, Qualcomm, Broadcom | Expanding (AI premium) | **HERE — 57% GM** |
| Foundry / Manufacturing | 50-60% | TSMC, Samsung, Intel Foundry | Stable-Expanding | Not here (fabless) |
| Advanced Packaging (CoWoS, HBM) | 25-40% | TSMC, ASE, Amkor, SK Hynix | Expanding (supply-constrained) | Not here (TSMC dependency) |
| Memory (HBM) | 30-50% | SK Hynix, Samsung, Micron | Expanding (HBM scarcity) | Not here |
| System Integration (servers, racks) | 15-25% | Dell, HPE, Supermicro, ODMs | Compressing | Not here (Helios = partial entry) |
| Software / Ecosystem | 80-90% | NVIDIA (CUDA), AMD (ROCm) | Stable | **Partial — ROCm maturing** |

**Value migration assessment:** Value is migrating **upstream** toward chip design and advanced packaging. The shift to AI accelerators has increased the design-stage margin pool dramatically — NVIDIA's 75% gross margin reflects the value accruing to chip architects who control the AI compute stack. AMD at 57% gross margin sits in the second-highest margin pool.

**Critical dependency — TSMC:** AMD is 100% dependent on TSMC for leading-edge manufacturing (3nm for MI450, 4nm for MI350, 5nm for EPYC Turin). This creates three risks:

1. **Capacity allocation:** TSMC CoWoS capacity is fully booked through 2026. NVIDIA has ~60% allocation, Broadcom ~15%. AMD must compete for the remaining ~25% with all other customers. At 12 GW of committed deployment (OpenAI + Meta), AMD's TSMC capacity requirements will increase dramatically in 2026-2027.

2. **Pricing power:** TSMC raised advanced node prices 5-8% in 2025 and is expected to raise again in 2026. AMD absorbs this as COGS — unlike Intel, which manufactures internally.

3. **Geopolitical risk:** TSMC's primary fabs are in Taiwan. A cross-strait disruption would halt AMD's entire product line. TSMC's Arizona fabs (expected 2025-2027) provide partial mitigation but are not yet at scale for leading-edge AI chips.

`[Source: TSMC earnings, TrendForce, Digitimes — Tier 3, retrieved 2026-03-09]`

**Disintermediation risk:** Hyperscaler custom ASICs (Google TPU, Amazon Trainium, Microsoft Maia) bypass the GPU design layer entirely, going directly from in-house design to TSMC fabrication. This disintermediates both NVIDIA and AMD for a portion of inference workloads. The offsetting factor: AMD's OpenAI and Meta mega-deals demonstrate that even hyperscalers building custom silicon still need GPU infrastructure. GPUs and ASICs are complementary, not purely substitutional — but the ratio may shift toward ASICs over time.

---

## 6. Secular Trends

| # | Secular Trend | Stage | Impact on AMD | Timeline |
|---|:-------------|:------|:-------------|:---------|
| 1 | AI infrastructure buildout | Early Majority (inflecting) | **Strong tailwind** — Data Center revenue +39% YoY, 12 GW committed | 3-5 years of above-trend growth |
| 2 | Inference scaling (vs. training) | Early | **Tailwind** — AMD's price-performance advantage strongest in inference | 2-4 years to material shift |
| 3 | Cloud/data center expansion | Mature growth | **Tailwind** — EPYC share gains continue | Ongoing |
| 4 | Edge AI / on-device inference | Early Adopters | **Moderate tailwind** — Ryzen AI NPUs, embedded FPGA | 3-5 years |
| 5 | China technology decoupling | Accelerating | **Headwind** — Lost $1.5-1.8B FY2025; further restrictions possible | Ongoing, worsening |

### Trend Detail

**1. AI Infrastructure Buildout — Who Benefits Most**
- **NVIDIA** benefits most today due to CUDA lock-in for training workloads
- **AMD** is the primary beneficiary of the "second source" dynamic — hyperscalers want to avoid NVIDIA monopoly pricing
- **Broadcom/Marvell** benefit from custom ASIC trend
- **Financial magnitude for AMD:** AI GPU revenue could grow from ~$12B (FY2025) to $50-71B by 2030 (base case model)
- **Leading indicators:** Hyperscaler capex announcements, TSMC CoWoS booking rates, MI450 benchmark results

**2. Inference Scaling**
- Training compute may be approaching efficiency plateaus (DeepSeek demonstrated 20x training cost reduction)
- Inference demand is growing faster than training as deployed AI models serve billions of queries
- AMD's MI355X delivers 40% better tokens-per-dollar vs NVIDIA B200 in inference benchmarks
- **Who is most at risk:** NVIDIA — training monopoly is durable but inference competition is intensifying
- **Leading indicators:** Inference-to-training ratio in hyperscaler capex, tokens served per day metrics

**3. Cloud/Data Center Expansion**
- Global data center capacity growing ~15-20% annually
- AMD EPYC is the structural share gainer, benefiting from Intel's multi-generation lag
- **Who is most at risk:** Intel — Xeon losing share on performance AND price
- **Financial magnitude for AMD:** Server CPU revenue could grow from ~$10B to $30B by 2030

**4. Edge AI / On-Device AI**
- Edge AI chip market growing at 21% CAGR ($3.7B in 2025 → $9.5B by 2030)
- AMD positioned via Ryzen AI (NPU-equipped laptop/desktop CPUs) and Xilinx FPGAs
- **Who benefits most:** Qualcomm (mobile inference), NVIDIA (Jetson), AMD (PC inference)
- **Financial magnitude for AMD:** Incremental — ~$2-5B of revenue uplift by 2030 from AI PC premium

**5. China Technology Decoupling**
- U.S. export controls have cost AMD $1.5-1.8B in FY2025 and continue to evolve
- January 2026 rule: case-by-case licensing replaces presumption of denial, but uncertainty remains
- China building parallel AI chip ecosystem (Huawei Ascend) — likely closed to AMD long-term
- **Who is most at risk:** AMD and NVIDIA equally (~20-25% of pre-restriction revenue from China)
- **Financial magnitude for AMD:** $1.5-3B annual revenue at risk, partially offset by MI308 approved exports at 15% fee

---

## 7. Sector Financial Benchmarks

### Profitability Tiers

| Tier | Companies | Rev Growth | Gross Margin | EBITDA Margin | ROIC | Differentiator |
|:-----|:----------|:---------:|:----------:|:-----------:|:---:|:--------------|
| Top quartile | NVIDIA, Broadcom, ASML | >30% | >65% | >50% | >40% | AI monopoly / deep moat |
| Median | AMD, Qualcomm, Marvell | 15-30% | 50-65% | 25-40% | 15-25% | Competitive but scaling |
| Bottom quartile | Intel, GlobalFoundries | <10% | <40% | <15% | <10% | Subscale / restructuring |
| **AMD** | **AMD** | **34% (FY2025)** | **52% (GAAP) / 57% (non-GAAP)** | **~28% (GAAP)** | **~15% [ESTIMATED]** | **Median tier, trending to top** |

**Key observation:** AMD sits in the **median tier** on margins and ROIC, but its 34% revenue growth rate is top-quartile. The margin trajectory is upward as the revenue mix shifts toward higher-margin Data Center (57%+ non-GAAP GM) and away from lower-margin Gaming/Embedded. Management targets 35% operating margin long-term (from ~24% currently). If achieved, AMD would move to the top quartile on profitability.

### Capital Intensity and Returns

| Metric | Sector Median | AMD | Gap | Notes |
|:-------|:-------------|:----|:----|:------|
| CapEx / Revenue | 8-12% (IDMs), 3-5% (fabless) | ~3.5% | At sector median for fabless | Fabless model = low capex |
| R&D / Revenue | 15-20% | ~18% | At median | Appropriate for product breadth |
| Working Capital / Revenue | 15-25% | ~20% [ESTIMATED] | At median | |
| Asset Turnover | 0.4-0.8x | ~0.5x [ESTIMATED] | At median | Xilinx goodwill inflates asset base |
| ROIC | 15-25% (fabless) | ~15% [ESTIMATED] | Below median | Depressed by Xilinx acquisition amortization |
| WACC | 10-12% | ~11% [ESTIMATED] | At median | Beta 2.02 raises equity cost |
| ROIC - WACC Spread | 5-15pp | ~4pp [ESTIMATED] | Below median | Marginal value creator currently |

`[ESTIMATED: ROIC and WACC based on public financial data and beta. Xilinx acquisition (2022) created ~$25B in goodwill that depresses ROIC on an invested capital basis. Excluding goodwill, organic ROIC would be significantly higher.]`

**Implication:** AMD is currently a marginal value creator (ROIC barely exceeds WACC) due to the Xilinx acquisition's goodwill drag. As the AI GPU and EPYC businesses scale, ROIC should expand. The key question: Can AMD scale AI GPU revenue without proportional R&D and marketing investment? The OpenAI/Meta mega-deals suggest yes — committed volume reduces customer acquisition cost.

---

## 8. Supply/Demand Analysis — Advanced Semiconductor Capacity

This section is **critical** for AMD. As a fabless company dependent on TSMC, supply constraints directly limit AMD's revenue growth potential.

### TSMC CoWoS Advanced Packaging (Binding Constraint)

| Metric | Current (Q1 2026) | +1Y (2027) | +3Y (2029) | +5Y (2031) |
|:-------|:------------------:|:----------:|:----------:|:----------:|
| CoWoS Capacity (wafers/month) | ~80,000 | 130,000 (target) | ~200,000 [EST] | ~300,000 [EST] |
| Demand (wafers/month) | >85,000 [EST] | >140,000 [EST] | >220,000 [EST] | Unknown |
| Utilization Rate | >100% (oversubscribed) | ~100% | ~100% | Easing |
| NVIDIA allocation | ~60% | ~55% | ~50% | Declining share |
| AMD allocation | ~8-10% | ~12-15% | ~15-18% | Growing |
| Broadcom allocation | ~15% | ~15% | ~15% | Stable |
| **Balance** | **Extremely tight** | **Tight** | **Tight** | **Easing** |

`[Source: TrendForce, Digitimes, TSMC earnings — Tier 3. TSMC targeting 130,000 CoWoS wafers/month by late 2026, quadrupling from late 2024.]`

### TSMC Leading-Edge Logic (3nm / 2nm)

| Metric | Current | +1Y | +3Y |
|:-------|:-------:|:---:|:---:|
| 3nm utilization | >90% | >90% | Easing (2nm ramp) |
| Key AMD products on 3nm | MI450 (H2 2026) | MI500 series | Next-gen |
| 2nm timeline | — | Risk production 2027 | Volume 2028 |

### HBM Memory Supply

| Metric | 2025 | 2026 | 2027 |
|:-------|:----:|:----:|:----:|
| HBM market size | $30B | $50B+ [EST] | $70B+ [EST] |
| Supply leaders | SK Hynix (~50%), Samsung (~40%), Micron (~10%) | Same | Same |
| AMD HBM needs | HBM3E (MI350) | HBM4 (MI450) | HBM4E |
| **Balance** | Tight | Tight | Easing |

**Pricing power implication:** CoWoS oversubscription through 2026-2027 means TSMC holds pricing power over AMD. AMD cannot ramp AI GPU production faster than TSMC allocates CoWoS capacity. This is the **single most important supply-side constraint** on AMD's near-term revenue growth. NVIDIA's 60% CoWoS allocation provides it with a structural supply advantage. AMD's 12 GW mega-deal commitments may exceed its current TSMC allocation — forcing either: (a) expanded allocation at higher cost, (b) delayed delivery timelines, or (c) outsourcing packaging to OSATs (ASE's CoWoP alternative).

---

## 9. Sector Summary

The semiconductor sector structure is **favorable for AMD but with critical constraints.** AMD is positioned in the right markets (AI accelerators and server CPUs are the two fastest-growing sub-sectors), gaining share in concentrated markets where it is the #2 player, and operating in the highest-margin portion of the value chain (fabless chip design at 57% gross margin).

**The single most important sector dynamic for the investment thesis** is TSMC CoWoS capacity allocation. AMD's ability to fulfill its 12 GW mega-deal commitments (OpenAI + Meta) is supply-constrained, not demand-constrained. If TSMC allocates AMD sufficient CoWoS capacity in 2026-2027, AMD's revenue trajectory accelerates dramatically. If CoWoS remains NVIDIA-dominated at 60% allocation, AMD's AI GPU share gains will be slower than the market expects.

**Structural advantages:** AMD is a share gainer in three concentrated markets simultaneously — a rare position that produces above-market revenue growth even without TAM expansion. The fabless model provides capital efficiency (3.5% capex/revenue vs 25%+ for IDMs) but creates single-source dependency on TSMC. The regulatory environment is net negative (export controls cost more than CHIPS Act subsidies for fabless companies), but manageable.

**Structural risks:** (1) CUDA software moat limits AMD's AI GPU ceiling to ~20-25% without a step-function improvement in ROCm. (2) Custom ASIC growth (44.6% in 2026) could erode the GPU TAM over time, though AMD's mega-deals suggest GPUs and ASICs coexist. (3) TSMC concentration risk — any Taiwan disruption halts AMD's entire product line. (4) The company is attempting to execute at a scale it has never achieved (12 GW deployment), creating meaningful execution risk.

**Is the company in the right tier and right part of the value chain?** Yes. AMD sits in the median profitability tier but is trending toward top-quartile as Data Center mix increases. It occupies the highest-margin value chain position (fabless design). The key question is whether AMD can convert its hardware competitiveness into durable share gains despite NVIDIA's software moat and TSMC's capacity constraints.

---

## Cross-Stock Intelligence Notes Filed

1. `output/notes/AMD-to-NVDA-2026-03-09.md` — AI GPU share shift and inference competitive dynamics
2. `output/notes/AMD-to-INTC-2026-03-09.md` — Server CPU share erosion and two-front competitive squeeze
3. `output/notes/AMD-to-AVGO-2026-03-09.md` — Custom ASIC growth and GPU/ASIC coexistence thesis

---

## Python Models Generated

1. `output/models/amd-sector-growth-model.py` — 5-year TAM forecast for 9 semiconductor sub-sectors, growth driver decomposition, adoption curve analysis, sensitivity tables
2. `output/models/amd-sector-share-model.py` — Market share shift projections for AI GPU, server CPU, and client PC markets; HHI concentration tracking; AMD combined revenue projection

---

## Data Sources

- WSTS Semiconductor Forecast Autumn 2025 [Tier 5]: Global semi market $772B (2025), approaching $975B (2026)
- Bloomberg Intelligence AI Accelerator Market [Tier 6]: $116B (2024), CAGR 16% to $604B by 2033
- TrendForce / Digitimes [Tier 3]: TSMC CoWoS capacity, NVIDIA 60% allocation, fully booked through 2026
- Mercury Research Q4 2025 [Tier 3]: AMD server CPU unit share 28.8%, +3.1pp YoY
- Fusion Worldwide [Tier 3]: AMD server revenue share 41% in Q2 2025
- AMD Q4 FY2025 Press Release [Tier 1]: Revenue $10.3B (+34%), Data Center $5.4B (+39%)
- AMD Q4 FY2025 Transcript [Tier 2]: Lisa Su targets >60% annual DC growth, >35% revenue CAGR
- Grand View Research [Tier 6]: Edge AI market $24.9B (2025), 21.7% CAGR to $118.7B by 2033
- SEMI Europe Chips Act Report [Tier 5]: EU €86B semiconductor investment target by 2030
- BIS Final Rule Jan 2026 [Tier 1]: Case-by-case licensing for AI chips to China replaces presumption of denial
- Tom's Hardware [Tier 3]: AMD MI355X 20% faster than B200, 40% better $/token in inference
- Omdia [Tier 6]: AI data center chip market to hit $286B, custom ASICs gaining ground
