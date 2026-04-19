# `--as-of` Contract

All data-retrieval tools in `tools/` implement a uniform `--as-of YYYY-MM-DD` contract.
Its purpose is to make historical (retroactive) research runs **lookahead-leak-proof** — when the
system is evaluated on a past decision date, it sees only information that was publicly available
on or before that date.

This is the load-bearing engineering for Track 1 of the outcome-evidence strategy. Without
this layer, no retroactive backtest is credible.

## Flag and precedence

| Source | Precedence | Notes |
|---|---|---|
| `--as-of YYYY-MM-DD` CLI flag | 1 (highest) | Per-invocation override |
| `EQUITY_SWARM_AS_OF` env var | 2 | Set once per backtest run; inherited by all tools |
| Unset / `today` / future date | 3 | "Live mode" — tools behave as if no flag was passed |

Today's date is the boundary. If the resolved as-of date is today or in the future, tools
operate in **live mode** and return current data. If it is in the past, tools operate in
**historical mode**.

## Historical-mode semantics

Every tool falls into exactly one of three categories for each of its commands:

### Category A — Natively filterable

The underlying data source exposes dates on each record (e.g., SEC filing date, FRED
observation date, price bar date). The tool filters records to those with
`record_date <= as-of`. No error is raised when as-of is in the past.

**Examples:**
- SEC filings (`filingDate` field)
- SEC Form 4 insider trades (`filing_date` field)
- XBRL financial facts (`filed` field)
- FRED economic series (observation date; also use `realtime_end` for vintage data)
- Yahoo price history (bar dates; set `period2` epoch to as-of)
- Finnhub transcript list (date field)

### Category B — Vintage-capable

The underlying data source exposes both an **observation date** and a **publication / revision
date**. These tools use the revision date to retrieve the version of the data that was
available on the as-of date — not the latest revised version.

**Examples:**
- FRED real-time series (`realtime_start`, `realtime_end` params — returns the values as they
  were reported on `realtime_end`, including subsequent revisions only if they were published
  by that date)
- XBRL filed values (filter on `filed <= as-of`, not just `end <= as-of`, to capture only the
  values that had been reported by the as-of date)

Vintage mode is the strongest lookahead control and should be preferred over plain date
filtering whenever the source supports it.

### Category C — Current-only

The underlying data source returns only a live snapshot with no historical equivalent:
Yahoo Finance quote / key statistics / options chains / profile / peers; third-party
summary pages (Finviz, WhaleWisdom current ownership, MarketBeat current estimates);
Motley Fool transcript *discovery* (the transcript content itself is dated, but the search
page is current).

When as-of is in the past, these tools **hard-fail** with a clear error and a non-zero
exit code. They do **not** silently return current data, and they do **not** attempt to
"estimate" historical values.

The error message must include:
1. The tool name and command
2. The resolved as-of date
3. A one-line description of why historical retrieval is impossible for this source
4. A suggested alternative (if any) — e.g., "use `financial-data.sh filing TICKER 10-K --as-of`
   to pull the historical 10-K share count instead of current market cap"

## Error format

```
ERROR: market-data.sh quote AAPL --as-of 2023-01-15 is not supported.
  Reason: Yahoo Finance /v7/quote returns only live snapshot data. Historical
          intraday quotes are not available via the free API.
  Alternative: market-data.sh history AAPL 1d --as-of 2023-01-15
              (historical daily bars are filterable)
```

Exit code: `2` for current-only hard-fail (distinct from `1` for other errors).

## Live-mode semantics

When as-of is unset, today, or in the future, tools behave exactly as they did before the
`--as-of` contract existed. No behavior change, no warnings, no extra output.

## Common contract rules (all tools)

1. `--as-of` is a **universal flag**, recognized by every tool even for commands where it
   has no effect (e.g., local-only `extract` commands). This keeps agent invocations
   uniform; tools silently ignore it when it's a no-op.
2. The flag accepts exactly the format `YYYY-MM-DD`. Any other format is a parse error
   with exit code `1`.
3. Dates before `1990-01-01` are rejected (no reliable free data before that window).
4. If both the flag and the env var are set, the flag wins. No warning is emitted.
5. When in historical mode, every tool logs one line to stderr on startup:
   `[as-of] historical mode: <date>` — so log scraping can confirm the mode was honored.
