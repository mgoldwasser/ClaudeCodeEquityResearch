# NVIDIA (NVDA) — Data Intelligence Memo
## FULL VERSION (Director's Eyes Only — Contains Price Data)
**Prepared by:** Research Analyst (Phase 0)
**Date:** 2026-03-19
**Run:** output/NVDA/2026-03-19/
**Fiscal Year Note:** NVIDIA fiscal year ends last Sunday of January. FY2026 ended January 25, 2026.

---

## 1. DATA RETRIEVAL SUMMARY

### Tier 1 (Foundation) Data — Retrieval Status

| Data Source | Status | File Location | Notes |
|-------------|--------|---------------|-------|
| 10-K FY2026 (Jan 25, 2026) | PARTIAL | input/filings/nvda-10k-fy2026-summary.md | Full text fetched from last10k.com; SEC EDGAR CIK resolution failed for edgar-enhanced.py script — used web research instead |
| 10-Q Q3 FY2026 (Oct 26, 2025) | PARTIAL | References in financials | SEC EDGAR script CIK resolution failure; data from press releases |
| Q4 FY2026 Earnings Transcript | RETRIEVED | input/transcripts/nvda-q4-fy2026-earnings-call.md | Key quotes extracted from Motley Fool + Yahoo Finance transcript |
| Current Market Data | RETRIEVED | input/price-data/nvda-price-data.json | $180.25 as of 2026-03-19 |
| Historical Prices (3Y) | PARTIAL | input/price-data/nvda-price-data.json | Key levels retrieved; full tick data not downloaded |
| Proxy Statement DEF 14A | PARTIAL | input/filings/nvda-10k-fy2026-summary.md | May 2025 proxy referenced; full compensation tables not extracted |
| XBRL Financials | PARTIAL | input/financials/ | SEC EDGAR XBRL tool failed (CIK resolution); reconstructed from press releases and stockanalysis.com |

**EDGAR Tool Note:** The `edgar-enhanced.py` tool returned `{"error": "Could not resolve ticker NVDA to CIK"}` for all NVDA queries. NVDA's SEC CIK is 1045810. This is a tool configuration issue. All Tier 1 data was retrieved via web fetch from official NVIDIA investor relations, last10k.com, and stockanalysis.com as fallback.

### Tier 2 (Analytical Depth) Data — Retrieval Status

| Data Source | Status | File Location | Notes |
|-------------|--------|---------------|-------|
| Insider Trading | RETRIEVED | input/filings/nvda-insider-trading.md | Jensen Huang 10b5-1 plan sales; other insiders partial |
| Institutional Holdings | RETRIEVED | input/alt-data/nvda-institutional-short-interest.md | Vanguard ~8.7%, BlackRock ~7.4%; full 13F not retrieved |
| Short Interest | RETRIEVED | input/alt-data/nvda-institutional-short-interest.md | 0.86% of float (very low) |
| Analyst Estimates | RETRIEVED | input/price-data/nvda-price-data.json | 39 covering; 39 Buy, 1 Hold; avg PT $269 |
| Peers | RETRIEVED | input/market/nvda-competitive-landscape.md | AMD, Intel, custom silicon analyzed |
| Macro Data (FRED) | PARTIAL | input/macro/nvda-macro-data.json | Tools failed; secondary source data used |
| Competitor Overviews | RETRIEVED | input/market/nvda-competitive-landscape.md | AMD, Intel coverage from existing file |

### Tier 3 (Context) Data — Web Research

| Topic | Status | Source Quality |
|-------|--------|----------------|
| Q4 FY2026 earnings results | RETRIEVED | Official press release (Tier 1) |
| GTC 2026 keynote (Mar 16-19, 2026) | RETRIEVED | NVIDIA newsroom + multiple news sources |
| AI GPU TAM (2 independent estimates) | RETRIEVED | Verified Market Research + SparkCo (Tier 6-7) |
| Competitive dynamics | RETRIEVED | Multiple Tier 5-8 sources |
| Bear case / risk factors | RETRIEVED | CNBC, SeekingAlpha (Tier 7-9) |
| Supply chain constraints | RETRIEVED | Tom's Hardware, FusionWW (Tier 6) |
| Export control (H20/China) | RETRIEVED | CNBC, Computer Weekly (Tier 7-8) |
| DeepSeek impact analysis | RETRIEVED | CNBC, TechBrew (Tier 7-8) |

