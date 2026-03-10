# Cross-Stock Intelligence Note

**From:** Competitive Analyst researching AMD
**To:** Analysts researching NVDA
**Date:** 2026-03-09
**Priority:** High
**Category:** Competitive Threat / Market Share

---

## Observation

AMD's MI355X benchmarks 20-30% faster than NVIDIA B200 in specific inference workloads (DeepSeek R1 FP4, Llama 3.1 405B) and delivers 40% more tokens per dollar. More critically, AMD secured 12 GW of GPU deployment commitments from OpenAI (6 GW, Oct 2025) and Meta (6 GW, Feb 2026) — two of NVIDIA's largest customers — with combined potential revenue exceeding $200B. AMD gained 2.6pp of AI GPU share in Q4 2025 while NVIDIA lost 1.4pp. MI450 (H2 2026) offers 50% more memory capacity than NVIDIA's Vera Rubin VR200 (432GB vs. 288GB HBM4), a meaningful advantage for large-model inference.

## Implication for Target

NVIDIA's >80% AI GPU share is beginning to erode from two vectors simultaneously: AMD GPU competition (hardware now credibly competitive, mega-deals validating ROCm) and custom ASICs (growing 44.6% vs. GPU 16.1% in 2026). The OpenAI and Meta deals with AMD signal that NVIDIA's two largest hyperscaler customers are actively diversifying GPU supply — even as they also expand NVIDIA purchases. NVIDIA's CUDA moat remains the primary defense, but OpenAI's Triton framework and framework-level abstractions (PyTorch ROCm support) are gradually weakening CUDA lock-in. NVIDIA's pricing power could face pressure if AMD's MI450 delivers competitive performance at scale.

## Supporting Evidence

- AMD Q4 FY2025 earnings call: MI350 deployed at 8/10 top AI companies, gained 2.6pp share [Tier 2]
- AMD IR: OpenAI 6 GW deal (Oct 2025), Meta 6 GW deal (Feb 2026) [Tier 1]
- SemiAnalysis: MI355X FP6 2.2x faster than B200 FP6; MI450 specs competitive with Vera Rubin [Tier 3]
- Bloomberg Intelligence: Custom ASIC shipments growing 44.6% in 2026 vs. GPU 16.1% [Tier 6]

## Estimated Impact

| Dimension | Direction | Magnitude | Confidence |
|-----------|-----------|-----------|------------|
| Revenue | Neutral (TAM growing fast enough to offset share loss) | Low | Medium |
| Margins | Negative (pricing pressure from credible AMD alternative) | Low-Medium | Medium |
| Valuation | Negative (share erosion narrative compresses premium) | Medium | Medium |

## Suggested Action

NVIDIA analysts should: (1) model AI GPU market share erosion scenarios from >80% to 70-75% by 2028, quantifying revenue impact; (2) assess whether CUDA's developer moat is weakening by tracking Triton/ROCm adoption metrics; (3) evaluate whether NVIDIA's Vera Rubin memory capacity disadvantage (288GB vs. AMD's 432GB) matters for next-gen model architectures; (4) investigate whether the OpenAI/Meta AMD deals reduce NVIDIA's per-customer revenue concentration risk or increase competitive pressure.

---

*Filed by Competitive Analyst on 2026-03-09. Check `output/notes/` for related cross-stock notes.*