6. When a tool filters results, the count of records dropped by the filter is logged to
   stderr: `[as-of] filtered N records with date > <as-of>`.

## Shared helpers

Two small helpers implement the contract once so every tool can use them:

- **`tools/_as_of.py`** — Python module. Exports `resolve(cli_value)`, `is_historical()`,
  `assert_live_only(tool, cmd, reason, alternative=None)`, `filter_by_date(records, key)`.
- **`tools/_as_of.sh`** — Bash source-able. Exports `as_of_resolve`, `as_of_is_historical`,
  `as_of_assert_live_only`, `as_of_epoch` (for Yahoo `period2` computation).

Tools that have not yet been retrofitted are listed in their own section of this doc.

## Per-tool behavior map

| Tool | Command | Category | Notes |
|---|---|---|---|
| `financial-data.sh` | `ticker` | Live-or-A | CIK is stable; returns same value regardless of as-of |
| `financial-data.sh` | `submissions` | A | Filter `filingDate <= as-of` |
| `financial-data.sh` | `filing` | A | Return most recent filing with `filingDate <= as-of` |
| `financial-data.sh` | `company` | B | Filter XBRL `filed <= as-of` (vintage) |
| `market-data.sh` | `quote` | C | Hard-fail; suggest `history` |
| `market-data.sh` | `profile` | C | Hard-fail; profiles have no dated equivalent |
| `market-data.sh` | `peers` | C | Hard-fail; Yahoo peer lists are live |
| `market-data.sh` | `stats` | C | Hard-fail; key statistics are live snapshot |
| `market-data.sh` | `summary` | C | Hard-fail (composite of live sources) |
| `market-data.sh` | `history` | A | Set `period2=as-of_epoch`, `period1=as-of-range_epoch` |
| `market-data.sh` | `options` | C | Hard-fail; historical options chains are paid data |
| `edgar-enhanced.py` | `filing` | A | Filter filings by `filingDate <= as-of` |
| `edgar-enhanced.py` | `insider` | A | Filter Form 4 by `filing_date <= as-of` |
| `edgar-enhanced.py` | `institutional` | A | Filter 13Fs by `filing_date <= as-of` |
| `edgar-enhanced.py` | `financials` | B | Filter XBRL annual values by `filed <= as-of` |
| `edgar-enhanced.py` | `search` | A | `date_end = as-of` override |
| `edgar-enhanced.py` | `company` | Live-or-A | Metadata is stable; pass-through |
| `transcript-fetcher.py` | `search` | A (guidance) | Add as-of to the search-guidance JSON; agent must filter |
| `transcript-fetcher.py` | `finnhub` | A | Filter transcript list by dated fields before fetching content |
| `transcript-fetcher.py` | `ir` | Live-or-A | Guidance-only; pass-through |
| `transcript-fetcher.py` | `extract` | N/A | Local file op; pass-through |
| `macro-data.py` | `fred` | B | `observation_end=as-of`, `realtime_end=as-of` (vintage) |
| `macro-data.py` | `rates` | B | Same as `fred` |
| `macro-data.py` | `macro-snapshot` | B | Same as `fred`, across curated series |
| `macro-data.py` | `industry` | Live-or-A | Guidance-only; pass-through |
| `macro-data.py` | `list-series` | N/A | Local dict |
| `alt-data.py` | `insider` | Mixed | Finnhub: A. All other sources: C (hard-fail unless using `edgar-enhanced.py insider`) |
| `alt-data.py` | `institutional` | C | Yahoo/WhaleWisdom/Finviz are live-only; suggest `edgar-enhanced.py institutional` |
| `alt-data.py` | `short-interest` | C | All free sources are live-only; FINRA historical requires paid API |
| `alt-data.py` | `ownership-summary` | C | Composite of live-only sources |
| `alt-data.py` | `analyst-estimates` | C | Consensus is by definition "as of now" on free sources |
| `alt-data.py` | `peers` | Live-or-A | Peer lists change slowly; pass-through with a warning |

## Test harness

`tests/test_as_of.py` runs every tool against the as-of date `2023-01-01` and asserts:

1. **No record with date > 2023-01-01 appears in the response** (Category A/B).
2. **Current-only commands exit non-zero with the documented error** (Category C).
3. **Live mode with no flag produces identical output to the prior, pre-contract version**
   (captured once and committed as a golden).

Any tool change that breaks either (1) or (2) is treated as a critical regression.
