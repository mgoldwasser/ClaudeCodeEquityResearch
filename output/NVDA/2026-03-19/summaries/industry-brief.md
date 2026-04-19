# Industry Brief — NVIDIA (NVDA)

**Analyst:** Industry Analyst

**Headline Finding:** NVIDIA controls 86-92% of AI accelerator market but Strategic Power composite score of 54/70 reveals 6 of 7 Helmer Powers present; critical vulnerability is TAM narrowing from hyperscaler custom ASICs (growing 44.6% vs. GPUs 16.1%) rather than AMD share erosion; CUDA network effects and switching costs protect training market (>95% share) through 2028-2029 but decay timeline shows cliff risk in 2027-2028 window when three powers (Cornered Resource, Counter-Positioning, Switching Costs) simultaneously show erosion signals.

**Key Numbers:**
- NVIDIA AI accelerator market share: 86-92% (vs. AMD 5-8%, Intel <3%, custom ASICs <5% external, growing)
- Strategic Power composite score: 54/70 (54/70 breakdown: Scale 8/10, Network Effects 9/10, Counter-Positioning 6/10, Switching Costs 9/10, Branding 7/10, Cornered Resource 8/10, Process Power 7/10)
- CUDA ecosystem scale: 4M+ developers, 20-year accumulation, 3,500+ optimized libraries
- CoWoS packaging capacity: NVIDIA controls ~70% through 2027; decay timeline 2027-2028
- Custom ASIC growth rate: 44.6% (2026) vs. GPU 16.1%; projected to reach 25-30% of AI compute by 2028
- Market share trajectory by 2030 (base case): NVIDIA 65-72% of AI accelerator market (down from 86-92% today)
- Power durability analysis: Network Effects half-life 2029-2031; Switching Costs half-life 2028-2030; Cornered Resource half-life 2027
- TAM estimates: Top-down $300-500B (2030); bottom-up $640-950B (2030); gap >20% flagged for director reconciliation
- Demand multiplier scenarios: Agentic AI $96B (60% probability), Physical AI $30B (40%), Sovereign AI $42B (70%), Video AI $45B (50%), Scientific AI $13.5B (45%)

**Critical Assumptions:**
- [ASSUMPTION: Jevons paradox sustains demand growth — efficiency improvements drive more compute usage, not less]
- [ASSUMPTION: PyTorch hardware abstraction (full parity with CUDA) arrives 2027-2028; prior to that, CUDA moat remains 95%+ effective for training]
- [ASSUMPTION: Hyperscaler custom ASIC penetration grows to 25-30% by 2028 (from current <15%), structurally narrowing GPU TAM but not NVIDIA's share]
- [ASSUMPTION: Rubin production on schedule H2 2026; 10x inference cost improvement will pull demand forward]
- [ASSUMPTION: Sovereign AI expands from ~20 countries (current) to 50+ by 2030, adding $60-80B incremental demand]
- [ASSUMPTION: AMD MI450 reaches 15-20% share of inference workloads by 2028 (from current <5%)]

**Data Gaps:**
- [DATA GAP: Third independent TAM estimate (Gartner/IDC) not retrieved — only two Tier 5-7 estimates available; gap >50% unexplained]
- [DATA GAP: Agentic AI compute intensity per workload not quantified; 5-10x multiplier assumption carries HIGH UNCERTAINTY]
- [DATA GAP: Physical AI GPU demand per robot unit unknown; scenario range very wide ($5-15B FY2027 range)]
- [DATA GAP: Hyperscaler custom chip deployment metrics not available for 2026 update; risk modeling based on 2025 estimates]

**Fair Value Estimate:** [Supports DCF revenue trajectory of $583B FY2031 if NVIDIA captures 65-70% of $640-950B TAM range — base case reconciliation margin ~15%]

**Biggest Risk/Concern:** Custom ASIC displacement is more structural and faster-moving than AMD competition; it represents TAM contraction, not share loss — hyperscalers (40-50% of NVIDIA revenue) are systematically insourcing GPU workloads and will achieve 20-30% self-sufficiency by 2028, permanently reducing NVIDIA's addressable market. The CUDA moat protects the GPU market share remaining after ASIC extraction but does not restore the TAM. Strategic Power decay timeline shows 2027-2028 window when Cornered Resource (CoWoS), Counter-Positioning (ASIC acceleration), and Switching Costs (PyTorch abstraction) all show simultaneous erosion signals — potential cliff risk for consensus assumptions.

**Signal for Pass 2:**
- Director must obtain third-party TAM estimate (Gartner or IDC) to resolve >50% gap between top-down and bottom-up forecasts
- Industry analyst should provide explicit answer: at what custom ASIC penetration rate does NVIDIA's revenue peak? (Current consensus assumes growth continues; risk is penetration reaches 40%+ by 2030)
- Request bottom-up reconciliation: DCF model FY2031 revenue $583B; 65-70% share of $640-950B TAM implies either (a) TAM hitting low end ($830B), or (b) NVIDIA share stays above 70% despite ASIC growth
- Flag critical assumption: "CUDA abstraction doesn't materialize until 2027-2028" — this is the single point of failure for margin assumptions. If PyTorch 2.0 full parity arrives in 2026 instead, decay timeline accelerates 2 years

