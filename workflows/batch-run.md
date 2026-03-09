# Workflow: Batch Run

## Trigger
Running research on multiple stocks — by tag, sector, staleness, or the full universe.

## Prerequisites
- Stock database populated at `data/stocks.json`
- `tools/batch-runner.py` available

## Execution Steps

### Step 1: Check Database Freshness

Before any batch run, check if the database itself needs updating:

```bash
python tools/batch-runner.py update-db
```

This scans `output/` for existing research notes and updates `last_researched` dates.

### Step 2: Identify Stocks to Run

Use one of these filter strategies:

**By tag:**
```bash
python tools/batch-runner.py plan --tag mag7
python tools/batch-runner.py plan --tag ai --tag semiconductors
```

**By sector:**
```bash
python tools/batch-runner.py plan --sector Healthcare
python tools/batch-runner.py plan --sector Technology
```

**Stale stocks only (not researched in 7+ days):**
```bash
python tools/batch-runner.py plan --stale
python tools/batch-runner.py plan --stale --days 14
```

**All stocks:**
```bash
python tools/batch-runner.py plan --all
```

### Step 3: Execute Sequentially

For each stock in the plan, run the full-research-note workflow sequentially:

```
For each TICKER in [batch plan]:
  1. Run the full-research-note workflow for TICKER (see workflows/full-research-note.md)
  2. After completion, mark the stock as researched:
     python tools/batch-runner.py mark-complete TICKER
  3. Check output/notes/ for cross-stock notes generated during this analysis
  4. If a cross-stock note targets a stock ALREADY completed in this batch:
     - Assess materiality per workflows/cross-stock-trigger.md
     - If High priority: queue a Cross-Stock Review for that stock after the batch completes
     - If Medium/Low: add footnote to existing note
  5. Proceed to next stock
```

### Step 4: Post-Batch Processing

After all stocks in the batch are complete:

1. **Process cross-stock reviews:**
   - Run any queued Cross-Stock Reviews (per `workflows/cross-stock-trigger.md`)
   - These are lightweight — only 3 analysts per review

2. **Check for portfolio construction:**
   - If 5+ stocks completed, consider running the portfolio-construction workflow
   - `python tools/batch-runner.py list --tag [batch-tag]` to verify coverage

3. **Update status:**
   ```bash
   python tools/batch-runner.py status
   ```

4. **Generate batch summary:**
   - List of all stocks researched with ratings and price targets
   - Cross-stock notes generated
   - Any stocks requiring follow-up

## Batch Execution Order

When running a large batch, order matters for cross-stock intelligence:

1. **Start with the largest/most important stocks** — they generate the most cross-stock notes
2. **Run competitors together** — e.g., AAPL + MSFT + GOOGL, not AAPL + JPM + XOM
3. **Process cross-stock notes between related stocks** before moving to the next cluster

### Recommended Batch Clusters

| Cluster | Stocks | Rationale |
|---------|--------|-----------|
| Mag 7 Tech | AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA | Heavy cross-stock intelligence |
| Semiconductors | NVDA, AMD, AVGO | Direct competitors |
| Cloud | MSFT, AMZN, GOOGL, CRM | Overlapping markets |
| Financials | JPM, V, MA | Related but distinct |
| Healthcare | UNH, JNJ, LLY | Sector peers |
| Consumer | PG, KO, COST, WMT, HD | Consumer spending exposure |
| Media | NFLX, DIS | Direct streaming competitors |
| Energy | XOM, CVX | Sector peers |

## Staleness Management

The database tracks when each stock was last researched. The default staleness threshold is **7 days**.

### Automatic Staleness Check

At the start of any batch run, the Director should:
1. Run `python tools/batch-runner.py stale` to see what needs refreshing
2. Prioritize stale stocks over fresh ones
3. Never skip a stock just because it was recently researched if it's in the requested batch

### Staleness Triggers

Beyond time-based staleness, stocks should be re-researched when:
- Earnings are released (within 24 hours if possible)
- Material news breaks (M&A, regulatory action, product launch)
- A cross-stock note with High priority targets the stock
- The stock price moves >10% in a day
- An analyst rating change or significant price target revision

## Adding Stocks

To expand the universe:

```bash
# Add a single stock
python tools/batch-runner.py add PLTR "Palantir Technologies" --sector Technology --tags ai,software,government,datacenter

# Add with full details
python tools/batch-runner.py add SNOW "Snowflake Inc." --sector Technology --industry "Software - Infrastructure" --tags cloud,software,ai,datacenter
```

### Tag Convention

Use existing tags from `data/stocks.json` → `tag_definitions` when possible. If a new tag is needed:
1. Add the stock with the new tag
2. Add the tag definition to `tag_definitions` in `data/stocks.json`
3. Apply the tag to any existing stocks that should have it

## Output

Batch run produces:
- Individual research notes for each stock (see `workflows/full-research-note.md` for per-stock output)
- Cross-stock intelligence notes in `output/notes/`
- Updated staleness tracking in `data/stocks.json`
- Optional: portfolio construction if 5+ stocks completed
