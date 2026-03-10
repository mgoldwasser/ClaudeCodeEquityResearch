# Devil's Advocate Report — AMD (Advanced Micro Devices, Inc.)

**Date:** 2026-03-09
**Current Price:** $190.40 | **Market Cap:** $310B | **Trailing P/E:** 71.7x | **Forward P/E:** 28.6x
**Role:** Systematic assumption challenger — independent bear case construction

---

## 1. Assumption Dependency Chain

The AMD bull thesis at $190.40 depends on five key assumptions, each of which must substantially hold for the stock to work. Failure of any single assumption materially damages the thesis; failure of two or more is catastrophic.

| # | Key Assumption | Required for Bull Case? | Required for Base Case? | Falsifiable? | Confidence (1-5) | Fragility (1-5) | Verifiability (1-5) |
|---|----------------|------------------------|------------------------|-------------|-------------------|------------------|---------------------|
| 1 | OpenAI + Meta mega-deals (12 GW, ~$200B) execute on schedule and scale | Yes | Partially (base case needs at least 4-6 GW) | Yes — MI450 shipment data in H2 2026 | 2 | 5 | 4 |
| 2 | CUDA/ROCm software gap narrows enough for enterprise adoption | Yes | Yes | Yes — benchmark gaps, developer adoption metrics | 2 | 4 | 3 |
| 3 | Custom ASICs do not cannibalize GPU demand from hyperscalers | Yes | Partially | Yes — hyperscaler internal chip deployment data | 2 | 4 | 3 |
| 4 | AI infrastructure spending sustains >30% growth through 2028 | Yes | Yes | Yes — hyperscaler capex guidance, quarterly trends | 3 | 5 | 4 |
| 5 | Warrant dilution (320M shares, ~20%) is offset by revenue/earnings growth | Yes | No — base case still sees 10-15% dilution impact | Partially — depends on vesting milestones | 3 | 3 | 4 |

**Composite Fragility Score: 4.2/5 — Extremely fragile thesis.** The bull case requires near-simultaneous success across five independent dimensions, each with sub-50% individual confidence.

---

## 2. Inversion Analysis — What Breaks Each Assumption?

### Assumption 1: Mega-Deal Execution (12 GW at Scale)

**What would falsify this?** MI450/Helios delays beyond Q4 2026; yield issues at TSMC 3nm advanced packaging; OpenAI or Meta scaling back or diversifying away from AMD GPUs.

**Historical base rate:** AMD has never manufactured at anything close to 12 GW scale. The MI350 was described as the "fastest ramp in company history" — but it reached 8 of 10 top AI companies at volumes measured in thousands of units, not the millions implied by 12 GW. NVIDIA took 5+ years to scale from initial data center GPU to multi-billion-dollar quarterly revenue. AMD is attempting to compress this into 18 months.

