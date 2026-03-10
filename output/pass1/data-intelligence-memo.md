# Data Intelligence Memo — AMD (Advanced Micro Devices, Inc.)
Date: 2026-03-09

## Data Inventory

| Data Type | Status | Source | File/Location | Source Tier |
|-----------|--------|--------|---------------|-------------|
| 10-K (FY2025, filed 2026-02-04) | ✅ Retrieved (URLs + summary) | SEC EDGAR / AMD IR | `input/AMD-filing-urls.md` | Tier 1 |
| 10-K/A (FY2025 Amended) | ✅ URL identified | SEC EDGAR / AMD IR | `input/AMD-filing-urls.md` | Tier 1 |
| 10-Q (Q3 FY2025, latest quarterly) | ✅ URL identified | SEC EDGAR / AMD IR | `input/AMD-filing-urls.md` | Tier 1 |
| Q4 FY2025 earnings press release | ✅ Full text retrieved | AMD IR | `input/AMD-Q4-FY2025-earnings-summary.md` | Tier 1 |
| Q4 FY2025 earnings transcript | ✅ Summary retrieved | Motley Fool | `input/AMD-Q4-FY2025-earnings-summary.md` | Tier 2 |
| DEF 14A proxy statement | ⚠️ URL not retrieved (EDGAR CIK issue) | — | [DATA GAP] | — |
| Current market data & valuation | ✅ Retrieved | StockAnalysis.com, WebSearch | `output/data/AMD-market-data.json` | Tier 4 |
| 3-year historical price data | ❌ Not retrieved (market-data.sh bash version error) | — | [DATA GAP — tool error] | — |
| Options chain data | ❌ Not retrieved (market-data.sh bash version error) | — | [DATA GAP — tool error] | — |
| Insider trades (12M) | ✅ Key transactions found | WebSearch (StockTitan, MarketDaily) | See memo below | Tier 2 |
| Institutional ownership | ✅ Summary data | StockAnalysis.com | `output/data/AMD-market-data.json` | Tier 4 |
| Short interest | ✅ Retrieved | StockAnalysis.com | `output/data/AMD-market-data.json` | Tier 4 |
| Analyst consensus & targets | ✅ Retrieved | StockAnalysis.com, WebSearch | `output/data/AMD-market-data.json` | Tier 4 |
| Macro rates data | ✅ Retrieved | Fed H.15, WebSearch | `output/data/AMD-market-data.json` | Tier 5 |
| Semiconductor industry data | ✅ Retrieved | WSTS, Deloitte, StartUs | See memo below | Tier 6 |
| Competitive intelligence | ✅ Comprehensive | Multiple sources | `output/data/AMD-competitive.json` | Tier 2-6 |
| Peer comparison data | ✅ Qualitative | WebSearch | `output/data/AMD-competitive.json` | Tier 6 |
| Bear case evidence | ✅ Specifically searched | Seeking Alpha, WebSearch | See memo below | Tier 6 |
| Management interviews/podcasts | ✅ Key appearances identified | CES 2026, CNBC, Stanford | See memo below | Tier 2-3 |

## Key Findings from External Research

### Recent Developments (Last 90 Days)