---

## 2. KEY FINANCIAL DATA

### Revenue History and CAGRs

| Fiscal Year | Revenue ($M) | YoY Growth |
|-------------|-------------|-----------|
| FY2022 (Jan 2022) | $26,914 | — |
| FY2023 (Jan 2023) | $26,974 | +0.2% |
| FY2024 (Jan 2024) | $60,922 | +125.8% |
| FY2025 (Jan 2025) | $130,497 | +114.2% |
| FY2026 (Jan 2026) | $215,938 | +65.5% |

**CAGRs:**
- 1-Year (FY25→FY26): **65.5%**
- 3-Year (FY23→FY26): **100.0%** (tripling revenue every year for 3 years)
- 4-Year (FY22→FY26): **68.3%**

### Q4 FY2026 and Forward Guidance

| Metric | Q4 FY2026 | Q1 FY2027 Guidance |
|--------|-----------|-------------------|
| Revenue | $68,100M | $78,000M ±2% |
| Sequential growth | +20% QoQ | +14.5% QoQ |
| YoY growth | +73% | ~98% [ESTIMATED vs Q1 FY2026] |
| Non-GAAP Gross Margin | 75.2% | 75.0% ±50bps |
| Data Center Revenue | $62,300M | [guided by segment in call] |

### Segment Revenue (FY2026 Full Year)

| Segment | Revenue ($M) | % of Total | YoY |
|---------|-------------|-----------|-----|
| Data Center | $193,700 | 89.7% | +68% |
| Gaming | $16,000 | 7.4% | +41% |
| Professional Viz | $3,200 | 1.5% | +70% |
| Automotive & Robotics | $2,300 | 1.1% | +39% |
| **Total** | **$215,938** | **100%** | **+65.5%** |

### Profitability (FY2026)

| Metric | Value |
|--------|-------|
| Gross margin (GAAP) | 71.1% (note: depressed by $4.5B H20 charge in Q1 FY2026) |
| Gross margin (Non-GAAP) | 71.3% |
| Q4 FY2026 gross margin | 75.0% (run-rate without H20 impairment) |
| Operating margin | 60.4% |
| Net income margin | 55.6% |
| FCF | $96,676M |
| FCF margin | 44.8% |
| EPS (GAAP diluted) | $4.90 |
| EPS (Non-GAAP diluted) | $4.77 |

### Balance Sheet (Jan 25, 2026)

| Metric | Value |
|--------|-------|
| Cash + marketable securities | $62,600M |
| Total debt | $11,000M (LT: $7,500M) |
| Net cash | $51,600M |
| Shareholders' equity | $157,300M |
| Diluted shares | ~24,300M |
| Interest coverage | 503x |
| Total assets | $206,800M |

---

## 3. CURRENT PRICE & VALUATION (PRICE DATA — DIRECTOR ONLY)

**Current price (2026-03-19):** $180.25
**52-week range:** $86.62 – $212.19
**All-time high:** $212.19 (Oct 2025 approx)
**Market cap (approx):** ~$4.4 trillion
**Trailing P/E (GAAP):** ~36.8x ($180.25 / $4.90)
**Forward P/E (FY2027E):** ~22-25x [ESTIMATED based on Q1 $78B guidance extrapolation → ~$8 EPS]

**Analyst consensus:** 39 analysts, 39 Buy / 1 Hold / 0 Sell
**Average price target:** ~$269 (range: $220–$380)
**Implied upside from current price:** ~49%

**Stock context:** Trading ~15% below its October 2025 ATH of $212. Per CNBC (2026-03-17), stock has been "in a funk" in early 2026 despite record earnings and strong guidance. Technical consolidation after a near-doubling from April 2025 lows ($86.62).

---

## 4. QUALITATIVE INTELLIGENCE