**Strongest evidence against it:**
- MI455X delay rumors already emerged in early 2026, forcing AMD to issue a public denial calling the reports "BS" [Source: VideoCardz, Tom's Hardware — Tier 3, 2026-03-09]. Companies that need to publicly deny delays are often closer to the edge than they admit.
- NVIDIA has locked down >50% of TSMC's CoWoS advanced packaging capacity through 2027 [Source: SemiWiki — Tier 6]. AMD is competing for the remaining 40-50% alongside every other fabless AI chip company.
- OpenAI simultaneously signed a 10 GW custom ASIC deal with Broadcom [Source: Tom's Hardware — Tier 3, 2025-10-13]. Total OpenAI hardware commitments now exceed 26 GW. This is not a company betting exclusively on AMD — it is hedging massively.

**If this breaks, what else breaks?** Revenue growth collapses from the projected >60% DC CAGR to perhaps 15-25%. The $20+ EPS target becomes unreachable. The warrant vesting milestones (which require $600 stock price) become permanently unachievable, removing the "deal revenue offsets dilution" argument since partial vesting on deployment milestones still triggers dilution without full revenue.

### Assumption 2: CUDA/ROCm Software Gap Closes

**What would falsify this?** Enterprise customers continue choosing NVIDIA despite AMD hardware price/performance advantages; ROCm adoption stalls below critical mass; NVIDIA accelerates CUDA investment.

**Historical base rate:** Software ecosystem advantages in computing have historically proven extremely durable. Intel's x86 ecosystem lasted 30+ years. Microsoft Windows dominated for 25+ years. NVIDIA has invested 19 years in CUDA. No computing software moat of this duration has been cracked in under 5 years by a hardware competitor.

**Strongest evidence against it:**
- CUDA Gap Score ranges from 28.7 to 99.1 across benchmarks — meaning NVIDIA's software stack delivers an effective performance boost of 30-99% over equivalent hardware [Source: AIM Multiple — Tier 6, 2026-03-09]. This means AMD hardware that is 20-30% faster on paper can still lose in real-world deployment.
- ROCm compatibility "breaks down for custom kernels, advanced attention mechanisms, and cutting-edge training techniques" [Source: ThunderCompute — Tier 6, 2026-03-09]. The frontier models that OpenAI and Meta train are precisely the workloads that require custom kernels.
- CUDA has 6M+ developers, 300+ libraries, 600+ optimized AI models. ROCm has a fraction of this base. Developer ecosystem growth follows power laws — the gap compounds over time, it does not narrow linearly.
- ZLUDA (converting CUDA binaries to ROCm) achieves only 80-95% performance [Source: AMD competitive data]. A 5-20% performance penalty on top of the CUDA Gap Score means real-world underperformance could be 25-100%.

**If this breaks, what else breaks?** AMD GPUs become a "value" product competing on price, not a premium product competing on capability. Gross margins compress from the target 55%+ toward 45-48%. The mega-deal economics deteriorate because AMD must discount aggressively to compensate for software inferiority.

### Assumption 3: Custom ASICs Don't Cannibalize GPU Demand

**What would falsify this?** Hyperscalers shift inference workloads to custom silicon within 2-3 years, using GPU deals as bridge infrastructure.

**Historical base rate:** Every major cloud provider (Google, Amazon, Microsoft) has developed custom silicon when volumes justify it. Google has been on TPU v5+ for years. Amazon Trainium claims 30-40% better price-performance than merchant GPUs. The historical pattern is clear: hyperscalers vertically integrate once the technology matures.

**Strongest evidence against it:**
- Custom ASIC shipments growing 44.6% in 2026 vs. GPU shipments at 16.1% [Source: AMD competitive data]. ASICs are the faster-growing category.
- OpenAI signed a 10 GW deal with Broadcom for custom ASICs — 67% larger than its AMD deal (10 GW vs 6 GW) [Source: Tom's Hardware, CNBC — Tier 3, 2025-10-13]. If OpenAI believed GPUs were the long-term answer, why commit nearly twice as much capacity to custom silicon?
- Meta has proprietary chip development programs. Microsoft Maia is deployed with next-gen Braga in 2026 [Source: CNBC — Tier 3].
- The OpenAI and Meta AMD deals may be **bridge infrastructure** — maintaining GPU optionality while custom silicon matures. The 5-6 year warrant horizon aligns suspiciously well with the timeline for custom ASICs to reach full scale.

**If this breaks, what else breaks?** The $200B revenue potential from mega-deals shrinks dramatically as hyperscalers redirect incremental spend to internal silicon. AMD's data center TAM contracts. The GPU market bifurcates: NVIDIA retains premium training workloads, custom ASICs capture inference at scale, and AMD gets squeezed in the middle.

### Assumption 4: AI Infrastructure Spending Sustains >30% Growth

**What would falsify this?** Hyperscaler capex plateaus in 2027; AI monetization gap forces spending discipline; recession reduces enterprise IT budgets; regulatory intervention limits AI deployment.

**Historical base rate:** No technology capex cycle in history has sustained >30% growth for more than 3-4 years. The cloud computing buildout (2015-2020) averaged ~25% CAGR before moderating. The fiber optic buildout (1997-2001) sustained >40% growth for 4 years before collapsing 70%. The most relevant analogy is the telecom bubble, where infrastructure spending vastly exceeded near-term monetization.

**Strongest evidence against it:**
- Hyperscaler AI capex in 2026 is projected at $660-690B, but AI-related services generated only ~$25B in revenue in 2025 — a 25-28:1 investment-to-revenue ratio [Source: Futurum Group, Goldman Sachs — Tier 3-6, 2026-03-09]. This ratio is unsustainable. Even at optimistic 2026 AI revenue projections of $60-80B, the ratio remains 8-11:1.
- Capital intensity has surged to unprecedented levels: Oracle at 57% MRQ, Microsoft at 45% [Source: CreditSights — Tier 4]. Hyperscalers are increasingly funding capex with debt rather than cash flow. This is a late-cycle signal.
- Goldman Sachs projects capex of $1.15T from 2025-2027 — but also flags that "2027 guidance may begin to plateau as base effects grow and power constraints bite" [Source: Goldman Sachs — Tier 3].
- The Man Group identifies the current AI spending pattern as exhibiting classic bubble characteristics: "spending front-loaded while value capture is delayed and uneven" [Source: Man Group — Tier 6, 2026-03-09].

**If this breaks, what else breaks?** AMD's Data Center revenue (48% of total) hits a wall. The forward P/E of 28.6x, which assumes >40% EPS growth, rerates to 18-22x (mature semiconductor peer range). At $6.66 FY2026E EPS and 20x multiple, the stock is worth $133 — a 30% decline.

### Assumption 5: Warrant Dilution Is Manageable

**What would falsify this?** Partial vesting triggers significant dilution before full revenue realization; stock price never reaches $600, so AMD gives away equity for deals that don't fully materialize.

**Strongest evidence against it:**
- 320M warrant shares at $0.01 exercise price is effectively a free equity grant worth ~$61B at current prices. Even partial vesting of 50% (160M shares on deployment milestones alone) represents ~10% dilution — equivalent to wiping out roughly 2 years of share repurchase activity.
- The warrant structure creates a perverse incentive: OpenAI and Meta benefit most from AMD stock appreciation, not from AMD product performance. They can vest warrants, sell shares, and fund their own custom silicon programs with the proceeds.
- Analysts have questioned "why the product doesn't sell itself without giving up 10% of equity" [Source: Tom's Hardware — Tier 3, 2026-03-09]. This is the right question. If MI450 were truly competitive with NVIDIA H200/B200 on its own merits, mega-deals would not require effectively paying customers $30B+ in equity to adopt it.
- Full vesting requires $600/share — a 3.15x from current price, implying ~$980B market cap. This would make AMD the 5th most valuable company in the world. The base rate for semiconductor companies reaching this valuation tier is effectively zero (only NVIDIA has done it, and only during a once-in-a-generation AI cycle).

**If this breaks, what else breaks?** EPS dilution of 10-20% at a time when the growth narrative is already under pressure creates a vicious cycle: lower EPS -> lower stock price -> warrant vesting slows -> deal execution questioned -> further multiple compression.

---

## 3. Disconfirming Evidence Register

| # | Evidence | Source | Severity | Bull Case Response (if any) |
|---|----------|--------|----------|---------------------------|
| 1 | OpenAI's Broadcom custom ASIC deal (10 GW) is 67% larger than its AMD deal (6 GW). OpenAI's total hardware commitments = 26 GW, of which AMD is only 23%. | Tom's Hardware, CNBC — Tier 3 | **High** | Bulls argue GPUs and ASICs serve different workloads (training vs inference). But inference is 60-80% of compute demand and growing. |
| 2 | CUDA Gap Score of 28.7-99.1 means NVIDIA's software delivers 30-99% effective performance boost over equivalent hardware. AMD's 20-30% hardware advantages are potentially fully negated. | AIM Multiple — Tier 6 | **High** | Bulls point to ROCm 6.0 improvements and ZLUDA. But ZLUDA delivers only 80-95% CUDA performance, and custom kernels still break on ROCm. |
| 3 | MI455X delay rumors forced AMD to issue public denial in early 2026. | VideoCardz, Tom's Hardware — Tier 3 | **Medium** | AMD called it "BS" and reaffirmed H2 2026 timeline. But denial of delays is a standard playbook — Intel denied Sapphire Rapids delays for 18 months before admitting them. |
| 4 | NVIDIA controls >50% of TSMC CoWoS advanced packaging through 2027. AMD competes for remaining 40-50% with all other fabless AI companies. | SemiWiki, TSMC reports — Tier 3-6 | **High** | Bulls argue TSMC is expanding capacity. True, but expansion timelines are 18-24 months, and NVIDIA has pre-booked the incremental capacity. |
| 5 | AI capex-to-revenue ratio of 25-28:1 ($660B+ capex vs ~$25B AI revenue). Historically, no capex cycle survives this imbalance beyond 3-4 years. | Futurum Group, Goldman Sachs — Tier 3-6 | **High** | Bulls argue this is "foundational infrastructure" like the internet. The internet buildout had a similar ratio — and the telecom companies that built it went bankrupt. |
| 6 | Lisa Su sold 125,000 shares at $214 in Feb 2026 and 225,000 shares at $162-166 in Aug 2025. Programmatic via 10b5-1 plans. | SEC Form 4, StockTitan — Tier 2 | **Low** | Programmatic sales are not discretionary signals. CEO retains ~$600M+ in AMD stock. |
| 7 | Seeking Alpha article titled "AMD: You're About To Get Crushed" argues overvaluation and overhyped OpenAI expectations. Goldman Sachs maintains only Hold rating at $240 target. | Seeking Alpha — Tier 6, Goldman Sachs — Tier 3 | **Medium** | Contrarian retail analysis is noisy. But Goldman's Hold is notable — they have deep semiconductor coverage and access to management. |
| 8 | AMD forward P/E of 28.6x is higher than NVIDIA's on a PEG-adjusted basis given NVIDIA's superior margins (75% GM vs AMD's 52%). AMD pays a higher multiple for weaker economics. | StockAnalysis.com — Tier 4 | **Medium** | Bulls argue AMD is earlier in its growth curve. But earlier-stage growth should come with higher uncertainty discount, not a premium. |
| 9 | China revenue permanently impaired: was 24% of FY2024 revenue, now guided at ~$100M/quarter (~4% annualized). $800M inventory charge already taken. Further export restrictions possible. | AMD 8-K, TechCrunch — Tier 1-3 | **High** | Bulls argue China loss is already priced in. But $1.5-1.8B annual revenue loss has not been replaced — it has been masked by Data Center growth elsewhere. |
| 10 | Semi-custom gaming declining significantly (console cycle year 7). Next-gen Xbox not until 2027. Embedded growing only 2.9% YoY. Combined = ~25-30% of revenue under pressure. | AMD 10-K, earnings call — Tier 1 | **Medium** | Bulls dismiss non-DC segments as irrelevant. But at 28.6x forward P/E, every dollar of earnings matters. |
| 11 | Custom ASIC shipments growing 44.6% in 2026 vs GPU shipments at 16.1%. ASICs are structurally the faster-growing accelerator category. | Industry data — Tier 6 | **High** | Bulls argue training still requires GPUs. True today, but inference (60-80% of compute) increasingly moves to ASICs. |
| 12 | AMD's GAAP operating margin of 10.8% vs non-GAAP of 27.8% — a 17pp gap driven by stock-based comp and amortization of acquired intangibles (Xilinx). True profitability is significantly lower than headline numbers suggest. | AMD 10-K — Tier 1 | **Medium** | Non-GAAP adjustments are standard for acquisitive semiconductor companies. But the magnitude (17pp) is large and growing with warrant-based equity grants. |

---

## 4. Contrarian Thesis

**The Consensus View:** AMD is a multi-year AI beneficiary executing a successful pivot from CPU underdog to AI GPU challenger. The OpenAI and Meta mega-deals validate the product roadmap, server CPU share gains provide a durable revenue base, and the stock is cheap at 28.6x forward P/E given >35% revenue CAGR guidance. The $200B+ deal pipeline transforms AMD into a top-tier AI infrastructure company alongside NVIDIA.

**Why the Consensus May Be Wrong:**

1. **The mega-deals are bridge contracts, not long-term commitments.** OpenAI's 10 GW Broadcom custom ASIC deal is 67% larger than its AMD GPU deal. The 5-6 year warrant horizon aligns with the timeline for custom silicon to reach scale. AMD is being used as a second source to pressure NVIDIA pricing and maintain optionality while hyperscalers develop their own silicon. When custom ASICs mature, GPU volumes from these customers will plateau or decline.

2. **The CUDA software moat is not closing — it is widening.** Every incremental NVIDIA GPU sold adds another developer to the CUDA ecosystem, another optimized library, another pre-trained model. AMD's ROCm improvements are real but run on a treadmill: the absolute gap in developer tooling, model optimization, and enterprise support grows wider in absolute terms even as AMD closes the percentage gap. The CUDA Gap Score (30-99% effective performance boost) means AMD hardware advantages are illusory for real-world workloads.

3. **The AI capex cycle is in late innings, not early innings.** With a 25-28:1 capex-to-revenue ratio and hyperscalers funding investment with debt for the first time, the AI infrastructure buildout resembles the telecom bubble of 1999-2001 more than the early internet of 1995. The correction does not require AI to fail — it only requires CFOs to demand ROI proof before approving the next wave of spend. A 20-30% capex deceleration in 2027-2028 would cut AMD's addressable market precisely when it needs it most to justify its current multiple.

**The Contrarian Thesis (2-3 sentences):**

AMD at $190.40 is priced for a world where all five critical assumptions hold simultaneously: mega-deal execution at unprecedented scale, CUDA gap closure, sustained AI spending, limited ASIC cannibalization, and manageable dilution. The probability of all five holding is materially below the ~70% bull/base probability implied by the current stock price. The most likely outcome is that AMD delivers strong but disappointing growth (20-30% DC CAGR vs the guided >60%), while margin compression from CUDA-driven discounting and 10-20% warrant dilution push the stock to $120-150 within 18 months — a classic "good company, bad stock" setup.

---

## 5. Pre-Mortem: "It's March 2028 and AMD Is at $80. What Went Wrong?"

**What Happened:**

The unraveling began in Q4 2026 when MI450 shipments to OpenAI came in at 40% below the contracted ramp schedule. TSMC CoWoS yield issues, exacerbated by NVIDIA's priority access to the best packaging lines, forced AMD to push volume production to Q1 2027 — six months late. OpenAI, which had been running its Broadcom custom ASICs for inference since mid-2026, quietly shifted incremental training capacity to NVIDIA Vera Rubin rather than waiting for MI450 at scale. Meta followed suit in Q1 2027, citing "customer experience requirements" that ROCm could not meet for real-time inference in Ray-Ban Meta glasses and AI agents.

By mid-2027, the AI capex correction arrived. Microsoft cut its 2028 capex guidance by 25% after Azure AI revenue grew only 18% YoY against expectations of 40%. Amazon followed. Hyperscaler orders for all GPU vendors declined sequentially for the first time in 12 quarters. AMD's Data Center revenue, which had grown 45% in FY2026 (missing the >60% target), decelerated to 8% in H1 2027 as order deferrals mounted.

The warrant dilution became toxic. OpenAI and Meta had vested approximately 180M of their combined 320M warrant shares based on deployment milestones (even though volumes undershot targets, the milestones were structured as cumulative thresholds). At $80/share, these warrant shares represented a $14.4B wealth transfer from existing shareholders to two companies that were simultaneously investing billions in competing custom silicon. The market revalued AMD at 15x forward EPS of $5.20 (vs the peak expectation of $20+), assigning a mature semiconductor multiple to a company that had failed to prove it could be an AI infrastructure leader.

**Warning Signs That Were Visible Today (March 2026):**

1. **OpenAI's Broadcom deal was 67% larger than its AMD deal.** The market celebrated the AMD deal in isolation without recognizing that AMD was the smaller bet in OpenAI's diversified hardware strategy. This was visible in October 2025 when Broadcom's deal was announced one week after AMD's.

2. **The MI455X delay rumors required a public denial.** Healthy product launches do not generate delay rumors that require CEO-level denial 6 months before ship date. The AMD denial ("BS") was emphatic in a way that suggested the rumors were close enough to reality to be threatening.

3. **The CUDA Gap Score data was public and unambiguous.** Independent benchmarks showed 30-99% effective performance advantages for NVIDIA's software stack. AMD's hardware spec sheets showed 20-30% advantages. The math was clear: software > hardware. The market chose to believe the hardware specs.

4. **AI capex-to-revenue ratio of 25:1 exceeded every historical precedent** for sustainable infrastructure buildouts. The telecom bubble had a similar ratio and unwound over 18 months.

5. **The warrant structure incentivized deal signing, not deal execution.** OpenAI and Meta received warrants that vest partially on deployment (not performance), meaning AMD was paying customers to take delivery of chips they might not fully utilize.

---

## 6. Break-Even Probability Analysis

### Scenario 1: Standard Bull/Base/Bear (Analyst Consensus-Adjacent)

```
Bull: $350 (25% probability) — Mega-deals execute, CUDA gap narrows, >$15 EPS by FY2028
Base: $220 (45% probability) — Partial execution, 30-40% DC growth, ~$8-10 EPS
Bear: $80  (30% probability) — Mega-deal underdelivery, AI capex correction, margin compression
Current: $190.40
```

**Results:**
- Expected value: $210.50 (+10.6%)
- Full Kelly: 26.4% (dangerously concentrated)
- Half Kelly: 13.2%
- Upside/downside ratio: 1.45x
- **Break-even bear probability: 41%**

**Interpretation:** If bear probability exceeds 41%, the expected value turns negative. The current implied bear probability based on consensus analyst targets (~$261 average) is approximately 15-20%. The question is whether 15-20% adequately captures the compounding risk across five fragile assumptions.

### Scenario 2: Devil's Advocate Adjusted Weights

```
Bull: $300 (20% probability) — Reduced bull price due to dilution + CUDA discount
Base: $200 (45% probability) — Modest beat with lower margins
Bear: $80  (35% probability) — Elevated due to ASIC cannibalization + capex cycle risk
Current: $190.40
```

**Results:**
- Expected value: $178.00 (-6.5%)
- Full Kelly: -30.7% (NEGATIVE — the position loses money on average)
- **Break-even bear probability: 27%**

**Interpretation:** Under more realistic scenario weights that account for the five assumption risks, the expected value is negative. AMD is a **negative expected value bet** at $190.40 unless the bull probability exceeds 25% AND the bear probability stays below 27%. This is a narrow window that leaves no margin of safety.

### Sensitivity Table

| Bull Prob | Base Prob | Bear Prob | Expected Value | EV Return | Kelly |
|:-:|:-:|:-:|:-:|:-:|:-:|
| 30% | 45% | 25% | $220.50 | +15.8% | 38.7% |
| 25% | 45% | 30% | $210.50 | +10.6% | 26.4% |
| 20% | 45% | 35% | $178.00 | -6.5% | -30.7% |
| 15% | 45% | 40% | $168.00 | -11.8% | **Negative** |
| 10% | 45% | 45% | $158.00 | -17.0% | **Negative** |

**The critical threshold is 27-35% bear probability.** Above this range, the expected value turns negative under all reasonable scenario calibrations.

### Current Implied Bear Probability Assessment

The market at $190.40 with consensus target of $261 is pricing approximately 15-20% bear probability. This is too low given:
- Five independent fragile assumptions each with sub-50% confidence
- ASIC cannibalization evidence that is structural, not cyclical
- CUDA moat that has not narrowed in absolute terms despite 2+ years of ROCm investment
- AI capex cycle showing late-stage characteristics (debt-funded, 25:1 capex-to-revenue ratio)
- 320M warrant shares creating 20% dilution overhang

**Devil's Advocate assessed bear probability: 30-35%.** This is above the break-even threshold of 27% under adjusted scenarios, making AMD a marginal-to-negative expected value position at current prices.

---

## 7. The Single Most Dangerous Assumption

**The single most dangerous assumption is that the OpenAI and Meta mega-deals represent durable, long-term demand rather than bridge contracts while custom ASICs mature.**

This assumption is dangerous because:

1. **It is the foundation of the entire bull case.** Remove the mega-deals and AMD's Data Center growth decelerates from >60% to 25-30%, the $20+ EPS target becomes unreachable, and the stock deserves a 20-22x multiple (= $133-146 stock price).

2. **The evidence against it is strong and structural.** OpenAI's Broadcom deal is 67% larger than its AMD deal. Every major hyperscaler is investing in custom silicon. The 5-6 year warrant horizon matches the ASIC maturity timeline.

3. **It is the least verifiable in the near term.** AMD can ship MI450 on time and report strong revenue for 2-3 quarters before the underlying demand shift becomes visible. By the time the bridge-contract nature reveals itself, the stock will have already priced in multi-year revenue that never materializes.

4. **It creates the deepest second-order damage.** If the mega-deals are bridge contracts, AMD will have given away 320M warrant shares (~20% dilution) for temporary revenue that disappears as custom ASICs scale. The equity cost is permanent; the revenue benefit is transient.

---

## 8. Summary

The most dangerous assumption is that the OpenAI and Meta mega-deals (12 GW, ~$200B potential) represent durable long-term demand rather than bridge infrastructure while both companies scale custom ASICs. The break-even bear probability is 27-41% depending on scenario calibration. Under the Devil's Advocate adjusted weights (35% bear probability), AMD is a negative expected value position at $190.40 with a Kelly fraction of -30.7%. The strongest disconfirming evidence is that OpenAI simultaneously signed a 10 GW custom ASIC deal with Broadcom — 67% larger than its AMD commitment — signaling that AMD GPUs are a hedge, not a conviction bet, for the largest AI infrastructure buyer in the world.

---

## Sources

- [AMD Q4 FY2025 Earnings Press Release](https://ir.amd.com/news-events/press-releases/detail/1276/) — Tier 1
- [AMD-Meta Partnership Press Release](https://ir.amd.com/news-events/press-releases/detail/1279/) — Tier 1
- [AMD-OpenAI Partnership Press Release](https://ir.amd.com/news-events/press-releases/detail/1260/) — Tier 1
- [AMD 8-K Export Control Charge](https://ir.amd.com/financial-information/sec-filings/content/0000002488-25-000039/amd-20250415.htm) — Tier 1
- [CNBC: Meta-AMD Deal](https://www.cnbc.com/2026/02/24/meta-to-use-6gw-of-amd-gpus-days-after-expanded-nvidia-ai-chip-deal.html) — Tier 3
- [Tom's Hardware: AMD-Meta $100B Deal](https://www.tomshardware.com/tech-industry/artificial-intelligence/amd-meta-100-billion-deal) — Tier 3
- [Tom's Hardware: OpenAI-Broadcom Custom ASIC Deal](https://www.tomshardware.com/openai-broadcom-to-co-develop-10gw-of-custom-ai-chips) — Tier 3
- [CNBC: Broadcom-OpenAI Custom Chip Deal](https://www.cnbc.com/2025/10/13/openai-partners-with-broadcom-custom-ai-chips-alongside-nvidia-amd.html) — Tier 3
- [VideoCardz: AMD Denies MI455X Delays](https://videocardz.com/newz/amd-denies-mi455x-delay-claims-says-shipments-remain-set-for-h2-2026) — Tier 3
- [Tom's Hardware: AMD Denies MI455X Delays](https://www.tomshardware.com/tech-industry/artificial-intelligence/amd-denies-report-of-mi455x-delays-as-nvidia-vr200-systems-are-rumored-to-arrive-early-company-says-helios-systems-on-target-for-2h-2026) — Tier 3
- [AIM Multiple: CUDA vs ROCm 2026](https://research.aimultiple.com/cuda-vs-rocm/) — Tier 6
- [ThunderCompute: ROCm vs CUDA](https://www.thundercompute.com/blog/rocm-vs-cuda-gpu-computing) — Tier 6
- [PitchGrade: AMD AI Margin Pressure](https://pitchgrade.com/research/amd-ai-margin-pressure) — Tier 6
- [Futurum: AI Capex 2026 $690B Sprint](https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/) — Tier 3
- [Goldman Sachs: AI Capex $500B+](https://www.goldmansachs.com/insights/articles/why-ai-companies-may-invest-more-than-500-billion-in-2026) — Tier 3
- [Man Group: The AI Bubble](https://www.man.com/insights/the-ai-bubble) — Tier 6
- [RIA: Capex Masking Economic Weakness](https://realinvestmentadvice.com/resources/blog/capex-spending-on-ai-is-masking-economic-weakness/) — Tier 6
- [SemiWiki: TSMC CoWoS Capacity](https://semiwiki.com/forum/threads/tsmc%E2%80%99s-advanced-packaging-capacity-is-fully-booked-for-next-two-years-by-nvidia-and-amd.20157/) — Tier 6
- [Seeking Alpha: AMD Bear Case](https://seekingalpha.com/article/4831137-amd-youre-about-to-get-crushed) — Tier 6
- [Seeking Alpha: Growth at Unreasonable Price](https://seekingalpha.com/article/4856960-amd-growth-at-unreasonable-price) — Tier 6
- [StockAnalysis.com: AMD Statistics](https://stockanalysis.com/stocks/amd/statistics/) — Tier 4
- [More Than Moore: AMD-OpenAI 6GW Bet](https://morethanmoore.substack.com/p/amd-and-openai-the-6-gigawatt-bet) — Tier 6
- [TrendForce: OpenAI Custom Chip 2026](https://www.trendforce.com/news/2026/01/15/news-openai-reportedly-to-deploy-custom-ai-chip-on-tsmc-n3-by-end-2026-second-gen-planned-for-a16/) — Tier 3
- [CreditSights: Hyperscaler Capex 2026](https://know.creditsights.com/insights/technology-hyperscaler-capex-2026-estimates/) — Tier 4
- [Morningstar: AI Arms Race](https://www.morningstar.com/financial-advisors/ai-arms-race-how-techs-capital-surge-will-reshape-investment-landscape-2026) — Tier 3