**1. Meta Partnership (2026-02-24) — Potentially Transformational**
AMD and Meta announced a 6 GW, multi-year, multi-generational GPU deployment deal for AI infrastructure. Initial 1 GW deployment of custom MI450-based GPUs begins H2 2026. Meta received warrants for 160M AMD shares (~10% of outstanding) at $0.01/share, vesting on deployment milestones and AMD stock price thresholds. Estimated deal revenue: ~$100B over multi-year period. [Source: AMD IR, CNBC, Tom's Hardware — Tier 1-3, retrieved 2026-03-09]

**2. Q4 FY2025 Record Results (2026-02-03)**
Revenue: $10.3B (+34% YoY), beating consensus of $9.7B. Non-GAAP EPS: $1.53 (record). Data Center segment: $5.4B (+39% YoY). Q1 2026 guidance: ~$9.8B (+32% YoY) above consensus of $9.4B. Management reiterated long-term targets including >60% annual DC growth and >$20 EPS. [Source: AMD IR Press Release — Tier 1, retrieved 2026-03-09]

**3. OpenAI Partnership Reaffirmed (Originally announced 2025-10-06)**
6 GW agreement, 1 GW initial MI450 deployment beginning H2 2026. 160M share warrants (separate from Meta warrants). Lisa Su confirmed "on track" on Q4 call. Combined OpenAI + Meta = 12 GW committed, ~$200B+ potential revenue, 320M warrant shares (~20% dilution at full vesting). [Source: AMD IR, OpenAI — Tier 1, retrieved 2026-03-09]

**4. CES 2026 Keynote (2026-01-05)**
Lisa Su outlined MI400 series (MI430X, MI440X, MI455X) and Helios rack-scale architecture. HPE announced as first major Helios partner. TCS partnership for 200MW India deployment. [Source: Engadget, Tom's Hardware — Tier 3, retrieved 2026-03-09]

**5. China Export Controls — Ongoing Risk**
$800M inventory charge taken in 2025 for MI308 products. $1.5-1.8B total 2025 revenue impact. MI308 now approved for export with 15% revenue fee to U.S. Treasury. Q1 2026 guidance includes only $100M China MI308 revenue; no further China revenue assumed. China was ~24% of FY2024 revenue. [Source: AMD 8-K, TechCrunch, The Register — Tier 1-3, retrieved 2026-03-09]

**6. Segment Restructuring (FY2025)**
Client and Gaming segments combined into one reportable segment. Semi-custom gaming revenue declining significantly as current console cycle matures (7th year). Next-gen Xbox AMD SoC expected 2027. [Source: AMD 10-K — Tier 1, retrieved 2026-03-09]

### Analyst Consensus

- **Consensus Rating:** Buy (34 analysts)
- **Rating Breakdown:** Strong Buy: 14 | Buy: 12 | Hold: 8 | Sell: 0
- **Average Price Target:** $261.21 (implied upside: +37.2% from $190.40)
- **Median Price Target:** $280.00
- **Range:** $120.00 — $358.00
- **Recent Rating Changes (Feb 2026):**
  - Evercore ISI (Mark Lipacis): Raised to $358, Buy — most bullish
  - Benchmark (Cody Acree): Reiterated $325, Strong Buy
  - Mizuho (Vijay Rakesh): Raised to $280, Buy
  - Goldman Sachs (James Schneider): Raised to $240, Hold — cautious
  - RBC Capital (Srini Pajjuri): Reiterated $230, Hold — cautious
  - Stephen Guilfoyle: Reset to $274 (down from $320) post-Meta deal
- **Key Observation:** Wide target range ($238 spread) reflects genuine disagreement about execution risk on mega-deals and AI GPU scaling. Hold-rated analysts cluster around $230-240, suggesting limited upside in base case.

[Source: StockAnalysis.com — Tier 4, retrieved 2026-03-09]

### Management Commentary (Beyond Earnings Call)

**Lisa Su at CES 2026 (January 5-10, 2026):**
- Discussed growing AI demand and applications across consumer electronics, healthcare, and space exploration
- Outlined MI400 family and Helios architecture
- "AI demand going through the roof as chip prices hit thousands"
[Source: Fox News podcast, Engadget, Rev.com transcript — Tier 3, retrieved 2026-03-09]

**Lisa Su on CNBC (February 4, 2026):**
- Post-earnings discussion covering CPU business, AI demand state, 2026 outlook
- Addressed guidance concerns and OpenAI relationship status
- Discussed competitive positioning
[Source: CNBC — Tier 3, retrieved 2026-03-09]

**Lisa Su at Stanford GSB:**
- Discussed career trajectory and AMD transformation
- Revenue grown from $5B to ~$35B under her leadership (since 2014)
[Source: Stanford GSB "View From The Top" podcast — Tier 3, retrieved 2026-03-09]

### Competitive Intelligence

**Server CPU Market (AMD EPYC vs. Intel Xeon):**
- AMD server CPU share: 36-40% in 2025 (from 2% in 2017)
- AMD revenue share in servers: 41% in Q2 2025
- EPYC Turin (5th gen) now >50% of AMD server revenue
- ~1,600 EPYC cloud instances (+50% YoY)
- Intel Xeon "more than one generation behind" AMD EPYC
- Analyst projection: AMD could reach 50% server share by 2026
- Performance: Turin delivers up to 40% better than equivalent Intel Xeon in 2P configs
[Source: Fusion Worldwide, TechNetBooks, various — Tier 3-6, retrieved 2026-03-09]

**AI GPU Market (AMD Instinct vs. NVIDIA):**
- NVIDIA holds >80% AI GPU market share
- AMD holds ~8-12%, gained 2.6pp in Q4 2025
- MI350 Series: Fastest ramp in AMD history, deployed at 8/10 top AI companies
- MI355X benchmarks: 20% faster than NVIDIA B200 (DeepSeek R1 FP4), 30% faster (Llama 3.1 405B), 40% more tokens per dollar
- MI450/Helios (H2 2026): 72 GPUs = 1.4 exaFLOPS FP8, 31TB HBM4
- Helios claims 50% more memory capacity than NVIDIA Vera Rubin
- Key AMD weakness: ROCm software ecosystem significantly behind CUDA (6M developers, 300+ libraries vs. smaller ROCm base). CUDA gap score 28.7-99.1 across benchmarks.
[Source: Multiple — Tier 3-6, retrieved 2026-03-09]

**Custom ASIC Threat:**
- Custom ASIC shipments growing 44.6% in 2026 vs. GPU shipments 16.1%
- Google TPU, Amazon Trainium, Microsoft Maia (delayed to 2026), OpenAI custom chip (with Broadcom, mass production 2026)
- Custom ASICs target 15-25% market share, primarily internal hyperscaler inference
- Amazon Trainium: 30-40% better price-performance vs. other vendors
- Mitigation: AMD's OpenAI and Meta deals suggest GPUs remain core infrastructure even for hyperscalers building custom silicon
[Source: CNBC, multiple — Tier 3-6, retrieved 2026-03-09]

**Embedded/FPGA Market:**
- AMD targets >70% revenue market share in adaptive computing
- Embedded segment recovering slowly: $950M Q4 2025 (+2.9% YoY)
- Competition from Lattice Semiconductor (small/mid-range FPGAs) and Intel
- AWS launched FPGA-accelerated instances on AMD EPYC + Xilinx Virtex
[Source: Zacks, AMD IR — Tier 4-6, retrieved 2026-03-09]

### Alternative Data Signals

**Insider Trading (Last 12 Months):**
- Lisa Su (CEO): Net seller via 10b5-1 plans (pre-programmed, not discretionary)
  - Feb 2026: Sold 125,000 shares at avg $214.36 ($26.8M)
  - Dec 2025: Sold ~45,000 shares at avg $212-221
  - Aug 2025: Exercised 224,727 options at $34.19, sold 225,000 shares at $162-166
  - Retains 3,152,476 shares directly + indirect holdings via trusts
- **Signal Assessment:** Consistent, programmatic selling via 10b5-1 plans — NEUTRAL. Not indicative of bearish view. CEO retains substantial position (~$600M+ at current prices).
[Source: StockTitan, MarketDaily, SEC Form 4 — Tier 2, retrieved 2026-03-09]

**Institutional Ownership:** 68.68%
- Typical for mega-cap semi. Not crowded.
[Source: StockAnalysis.com — Tier 4, retrieved 2026-03-09]

**Short Interest:** 1.88% of shares outstanding
- Low short interest. No significant bearish positioning.
- Short interest at 39.2M shares, ~2.4% of float.
- Days to cover: Not retrieved [DATA GAP]
[Source: StockAnalysis.com, Fintel — Tier 4, retrieved 2026-03-09]

### Bear Case Evidence

**1. Valuation Concern (Strongest Bear Argument)**
- Trailing P/E: 71.7x; Forward P/E: 28.6x; PEG: 0.68
- EV/Revenue: 8.87x; EV/EBITDA: 45.5x
- At $190, AMD is priced for near-flawless execution on multiple long-term targets
- Seeking Alpha "You're About To Get Crushed" article argues overvaluation + overhyped OpenAI expectations [Source: Seeking Alpha — Tier 6, accessed 2026-03-09; article was paywalled]

**2. Warrant Dilution Risk**
- 320M warrant shares (OpenAI 160M + Meta 160M) = ~20% potential dilution
- Exercise at $0.01/share is effectively free equity given away
- Full vesting requires $600 stock price (~3x current) but milestones could trigger partial vesting earlier
- At current $190, 160M warrants = ~$30B dilution vs. projected deal revenue — "even swap in NPV terms" per analysts
[Source: Tom's Hardware, The Decoder, multiple — Tier 3-6, retrieved 2026-03-09]

**3. China/Export Control Risk**
- $800M inventory charge already absorbed
- $1.5-1.8B FY2025 revenue lost to export controls
- China was 24% of FY2024 revenue — now guided at ~$100M/quarter
- MI308 exports require 15% fee to U.S. Treasury
- Regulatory environment "very dynamic" — further tightening possible
- Risk of blanket China AI chip ban not priced in
[Source: AMD 8-K, TechCrunch, Register — Tier 1-3, retrieved 2026-03-09]

**4. CUDA/ROCm Software Moat**
- NVIDIA's 18-year CUDA investment creates performance gap of 30-99% across benchmarks
- ROCm developer base fraction of CUDA's 6M developers
- Enterprise customers resistant to switching software stacks
- Risk: Even with superior hardware specs, AMD GPUs underperform NVIDIA in real-world deployments due to software optimization gap
[Source: AIM Multiple, ThunderCompute — Tier 6, retrieved 2026-03-09]

**5. Custom ASIC Cannibalization**
- Custom ASIC growth (44.6%) outpacing GPU growth (16.1%) in 2026
- OpenAI simultaneously building custom chips with Broadcom
- Meta has proprietary chip development programs
- Microsoft Maia already deployed; next-gen Braga in 2026
- Risk: Hyperscalers use AMD GPU deals as bridge while building their own silicon
[Source: CNBC, multiple — Tier 3-6, retrieved 2026-03-09]

**6. Execution Risk on Mega-Deals**
- 12 GW committed deployment is unprecedented for AMD
- MI450 not yet shipping — relies on H2 2026 production ramp
- Supply chain execution (TSMC 3nm/advanced packaging) at scale untested
- If MI450 delays or underperforms, both mega-deals at risk
[ASSUMPTION based on deal structure analysis]

**7. Gaming/Embedded Headwinds**
- Semi-custom gaming declining significantly (console cycle maturity)
- Embedded recovering but slowly (+2.9% YoY in Q4)
- Combined, these segments offset ~25-30% of revenue growth momentum
[Source: AMD earnings, TweakTown — Tier 1-3, retrieved 2026-03-09]

**8. High Beta / Macro Sensitivity**
- Beta of 2.02 — AMD falls ~2x harder than market in downturns
- Fed funds rate at 3.50-3.75%; 10Y at 4.15% — elevated rates pressure growth multiples
- Any macro slowdown compresses the 28.6x forward P/E aggressively
[Source: StockAnalysis.com, Fed data — Tier 4-5, retrieved 2026-03-09]

## Data Gaps

| Data Type | Reason | Impact | Priority |
|-----------|--------|--------|----------|
| DEF 14A (Proxy Statement) | EDGAR CIK resolution failed for AMD (tool bug) | Limits governance/comp analysis | Medium — ESG analyst should retrieve via `https://ir.amd.com/financial-information/sec-filings` |
| 3-year historical price data | `market-data.sh` bash version incompatibility (`${1^^}` not supported) | Limits technical analysis, drawdown analysis | High — Technical Analyst should use WebFetch on Yahoo Finance |
| Options chain data | Same bash tool error | Limits implied volatility analysis, put/call analysis | Medium — Trade Structurer should retrieve directly |
| Full 10-K text | EDGAR CIK resolution failed | Analysts lack full filing text for risk factors, segment detail | High — Use direct URL: `https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000018/amd-20251227.htm` |
| Days to cover (short interest) | MarketBeat blocked (403) | Minor — short interest is low at 1.88% | Low |
| FRED macro time series | No FRED API key configured | Macro Analyst should use WebFetch on FRED CSV URLs | Medium |
| Competitor financials (NVDA, INTC) | Not retrieved for this memo | Quant Analyst needs for comp table | High — use EDGAR or WebSearch |
| Institutional holdings detail | Yahoo/WhaleWisdom not fetched | Limits ownership change analysis | Medium |
| AMD patent activity | Not retrieved | Limits innovation assessment | Low |
| Employee sentiment (Glassdoor) | Not retrieved | Limits qualitative assessment | Low |

## Source Bibliography

### Tier 1 — SEC Filings & Official Disclosures
1. AMD 10-K FY2025 (filed 2026-02-04): https://ir.amd.com/financial-information/sec-filings/content/0000002488-26-000018/amd-20251227.htm [Retrieved 2026-03-09]
2. AMD Q4 FY2025 Press Release: https://ir.amd.com/news-events/press-releases/detail/1276/amd-reports-fourth-quarter-and-full-year-2025-financial-results [Retrieved 2026-03-09]
3. AMD-OpenAI Partnership Press Release (2025-10-06): https://ir.amd.com/news-events/press-releases/detail/1260/ [Retrieved 2026-03-09]
4. AMD-Meta Partnership Press Release (2026-02-24): https://ir.amd.com/news-events/press-releases/detail/1279/ [Retrieved 2026-03-09]
5. AMD-HPE Helios Press Release (2025-12-02): https://ir.amd.com/news-events/press-releases/detail/1269/ [Retrieved 2026-03-09]
6. AMD 8-K — $800M Export Control Charge (2025-04-16): https://ir.amd.com/financial-information/sec-filings/content/0000002488-25-000039/amd-20250415.htm [Retrieved 2026-03-09]

### Tier 2 — Earnings Transcripts & Insider Filings
7. AMD Q4 FY2025 Earnings Call Transcript: https://www.fool.com/earnings/call-transcripts/2026/02/03/amd-amd-q4-2025-earnings-call-transcript/ [Retrieved 2026-03-09]
8. Lisa Su Form 4 (Feb 2026 sale): https://www.stocktitan.net/sec-filings/AMD/form-4-advanced-micro-devices-inc-insider-trading-activity-77336ff2e4d5.html [Retrieved 2026-03-09]

### Tier 3 — Company IR & News
9. AMD CES 2026 Keynote: https://www.engadget.com/computing/amd-at-ces-2026-live-updates-from-ceo-lisa-sus-keynote-presentation-190012370.html [Retrieved 2026-03-09]
10. CNBC Lisa Su Interview (2026-02-04): https://www.cnbc.com/video/2026/02/04/watch-cnbcs-full-interview-with-amd-chair-and-ceo-lisa-su.html [Retrieved 2026-03-09]
11. CNBC Meta-AMD Deal Coverage: https://www.cnbc.com/2026/02/24/meta-to-use-6gw-of-amd-gpus-days-after-expanded-nvidia-ai-chip-deal.html [Retrieved 2026-03-09]
12. Tom's Hardware AMD-Meta Deal: https://www.tomshardware.com/tech-industry/artificial-intelligence/amd-meta-100-billion-deal [Retrieved 2026-03-09]
13. Futurum Group Q4 Analysis: https://futurumgroup.com/insights/amd-q4-fy-2025-record-data-center-and-client-momentum/ [Retrieved 2026-03-09]
14. The Decoder AMD-Meta Analysis: https://the-decoder.com/amd-basically-copy-pasted-its-openai-deal-for-meta-six-gigawatts-and-ten-percent-equity-included/ [Retrieved 2026-03-09]
15. TechCrunch $800M Charge: https://techcrunch.com/2025/04/16/amd-takes-800m-charge-on-us-license-requirement-for-ai-chips/ [Retrieved 2026-03-09]
16. Quartz $800M Charge: https://qz.com/amd-lisa-su-china-export-restrictions-commerce-department [Retrieved 2026-03-09]

### Tier 4 — Financial Data Aggregators
17. StockAnalysis.com AMD Statistics: https://stockanalysis.com/stocks/amd/statistics/ [Retrieved 2026-03-09]
18. StockAnalysis.com AMD Forecast: https://stockanalysis.com/stocks/amd/forecast/ [Retrieved 2026-03-09]
19. MacroTrends AMD P/E: https://www.macrotrends.net/stocks/charts/AMD/amd/pe-ratio [Retrieved 2026-03-09]
20. MarketBeat AMD Forecast: https://www.marketbeat.com/stocks/NASDAQ/AMD/forecast/ [Attempted 2026-03-09; 403 blocked]

### Tier 5 — Government/Official Data
21. Federal Reserve H.15 Rates (2026-03-06): https://www.federalreserve.gov/releases/h15/ [Retrieved 2026-03-09]
22. WSTS Semiconductor Forecast: https://www.wsts.org/76/Global-Semiconductor-Market-Approaches-1T-in-2026 [Retrieved 2026-03-09]

### Tier 6 — Industry Reports & Analysis
23. Deloitte Semiconductor Industry Outlook 2026: https://www.deloitte.com/us/en/insights/industry/technology/technology-media-telecom-outlooks/semiconductor-industry-outlook.html [Retrieved 2026-03-09]
24. Fusion Worldwide Server CPU Market: https://www.fusionww.com/insights/blog/server-cpu-market-dynamics-in-2025 [Retrieved 2026-03-09]
25. TechNetBooks GPU Market Report Q4 2025: https://www.technetbooks.com/2026/03/global-gpu-market-report-q4-2025.html [Retrieved 2026-03-09]
26. AIM Multiple CUDA vs ROCm: https://research.aimultiple.com/cuda-vs-rocm/ [Retrieved 2026-03-09]
27. Seeking Alpha Bear Case: https://seekingalpha.com/article/4831137-amd-youre-about-to-get-crushed [Attempted 2026-03-09; paywalled]
28. Precedence Research AI Data Center GPU Market: https://www.precedenceresearch.com/ai-data-center-gpu-market [Retrieved 2026-03-09]
29. Chipstrat AMD AI Accelerator Analysis: https://www.chipstrat.com/p/amds-ai-accelerator-business-puts [Retrieved 2026-03-09]

---

## Research Analyst Summary

AMD is one of the most well-covered stocks in the semiconductor universe with extensive analyst coverage (34 analysts), deep sell-side research, and high retail investor interest. The data picture is comprehensive with one notable gap: the EDGAR tool failed CIK resolution for AMD (CIK: 0000002488), preventing automated retrieval of full 10-K text, proxy statement, and XBRL financials — analysts should retrieve these directly from the filing URLs provided above.

**The single most important finding not in the filings:** The combined OpenAI + Meta deals (announced October 2025 and February 2026 respectively) represent a potential step-function change in AMD's AI GPU business trajectory. Together they commit 12 GW of deployment with ~$200B in potential multi-year revenue — but come with 320M warrant shares (~20% potential dilution) that vest on deployment and $600 stock price milestones. This creates a unique risk/reward dynamic where the bull case depends on AMD executing at a scale it has never achieved, while failure risk is partially mitigated by the fact that full dilution only occurs alongside massive revenue realization. The market has not fully processed the dilution implications — the stock trades at $190, and full vesting requires $600.

**Critical data gaps that could undermine analysis:** (1) Full 10-K text needed for detailed segment margins, risk factors, and off-balance-sheet items. (2) Historical price data not retrieved — technical analyst needs this urgently. (3) Options chain data missing — needed for implied volatility and trade structuring. (4) Competitor financial data (NVDA, INTC) not retrieved for comp analysis.

**Information environment:** Well-covered large-cap with strong analyst following. Key differentiation comes from understanding the deal economics of the OpenAI/Meta partnerships, the CUDA/ROCm software gap's real-world impact, and the China regulatory tail risk. The bear case is under-discussed relative to the bull case in public discourse — most coverage is promotional. The 8 bear case vectors identified above deserve rigorous modeling.