### Bull Case Data Points
1. **Record results**: FY2026 revenue $215.9B (+65%), Q4 $68.1B (+73% YoY, +20% QoQ)
2. **Guidance acceleration**: Q1 FY2027 guided at $78B — exceeds prior $500B Blackwell/Rubin lifetime opportunity
3. **Inference inflection**: Jensen Huang frames inference as the new secular growth driver ("inference = revenues")
4. **Hyperscaler commitment**: Big 4 hyperscalers spending ~$660B in 2026 capex, 75% AI-directed
5. **CUDA moat**: 4M+ developers, 3,000+ optimized apps, 20-year head start; rewriting to AMD ROCm costs months + $100K+
6. **Supply chain lock-up**: NVIDIA has booked CoWoS capacity years ahead; HBM allocation dominates
7. **$1 trillion opportunity**: Jensen Huang raised revenue visibility to $1T from 2025-2027 at GTC 2026
8. **Vera Rubin roadmap**: 10x inference cost reduction vs. Blackwell; Rubin Ultra in H2 2027 (4x Rubin performance)
9. **New demand waves**: Agentic AI, physical AI/robotics, sovereign AI not yet in revenue run rate
10. **Short interest only 0.86%**: Bears not positioned against stock

### Bear Case Data Points
1. **Valuation**: $4.4T market cap; stock appears ~31% overvalued relative to some intrinsic value estimates ($142.88 fair value per AlphaSpread)
2. **China risk**: H20 chips restricted; $4.5B inventory charge taken; China once ~20%+ of DC revenue; domestic Chinese AI chip development accelerating
3. **Custom silicon displacement**: Custom ASIC shipments growing 44.6% in 2026 vs GPU shipments +16.1%; by 2028, custom chips could be 45% of AI chip market
4. **Market share erosion**: From 87% peak toward 75% by 2026, likely lower long-term
5. **AI spending concentration/circularity**: Top 5 customers = ~50% of revenue; NVIDIA investment in AI companies that buy NVIDIA chips is "circular investment" concern
6. **Jevons paradox — two-sided risk**: More efficient AI (DeepSeek R1 style) could reduce compute per inference — opposite of Jevons
7. **Microsoft slowdown signal**: Reports of Microsoft slowing data center development plans
8. **Size constraint**: Market cap so large that "Nvidia no longer trades like other stocks" — fund flow dynamics different
9. **Gaming supply constraints**: Self-described constraint headwind to Gaming Q1 and beyond
10. **Stock in consolidation**: 15% below ATH; "funk" characterization per CNBC

### Management Tone Analysis
- Jensen Huang tone at GTC 2026: **Highly confident / forward-leaning**
  - Raised revenue opportunity from $500B to $1T
  - "AI is no longer a single breakthrough — it is essential infrastructure"
  - Framed inference as new secular growth driver
- Colette Kress (CFO) at Q4 call: **Precise / conservative on China, bullish on rest**
  - Explicitly excluded China from guidance
  - Guided margins flat (75%) signaling confidence in pricing power
  - Note on sequential growth: "throughout calendar 2026, exceeding" $500B opportunity

---

## 5. SUPPLY CHAIN & COMPETITIVE INTELLIGENCE

### Supply Chain Status (March 2026)
- **CoWoS (advanced packaging):** Oversubscribed through mid-2026; NVIDIA has priority allocation booking 800K-850K wafers in 2026; ~50%+ of TSMC CoWoS capacity
- **HBM3E:** Fully allocated through 2026; Micron HBM sold out through CY2026
- **HBM4:** On track for H2 2025 ramp (for Vera Rubin); SK Hynix and Samsung supplying; NVIDIA secured majority of supply
- **TSMC 3nm:** Vera Rubin on 3nm; production track for H2 2026
- **Implication:** Supply constraints support near-term pricing power; long-term constraints are a risk to revenue upside if demand exceeds packaged output

### Key Competitive Developments (2026)
- AMD MI300X remains best alternative; gaining hyperscaler design wins; but ROCm software significantly behind CUDA
- Groq integration with NVIDIA announced at GTC 2026 (partnership, not competition)
- OpenAI Triton (hardware-agnostic compiler) gaining adoption — slow CUDA erosion

---

## 6. TAM AND DEMAND ANALYSIS

### Two Independent TAM Estimates (Required)
1. **Verified Market Research:** AI GPU market = $120.4B in 2026 (narrow GPU definition)
2. **SparkCo AI Infrastructure:** AI infrastructure TAM = $160B (2025) → $280B (2027) at 25% CAGR (broader definition)

**Top-Down vs. Bottom-Up Reconciliation:**
- Top-down (Verified Market Research): ~$120B for 2026
- Bottom-up (Hyperscaler capex, 75% AI, NVIDIA 90% capture): ~$180B [ESTIMATED]
- **Gap:** ~$60B (50% divergence)
- **Explanation:** Top-down uses narrower "GPU" definition; bottom-up includes networking (NVLink, Spectrum) which NVIDIA generated ~$11B in Q4 FY2026 alone. When networking is included, estimates converge.
- **[DATA GAP]:** Need a third independent TAM estimate from a Tier 4-5 source (Gartner, IDC, McKinsey) for better triangulation.

