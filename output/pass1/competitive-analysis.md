# Competitive Analysis — AMD (Advanced Micro Devices, Inc.)

**Analyst:** Competitive Analyst
**Date:** 2026-03-09
**Stock:** AMD | $190.40 | Market Cap: ~$310B

---

## 1. Competitive Landscape Map

AMD competes across five distinct arenas, each with different competitors, market structures, and share dynamics. This analysis treats each arena separately before synthesizing an overall competitive score.

---

### Arena 1: Server CPU (EPYC vs. Intel Xeon)

**Market Definition:** x86 data center processors for cloud, enterprise, and HPC servers. Excludes Arm-based alternatives (AWS Graviton, Ampere Altra, NVIDIA Grace) which hold <10% combined share but are growing.

**Market Size:** ~$14B in 2025, projected ~$21-26B by 2031-2033 (6-7% CAGR). AMD management guides "strong double-digit" TAM growth in 2026 driven by AI-adjacent server demand. [Source: Coherent Market Insights, Precedence Research — Tier 6]

| Competitor | Unit Share (Q4 2025) | Revenue Share | Trend |
|-----------|---------------------|---------------|-------|
| **Intel (Xeon)** | ~60-64% | ~59% | Losing 6-8pp/year |
| **AMD (EPYC)** | ~36-40% | ~41% | Gaining steadily; parity possible 2026 |
| **Arm-based (Graviton, Ampere, Grace)** | <5% | <5% | Growing in cloud-native workloads |

