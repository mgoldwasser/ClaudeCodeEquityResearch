# Comprehensive Free Data Sources for Equity Research
## Compiled: March 2026 | For Automated Data Retrieval Systems

---

## 1. SEC/REGULATORY FILINGS

### 1.1 SEC EDGAR Official APIs (data.sec.gov)
- **URL**: https://data.sec.gov
- **Data**: All SEC filings, XBRL financial data, submission histories
- **Registration**: None required. No API key needed.
- **Rate Limit**: 10 requests/second. Must include descriptive `User-Agent` header (e.g., `CompanyName admin@company.com`).
- **Access Method**: REST API returning JSON

**Key Endpoints:**

| Endpoint | URL Pattern | Description |
|----------|------------|-------------|
| Submissions | `https://data.sec.gov/submissions/CIK{10-digit}.json` | Full filing history for a company |
| Company Facts | `https://data.sec.gov/api/xbrl/companyfacts/CIK{10-digit}.json` | All XBRL data for a company across all filings |
| Company Concept | `https://data.sec.gov/api/xbrl/companyconcept/CIK{10-digit}/us-gaap/{Tag}.json` | Single XBRL concept history (e.g., `Revenue`, `Assets`) |
| Frames | `https://data.sec.gov/api/xbrl/frames/us-gaap/{Tag}/{Unit}/{Period}.json` | Cross-company comparison for one concept in one period |
| Bulk Submissions | `https://data.sec.gov/submissions/submissions.zip` | All submission metadata |
| Bulk Company Facts | `https://data.sec.gov/api/xbrl/companyfacts/companyfacts.zip` | All XBRL data |

**Period Format for Frames**: `CY2024` (annual), `CY2024Q1` (quarterly duration), `CY2024Q1I` (instantaneous/balance sheet)

**Lookup Files**:
- `https://www.sec.gov/files/company_tickers.json` -- ticker to CIK mapping
- `https://www.sec.gov/files/company_tickers_exchange.json` -- ticker, CIK, exchange mapping

### 1.2 EDGAR Full-Text Search (efts.sec.gov)
- **URL**: https://efts.sec.gov/LATEST/search-index
- **Web UI**: https://www.sec.gov/cgi-bin/browse-edgar and https://efts.sec.gov/LATEST/search-index?q=...
- **Data**: Full-text search across all filings since 2001, including exhibits
- **Registration**: None
- **Rate Limit**: 10 req/sec (same fair-access policy)
- **Access Method**: HTTP GET with query parameters

**Query Parameters**:
- `q` -- search term or phrase
- `dateRange` -- filter by filing date (e.g., `custom&startdt=2024-01-01&enddt=2024-12-31`)
- `forms` -- comma-separated form types (e.g., `10-K,10-Q`)
- `from` -- pagination offset

### 1.3 EDGAR Filing Index
- **URL**: `https://www.sec.gov/Archives/edgar/full-index/`
- **Data**: Master index files of all filings, organized by year/quarter
- **Access Method**: Direct download of `.idx` files
- **Pattern**: `https://www.sec.gov/Archives/edgar/full-index/{YYYY}/QTR{1-4}/master.idx`

### 1.4 EdgarTools (Python Library)
- **URL**: https://github.com/dgunning/edgartools
- **Install**: `pip install edgartools`
- **Data**: Parsed SEC filings (10-K, 10-Q, 8-K, 13F, Form 4, DEF 14A, S-1, etc.) as Python objects and Pandas DataFrames
- **Registration**: None (uses SEC APIs directly)
- **Rate Limit**: Inherits SEC 10 req/sec limit
- **Notes**: Full XBRL standardization, cross-company comparisons, MIT license

### 1.5 sec-api.io (Third-Party Enhanced)
- **URL**: https://sec-api.io
- **Data**: Full-text search, XBRL-to-JSON, real-time WebSocket stream, 18M+ filings
- **Registration**: Yes (free API key)
- **Free Tier**: Limited queries; paid tiers for production use
- **Access Method**: REST API + WebSocket

---

## 2. EARNINGS CALL TRANSCRIPTS