### Historical vs. Forward CAGRs
- NVIDIA's 3-year revenue CAGR (FY23-FY26): **100.0%** — exceptional
- Forward: Q1 FY2027 guidance implies $78B/quarter → annualized ~$312B (FY2027E), or +44% growth
- **Growth deceleration mechanism**: From 65% to ~44% is structural, not alarming:
  - Base effect (harder to grow 65% on $215B than on $130B)
  - Blackwell ramp completing; Vera Rubin takes time to ramp in H2 2026 / full 2027
  - China revenue excluded from guidance baseline
- **Jevons paradox test:** DeepSeek R1 (Jan 2025) showed more efficient models → more usage, more compute demand. NVDA results validated this: despite efficiency improvements, FY2026 revenue +65%.

### Application Demand Decomposition
See `input/market/nvda-tam-industry-data.json` for full breakdown. Summary:
1. **LLM Training** (Early majority; >95% NVIDIA share) — Driven by model scale
2. **LLM Inference** (Growth; 60-75% share) — Fastest growing by volume; Jevons dynamic strongest here
3. **Agentic AI** (Early adopter; undefined share) — "ChatGPT moment has arrived" per Huang
4. **Sovereign AI** (Early adopter; very high NVIDIA share) — National programs, every country building
5. **Physical AI / Robotics** (Early; revenue ~FY2028+) — Multi-year pipeline
6. **Enterprise AI** (~70% share) — Steady state, CUDA lock-in

---

## 7. GOVERNANCE & ESG SUMMARY

- **Board:** Independent directors met in executive sessions at all 4 quarterly meetings in FY2025
- **Compensation:** Performance-based; say-on-pay vote requested FY2025
- **ESG oversight:** Nominating and Corporate Governance Committee covers AI impact + climate
- **Jensen Huang control:** ~3.5% ownership at $153B+ value; aligned but also entrenched
- **[DATA GAP]:** Specific board diversity statistics, executive pay vs. peers, say-on-pay vote results not retrieved

---

## 8. DATA GAPS AND LIMITATIONS

### Critical Data Gaps
- **[CRITICAL DATA GAP]:** EDGAR tool CIK resolution failure — full 10-K text not retrieved directly. Mitigated by last10k.com and press releases, but some tables (geographic revenue breakdown, note-level debt detail, option grant tables) not fully extracted.
- **[DATA GAP]:** Specific geographic revenue breakdown (US vs. international percentages) not extracted from 10-K.
- **[DATA GAP]:** R&D expense dollar amount for FY2026 not retrieved.
- **[DATA GAP]:** Full executive compensation tables from DEF 14A not extracted.
- **[DATA GAP]:** Options chain (IV, put/call ratio) not retrieved — run `tools/market-data.sh options NVDA`.
- **[DATA GAP]:** FRED API rates and economic series not directly queried — secondary source macro data used.
- **[DATA GAP]:** Full insider trading activity beyond Jensen Huang not retrieved (CFO, Board members).
- **[DATA GAP]:** Altman Z-Score and Beneish M-Score not calculated — requires raw accruals data.
- **[DATA GAP]:** Debt maturity profile and covenant terms not extracted.
- **[DATA GAP]:** Third independent TAM estimate (Gartner, IDC, McKinsey) not retrieved.
- **[DATA GAP]:** NVIDIA Q1-Q3 FY2026 quarterly detail for individual quarters.

