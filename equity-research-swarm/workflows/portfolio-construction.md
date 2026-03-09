# Workflow: Portfolio Construction

## Trigger
After running the full-research-note workflow for multiple stocks, construct an optimized portfolio from the individual analyses. Can also be triggered directly with a universe (e.g., "Build a 30-position portfolio from the Russell 3000").

## Input Requirements
- **Multiple completed research notes** in `output/` (minimum 15, ideally 30+)
- OR **Universe specification** (e.g., "Russell 3000", "S&P 500 Technology sector") with instruction to analyze and select
- **Portfolio constraints** (optional — defaults provided):
  - Target number of positions (default: 25-35)
  - Max single position weight (default: 8%)
  - Max sector weight (default: 25%)
  - Target portfolio volatility (default: 15% annualized)
  - Long-only or long-short (default: long-only)
  - Benchmark (default: S&P 500)

## Execution Steps

### Phase 0: Universe Assembly (Director)

**If individual research notes already exist:**
1. Read all completed research notes in `output/`.
2. Extract key inputs for each stock: expected return, conviction, volatility, beta, sector, Kelly fraction, catalyst timeline.
3. Proceed to Phase 1.

**If starting from a universe specification:**
1. Use screening tools to identify candidates from the universe.
2. Apply initial filters (market cap, liquidity, data availability).
3. Run the `full-research-note` workflow for each candidate stock. This can be done in batches to manage workload.
4. Collect all completed notes, then proceed to Phase 1.

### Phase 1: Portfolio Manager Analysis

Spawn the Portfolio Manager:

```
Read all completed research notes in output/. Follow the framework in agents/portfolio-manager.md.

1. Build the correlation matrix across all candidates.
2. Identify correlation clusters.
3. Analyze factor exposures.
4. Run portfolio optimization with the specified constraints.
5. Produce the final portfolio with weights, expected returns, and risk metrics.
6. Generate implementation plan (entry schedule, rebalancing policy).
7. Save portfolio output to output/portfolio/portfolio-construction-[DATE].md.
```

### Phase 2: Model Builder — Portfolio Models

Spawn the Model Builder in parallel with or after the Portfolio Manager:

```
Generate executable Python models for portfolio optimization following agents/model-builder.md.

Produce:
1. output/models/portfolio_optimizer.py — Optimization engine
2. output/portfolio/correlation-matrix.py — Correlation analysis
3. output/portfolio/scenario-model.py — Monte Carlo simulation

All models must be executable with python3 and use the portfolio weights from the Portfolio Manager's output.
```

### Phase 3: Risk Validation

Spawn the Risk Analyst to validate the portfolio:

```
Read the Portfolio Manager's portfolio construction in output/portfolio/. Validate:
1. Portfolio-level VaR and CVaR within risk budget
2. Stress test the portfolio under historical episodes (GFC, COVID, Rate Shock)
3. Verify no hidden correlation clusters were missed
4. Check tail risk — what happens in a correlated drawdown?
5. Save validation report to output/portfolio/risk-validation.md.
```

### Phase 4: Director Review

The Director:
1. Reviews the portfolio construction and risk validation.
2. Approves or modifies the portfolio.
3. Assigns a portfolio-level conviction rating.
4. Writes the portfolio summary.
5. Saves final portfolio to `output/portfolio/portfolio-final-[DATE].md`.

## Output

```
output/portfolio/
├── portfolio-construction-[DATE].md   # Full portfolio with all positions and weights
├── portfolio-final-[DATE].md          # Director-approved final portfolio
├── risk-validation.md                 # Risk Analyst validation
├── optimizer.py                       # Executable optimization model
├── correlation-matrix.py              # Correlation analysis code
└── scenario-model.py                  # Monte Carlo simulation
```

## Portfolio Output Format

```markdown
# Portfolio Construction — [Date]
## [Strategy Name / Universe]

### Portfolio Summary
| Metric | Value |
|--------|-------|
| Number of positions | [X] |
| Expected annual return | [X]% |
| Portfolio volatility | [X]% |
| Sharpe ratio | [X] |
| Max expected drawdown (95%) | [X]% |
| Portfolio beta | [X] |
| Effective independent bets | [X] |

### Positions
[Full table with all positions, weights, expected returns, conviction, sector, beta, risk contribution]

### Sector Allocation
[Sector weight breakdown]

### Factor Exposures
[Intentional and unintentional tilts]

### Implementation Plan
[Entry schedule, rebalancing triggers, monitoring dashboard]

### Risk Report
[Stress test results, tail risk assessment, correlation analysis]
```

## Estimated Agent Calls
- Portfolio Manager: 1 agent
- Model Builder: 1 agent (can run in parallel)
- Risk Analyst: 1 agent (validation)
- Director: final review
- Total: 3-4 agent invocations (plus however many full-research-note runs were needed for the universe)