### 2.1 Motley Fool Transcripts
- **URL**: https://www.fool.com/earnings-call-transcripts/
- **Data**: Earnings call transcripts for companies they cover
- **Registration**: None for basic access
- **Access Method**: Web scraping (HTML pages)
- **URL Pattern**: `https://www.fool.com/earnings/call-transcripts/{YYYY}/{MM}/{DD}/{company-slug}/`
- **Scraping Tools**:
  - `pip install foolcalls` (Python: https://github.com/talsan/foolcalls)
  - https://github.com/hamid-vakilzadeh/motley-fool-scraper
- **Pre-scraped Dataset**: https://www.kaggle.com/datasets/tpotterer/motley-fool-scraped-earnings-call-transcripts (18,755 transcripts)

### 2.2 Seeking Alpha Transcripts
- **URL**: https://seekingalpha.com/earnings/earnings-call-transcripts
- **Data**: 4,500+ companies per earnings season
- **Registration**: Free account for limited access
- **Restrictions**: Free tier severely limited; most transcripts behind paywall ($239/yr Premium). Heavy anti-scraping (Cloudflare/PerimeterX). Copyright restrictions on commercial use.
- **Access Method**: Not reliably scrapable for automated systems

### 2.3 Finnhub Earnings Transcripts API
- **URL**: https://finnhub.io/docs/api/earnings-call-transcripts-api
- **Endpoint**: `GET https://finnhub.io/api/v1/stock/transcripts?symbol=AAPL&token={API_KEY}`
- **Registration**: Yes (free API key)
- **Rate Limit**: 60 calls/minute on free tier
- **Data**: Transcript text with speaker identification

### 2.4 Company Investor Relations Pages
- **Access Method**: Direct navigation to company IR pages
- **Common Patterns**:
  - `https://investor.{company}.com/`
  - `https://ir.{company}.com/`
  - `https://www.{company}.com/investor-relations/`
- **Data**: Earnings releases, call transcripts/webcasts, presentations, SEC filings
- **Examples**:
  - Apple: https://investor.apple.com/
  - Microsoft: https://www.microsoft.com/en-us/investor
  - Amazon: https://ir.aboutamazon.com/
- **Notes**: Many companies now post full transcripts; others only post audio webcasts

### 2.5 EarningsCall.biz
- **URL**: https://earningscall.biz/api-guide
- **Data**: Earnings call transcripts, audio files, schedules
- **Registration**: Yes
- **Access Method**: REST API
- **Free Tier**: Limited

---

## 3. SELL-SIDE RESEARCH (FREE ACCESS)

### 3.1 Broker Research via Free Brokerage Accounts
Open a zero-cost brokerage account to access sell-side research:

| Broker | URL | Research Available | Registration |
|--------|-----|-------------------|-------------|
| Charles Schwab | https://www.schwab.com/research | ~10 third-party analyst firms, Schwab's own research | Free account required |
| Fidelity | https://www.fidelity.com/stock-trading/overview | 20+ analyst firms (most comprehensive) | Free account required |
| Interactive Brokers | https://www.interactivebrokers.com/ | Analyst reports, fundamentals | Free account required |

### 3.2 Federal Reserve Research (Equity-Adjacent)
- **Fed Board**: https://www.federalreserve.gov/econres.htm (working papers, financial stability reports)
- **NBER Working Papers**: https://www.nber.org/papers (many equity-relevant, free access to abstracts)
- **St. Louis Fed (FRASER)**: https://fraser.stlouisfed.org/ (historical economic documents)
- **Regional Fed Banks**:
  - NY Fed: https://www.newyorkfed.org/research
  - Chicago Fed: https://www.chicagofed.org/publications/index
  - Minneapolis Fed: https://www.minneapolisfed.org/economic-research/working-papers
- **Access Method**: Direct PDF download, RSS feeds
- **Registration**: None

### 3.3 SSRN / Academic Research
- **URL**: https://papers.ssrn.com/
- **Data**: Pre-print academic papers on equity markets, factor investing, valuation
- **Registration**: Free account
- **Access Method**: Direct download, search API

### 3.4 BIS (Bank for International Settlements)
- **URL**: https://www.bis.org/research/
- **Data**: Global financial stability research, cross-border capital flows
- **Registration**: None
- **Access Method**: PDF download

---

## 4. PODCAST TRANSCRIPTS (FUNDAMENTAL ANALYSIS)

### 4.1 Invest Like the Best (Colossus)
- **URL**: https://www.joincolossus.com/episodes
- **Transcripts**: Published on the website for each episode
- **Access Method**: Web scraping of episode pages
- **Third-Party Transcripts**: https://podcasts.happyscribe.com/invest-like-the-best

### 4.2 Odd Lots (Bloomberg)
- **URL**: https://www.bloomberg.com/oddlots
- **Transcripts**: Available on Bloomberg.com (some may require subscription)
- **Free Transcript Aggregators**:
  - Metacast: https://metacast.app/podcast/odd-lots/BsS6SNUS
  - Tapesearch: https://www.tapesearch.com/podcast/odd-lots/1056200096

### 4.3 The Acquirers Podcast
- **URL**: https://acquirersmultiple.com/podcast/
- **Transcripts**: Check individual episode pages
- **Access Method**: Web scraping; also check YouTube auto-generated transcripts

### 4.4 General Podcast Transcript Sources
- **Spotify**: Now provides auto-generated transcripts for many podcasts
- **Apple Podcasts**: Transcript support for many shows
- **YouTube**: Auto-generated captions downloadable via `youtube-transcript-api` Python package (`pip install youtube-transcript-api`)
- **Podscribe**: https://podscribe.ai/ (AI-generated transcripts for popular podcasts)

---

## 5. FINANCIAL DATA APIs (FREE TIERS)

### 5.1 Alpha Vantage
- **URL**: https://www.alphavantage.co/
- **Docs**: https://www.alphavantage.co/documentation/
- **Registration**: Yes (free API key at https://www.alphavantage.co/support/#api-key)
- **Rate Limit**: 25 requests/day, 5 requests/minute on free tier
- **Data**: Stock prices (daily/intraday), forex, crypto, 50+ technical indicators, fundamental data (income statement, balance sheet, cash flow), economic indicators
- **Endpoint Examples**:
  - Daily prices: `https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey={KEY}`
  - Income statement: `https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=AAPL&apikey={KEY}`
  - RSI: `https://www.alphavantage.co/query?function=RSI&symbol=AAPL&interval=daily&time_period=14&series_type=close&apikey={KEY}`
- **Format**: JSON, CSV

### 5.2 Yahoo Finance (yfinance)
- **URL**: https://github.com/ranaroussi/yfinance
- **Install**: `pip install yfinance`
- **Registration**: None
- **Rate Limit**: Unofficial/undocumented; subject to throttling. Personal use only.
- **Data**: Real-time quotes, historical OHLCV, dividends, splits, options chains, financial statements, analyst recommendations, institutional holders
- **Python Example**:
  ```python
  import yfinance as yf
  ticker = yf.Ticker("AAPL")
  hist = ticker.history(period="1y")
  income = ticker.financials
  balance = ticker.balance_sheet
  options = ticker.options
  ```
- **Caution**: Unofficial API; may break if Yahoo changes site structure. Not for commercial use.

### 5.3 Financial Modeling Prep (FMP)
- **URL**: https://site.financialmodelingprep.com/
- **Docs**: https://site.financialmodelingprep.com/developer/docs
- **Registration**: Yes (free API key)
- **Rate Limit**: 250 requests/day on free tier
- **Data**: Financial statements, ratios, DCF, stock prices, earnings transcripts, press releases, 13F filings, ESG scores, SEC filings
- **Endpoint Examples**:
  - Profile: `https://financialmodelingprep.com/api/v3/profile/AAPL?apikey={KEY}`
  - Income: `https://financialmodelingprep.com/api/v3/income-statement/AAPL?limit=10&apikey={KEY}`
  - Earnings transcript: `https://financialmodelingprep.com/api/v3/earning_call_transcript/AAPL?quarter=4&year=2024&apikey={KEY}`

### 5.4 Finnhub
- **URL**: https://finnhub.io/
- **Docs**: https://finnhub.io/docs/api
- **Registration**: Yes (free API key)
- **Rate Limit**: 60 calls/minute (most generous free tier)
- **Data**: Real-time US stock prices, company profiles, financials, news, analyst recommendations, earnings, insider transactions, ESG, patent data, SEC filings
- **Endpoint Examples**:
  - Quote: `GET https://finnhub.io/api/v1/quote?symbol=AAPL&token={KEY}`
  - Company news: `GET https://finnhub.io/api/v1/company-news?symbol=AAPL&from=2024-01-01&to=2024-12-31&token={KEY}`
  - Financials: `GET https://finnhub.io/api/v1/stock/financials-reported?symbol=AAPL&token={KEY}`
  - Press releases: `GET https://finnhub.io/api/v1/press-releases?symbol=AAPL&token={KEY}`

### 5.5 Polygon.io
- **URL**: https://polygon.io/
- **Registration**: Yes (free tier available)
- **Rate Limit**: 5 calls/minute on free tier; limited historical data
- **Data**: Stock prices, options, forex, crypto with very low latency (<10ms)
- **Endpoint Example**: `GET https://api.polygon.io/v2/aggs/ticker/AAPL/range/1/day/2024-01-01/2024-12-31?apiKey={KEY}`
- **Formats**: REST + WebSocket

### 5.6 FRED (Federal Reserve Economic Data)
- **URL**: https://fred.stlouisfed.org/
- **Docs**: https://fred.stlouisfed.org/docs/api/fred/
- **Registration**: Yes (free API key at https://fred.stlouisfed.org/docs/api/api_key.html)
- **Rate Limit**: 120 requests/minute
- **Data**: 765,000+ time series -- GDP, inflation, unemployment, interest rates, yield curves, money supply, housing, and many more
- **Endpoint Examples**:
  - Series data: `https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key={KEY}&file_type=json`
  - Search: `https://api.stlouisfed.org/fred/series/search?search_text=unemployment+rate&api_key={KEY}&file_type=json`
- **Python**: `pip install fredapi`
  ```python
  from fredapi import Fred
  fred = Fred(api_key='{KEY}')
  data = fred.get_series('UNRATE')
  ```

---

## 6. ALTERNATIVE DATA

### 6.1 Reddit Sentiment Data

#### Arctic Shift (Pushshift Successor)
- **URL**: https://arctic-shift.photon-reddit.com/
- **GitHub**: https://github.com/ArthurHeitmann/arctic_shift
- **Data**: Historical Reddit submissions and comments (archive of Pushshift data)
- **Access Method**: API for queries; bulk data via Academic Torrents (zst compressed dumps)
- **Registration**: None
- **Limitations**: FTS only per-user or per-subreddit (not Reddit-wide)
- **Key Subreddits for Equity Research**: r/wallstreetbets, r/stocks, r/investing, r/SecurityAnalysis, r/options

#### PullPush.io
- **URL**: https://pullpush.io/
- **Data**: Reddit submissions and comments with full-text search
- **Access Method**: REST API
- **Advantage**: Reddit-wide full-text search capability

#### Reddit Official API
- **URL**: https://www.reddit.com/dev/api/
- **Registration**: Yes (OAuth required)
- **Rate Limit**: 60 requests/minute for OAuth clients
- **Limitations**: Limited historical data; current/recent posts only

### 6.2 Google Trends
- **URL**: https://trends.google.com/trends/
- **Python Library**: `pip install pytrends`
- **Registration**: None (unofficial API)
- **Rate Limit**: ~1,400 sequential requests before throttling; use 60-second sleep between requests
- **Data**: Relative search interest over time, by region, related queries
- **Python Example**:
  ```python
  from pytrends.request import TrendReq
  pytrends = TrendReq()
  pytrends.build_payload(['AAPL', 'MSFT'], timeframe='today 12-m')
  data = pytrends.interest_over_time()
  ```
- **Caution**: Unofficial/reverse-engineered; 429 errors common. Use proxies and sleep for production.

### 6.3 USPTO Patent Data

#### PatentsView
- **URL**: https://patentsview.org/
- **API Docs**: https://patentsview.org/apis/api-endpoints
- **Data**: All granted US patents with assignee, inventor, classification, citation data
- **Registration**: Free API key
- **Access Method**: REST API + bulk CSV downloads at https://patentsview.org/download/data-download-tables
- **Endpoint Example**: `https://api.patentsview.org/patents/query?q={"assignee_organization":"Apple Inc"}&f=["patent_number","patent_title","patent_date"]`

#### USPTO Open Data Portal
- **URL**: https://data.uspto.gov/
- **Bulk Downloads**: https://data.uspto.gov/bulkdata
- **Data**: Patent applications, grants, trademark data
- **Registration**: None for bulk downloads

### 6.4 Job Postings as Growth Proxy

#### Revelio Labs Public Labor Statistics (RPLS)
- **URL**: https://www.reveliolabs.com/public-labor-statistics/
- **Data**: Free macroeconomic labor dataset from 100M+ US profiles -- employment levels, wages, job transitions
- **Registration**: Free access
- **Access Method**: Download from website

#### Indeed Hiring Lab
- **URL**: https://www.hiringlab.org/
- **Data**: Aggregate job posting trends by industry, metro area, occupation
- **Access Method**: Published reports and downloadable charts/data
- **Registration**: None

---

## 7. MACRO DATA

### 7.1 FRED (Federal Reserve Economic Data)
- (See Section 5.6 above for full details)
- **Key Series IDs**: GDP, UNRATE, CPIAUCSL, FEDFUNDS, T10Y2Y, DEXUSEU, VIXCLS, M2SL, UMCSENT

### 7.2 Bureau of Labor Statistics (BLS)
- **URL**: https://www.bls.gov/developers/
- **API Docs**: https://www.bls.gov/developers/api_signature_v2.htm
- **Registration**: Version 1 -- No registration. Version 2 -- Free registration (email for API key)
- **Rate Limit**: V1: 25 queries/day, 10 years, 25 series. V2: 500 queries/day, 20 years, 50 series.
- **Data**: CPI, PPI, employment/unemployment, wages, productivity
- **Endpoint**: `POST https://api.bls.gov/publicAPI/v2/timeseries/data/`
- **Request Body**: `{"seriesid": ["CUUR0000SA0", "LNS14000000"], "startyear": "2020", "endyear": "2024", "registrationkey": "{KEY}"}`
- **Popular Series Endpoint**: `https://api.bls.gov/publicAPI/v2/timeseries/popular?survey=CU&registrationkey={KEY}`

### 7.3 Bureau of Economic Analysis (BEA)
- **URL**: https://www.bea.gov/tools
- **API Signup**: https://apps.bea.gov/api/signup/ (free)
- **Endpoint**: `https://apps.bea.gov/api/data/?&UserID={KEY}&method=GetData&DataSetName=NIPA&TableName=T10101&Frequency=Q&Year=2024&ResultFormat=JSON`
- **Data**: GDP, personal income, corporate profits, international trade, regional economic data
- **Datasets**: NIPA, Fixed Assets, GDP by Industry, International Transactions, Regional

### 7.4 Census Bureau
- **URL**: https://www.census.gov/data/developers.html
- **API Key Signup**: https://api.census.gov/data/key_signup.html (free)
- **Data**: Population, housing, business establishment counts, retail sales, international trade
- **Endpoint Example**: `https://api.census.gov/data/2023/acs/acs1?get=B01003_001E,NAME&for=state:*&key={KEY}`
- **Key Datasets**: ACS 1-Year, ACS 5-Year, Economic Census, County Business Patterns, International Trade

### 7.5 World Bank
- **URL**: https://data.worldbank.org/
- **API Docs**: https://datahelpdesk.worldbank.org/knowledgebase/articles/889392
- **Registration**: None
- **Rate Limit**: None documented
- **Data**: 16,000+ time series -- GDP, population, poverty, education, health for 200+ countries
- **Endpoint Example**: `https://api.worldbank.org/v2/country/US/indicator/NY.GDP.MKTP.CD?format=json&date=2015:2024`
- **Format**: JSON, XML

### 7.6 IMF Data
- **URL**: https://data.imf.org/
- **API**: SDMX 2.1 and 3.0 APIs
- **Registration**: None
- **Data**: World Economic Outlook (GDP forecasts, inflation, unemployment for 190+ countries), Balance of Payments, International Financial Statistics
- **WEO Dataset**: https://data.imf.org/en/datasets/IMF.RES:WEO
- **Endpoint Pattern**: `https://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/{database}/{dimensions}?startPeriod={year}&endPeriod={year}`

---

## 8. ESG/GOVERNANCE DATA

### 8.1 SEC N-PX Filings (Proxy Voting Records)
- **URL**: Search EDGAR for Form N-PX filings
- **Data**: How institutional investors voted on proxy proposals (including say-on-pay). XML-structured since August 2024.
- **Access Method**: EDGAR full-text search for `N-PX` filings, or direct index at `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=N-PX`
- **Registration**: None
- **Notes**: Since Aug 2024, 13F filers must also report executive compensation votes via N-PX

### 8.2 SEC DEF 14A (Proxy Statements / Executive Compensation)
- **URL**: Search EDGAR for DEF 14A filings
- **Data**: Executive compensation tables, board composition, governance policies, shareholder proposals
- **Access Method**: EDGAR search; parse HTML/XML filing documents
- **Python**: Use EdgarTools to parse proxy statements programmatically

### 8.3 SEC Executive Compensation Data
- **URL**: https://www.sec.gov/data-research/sec-markets-data
- **Data**: Structured executive compensation extracted from filings
- **Access Method**: Bulk download

### 8.4 ESG Scores (Free Sources)
- **Finnhub ESG**: `GET https://finnhub.io/api/v1/stock/esg?symbol=AAPL&token={KEY}` (free tier)
- **FMP ESG**: `https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data?symbol=AAPL&apikey={KEY}`
- **MSCI ESG Ratings**: https://www.msci.com/our-solutions/esg-investing/esg-ratings/esg-ratings-corporate-search-tool (limited free lookup)
- **CSRHub**: https://www.csrhub.com/ (limited free access to ESG ratings)

### 8.5 Corporate Governance Data
- **SEC Ownership Data**: 13F filings (see Section 13)
- **Board Composition**: Parseable from DEF 14A filings via EdgarTools
- **ISS/Glass Lewis**: Subscription required for full data; limited free summaries

---

## 9. TECHNICAL/MARKET DATA

### 9.1 Free Historical Price Data
- **Yahoo Finance (yfinance)**: See Section 5.2. Full daily OHLCV back to ~1970 for major tickers.
- **Alpha Vantage**: See Section 5.1. 20+ years daily, intraday with free tier limits.
- **Stooq**: https://stooq.com/ -- Direct CSV downloads: `https://stooq.com/q/d/l/?s={TICKER}.us&d1={YYYYMMDD}&d2={YYYYMMDD}&i=d`
- **NASDAQ Data Link (formerly Quandl)**: https://data.nasdaq.com/ -- Some free datasets remain (WIKI prices dataset discontinued but alternatives exist)

### 9.2 Options Data
- **Yahoo Finance (yfinance)**: Options chains via `ticker.option_chain(date)` -- free, real-time
- **CBOE**: https://www.cboe.com/market_statistics/ -- Daily market statistics, put/call ratios
- **OCC (Options Clearing Corp)**: https://www.theocc.com/Market-Data/Market-Data-Reports -- Volume/open interest reports

### 9.3 Short Interest Data (FINRA)

#### Daily Short Sale Volume
- **URL**: https://www.finra.org/finra-data/browse-catalog/short-sale-volume-data/daily-short-sale-volume-files
- **API**: `GET https://api.finra.org/data/group/otcMarket/name/regSHODaily` at https://developer.finra.org/
- **Data**: Daily aggregated short sale volume by security
- **Format**: CSV or JSON
- **Registration**: None for file downloads; API registration for developer center

#### Short Interest (Bi-Monthly)
- **URL**: https://www.finra.org/finra-data/browse-catalog/equity-short-interest
- **API Endpoint**: `https://api.finra.org/data/group/otcMarket/name/EquityShortInterest`
- **Data**: Short interest positions reported twice monthly
- **Historical**: 5 rolling years available for free

---

## 10. INDUSTRY/SECTOR DATA

### 10.1 Energy (EIA)
- **URL**: https://www.eia.gov/opendata/
- **API Docs**: https://www.eia.gov/opendata/documentation.php
- **Registration**: Yes (free API key at https://www.eia.gov/opendata/register.php)
- **Data**: Oil/gas production, refinery data, electricity generation, prices, inventories, emissions, renewables
- **Base Endpoint**: `https://api.eia.gov/v2/`
- **Example**: `https://api.eia.gov/v2/petroleum/pri/spt/data/?api_key={KEY}&frequency=daily&data[0]=value&facets[product][]=EPCBRENT`
- **Categories**: petroleum, natural-gas, electricity, coal, nuclear-outages, total-energy, SEDS
- **Dashboard**: https://www.eia.gov/opendata/browser/

### 10.2 Pharma/Biotech (FDA)
- **URL**: https://open.fda.gov/
- **API Docs**: https://open.fda.gov/apis/
- **Registration**: Optional (API key increases rate limit)
- **Rate Limit**: Without key: 40 req/min, 1000/day. With key: 240 req/min.
- **Data**: Drug approvals (since 1939), adverse events, labeling, recalls, device data
- **Endpoint Examples**:
  - Drug approvals: `https://api.fda.gov/drug/drugsfda.json?search=sponsor_name:"Pfizer"&limit=10`
  - Adverse events: `https://api.fda.gov/drug/event.json?search=patient.drug.openfda.brand_name:"Humira"&limit=10`
- **Bulk Downloads**: `https://download.open.fda.gov/drug/drugsfda/drug-drugsfda-0001-of-0001.json.zip`

#### ClinicalTrials.gov
- **URL**: https://clinicaltrials.gov/
- **API**: `https://clinicaltrials.gov/api/v2/studies?query.term=pembrolizumab&pageSize=10`
- **Data**: Clinical trial registrations, status, results
- **Registration**: None
- **Bulk Download**: https://clinicaltrials.gov/AllPublicXML.zip

### 10.3 Telecom (FCC)
- **URL**: https://www.fcc.gov/reports-research/developers
- **Broadband Data API**: https://broadbandmap.fcc.gov/ (public data API spec available)
- **Area/Census API**: `https://geo.fcc.gov/api/census/area?lat=40.7128&lon=-74.0060&format=json`
- **Data Downloads**: https://broadbandmap.fcc.gov/data-download
- **Registration**: None
- **Data**: Broadband availability, provider coverage, spectrum licensing

### 10.4 General Industry Data (Government)
- **Bureau of Transportation Statistics**: https://www.bts.gov/browse-statistical-products-and-data
- **USDA Economic Research Service**: https://www.ers.usda.gov/data-products/
- **HUD Housing Data**: https://www.huduser.gov/portal/datasets/
- **FDIC Bank Data**: https://www.fdic.gov/analysis/quarterly-banking-profile (bank financial data)
- **FFIEC**: https://www.ffiec.gov/nicpubweb/nicweb/nichome.aspx (bank holding company data)

### 10.5 Trade Association / Consulting Reports
- **McKinsey Global Institute**: https://www.mckinsey.com/mgi/overview (free reports)
- **Deloitte Insights**: https://www2.deloitte.com/us/en/insights.html (free industry reports)
- **PwC Research**: https://www.pwc.com/us/en/library.html
- **BCG Publications**: https://www.bcg.com/publications
- **Access Method**: Web scraping or RSS feeds for new publications

---

## 11. NEWS AND SENTIMENT

### 11.1 Finnhub News API
- **Endpoint**: `GET https://finnhub.io/api/v1/company-news?symbol=AAPL&from=2024-01-01&to=2024-03-01&token={KEY}`
- **Market News**: `GET https://finnhub.io/api/v1/news?category=general&token={KEY}`
- **Rate Limit**: 60/minute free
- (See Section 5.4 for full details)

### 11.2 GNews API
- **URL**: https://gnews.io/
- **Registration**: Yes (free tier)
- **Rate Limit**: 100 requests/day free
- **Data**: News articles from 60,000+ sources
- **Endpoint**: `https://gnews.io/api/v4/search?q=Apple+earnings&token={KEY}`

### 11.3 NewsAPI.org
- **URL**: https://newsapi.org/
- **Registration**: Yes (free for development)
- **Rate Limit**: 100 requests/day, 1 month historical
- **Restriction**: Free tier for development only; production requires paid plan
- **Endpoint**: `https://newsapi.org/v2/everything?q=AAPL+earnings&apiKey={KEY}`

### 11.4 Press Release Databases
- **PR Newswire**: https://www.prnewswire.com/ (searchable; limited API access)
- **BusinessWire**: https://www.businesswire.com/ (searchable)
- **GlobeNewswire**: https://www.globenewswire.com/ (searchable, RSS feeds available)
- **Access Method**: RSS feeds are the most reliable free method
  - GlobeNewswire RSS: `https://www.globenewswire.com/RssFeed/orgclass/1/feedTitle/GlobeNewswire`
- **FMP Press Releases**: `https://financialmodelingprep.com/api/v3/press-releases/AAPL?apikey={KEY}`

### 11.5 SEC RSS Feeds
- **Latest Filings RSS**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={CIK}&type=&dateb=&owner=include&count=40&search_text=&action=getcompany&output=atom`
- **All Latest Filings**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=&company=&dateb=&owner=include&count=40&search_text=&start=0&output=atom`

---

## 12. INSIDER TRADING

### 12.1 SEC Insider Transactions Data Sets (Official)
- **URL**: https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets
- **Data**: Structured data from Forms 3, 4, and 5 (non-derivative and derivative transactions, ownership)
- **Format**: Tab-delimited files (quarterly), JSONL bulk downloads
- **Access Method**: Direct download
- **Registration**: None
- **File Pattern**: `https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{YYYY}q{Q}_form345.zip`

### 12.2 OpenInsider
- **URL**: http://openinsider.com/
- **Data**: SEC Form 4 insider purchases and sales, filterable by date, insider type, transaction size
- **Access Method**: Web scraping (no official API)
- **Registration**: None
- **URL Patterns**:
  - Latest buys: `http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=7&fdr=&td=0&tdr=&feession=&cession=&sidTicker=&sicAndOr=AND&sicCode=&ntession=4&ntlk=&ntfr=&nession=1&nilk=&nifr=&nession=&nession=&xession=1`
  - By ticker: `http://openinsider.com/search?q={TICKER}`
- **Scraping Tool**: https://github.com/soemyatmyat/open-insider-trades

### 12.3 SecForm4.com
- **URL**: https://www.secform4.com/
- **Data**: Parsed Form 4 filings with analytics
- **Access Method**: Web interface (limited free access)

### 12.4 Finnhub Insider Transactions
- **Endpoint**: `GET https://finnhub.io/api/v1/stock/insider-transactions?symbol=AAPL&token={KEY}`
- **Rate Limit**: 60/minute free tier

### 12.5 FMP Insider Trading
- **Endpoint**: `https://financialmodelingprep.com/api/v4/insider-trading?symbol=AAPL&apikey={KEY}`

---

## 13. INSTITUTIONAL HOLDINGS

### 13.1 SEC 13F Data Sets (Official)
- **URL**: https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets
- **Data**: Quarterly institutional holdings from XML-based 13F-HR filings, flattened format
- **Access Method**: Direct download (quarterly ZIP files)
- **Registration**: None
- **Format**: Tab-delimited files

### 13.2 SEC EDGAR 13F Filing Access
- **Search**: `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=13F-HR&dateb=&owner=include&count=40`
- **Access Method**: Parse individual 13F-HR filings from EDGAR
- **Python**: EdgarTools provides structured 13F parsing

### 13.3 WhaleWisdom
- **URL**: https://whalewisdom.com/
- **Data**: Parsed 13F data with analytics, stock allocation, position changes
- **Free Tier**: Last 9 quarters (approximately 2 years) accessible free; earlier data requires paid access
- **Registration**: Free account for basic access
- **Access Method**: Web interface (no public API; third-party scrapers exist on Apify)
- **Historical Coverage**: Data back to Q1 2001

### 13.4 FMP 13F Holdings
- **Endpoint**: `https://financialmodelingprep.com/api/v3/form-thirteen/AAPL?apikey={KEY}`
- **Data**: 13F holders for a given stock
- **Free Tier**: 250 requests/day

### 13.5 Finnhub Institutional Holdings
- **Endpoint**: `GET https://finnhub.io/api/v1/institutional-ownership?symbol=AAPL&token={KEY}`

### 13.6 forms13f.com API
- **URL**: https://forms13f.github.io/api-docs/
- **Data**: 13F filings by CIK with date range filtering and pagination
- **Access Method**: REST API

---

## SUMMARY: RECOMMENDED PRIORITY STACK

For building an automated equity research data retrieval system, prioritize these sources for the best coverage-to-complexity ratio:

| Priority | Source | Why |
|----------|--------|-----|
| 1 | **SEC EDGAR APIs** (data.sec.gov) | Foundation for all US equity data -- filings, financials, ownership, insider trades |
| 2 | **FRED API** | Comprehensive macro/economic data in one place |
| 3 | **Finnhub** | Best free tier (60/min) covering prices, news, fundamentals, ESG, insider trades |
| 4 | **yfinance** | Easiest real-time price data + options + financials (no key needed) |
| 5 | **FMP** | Good fill for transcripts, press releases, 13F data |
| 6 | **Motley Fool scraping** | Best free earnings transcript source |
| 7 | **FINRA** | Short interest + daily short volume |
| 8 | **OpenInsider** | Quick insider trading screening |
| 9 | **EIA/openFDA** | Sector-specific data for energy/pharma |
| 10 | **Google Trends + Arctic Shift** | Alternative/sentiment data |

### Key Python Packages
```
pip install edgartools yfinance fredapi pytrends finnhub-python requests pandas
```

### Rate Limit Summary

| Source | Free Rate Limit | Key Required |
|--------|----------------|-------------|
| SEC EDGAR | 10 req/sec | No |
| FRED | 120 req/min | Yes |
| Finnhub | 60 req/min | Yes |
| Alpha Vantage | 5 req/min, 25/day | Yes |
| FMP | 250 req/day | Yes |
| Polygon.io | 5 req/min | Yes |
| yfinance | Undocumented (throttled) | No |
| BLS v2 | 500 queries/day | Yes |
| BEA | Not published | Yes |
| EIA | Not published | Yes |
| openFDA (no key) | 40 req/min | No |
| openFDA (with key) | 240 req/min | Yes |
| World Bank | Unlimited | No |
| Census | Standard limits | Yes |
| FINRA | Standard limits | Varies |