### Data Reliability Notes
- Current stock price ($180.25) sourced from multiple web searches — treat as approximate
- Analyst price targets sourced from aggregators (MarketBeat, StockAnalysis) — precise per-analyst targets not individually verified
- Supply chain constraints data from industry blogs (Tom's Hardware, FusionWW) — credible Tier 6, not primary sources
- TAM estimates vary significantly across providers due to scope differences

---

## 9. SOURCE BIBLIOGRAPHY

| # | Source | Tier | Type | Retrieved |
|---|--------|------|------|-----------|
| 1 | NVIDIA Q4 FY2026 Press Release (nvidianews.nvidia.com) | 1 | Financial data | 2026-03-19 |
| 2 | NVIDIA 10-K FY2026 via last10k.com | 1 | Annual filing | 2026-03-19 |
| 3 | NVIDIA Q4 FY2026 Earnings Transcript (Motley Fool) | 2 | Transcript | 2026-03-19 |
| 4 | NVIDIA Q4 FY2026 Earnings Transcript (Yahoo Finance highlights) | 2 | Transcript | 2026-03-19 |
| 5 | StockAnalysis.com — NVDA Income Statement | 3 | Financial data | 2026-03-19 |
| 6 | StockAnalysis.com — NVDA Balance Sheet | 3 | Financial data | 2026-03-19 |
| 7 | StockAnalysis.com — NVDA Cash Flow | 3 | Financial data | 2026-03-19 |
| 8 | SEC EDGAR Form 4 filings (via stocktitan.net, secform4.com) | 4 | Insider trades | 2026-03-19 |
| 9 | NVIDIA GTC 2026 Keynote (NVIDIA newsroom) | 1 | Management commentary | 2026-03-19 |
| 10 | CNBC: "Nvidia GTC 2026: CEO Jensen Huang sees $1 trillion in orders" | 7 | News | 2026-03-19 |
| 11 | Fortune: "Nvidia smashes Q4 2026 with $68 billion in revenue" | 7 | News | 2026-03-19 |
| 12 | Verified Market Research: AI GPU Market | 6 | TAM estimate | 2026-03-19 |
| 13 | SparkCo AI Infrastructure TAM | 7 | TAM estimate | 2026-03-19 |
| 14 | Tom's Hardware: CoWoS supply chain | 6 | Supply chain | 2026-03-19 |
| 15 | Introl Blog: HBM supply cycle | 7 | Supply chain | 2026-03-19 |
| 16 | CNBC: "Nvidia China chip sales" (2026-02-26) | 7 | Risk/China | 2026-03-19 |
| 17 | Computer Weekly: H20 export restrictions | 7 | Risk/China | 2026-03-19 |
| 18 | SiliconAnalysts: NVIDIA market share 2024-2026 | 6 | Market share | 2026-03-19 |
| 19 | MarketBeat: Analyst ratings and PT | 6 | Consensus | 2026-03-19 |
| 20 | Fintel.io: Institutional ownership | 6 | Ownership | 2026-03-19 |
| 21 | Goldman Sachs Macro Outlook (Dec 2025) | 5 | Macro | 2026-03-19 |
| 22 | Deloitte: 2026 Semiconductor Industry Outlook | 5 | Industry | 2026-03-19 |
| 23 | TechBrew: DeepSeek impact analysis | 7 | Bear case | 2026-03-19 |
| 24 | CNBC: "Even a $1 trillion forecast can't break Nvidia out of a 2026 funk" | 7 | Bear case | 2026-03-19 |
| 25 | Seeking Alpha: Bear case analysis | 8 | Bear case | 2026-03-19 |
| 26 | Introl Blog: Hyperscaler capex 2026 | 7 | Demand | 2026-03-19 |
| 27 | NVDA existing competitive landscape file (2026-03-10) | Various | Market | Prior run |

---

## 10. DATA PARTITIONING CONFIRMATION

Files written to correct partitions:

| Partition | Files |
|-----------|-------|
| `input/financials/` | nvda-income-statement.json, nvda-balance-sheet.json |
| `input/transcripts/` | nvda-q4-fy2026-earnings-call.md |
| `input/filings/` | nvda-10k-fy2026-summary.md, nvda-insider-trading.md |
| `input/market/` | nvda-competitive-landscape.md (existing, updated context), nvda-tam-industry-data.json, nvda-product-roadmap.md |
| `input/macro/` | nvda-macro-data.json |
| `input/alt-data/` | nvda-institutional-short-interest.md |
| `input/price-data/` | nvda-price-data.json **[PRICE SENSITIVE — DO NOT SHARE WITH BLINDED ANALYSTS]** |

**BLINDING CONFIRMATION:** All price-derived data (stock price $180.25, P/E ratio, market cap, analyst price targets, EV metrics) has been placed ONLY in `input/price-data/`. All other partitions are free of price-derived valuation data.

---

*End of Data Intelligence Memo — FULL VERSION*
*Prepared: 2026-03-19 | Research Analyst Phase 0*