[ESTIMATED: Market share based on Mercury Research data cited by Tom's Hardware, Fusion Worldwide. Revenue share based on AMD Q4 2025 earnings + Intel implied. Tier 3-6 sources.]

**Market Structure:** Effective duopoly with nascent Arm entry. HHI ~5,000+ (highly concentrated). AMD has taken share in 18 consecutive quarters since EPYC Rome (2019).

**Key Dynamics:**
- EPYC Turin (5th gen) >50% of AMD server revenue in Q4 2025, delivering up to 40% better performance vs. Intel Xeon in 2P configurations [Source: AMD Q4 earnings call — Tier 2]
- ~1,600 EPYC cloud instances, +50% YoY [Source: AMD IR — Tier 1]
- Intel "more than one generation behind" per industry assessments [Source: Fusion Worldwide — Tier 6]
- Intel's Diamond Rapids (next-gen Xeon) delayed; foundry turnaround under new leadership uncertain
- AMD revenue share (41%) exceeds unit share (36-40%), indicating ASP premium in high-margin segments

**Pricing Power:** Strong. AMD commands premium ASPs in 2P/4P high-performance configs while undercutting Intel on TCO (total cost of ownership). Cloud customers are shifting to AMD for performance-per-watt advantages. AMD has demonstrated ability to raise ASPs through successive EPYC generations without volume loss. [DATA GAP: Exact ASP data not publicly disclosed]

---

### Arena 2: AI GPU / Accelerator (Instinct vs. NVIDIA vs. Custom ASICs)

**Market Definition:** Discrete AI training and inference accelerators for data centers. Includes GPUs and custom ASICs. Excludes general-purpose GPUs for graphics.

**Market Size:** AI accelerator TAM estimates vary widely:
- 2025: ~$126-160B [Source: Bloomberg Intelligence, industry analysts — Tier 6]
- 2026: ~$200-250B (consensus range)
- 2027: ~$280-350B
- 2030: ~$440-650B (narrower definition) to $1T+ (broader AI infrastructure)

[ASSUMPTION: TAM estimates sourced from Bloomberg Intelligence, Fortune Business Insights, Mordor Intelligence, Precedence Research. Third-party TAM estimates frequently overstate by 20-40%. Discount accordingly. Using $200-250B for 2026 as working estimate.]

| Competitor | Share (2025) | Trend | Key Product |
|-----------|-------------|-------|-------------|
| **NVIDIA** | >80% | Lost 1.4pp in Q4 2025 | B200/GB200, Vera Rubin (H2 2026) |
| **AMD** | ~8-12% | Gained 2.6pp in Q4 2025 | MI350/MI355X, MI450 (H2 2026) |
| **Google (TPU)** | ~5-8% (internal) | Expanding; TPU v6e/Ironwood | Internal + cloud customers |
| **Amazon (Trainium)** | ~3-5% (internal) | 500K+ Trainium2 deployed | Internal + AWS customers |
| **Microsoft (Maia)** | ~1-2% (internal) | Maia 200 on TSMC 3nm in 2026 | Internal Azure workloads |
| **Broadcom (custom ASIC)** | Growing | Building for OpenAI, others | Custom designs |

[ESTIMATED: Non-NVIDIA shares based on revenue estimates and analyst commentary. Google/Amazon shares are internal deployment, not open market. Tier 3-6 sources.]

**Market Structure:** Near-monopoly transitioning toward oligopoly. NVIDIA dominance is structural (CUDA ecosystem + NVLink interconnect) but erosion is beginning. Custom ASICs growing 44.6% vs. GPU 16.1% in 2026 — the fastest-growing competitive vector. [Source: CNBC, Bloomberg Intelligence — Tier 3-6]

**AMD's Position:**
- MI350 Series: Fastest ramp in AMD history, deployed at 8/10 top AI companies [Source: AMD Q4 call — Tier 2]
- MI355X benchmarks: 20% faster than B200 in DeepSeek R1 FP4; 30% faster in Llama 3.1 405B; 40% more tokens per dollar [Source: AMD presentations, SemiAnalysis — Tier 3-6]
- MI450/Helios (H2 2026): 72 GPUs = 1.4 exaFLOPS FP8, 31TB HBM4, 260 TB/s scale-up bandwidth
- MI450 specs: ~432 GB HBM4, ~40 PFLOPS FP4, ~19.6 TB/s bandwidth — competitive with NVIDIA Vera Rubin VR200 (288GB HBM4, 50 PFLOPS, 20 TB/s) [Source: SemiAnalysis, Tom's Hardware — Tier 3-6]
- AMD offers 50% more memory capacity than Vera Rubin — meaningful advantage for large model inference
- OpenAI deal: 6 GW, ~$100B potential revenue, MI450 ramp H2 2026 [Source: AMD IR — Tier 1]
- Meta deal: 6 GW, ~$100B potential revenue, custom MI450 H2 2026 [Source: AMD IR — Tier 1]

**Critical Weakness — The CUDA Gap:**
- NVIDIA's CUDA ecosystem: 6M+ developers, 300+ libraries, 600+ AI models, 18 years of investment
- CUDA Gap Score: 28.7-99.1 across benchmarks — software optimization gives NVIDIA an effective 30-99% performance advantage over raw hardware specs [Source: AIM Multiple — Tier 6]
- ROCm 7.0 narrowing gap: 10-30% behind CUDA in compute-intensive workloads (down from 30-99% historically) [Source: ThunderCompute — Tier 6]
- ROCm improving: day-zero support for major models, 3.5x better inference performance vs. prior versions
- Mitigants: OpenAI Triton and MLIR frameworks abstracting away CUDA lock-in; PyTorch now officially supports ROCm
- AMD's HIPIFY tool converts ~90% of CUDA code; ZLUDA runs unmodified CUDA binaries at 80-95% performance
- The OpenAI and Meta mega-deals signal that at least two of the world's most sophisticated AI customers find ROCm sufficient for their workloads — this is the strongest validation signal to date

**Pricing Power:** Moderate and improving. AMD historically priced MI-series at 15-30% discount to equivalent NVIDIA products to compensate for software gap. As ROCm matures and mega-deals establish credibility, pricing gap should narrow. MI450 pricing for OpenAI/Meta likely reflects volume discounts but at scale that generates attractive margins. [DATA GAP: Exact GPU ASP data not disclosed]

---

### Arena 3: Client CPU (Ryzen vs. Intel Core)

**Market Definition:** Consumer and commercial desktop and notebook x86 processors.

| Segment | AMD Share | Intel Share | Trend |
|---------|----------|-------------|-------|
| Desktop (units) | ~36.4% | ~63.6% | AMD +4.6pp YoY |
| Desktop (revenue) | ~42.6% | ~57.4% | AMD +14.6pp YoY |
| Mobile/Laptop (units) | ~20.6% | ~79.4% | Roughly stable |
| Overall Client (units) | ~29.2% (Q4 2025) | ~70.8% | AMD +4.6pp YoY |
| Steam Gaming | ~40.4% | ~59.6% | AMD gaining |

[Source: Mercury Research via Tom's Hardware, TweakTown — Tier 3-6]

**Key Dynamics:**
- Client segment revenue: $3,100M in Q4 2025 (+34% YoY), $10,640M FY2025
- Ryzen 9000 series (Zen 5) driving share gains in desktop
- AI PC refresh cycle beginning — Windows 11 + NPU requirements favor AMD's integrated NPU strategy
- Intel struggles with 18A process transition; Arrow Lake (Core Ultra 200) received mixed reviews
- AMD revenue share exceeding unit share (42.6% vs 36.4% desktop) indicates premium positioning
- Mobile remains Intel stronghold due to OEM relationships and brand perception, though AMD slowly gaining

**Pricing Power:** Moderate. AMD has successfully moved into premium desktop ($400+) with Ryzen 7/9 products. Revenue share exceeding unit share confirms ASP uplift. Mobile remains more competitive on pricing. [DATA GAP: Pricing power assessment based on public benchmark and retailer data, not transaction data]

---

### Arena 4: FPGA / Adaptive Computing (Xilinx vs. Intel Altera vs. Lattice)

**Market Definition:** Field-programmable gate arrays and adaptive SoCs for data center, aerospace/defense, automotive, communications, and industrial.

**Market Size:** ~$10-11B in 2025-2026, growing to ~$17-27B by 2031-2035 (9-15% CAGR depending on definition). [Source: Mordor Intelligence, Precedence Research — Tier 6]

| Competitor | Position | Notes |
|-----------|----------|-------|
| **AMD (Xilinx)** | #1 or #2 by revenue | Targets >70% revenue share in adaptive computing |
| **Intel (Altera)** | #1 or #2 | Spun out to Silver Lake (51% stake at $8.75B valuation) in 2025; becoming independent pure-play |
| **Lattice Semiconductor** | #3 (small/mid-range) | Strong in low-power FPGAs; Nexus/Avant product families |
| **Microchip (Microsemi)** | #4 | Aerospace/defense focus |
| **Achronix** | Niche | eFPGA IP licensing |

**Key Dynamics:**
- AMD Embedded segment: $950M Q4 2025 (+2.9% YoY), $3,454M FY2025 — recovering slowly from 2024 inventory correction
- Xilinx acquisition ($49B, 2022) gave AMD leading FPGA portfolio but integration still ongoing
- AWS launched FPGA-accelerated instances on EPYC + Xilinx Virtex — cross-selling opportunity
- Altera spin-out removes Intel's direct competitive investment but creates a focused competitor
- Versal AI Edge adaptive SoCs targeting automotive ADAS and industrial AI at the edge

**Pricing Power:** Strong in high-end FPGAs (limited competition, long design-in cycles). Weaker in mid-range where Lattice competes aggressively. Government/defense contracts provide pricing stability. [DATA GAP: Segment-level margin data not separately disclosed post-restructuring]

---

### Arena 5: Semi-Custom (Console SoCs)

**Market Definition:** Custom SoCs for gaming consoles and other fixed-function applications.

| Customer | Status | Notes |
|----------|--------|-------|
| Sony (PlayStation 5/Pro) | Active | Current-gen, ~7th year of cycle |
| Microsoft (Xbox Series) | Active | Current-gen, maturing |
| Microsoft (Next-gen Xbox) | Expected 2027 | AMD SoC confirmed [Source: AMD Q4 call — Tier 2] |
| Valve (Steam Deck) | Active | Custom AMD APU |

**Key Dynamics:**
- Gaming segment (includes semi-custom): $843M Q4 (+50% YoY), $3,910M FY2025
- Current console cycle maturing; management guided "significant decline" in semi-custom gaming revenue
- Next-gen Xbox expected 2027 — provides future revenue bridge
- Semi-custom has low margins (~20-25% gross margin vs. 50%+ for Data Center) but provides volume and engineering cost absorption
- AMD is effectively sole supplier for console SoCs — no competitive threat in current cycle

**Pricing Power:** Low. Semi-custom contracts are negotiated upfront at fixed margins. AMD is a price-taker on console SoCs. Value comes from volume guarantees, not pricing power.

---

## 2. Moat Assessment

| Moat Type | Score (1-10) | Evidence |
|-----------|-------------|----------|
| **Network Effects** | 4 | Limited direct network effects. Indirect effects through x86 ecosystem (software compatibility). ROCm ecosystem building but far behind CUDA's network effect. Developer adoption is the key battleground — PyTorch ROCm support is a positive signal but CUDA's 6M developer base creates substantial network effects for NVIDIA, not AMD. |
| **Switching Costs** | 6 | **Server CPU:** High switching costs once deployed — qualification cycles of 6-12 months, firmware/driver dependencies, workload optimization. AMD benefits from this now that EPYC is established. **AI GPU:** Moderate — ROCm still requires code porting, but OpenAI/Meta deals prove switching is feasible for sophisticated customers. **FPGA:** Very high — 12-24 month design-in cycles, RTL rewrite required to switch. **Semi-custom:** Essentially zero — locked in per console generation. |
| **Cost Advantages** | 5 | AMD benefits from TSMC's leading-edge process (fabless model avoids capex of Intel's fabs). EPYC chiplet architecture is a structural cost advantage — lower defect rates, better yields than monolithic designs. However, NVIDIA also uses TSMC and has superior scale in GPUs. AMD does not have unique cost advantages vs. NVIDIA in AI accelerators. |
| **Intangible Assets** | 7 | **x86 license:** One of only two companies with an x86 architectural license (the other being Intel). This is an effective duopoly barrier — no new entrant can build x86 chips. **Xilinx IP:** ~16,000 patents from Xilinx acquisition covering FPGA, adaptive computing, and signal processing. **Brand:** Lisa Su has built AMD from near-bankruptcy ($2B market cap in 2014) to $310B — brand credibility with hyperscalers is a measurable asset. **Key patent risk:** x86 cross-license with Intel is perpetual but theoretically voidable in M&A scenarios. [Source: AMD 10-K risk factors — Tier 1] |
| **Efficient Scale** | 5 | Server CPU market effectively supports only two x86 vendors (AMD + Intel) plus emerging Arm players. FPGA market supports 2-3 major players. But AI GPU market is large enough to support multiple entrants (NVIDIA, AMD, custom ASICs, startups). Semi-custom supports one vendor per console generation. The efficient scale moat is strongest in server CPU and FPGA, weakest in AI GPU. |

**Overall Competitive Score: 6 / 10**

**Justification:** AMD holds a strong and improving position in server CPUs (approaching parity with Intel in an effective duopoly with high barriers to entry). The x86 license is a durable intangible asset. However, the AI GPU business — which is the primary growth driver and the reason for AMD's $310B valuation — operates from a clear #2 position behind NVIDIA with a significant software ecosystem disadvantage (CUDA gap). AMD's moat in AI GPUs is narrow: it depends on hardware execution (MI450 ramp), software maturation (ROCm), and customer concentration (OpenAI + Meta = potentially >50% of AI GPU revenue). A score of 6 reflects a company with genuine competitive strengths in multiple arenas but whose highest-value business (AI GPU) has an unproven and still-narrow moat. A score of 7 would require demonstrating durable software ecosystem parity or clear multi-year market share gains above 15%.

---

## 3. Moat Durability (10-Year Horizon)

**Server CPU (Durability: HIGH — 8/10)**
AMD's server CPU moat is likely to persist and widen over the next decade. The x86 duopoly is structurally durable — no new x86 licensee will emerge. Arm-based server CPUs (Graviton, Ampere) will take share from the x86 pool but likely cap at 15-25% over 10 years, leaving a large addressable market for AMD. AMD's chiplet architecture provides a structural advantage that Intel is only now beginning to replicate. EPYC has crossed the critical mass threshold where ecosystem support (cloud instances, enterprise software qualification) is self-reinforcing.

**Risk to durability:** Arm-based CPUs could accelerate if Apple Silicon-style performance advantages materialize in servers. RISC-V is a theoretical 10-year threat but negligible near-term.

**AI GPU (Durability: MODERATE — 5/10)**
This is the most uncertain arena. Three scenarios:
1. **Bull (30% probability):** ROCm achieves CUDA parity, MI450/MI500 execute on schedule, AMD reaches 20-25% AI GPU share by 2030. Mega-deals with OpenAI/Meta prove AMD can compete at scale.
2. **Base (45% probability):** ROCm narrows gap but remains inferior. AMD holds 12-18% share. Custom ASICs take 15-20% from NVIDIA's share, with AMD as #2 GPU vendor.
3. **Bear (25% probability):** Custom ASICs cannibalize GPU demand. OpenAI/Meta develop internal chips and reduce AMD purchases. ROCm stagnates. AMD share stalls at 8-12%.

The moat is narrowing for NVIDIA (due to Triton/MLIR abstraction layers and custom ASICs) but this benefits the entire non-NVIDIA ecosystem, not just AMD.

**Client CPU (Durability: HIGH — 7/10)**
x86 duopoly persists. AMD's Zen architecture has structural advantages. AI PC refresh cycle provides multi-year tailwind. Risk: Qualcomm Snapdragon X / Arm-on-Windows could capture 10-15% of laptop market over 10 years.

**FPGA (Durability: HIGH — 7/10)**
Oligopoly with high switching costs. FPGA design-in cycles create durable revenue streams. Altera spin-out creates a more focused competitor but also validates FPGA as a standalone market. Versal AI Edge positions AMD well for edge AI growth.

**Semi-Custom (Durability: MODERATE — 5/10)**
Console cycle dependent. AMD's position is secure for current and next-gen (2027 Xbox), but long-term relevance depends on whether traditional consoles persist or shift to cloud gaming.

---

## 4. Pricing Power Summary

| Arena | Pricing Power | Direction | Evidence |
|-------|--------------|-----------|----------|
| Server CPU | **Strong** | Improving | Revenue share > unit share; ASP uplift through generations; TCO-based selling |
| AI GPU | **Moderate** | Improving | Historically 15-30% discount to NVIDIA; mega-deals suggest narrowing; MI450 pricing leverage from demand |
| Client CPU | **Moderate** | Stable | Premium desktop positioning (Ryzen 9); mobile still competitive pricing |
| FPGA | **Strong** | Stable | Limited competition in high-end; long design cycles create lock-in |
| Semi-Custom | **Weak** | Declining | Fixed-margin contracts; console cycle maturity |

---

## 5. #1 Competitive Threat: NVIDIA's CUDA Ecosystem + Custom ASIC Cannibalization

**What is the threat?** A dual threat: (1) NVIDIA's CUDA software moat keeps AMD permanently at a 10-15% AI GPU share ceiling, and (2) hyperscaler custom ASICs (Google TPU, Amazon Trainium, Microsoft Maia, OpenAI custom chip via Broadcom) erode the addressable GPU market from the other side, squeezing AMD between a dominant NVIDIA and cost-optimized custom silicon.

**Probability of materialization in next 3 years:** **Medium-High (60%)**

The CUDA gap has persisted for 18 years and is structural. While ROCm is improving, closing a 6M-developer ecosystem gap requires 5-10 years of sustained investment. Meanwhile, custom ASIC growth (44.6% in 2026 vs. GPU 16.1%) is accelerating. OpenAI is simultaneously buying AMD GPUs AND building custom chips with Broadcom — hedging its bets. Meta has internal chip programs alongside its AMD deal. The risk is that mega-deals are a bridge while hyperscalers build their own silicon, not a permanent shift to AMD.

**Impact if materialized:**
- AI GPU revenue growth stalls at ~$20-25B (vs. management's "tens of billions in 2027" target)
- Data Center segment growth decelerates from 60% to 15-25% annually
- Gross margin compression as AMD competes on price rather than ecosystem
- Revenue impact: -$5-15B vs. bull case by 2028
- Stock impact: 30-50% downside from current valuation, which prices in >20% AI GPU share

**Company's defensive response:**
1. **Open-source strategy:** ROCm is open-source, enabling community development and reducing dependence on AMD alone
2. **Mega-deal lock-in:** 6 GW commitments from OpenAI and Meta create multi-year revenue visibility
3. **Hardware differentiation:** MI450's memory capacity advantage (432GB vs. Vera Rubin's 288GB) matters for large model inference
4. **Acquisition optionality:** AMD could acquire AI software companies to accelerate ROCm ecosystem
5. **Ethernet-based networking:** AMD's open Ethernet approach (vs. NVIDIA's proprietary NVLink) appeals to customers wanting vendor flexibility

**Early warning indicators:**
- ROCm developer adoption metrics (GitHub stars, PyPI downloads, conference mentions)
- Custom ASIC share exceeding 20% of AI accelerator market
- OpenAI or Meta reducing GPU purchase commitments or accelerating custom chip timelines
- NVIDIA maintaining >75% share through 2027 despite competition
- AMD AI GPU revenue growing <30% annually (vs. guided >60% Data Center growth)

---

## 6. TAM Analysis

### AI Accelerator Market

| Year | TAM Estimate | Source | Confidence |
|------|-------------|--------|------------|
| 2025 | $126-160B | Bloomberg Intelligence, Fortune BI | Medium |
| 2026 | $200-250B | Consensus range | Medium |
| 2027 | $280-350B | Multiple analysts | Low-Medium |
| 2030 | $440-650B | Mordor Intelligence, Precedence Research | Low |

[ASSUMPTION: TAM estimates sourced from Bloomberg Intelligence, Fortune Business Insights, Mordor Intelligence, Precedence Research. Third-party TAM estimates frequently overstate by 20-40%. Using conservative end of ranges.]

**AMD's Serviceable Addressable Market (SAM):** AMD cannot compete for hyperscaler internal ASICs (Google TPU, Amazon Trainium). Excluding ~15-20% internal ASIC market, AMD's SAM is ~$170-210B in 2026. At 10% share, that implies ~$17-21B GPU revenue — consistent with management's trajectory.

**AMD's TAM Penetration:** ~8-12% of total AI accelerator TAM in 2025. At $16.6B Data Center revenue (includes CPUs), AMD's pure AI GPU revenue is estimated at ~$10-12B, or roughly 7-8% of $150B TAM.

### Server CPU Market

| Year | TAM Estimate | Source | Confidence |
|------|-------------|--------|------------|
| 2025 | ~$14B | Coherent Market Insights | Medium |
| 2026 | ~$16B | "Strong double-digit" growth per AMD | Medium |
| 2031 | ~$21-26B | Multiple estimates (6-7% CAGR) | Medium |

[ASSUMPTION: Server CPU TAM sourced from Coherent Market Insights, Precedence Research, Fact MR. AMD management's "strong double-digit" growth guide for 2026 may reflect AI-driven server demand acceleration.]

**AMD's SAM:** Virtually the entire x86 server CPU market (~85-90% of total, with 10-15% going to Arm). At 40% share of ~$14B = ~$5.6B server CPU revenue in 2025, consistent with Data Center segment ($16.6B) being split ~65% GPU / 35% CPU.

**AMD's TAM Penetration:** ~40% of x86 server CPU market, ~35% of total server CPU market (including Arm).

---

## 7. Competitive Position Summary

AMD occupies a structurally advantaged position in server CPUs (approaching parity with Intel in an effective duopoly with high barriers to entry) and a rapidly improving but still #2 position in AI GPUs (where hardware performance is competitive but the CUDA software ecosystem gap remains the binding constraint on market share). The OpenAI and Meta mega-deals (combined 12 GW, ~$200B potential revenue) represent the most significant competitive validation in AMD's history — two of the world's most demanding AI customers chose AMD as their primary GPU alternative to NVIDIA. However, these deals come with $0.01 warrants for 320M shares (~20% dilution) and execute against NVIDIA's Vera Rubin launch in the same H2 2026 timeframe.

The investment thesis is competitive-positive in server CPUs (widening moat, secular share gains) and competitive-neutral-to-positive in AI GPUs (improving from a weak base, validated by mega-deals, but CUDA gap and custom ASIC threat create real ceilings on upside). The biggest competitive risk is not that AMD loses ground — it is that AMD's AI GPU share gains plateau at 12-15% while custom ASICs take the rest of the non-NVIDIA market, leaving AMD's $310B valuation unsupported by the realized share and margin trajectory.

**Overall Competitive Score: 6 / 10** — Strong multi-segment franchise with durable server CPU moat, but AI GPU business (the primary valuation driver) operates with a narrow and unproven moat against the most dominant technology franchise in computing history (NVIDIA/CUDA). Score could move to 7 within 12-18 months if MI450 ramp succeeds and ROCm adoption accelerates measurably.

---

## Appendix: Source Bibliography

### Tier 1 — SEC Filings & Official Disclosures
- AMD Q4 FY2025 Earnings Press Release (2026-02-03)
- AMD-OpenAI Partnership Press Release (2025-10-06)
- AMD-Meta Partnership Press Release (2026-02-24)
- AMD 10-K FY2025 (filed 2026-02-04)

### Tier 2 — Earnings Transcripts
- AMD Q4 FY2025 Earnings Call Transcript (Motley Fool, 2026-02-03)

### Tier 3 — Industry Press
- [Tom's Hardware — AMD desktop/server market share](https://www.tomshardware.com/pc-components/cpus/amds-desktop-pc-market-share-hits-a-new-high-as-server-gains-slow-down-intel-now-only-outsells-amd-2-1-down-from-9-1-a-few-years-ago)
- [Tom's Hardware — NVIDIA Vera Rubin platform](https://www.tomshardware.com/pc-components/gpus/nvidias-vera-rubin-platform-in-depth-inside-nvidias-most-complex-ai-and-hpc-platform-to-date)
- [Tom's Hardware — AMD MI350X/MI355X announcement](https://www.tomshardware.com/pc-components/gpus/amd-announces-mi350x-and-mi355x-ai-gpus-claims-up-to-4x-generational-gain-up-to-35x-faster-inference-performance)
- [SemiAnalysis — AMD MI350X and MI400](https://newsletter.semianalysis.com/p/amd-advancing-ai-mi350x-and-mi400-ualoe72-mi500-ual256)
- [SemiAnalysis — Vera Rubin architecture](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution)
- [CNBC — Meta-AMD deal coverage](https://www.cnbc.com/2026/02/24/meta-to-use-6gw-of-amd-gpus-days-after-expanded-nvidia-ai-chip-deal.html)
- [The Register — AMD gains CPU share](https://www.theregister.com/2026/02/13/amd_intel_market_share/)

### Tier 4-5 — Financial Data & Government
- [StockAnalysis.com — AMD statistics](https://stockanalysis.com/stocks/amd/statistics/)
- [Fusion Worldwide — Server CPU market dynamics](https://www.fusionww.com/insights/blog/server-cpu-market-dynamics-in-2025)

### Tier 6 — Industry Research & Analysis
- [AIM Multiple — CUDA vs ROCm](https://research.aimultiple.com/cuda-vs-rocm/)
- [ThunderCompute — ROCm vs CUDA](https://www.thundercompute.com/blog/rocm-vs-cuda-gpu-computing)
- [Bloomberg Intelligence — AI accelerator market forecast](https://www.bloomberg.com/company/press/ai-accelerator-market-looks-set-to-exceed-600-billion-by-2033-driven-by-hyperscale-spending-and-asic-adoption-according-to-bloomberg-intelligence/)
- [Precedence Research — Data center CPU market](https://www.precedenceresearch.com/data-center-cpu-market)
- [Mordor Intelligence — FPGA market](https://www.mordorintelligence.com/industry-reports/field-programmable-gate-array-fpga-market)
- [Coherent Market Insights — Data center CPU market](https://www.coherentmarketinsights.com/industry-reports/data-center-cpu-market)
- [Fortune Business Insights — AI accelerator market](https://www.fortunebusinessinsights.com/ai-accelerator-market-113873)
- [KAD — AMD MI450X vs NVIDIA Rubin](https://www.kad8.com/hardware/amd-mi450x-vs-nvidia-rubin-ai-chip-battle-heats-up/)
- [TrendForce — Microsoft Maia 200](https://www.trendforce.com/news/2026/01/27/news-microsoft-unveils-maia-200-ai-chip-on-tsmc-3nm-sk-hynix-reportedly-sole-hbm3e-supplier/)
