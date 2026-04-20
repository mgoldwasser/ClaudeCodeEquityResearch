#!/usr/bin/env python3
"""
Portfolio Mathematics Calculator
================================
Executable Python tool for position sizing, portfolio optimization,
and probability-weighted expected value calculations.

Usage:
    python tools/portfolio-math.py kelly --win-prob 0.65 --win-return 0.30 --loss-return 0.15
    python tools/portfolio-math.py kelly-scenarios --bull-price 150 --base-price 120 --bear-price 80 \
        --bull-prob 0.25 --base-prob 0.50 --bear-prob 0.25 --current-price 100
    python tools/portfolio-math.py vol-size --stock-vol 0.35 --portfolio-vol 0.12 --num-positions 25
    python tools/portfolio-math.py liquidity --adv 50 --participation 0.15 --max-days 5 --portfolio-size 500
    python tools/portfolio-math.py expected-value --scenarios-file scenarios.json
    python tools/portfolio-math.py optimize --returns-file returns.json --cov-file cov.json --method max-sharpe
    python tools/portfolio-math.py risk-parity --cov-file cov.json
    python tools/portfolio-math.py correlation --tickers AAPL,MSFT,GOOGL --period 3y
    python tools/portfolio-math.py monte-carlo --portfolio-file portfolio.json --simulations 10000
    python tools/portfolio-math.py beneish --financials-file financials.json
    python tools/portfolio-math.py altman-z --financials-file financials.json
"""

import argparse
import json
import sys
import math
from typing import Dict, List, Tuple, Optional


# ============================================================
# KELLY CRITERION
# ============================================================

def kelly_criterion(win_prob: float, win_return: float, loss_return: float) -> Dict:
    """
    Classic Kelly criterion: f* = (p*b - q) / b
    where p = win probability, q = loss probability, b = win/loss ratio
    """
    q = 1.0 - win_prob
    if loss_return <= 0:
        return {"error": "loss_return must be positive (absolute value of loss)"}

    b = win_return / loss_return  # win/loss ratio
    full_kelly = (win_prob * b - q) / b
    expected_value = win_prob * win_return - q * loss_return
    edge = win_prob * (1 + win_return) + q * (1 - loss_return) - 1

    result = {
        "inputs": {
            "win_probability": win_prob,
            "loss_probability": q,
            "win_return": win_return,
            "loss_return": loss_return,
            "win_loss_ratio": round(b, 3),
        },
        "kelly_fractions": {
            "full_kelly": round(full_kelly, 4),
            "half_kelly": round(full_kelly / 2, 4),
            "quarter_kelly": round(full_kelly / 4, 4),
        },
        "expected_value_per_unit": round(expected_value, 4),
        "edge": round(edge, 4),
        "recommendation": "",
    }

    if full_kelly < 0:
        result["recommendation"] = (
            "NEGATIVE EXPECTED VALUE — do not take this position. "
            f"Kelly = {full_kelly:.2%}. The bet loses money on average."
        )
    elif full_kelly > 0.25:
        result["recommendation"] = (
            f"WARNING: Full Kelly = {full_kelly:.2%} — extremely concentrated. "
            f"Use half Kelly ({full_kelly/2:.2%}) or quarter Kelly ({full_kelly/4:.2%}) "
            "for institutional portfolios."
        )
    else:
        result["recommendation"] = (
            f"Full Kelly = {full_kelly:.2%}. "
            f"Recommended: half Kelly = {full_kelly/2:.2%} (standard institutional practice)."
        )

    return result


def kelly_from_scenarios(
    bull_price: float, base_price: float, bear_price: float,
    bull_prob: float, base_prob: float, bear_prob: float,
    current_price: float
) -> Dict:
    """
    Calculate Kelly from bull/base/bear scenarios with probabilities.
    """
    # Validate probabilities
    total_prob = bull_prob + base_prob + bear_prob
    if abs(total_prob - 1.0) > 0.01:
        return {"error": f"Probabilities must sum to 1.0, got {total_prob:.3f}"}

    # Calculate returns
    bull_return = (bull_price - current_price) / current_price
    base_return = (base_price - current_price) / current_price
    bear_return = (bear_price - current_price) / current_price

    # Expected value price target
    ev_price = bull_price * bull_prob + base_price * base_prob + bear_price * bear_prob
    ev_return = (ev_price - current_price) / current_price

    # For Kelly: win = scenarios where we make money, lose = scenarios where we lose
    # Weighted average win and weighted average loss
    wins = []
    losses = []

    for ret, prob in [(bull_return, bull_prob), (base_return, base_prob), (bear_return, bear_prob)]:
        if ret >= 0:
            wins.append((ret, prob))
        else:
            losses.append((abs(ret), prob))

    if not losses:
        return {
            "scenarios": {
                "bull": {"price": bull_price, "return": f"{bull_return:.2%}", "probability": bull_prob},
                "base": {"price": base_price, "return": f"{base_return:.2%}", "probability": base_prob},
                "bear": {"price": bear_price, "return": f"{bear_return:.2%}", "probability": bear_prob},
            },
            "expected_value_price": round(ev_price, 2),
            "expected_return": f"{ev_return:.2%}",
            "kelly": "N/A — no loss scenarios, Kelly is undefined (infinite)",
            "recommendation": "All scenarios are profitable. Size based on volatility and liquidity constraints."
        }

    if not wins:
        return {
            "scenarios": {
                "bull": {"price": bull_price, "return": f"{bull_return:.2%}", "probability": bull_prob},
                "base": {"price": base_price, "return": f"{base_return:.2%}", "probability": base_prob},
                "bear": {"price": bear_price, "return": f"{bear_return:.2%}", "probability": bear_prob},
            },
            "expected_value_price": round(ev_price, 2),
            "expected_return": f"{ev_return:.2%}",
            "kelly_fractions": {"full_kelly": 0, "half_kelly": 0, "quarter_kelly": 0},
            "recommendation": "NEGATIVE EXPECTED VALUE — all scenarios show losses. Do not take position."
        }

    total_win_prob = sum(p for _, p in wins)
    total_loss_prob = sum(p for _, p in losses)
    avg_win = sum(r * p for r, p in wins) / total_win_prob if total_win_prob > 0 else 0
    avg_loss = sum(r * p for r, p in losses) / total_loss_prob if total_loss_prob > 0 else 0

    kelly_result = kelly_criterion(total_win_prob, avg_win, avg_loss)

    # Upside/downside ratio
    upside = bull_price - current_price
    downside = current_price - bear_price
    upside_downside_ratio = upside / downside if downside > 0 else float('inf')

    # Break-even bear probability (what bear prob makes EV = current price)
    # EV = bull*pb + base*pbase + bear*pbear = current
    # If we increase bear prob by delta, decrease others proportionally:
    # This is complex, so compute the break-even probability for the bear case
    if bull_price != bear_price:
        # Simple: at what bear_prob does EV = current_price, holding bull/base ratio constant
        ratio = bull_prob / base_prob if base_prob > 0 else 1
        # EV = bull_price * ratio * x + base_price * x + bear_price * (1 - (1+ratio)*x) = current_price
        # Solve for x (base_prob in new scenario)
        denom = bull_price * ratio + base_price - bear_price * (1 + ratio)
        if abs(denom) > 0.001:
            x = (current_price - bear_price) / denom
            breakeven_bear = 1 - (1 + ratio) * x
        else:
            breakeven_bear = None
    else:
        breakeven_bear = None

    # Probability of loss
    prob_of_loss = sum(p for r, p in [(bear_return, bear_prob), (base_return, base_prob), (bull_return, bull_prob)] if r < 0)

    # Distribution skew (simple measure)
    if abs(upside) > abs(downside) * 1.2:
        skew = "Right-skewed (favorable — more upside than downside)"
    elif abs(downside) > abs(upside) * 1.2:
        skew = "Left-skewed (unfavorable — more downside than upside)"
    else:
        skew = "Approximately symmetric"

    return {
        "scenarios": {
            "bull": {"price": bull_price, "return": f"{bull_return:.2%}", "probability": f"{bull_prob:.0%}"},
            "base": {"price": base_price, "return": f"{base_return:.2%}", "probability": f"{base_prob:.0%}"},
            "bear": {"price": bear_price, "return": f"{bear_return:.2%}", "probability": f"{bear_prob:.0%}"},
        },
        "expected_value": {
            "price": round(ev_price, 2),
            "return": f"{ev_return:.2%}",
            "calculation": f"({bull_price} × {bull_prob:.0%}) + ({base_price} × {base_prob:.0%}) + ({bear_price} × {bear_prob:.0%}) = ${ev_price:.2f}"
        },
        "kelly_fractions": kelly_result.get("kelly_fractions", {}),
        "distribution": {
            "skew": skew,
            "upside_downside_ratio": f"{upside_downside_ratio:.2f}x",
            "probability_of_loss": f"{prob_of_loss:.0%}",
            "breakeven_bear_probability": f"{breakeven_bear:.0%}" if breakeven_bear is not None else "N/A",
        },
        "recommendation": kelly_result.get("recommendation", ""),
    }


# ============================================================
# VOLATILITY-ADJUSTED SIZING
# ============================================================

def vol_adjusted_size(stock_vol: float, portfolio_vol: float, num_positions: int,
                      avg_correlation: float = 0.3) -> Dict:
    """
    Equal-volatility position sizing.
    Per-position vol budget = portfolio_vol / sqrt(N * (1 + (N-1)*avg_corr))
    Weight = per_position_vol_budget / stock_vol
    """
    # Diversification factor
    portfolio_var_factor = num_positions * (1 + (num_positions - 1) * avg_correlation)
    per_position_vol_budget = portfolio_vol / math.sqrt(portfolio_var_factor)
    weight = per_position_vol_budget / stock_vol

    return {
        "inputs": {
            "stock_volatility": f"{stock_vol:.1%}",
            "portfolio_target_volatility": f"{portfolio_vol:.1%}",
            "num_positions": num_positions,
            "avg_pairwise_correlation": avg_correlation,
        },
        "calculation": {
            "diversification_factor": round(portfolio_var_factor, 2),
            "per_position_vol_budget": f"{per_position_vol_budget:.2%}",
            "vol_adjusted_weight": f"{weight:.2%}",
        },
        "weight": round(weight, 4),
    }


# ============================================================
# LIQUIDITY CONSTRAINT
# ============================================================

def liquidity_max_position(adv_millions: float, participation_rate: float,
                           max_days: int, portfolio_size_millions: float) -> Dict:
    """
    Maximum position size based on liquidity constraints.
    Max position ($) = ADV × participation_rate × max_days
    Max position (%) = Max position ($) / portfolio_size
    """
    max_daily_liquidation = adv_millions * participation_rate
    max_position_dollars = max_daily_liquidation * max_days
    max_position_pct = max_position_dollars / portfolio_size_millions

    return {
        "inputs": {
            "avg_daily_volume_millions": adv_millions,
            "participation_rate": f"{participation_rate:.0%}",
            "max_liquidation_days": max_days,
            "portfolio_size_millions": portfolio_size_millions,
        },
        "calculation": {
            "max_daily_liquidation_millions": round(max_daily_liquidation, 2),
            "max_position_millions": round(max_position_dollars, 2),
            "max_position_pct": f"{max_position_pct:.2%}",
        },
        "max_weight": round(max_position_pct, 4),
    }


# ============================================================
# EXPECTED VALUE FROM SCENARIOS
# ============================================================

def expected_value_from_scenarios(scenarios: List[Dict]) -> Dict:
    """
    Calculate probability-weighted expected value from a list of scenarios.
    Each scenario: {"name": str, "price": float, "probability": float, "description": str}
    """
    total_prob = sum(s["probability"] for s in scenarios)
    if abs(total_prob - 1.0) > 0.01:
        return {"error": f"Probabilities must sum to 1.0, got {total_prob:.3f}"}

    ev_price = sum(s["price"] * s["probability"] for s in scenarios)

    # Weighted standard deviation
    variance = sum(s["probability"] * (s["price"] - ev_price) ** 2 for s in scenarios)
    std_dev = math.sqrt(variance)

    # Build calculation string
    calc_parts = [f"(${s['price']:.2f} × {s['probability']:.0%})" for s in scenarios]
    calc_str = " + ".join(calc_parts) + f" = ${ev_price:.2f}"

    # Contribution breakdown
    contributions = []
    for s in scenarios:
        contributions.append({
            "scenario": s.get("name", "Unknown"),
            "price": s["price"],
            "probability": f"{s['probability']:.0%}",
            "contribution": round(s["price"] * s["probability"], 2),
            "description": s.get("description", ""),
        })

    return {
        "expected_value_price": round(ev_price, 2),
        "standard_deviation": round(std_dev, 2),
        "coefficient_of_variation": f"{std_dev / ev_price:.2%}" if ev_price > 0 else "N/A",
        "calculation": calc_str,
        "scenario_contributions": contributions,
    }


# ============================================================
# PORTFOLIO OPTIMIZATION (Mean-Variance)
# ============================================================

def mean_variance_optimize(expected_returns: List[float], cov_matrix: List[List[float]],
                           method: str = "max-sharpe", risk_free_rate: float = 0.05,
                           constraints: Optional[Dict] = None) -> Dict:
    """
    Mean-variance portfolio optimization using scipy.
    Methods: max-sharpe, min-variance, risk-parity, equal-weight
    """
    try:
        import numpy as np
    except ImportError:
        return {"error": "numpy required. Install: pip install numpy"}

    constraints = constraints or {}
    n = len(expected_returns)
    returns = np.array(expected_returns)
    cov = np.array(cov_matrix)

    def _require_scipy():
        try:
            from scipy.optimize import minimize
            return minimize
        except ImportError:
            return None

    if method == "equal-weight":
        weights = np.ones(n) / n
    elif method == "risk-parity":
        weights = _risk_parity_weights(cov)
    elif method == "min-variance":
        minimize = _require_scipy()
        if minimize is None:
            return {"error": "scipy required for min-variance. Install: pip install scipy"}

        def portfolio_variance(w):
            return w @ cov @ w

        cons = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]
        bounds = [(constraints.get("min_weight", 0.0), constraints.get("max_weight", 1.0)) for _ in range(n)]
        x0 = np.ones(n) / n
        result = minimize(portfolio_variance, x0, method="SLSQP", bounds=bounds, constraints=cons)
        weights = result.x
    elif method == "max-sharpe":
        minimize = _require_scipy()
        if minimize is None:
            # Numpy-only analytical max-Sharpe (no-short, no-cap).
            # w* proportional to Sigma^-1 (mu - rf), then clip to >=0 and
            # renormalize. Caller must apply its own cap/renormalization
            # afterward if bounds are required.
            try:
                cov_inv = np.linalg.inv(cov)
            except np.linalg.LinAlgError:
                return {"error": "covariance matrix not invertible"}
            excess = returns - risk_free_rate
            raw = cov_inv @ excess
            raw = np.maximum(raw, 0.0)
            s = raw.sum()
            if s <= 0:
                weights = np.ones(n) / n
            else:
                weights = raw / s
        else:
            def neg_sharpe(w):
                port_return = w @ returns
                port_vol = np.sqrt(w @ cov @ w)
                if port_vol < 1e-10:
                    return 1e10
                return -(port_return - risk_free_rate) / port_vol

            cons = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]
            bounds = [(constraints.get("min_weight", 0.0), constraints.get("max_weight", 1.0)) for _ in range(n)]
            x0 = np.ones(n) / n
            result = minimize(neg_sharpe, x0, method="SLSQP", bounds=bounds, constraints=cons)
            weights = result.x
    else:
        return {"error": f"Unknown method: {method}. Use max-sharpe, min-variance, risk-parity, equal-weight."}

    # Portfolio metrics
    port_return = float(weights @ returns)
    port_vol = float(np.sqrt(weights @ cov @ weights))
    sharpe = (port_return - risk_free_rate) / port_vol if port_vol > 0 else 0

    # Marginal contribution to risk
    mcr = (cov @ weights) / port_vol if port_vol > 0 else np.zeros(n)
    risk_contributions = weights * mcr

    positions = []
    for i in range(n):
        positions.append({
            "index": i,
            "weight": f"{weights[i]:.2%}",
            "expected_return": f"{returns[i]:.2%}",
            "risk_contribution": f"{risk_contributions[i]:.2%}",
        })

    return {
        "method": method,
        "portfolio_metrics": {
            "expected_return": f"{port_return:.2%}",
            "volatility": f"{port_vol:.2%}",
            "sharpe_ratio": round(sharpe, 3),
            "risk_free_rate": f"{risk_free_rate:.2%}",
        },
        "positions": positions,
        "weights": [round(float(w), 4) for w in weights],
    }


def _risk_parity_weights(cov_matrix) -> 'np.ndarray':
    """Equal risk contribution portfolio weights.

    Uses scipy SLSQP when available; falls back to a numpy-only fixed-point
    iteration (scale by sqrt(target_rc / rc), renormalize) when scipy is
    not installed. The fixed-point scheme converges monotonically for
    positive-definite covariance matrices in practice.
    """
    import numpy as np

    n = cov_matrix.shape[0]

    try:
        from scipy.optimize import minimize

        def risk_parity_objective(w):
            port_vol = np.sqrt(w @ cov_matrix @ w)
            if port_vol < 1e-10:
                return 1e10
            mcr = (cov_matrix @ w) / port_vol
            rc = w * mcr
            target_rc = port_vol / n
            return np.sum((rc - target_rc) ** 2)

        cons = [{"type": "eq", "fun": lambda w: np.sum(w) - 1.0}]
        bounds = [(0.01, 1.0) for _ in range(n)]
        x0 = np.ones(n) / n
        result = minimize(risk_parity_objective, x0, method="SLSQP",
                          bounds=bounds, constraints=cons)
        return result.x
    except ImportError:
        # Numpy-only fixed-point iteration.
        w = np.ones(n) / n
        for _ in range(500):
            port_vol = np.sqrt(w @ cov_matrix @ w)
            if port_vol < 1e-10:
                break
            mcr = (cov_matrix @ w) / port_vol
            rc = w * mcr
            target_rc = port_vol / n
            # Avoid zero or negative rc by clipping below.
            rc_safe = np.maximum(rc, 1e-12)
            scale = np.sqrt(target_rc / rc_safe)
            w_new = w * scale
            s = w_new.sum()
            if s <= 0:
                break
            w_new = w_new / s
            if np.max(np.abs(w_new - w)) < 1e-9:
                w = w_new
                break
            w = w_new
        return w


def black_litterman(prior_returns: List[float],
                    cov_matrix: List[List[float]],
                    views: List[Dict],
                    tau: float = 0.05) -> Dict:
    """Black-Litterman posterior expected returns.

    Inputs
    ------
    prior_returns : equilibrium returns pi (length N). For a CAPM prior,
                    pi_i = beta_i * (market_return - rf) + rf.
    cov_matrix    : asset return covariance Sigma (N x N). Annualized.
    views         : list of view dicts; each:
                    {
                      "assets": [ticker, ...],              # which assets
                      "weights": [float, ...],              # pick weights (same len as assets);
                                                            # for an absolute view on one asset, [1.0]
                      "expected_return": float,             # Q_i
                      "confidence": float,                  # 0..1, higher = more certain
                    }
                    All tickers in `views` must also appear in `tickers` passed in.
    tau           : scalar (0.025-0.05 typical) reflecting uncertainty in prior.

    Returns
    -------
    {
      "prior_returns": [...],
      "posterior_returns": [...],
      "posterior_cov": [[...]],
      "view_impact": [{"asset_index": i, "prior": x, "posterior": y, "delta": y-x}, ...]
    }

    This implementation uses the closed-form Black-Litterman posterior:
      M^-1 = (tau*Sigma)^-1 + P' * Omega^-1 * P
      E[R]_post = M * ((tau*Sigma)^-1 * pi + P' * Omega^-1 * Q)
    where Omega is diag(P * (tau*Sigma) * P') / confidence_i (Idzorek-style
    calibration: confidence=1 reproduces the view exactly; confidence=0 falls
    back to the prior).
    """
    import numpy as np

    pi = np.array(prior_returns, dtype=float)
    sigma = np.array(cov_matrix, dtype=float)
    n = len(pi)
    if sigma.shape != (n, n):
        return {"error": f"cov_matrix shape {sigma.shape} != ({n},{n})"}
    if not views:
        return {
            "prior_returns": list(pi),
            "posterior_returns": list(pi),
            "posterior_cov": [list(row) for row in sigma.tolist()],
            "view_impact": [],
            "note": "no views provided; posterior == prior",
        }

    # Build P (K x N), Q (K), Omega (K x K)
    tickers_by_idx = {i: i for i in range(n)}  # caller must pre-index views
    K = len(views)
    P = np.zeros((K, n))
    Q = np.zeros(K)
    confidences = np.zeros(K)
    for k, v in enumerate(views):
        idxs = v.get("asset_indices")
        weights = v.get("weights")
        if idxs is None or weights is None:
            return {"error": f"view {k} missing asset_indices or weights"}
        if len(idxs) != len(weights):
            return {"error": f"view {k}: asset_indices and weights length mismatch"}
        for idx, w in zip(idxs, weights):
            if not 0 <= idx < n:
                return {"error": f"view {k}: asset_index {idx} out of range"}
            P[k, idx] += float(w)
        Q[k] = float(v["expected_return"])
        c = float(v.get("confidence", 0.5))
        confidences[k] = max(min(c, 0.9999), 0.0001)

    # Omega diagonal: Idzorek-style: variance of view = diag(P*(tau*Sigma)*P')
    # scaled by (1/confidence - 1). confidence=1 -> Omega->0 (view dominates),
    # confidence=0 -> Omega->infinity (prior dominates).
    view_variance_uncalibrated = np.array(
        [float(P[k] @ (tau * sigma) @ P[k]) for k in range(K)]
    )
    omega_diag = view_variance_uncalibrated * (1.0 / confidences - 1.0)
    omega_diag = np.maximum(omega_diag, 1e-10)
    omega = np.diag(omega_diag)

    tau_sigma = tau * sigma
    try:
        tau_sigma_inv = np.linalg.inv(tau_sigma)
        omega_inv = np.linalg.inv(omega)
    except np.linalg.LinAlgError as e:
        return {"error": f"matrix inversion failed: {e}"}

    M_inv = tau_sigma_inv + P.T @ omega_inv @ P
    try:
        M = np.linalg.inv(M_inv)
    except np.linalg.LinAlgError as e:
        return {"error": f"posterior inversion failed: {e}"}

    posterior = M @ (tau_sigma_inv @ pi + P.T @ omega_inv @ Q)
    posterior_cov = sigma + M  # posterior covariance of returns

    view_impact = [
        {"asset_index": i, "prior": float(pi[i]),
         "posterior": float(posterior[i]),
         "delta": float(posterior[i] - pi[i])}
        for i in range(n)
    ]

    return {
        "prior_returns": [float(x) for x in pi],
        "posterior_returns": [float(x) for x in posterior],
        "posterior_cov": [[float(c) for c in row] for row in posterior_cov],
        "view_impact": view_impact,
        "tau": tau,
    }


# ============================================================
# CORRELATION MATRIX
# ============================================================

def build_correlation_matrix(tickers: List[str], period: str = "3y") -> Dict:
    """
    Build correlation matrix from Yahoo Finance historical data.
    Returns instructions and Python code to generate the matrix.
    """
    # Map period to days
    period_map = {"1y": 252, "2y": 504, "3y": 756, "5y": 1260}
    days = period_map.get(period, 756)

    ticker_str = ",".join(tickers)
    n = len(tickers)

    # Generate the Python code for correlation calculation
    code = f'''#!/usr/bin/env python3
"""Correlation Matrix Calculator for: {ticker_str}"""
import json
import urllib.request
import time

tickers = {json.dumps(tickers)}
period = "{period}"

def fetch_prices(ticker, days={days}):
    """Fetch historical closing prices from Yahoo Finance."""
    end = int(time.time())
    start = end - (days * 86400 * 1.5)  # Extra buffer for weekends
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{{ticker}}?period1={{int(start)}}&period2={{end}}&interval=1d"
    headers = {{"User-Agent": "Mozilla/5.0"}}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    prices = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
    return [p for p in prices if p is not None]

def calculate_returns(prices):
    """Calculate daily log returns."""
    import math
    returns = []
    for i in range(1, len(prices)):
        if prices[i] > 0 and prices[i-1] > 0:
            returns.append(math.log(prices[i] / prices[i-1]))
    return returns

def correlation(x, y):
    """Pearson correlation coefficient."""
    n = min(len(x), len(y))
    x, y = x[:n], y[:n]
    mx = sum(x) / n
    my = sum(y) / n
    cov = sum((x[i]-mx)*(y[i]-my) for i in range(n)) / (n-1)
    sx = (sum((xi-mx)**2 for xi in x) / (n-1)) ** 0.5
    sy = (sum((yi-my)**2 for yi in y) / (n-1)) ** 0.5
    return cov / (sx * sy) if sx > 0 and sy > 0 else 0

# Fetch all prices
print(f"Fetching {{period}} historical prices for {{len(tickers)}} tickers...")
all_returns = {{}}
for t in tickers:
    try:
        prices = fetch_prices(t)
        all_returns[t] = calculate_returns(prices)
        print(f"  {{t}}: {{len(prices)}} prices, {{len(all_returns[t])}} returns")
        time.sleep(0.5)
    except Exception as e:
        print(f"  {{t}}: ERROR - {{e}}")

# Build correlation matrix
print("\\nCorrelation Matrix:")
header = "       " + "  ".join(f"{{t:>7s}}" for t in tickers)
print(header)
matrix = []
for t1 in tickers:
    row = []
    row_str = f"{{t1:>6s}} "
    for t2 in tickers:
        if t1 in all_returns and t2 in all_returns:
            c = correlation(all_returns[t1], all_returns[t2])
        else:
            c = 0
        row.append(round(c, 3))
        row_str += f"  {{c:>6.3f}}"
    matrix.append(row)
    print(row_str)

# Effective independent bets (using simplified eigenvalue approach)
avg_corr = 0
count = 0
for i in range(len(tickers)):
    for j in range(i+1, len(tickers)):
        avg_corr += abs(matrix[i][j])
        count += 1
avg_corr /= max(count, 1)

n = len(tickers)
effective_bets = n / (1 + (n-1) * avg_corr)
print(f"\\nAverage pairwise correlation: {{avg_corr:.3f}}")
print(f"Number of positions: {{n}}")
print(f"Effective independent bets: {{effective_bets:.1f}}")

# Save to JSON
output = {{
    "tickers": tickers,
    "correlation_matrix": matrix,
    "avg_pairwise_correlation": round(avg_corr, 3),
    "effective_independent_bets": round(effective_bets, 1),
    "num_positions": n,
}}
with open("output/data/correlation-matrix.json", "w") as f:
    json.dump(output, f, indent=2)
print("\\nSaved to output/data/correlation-matrix.json")
'''

    return {
        "tickers": tickers,
        "period": period,
        "num_tickers": n,
        "instruction": f"Run the generated Python script to compute the {n}x{n} correlation matrix",
        "script_saved_to": "output/models/correlation-matrix.py",
        "code": code,
    }


# ============================================================
# MONTE CARLO SIMULATION
# ============================================================

def monte_carlo_portfolio(weights: List[float], expected_returns: List[float],
                          cov_matrix: List[List[float]], n_sims: int = 10000,
                          n_years: int = 1) -> Dict:
    """
    Monte Carlo portfolio simulation.
    """
    try:
        import numpy as np
    except ImportError:
        return {"error": "numpy required. Install: pip install numpy"}

    weights = np.array(weights)
    returns = np.array(expected_returns)
    cov = np.array(cov_matrix)
    n_days = n_years * 252

    # Daily returns and covariance
    daily_returns = returns / 252
    daily_cov = cov / 252

    # Simulate
    np.random.seed(42)
    portfolio_values = np.ones(n_sims)
    max_drawdowns = np.zeros(n_sims)

    for sim in range(n_sims):
        daily_r = np.random.multivariate_normal(daily_returns, daily_cov, n_days)
        portfolio_daily = daily_r @ weights
        cumulative = np.cumprod(1 + portfolio_daily)
        portfolio_values[sim] = cumulative[-1]

        # Max drawdown
        peak = np.maximum.accumulate(cumulative)
        drawdowns = (peak - cumulative) / peak
        max_drawdowns[sim] = np.max(drawdowns)

    final_returns = portfolio_values - 1.0
    percentiles = {
        "5th": round(float(np.percentile(final_returns, 5)), 4),
        "25th": round(float(np.percentile(final_returns, 25)), 4),
        "50th": round(float(np.percentile(final_returns, 50)), 4),
        "75th": round(float(np.percentile(final_returns, 75)), 4),
        "95th": round(float(np.percentile(final_returns, 95)), 4),
    }

    return {
        "simulation_parameters": {
            "n_simulations": n_sims,
            "n_years": n_years,
            "n_positions": len(weights),
        },
        "return_distribution": {
            "mean_return": f"{float(np.mean(final_returns)):.2%}",
            "median_return": f"{float(np.median(final_returns)):.2%}",
            "std_dev": f"{float(np.std(final_returns)):.2%}",
            "percentiles": {k: f"{v:.2%}" for k, v in percentiles.items()},
            "probability_of_loss": f"{float(np.mean(final_returns < 0)):.1%}",
        },
        "drawdown_distribution": {
            "mean_max_drawdown": f"{float(np.mean(max_drawdowns)):.2%}",
            "median_max_drawdown": f"{float(np.median(max_drawdowns)):.2%}",
            "95th_percentile_drawdown": f"{float(np.percentile(max_drawdowns, 95)):.2%}",
            "worst_drawdown": f"{float(np.max(max_drawdowns)):.2%}",
        },
    }


# ============================================================
# BENEISH M-SCORE (Fraud Detection)
# ============================================================

def beneish_m_score(financials: Dict) -> Dict:
    """
    Beneish M-Score for earnings manipulation detection.
    Requires two years of financial data.
    M-Score > -1.78 suggests higher probability of manipulation.

    Required financials keys (current and prior year):
    revenue, cogs, receivables, current_assets, ppe, total_assets,
    depreciation, sga, long_term_debt, current_liabilities,
    net_income, cfo, total_securities (optional)
    """
    curr = financials.get("current", {})
    prior = financials.get("prior", {})

    def safe_div(a, b):
        return a / b if b and b != 0 else 0

    # Days Sales in Receivables Index (DSRI)
    dsr_curr = safe_div(curr.get("receivables", 0), curr.get("revenue", 1)) * 365
    dsr_prior = safe_div(prior.get("receivables", 0), prior.get("revenue", 1)) * 365
    dsri = safe_div(dsr_curr, dsr_prior) if dsr_prior else 1.0

    # Gross Margin Index (GMI)
    gm_curr = safe_div(curr.get("revenue", 0) - curr.get("cogs", 0), curr.get("revenue", 1))
    gm_prior = safe_div(prior.get("revenue", 0) - prior.get("cogs", 0), prior.get("revenue", 1))
    gmi = safe_div(gm_prior, gm_curr) if gm_curr else 1.0

    # Asset Quality Index (AQI)
    aq_curr = 1 - safe_div(
        curr.get("current_assets", 0) + curr.get("ppe", 0),
        curr.get("total_assets", 1)
    )
    aq_prior = 1 - safe_div(
        prior.get("current_assets", 0) + prior.get("ppe", 0),
        prior.get("total_assets", 1)
    )
    aqi = safe_div(aq_curr, aq_prior) if aq_prior else 1.0

    # Sales Growth Index (SGI)
    sgi = safe_div(curr.get("revenue", 0), prior.get("revenue", 1))

    # Depreciation Index (DEPI)
    dep_rate_curr = safe_div(curr.get("depreciation", 0),
                             curr.get("depreciation", 0) + curr.get("ppe", 0))
    dep_rate_prior = safe_div(prior.get("depreciation", 0),
                              prior.get("depreciation", 0) + prior.get("ppe", 0))
    depi = safe_div(dep_rate_prior, dep_rate_curr) if dep_rate_curr else 1.0

    # SGA Expense Index (SGAI)
    sga_curr = safe_div(curr.get("sga", 0), curr.get("revenue", 1))
    sga_prior = safe_div(prior.get("sga", 0), prior.get("revenue", 1))
    sgai = safe_div(sga_curr, sga_prior) if sga_prior else 1.0

    # Leverage Index (LVGI)
    lev_curr = safe_div(
        curr.get("long_term_debt", 0) + curr.get("current_liabilities", 0),
        curr.get("total_assets", 1)
    )
    lev_prior = safe_div(
        prior.get("long_term_debt", 0) + prior.get("current_liabilities", 0),
        prior.get("total_assets", 1)
    )
    lvgi = safe_div(lev_curr, lev_prior) if lev_prior else 1.0

    # Total Accruals to Total Assets (TATA)
    tata = safe_div(
        curr.get("net_income", 0) - curr.get("cfo", 0),
        curr.get("total_assets", 1)
    )

    # M-Score calculation
    m_score = (
        -4.84
        + 0.920 * dsri
        + 0.528 * gmi
        + 0.404 * aqi
        + 0.892 * sgi
        + 0.115 * depi
        - 0.172 * sgai
        + 4.679 * tata
        - 0.327 * lvgi
    )

    if m_score > -1.78:
        assessment = "HIGH RISK — M-Score above -1.78 threshold. Elevated probability of earnings manipulation."
    elif m_score > -2.22:
        assessment = "MODERATE RISK — M-Score in gray zone (-2.22 to -1.78). Warrants closer examination."
    else:
        assessment = "LOW RISK — M-Score below -2.22. Low probability of earnings manipulation."

    return {
        "m_score": round(m_score, 3),
        "threshold": -1.78,
        "assessment": assessment,
        "components": {
            "DSRI (Days Sales Receivables Index)": round(dsri, 3),
            "GMI (Gross Margin Index)": round(gmi, 3),
            "AQI (Asset Quality Index)": round(aqi, 3),
            "SGI (Sales Growth Index)": round(sgi, 3),
            "DEPI (Depreciation Index)": round(depi, 3),
            "SGAI (SGA Expense Index)": round(sgai, 3),
            "LVGI (Leverage Index)": round(lvgi, 3),
            "TATA (Total Accruals / Total Assets)": round(tata, 4),
        },
        "red_flags": [
            comp for comp, val in [
                ("DSRI", dsri), ("GMI", gmi), ("AQI", aqi),
                ("SGI", sgi), ("DEPI", depi)
            ] if val > 1.2
        ],
    }


# ============================================================
# ALTMAN Z-SCORE (Bankruptcy Risk)
# ============================================================

def altman_z_score(financials: Dict) -> Dict:
    """
    Altman Z-Score for bankruptcy risk assessment.
    Z > 2.99: Safe zone | 1.81-2.99: Gray zone | Z < 1.81: Distress zone

    Required: working_capital, retained_earnings, ebit, market_cap,
              total_liabilities, revenue, total_assets
    """
    ta = financials.get("total_assets", 1)

    def safe_div(a, b):
        return a / b if b and b != 0 else 0

    x1 = safe_div(financials.get("working_capital", 0), ta)
    x2 = safe_div(financials.get("retained_earnings", 0), ta)
    x3 = safe_div(financials.get("ebit", 0), ta)
    x4 = safe_div(financials.get("market_cap", 0), financials.get("total_liabilities", 1))
    x5 = safe_div(financials.get("revenue", 0), ta)

    z = 1.2 * x1 + 1.4 * x2 + 3.3 * x3 + 0.6 * x4 + 1.0 * x5

    if z > 2.99:
        zone = "SAFE ZONE — Low probability of bankruptcy"
    elif z > 1.81:
        zone = "GRAY ZONE — Moderate risk, warrants monitoring"
    else:
        zone = "DISTRESS ZONE — Elevated bankruptcy risk"

    return {
        "z_score": round(z, 3),
        "zone": zone,
        "components": {
            "X1 (Working Capital / Total Assets)": round(x1, 4),
            "X2 (Retained Earnings / Total Assets)": round(x2, 4),
            "X3 (EBIT / Total Assets)": round(x3, 4),
            "X4 (Market Cap / Total Liabilities)": round(x4, 4),
            "X5 (Revenue / Total Assets)": round(x5, 4),
        },
        "thresholds": {"safe": "> 2.99", "gray": "1.81 - 2.99", "distress": "< 1.81"},
    }


# ============================================================
# CLI INTERFACE
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Portfolio Mathematics Calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  kelly            Kelly criterion from win/loss probabilities
  kelly-scenarios  Kelly from bull/base/bear scenarios
  vol-size         Volatility-adjusted position sizing
  liquidity        Liquidity-constrained max position
  expected-value   Probability-weighted expected price target
  optimize         Mean-variance portfolio optimization
  risk-parity      Risk parity portfolio weights
  correlation      Build correlation matrix (generates script)
  monte-carlo      Monte Carlo portfolio simulation
  beneish          Beneish M-Score (earnings manipulation)
  altman-z         Altman Z-Score (bankruptcy risk)
  black-litterman  Black-Litterman posterior from prior + views
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Kelly criterion
    kelly_parser = subparsers.add_parser("kelly", help="Kelly criterion sizing")
    kelly_parser.add_argument("--win-prob", type=float, required=True, help="Probability of winning")
    kelly_parser.add_argument("--win-return", type=float, required=True, help="Expected return if win")
    kelly_parser.add_argument("--loss-return", type=float, required=True, help="Expected loss if lose (positive number)")

    # Kelly from scenarios
    ks_parser = subparsers.add_parser("kelly-scenarios", help="Kelly from bull/base/bear")
    ks_parser.add_argument("--bull-price", type=float, required=True)
    ks_parser.add_argument("--base-price", type=float, required=True)
    ks_parser.add_argument("--bear-price", type=float, required=True)
    ks_parser.add_argument("--bull-prob", type=float, required=True)
    ks_parser.add_argument("--base-prob", type=float, required=True)
    ks_parser.add_argument("--bear-prob", type=float, required=True)
    ks_parser.add_argument("--current-price", type=float, required=True)

    # Vol-adjusted sizing
    vol_parser = subparsers.add_parser("vol-size", help="Volatility-adjusted sizing")
    vol_parser.add_argument("--stock-vol", type=float, required=True, help="Stock annualized volatility")
    vol_parser.add_argument("--portfolio-vol", type=float, required=True, help="Portfolio target volatility")
    vol_parser.add_argument("--num-positions", type=int, required=True, help="Number of positions")
    vol_parser.add_argument("--avg-correlation", type=float, default=0.3, help="Average pairwise correlation")

    # Liquidity
    liq_parser = subparsers.add_parser("liquidity", help="Liquidity-constrained max position")
    liq_parser.add_argument("--adv", type=float, required=True, help="Avg daily volume ($M)")
    liq_parser.add_argument("--participation", type=float, default=0.15, help="Max participation rate")
    liq_parser.add_argument("--max-days", type=int, default=5, help="Max days to liquidate")
    liq_parser.add_argument("--portfolio-size", type=float, required=True, help="Portfolio size ($M)")

    # Expected value
    ev_parser = subparsers.add_parser("expected-value", help="Expected value from scenarios")
    ev_parser.add_argument("--scenarios-file", type=str, help="JSON file with scenarios")
    ev_parser.add_argument("--scenarios", type=str, help="Inline JSON scenarios")

    # Optimize
    opt_parser = subparsers.add_parser("optimize", help="Portfolio optimization")
    opt_parser.add_argument("--returns-file", type=str, required=True, help="JSON file with expected returns")
    opt_parser.add_argument("--cov-file", type=str, required=True, help="JSON file with covariance matrix")
    opt_parser.add_argument("--method", type=str, default="max-sharpe",
                            choices=["max-sharpe", "min-variance", "risk-parity", "equal-weight"])
    opt_parser.add_argument("--risk-free-rate", type=float, default=0.05)
    opt_parser.add_argument("--max-weight", type=float, default=0.20)
    opt_parser.add_argument("--min-weight", type=float, default=0.0)

    # Risk parity
    rp_parser = subparsers.add_parser("risk-parity", help="Risk parity weights")
    rp_parser.add_argument("--cov-file", type=str, required=True, help="JSON file with covariance matrix")

    # Correlation
    corr_parser = subparsers.add_parser("correlation", help="Build correlation matrix")
    corr_parser.add_argument("--tickers", type=str, required=True, help="Comma-separated tickers")
    corr_parser.add_argument("--period", type=str, default="3y", choices=["1y", "2y", "3y", "5y"])

    # Monte Carlo
    mc_parser = subparsers.add_parser("monte-carlo", help="Monte Carlo simulation")
    mc_parser.add_argument("--portfolio-file", type=str, required=True, help="JSON with weights, returns, cov")
    mc_parser.add_argument("--simulations", type=int, default=10000)
    mc_parser.add_argument("--years", type=int, default=1)

    # Beneish M-Score
    ben_parser = subparsers.add_parser("beneish", help="Beneish M-Score")
    ben_parser.add_argument("--financials-file", type=str, required=True, help="JSON with current/prior financials")

    # Altman Z-Score
    alt_parser = subparsers.add_parser("altman-z", help="Altman Z-Score")
    alt_parser.add_argument("--financials-file", type=str, required=True, help="JSON with financials")

    # Black-Litterman
    bl_parser = subparsers.add_parser("black-litterman", help="Black-Litterman posterior")
    bl_parser.add_argument("--prior-file", type=str, required=True,
                           help="JSON list of equilibrium (prior) returns, one per asset")
    bl_parser.add_argument("--cov-file", type=str, required=True,
                           help="JSON N x N covariance matrix (same ordering as prior)")
    bl_parser.add_argument("--views-file", type=str, required=True,
                           help="JSON list of view dicts: {asset_indices, weights, expected_return, confidence}")
    bl_parser.add_argument("--tau", type=float, default=0.05,
                           help="Prior uncertainty scalar (default 0.05)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == "kelly":
        result = kelly_criterion(args.win_prob, args.win_return, args.loss_return)

    elif args.command == "kelly-scenarios":
        result = kelly_from_scenarios(
            args.bull_price, args.base_price, args.bear_price,
            args.bull_prob, args.base_prob, args.bear_prob,
            args.current_price
        )

    elif args.command == "vol-size":
        result = vol_adjusted_size(args.stock_vol, args.portfolio_vol,
                                   args.num_positions, args.avg_correlation)

    elif args.command == "liquidity":
        result = liquidity_max_position(args.adv, args.participation,
                                        args.max_days, args.portfolio_size)

    elif args.command == "expected-value":
        if args.scenarios_file:
            with open(args.scenarios_file) as f:
                scenarios = json.load(f)
        elif args.scenarios:
            scenarios = json.loads(args.scenarios)
        else:
            print("Error: Provide --scenarios-file or --scenarios")
            sys.exit(1)
        result = expected_value_from_scenarios(scenarios)

    elif args.command == "optimize":
        with open(args.returns_file) as f:
            returns = json.load(f)
        with open(args.cov_file) as f:
            cov = json.load(f)
        constraints = {"min_weight": args.min_weight, "max_weight": args.max_weight}
        result = mean_variance_optimize(returns, cov, args.method, args.risk_free_rate, constraints)

    elif args.command == "risk-parity":
        with open(args.cov_file) as f:
            cov = json.load(f)
        result = mean_variance_optimize(
            [0] * len(cov), cov, "risk-parity"
        )

    elif args.command == "correlation":
        tickers = [t.strip().upper() for t in args.tickers.split(",")]
        result = build_correlation_matrix(tickers, args.period)
        # Also save the generated script
        if "code" in result:
            code = result.pop("code")
            try:
                with open("output/models/correlation-matrix.py", "w") as f:
                    f.write(code)
                result["script_status"] = "Saved to output/models/correlation-matrix.py"
            except FileNotFoundError:
                result["script_status"] = "Could not save (output/models/ directory not found)"
                result["code_preview"] = code[:500] + "..."

    elif args.command == "monte-carlo":
        with open(args.portfolio_file) as f:
            pf = json.load(f)
        result = monte_carlo_portfolio(
            pf["weights"], pf["expected_returns"], pf["cov_matrix"],
            args.simulations, args.years
        )

    elif args.command == "beneish":
        with open(args.financials_file) as f:
            financials = json.load(f)
        result = beneish_m_score(financials)

    elif args.command == "altman-z":
        with open(args.financials_file) as f:
            financials = json.load(f)
        result = altman_z_score(financials)

    elif args.command == "black-litterman":
        with open(args.prior_file) as f:
            prior = json.load(f)
        with open(args.cov_file) as f:
            cov = json.load(f)
        with open(args.views_file) as f:
            views = json.load(f)
        result = black_litterman(prior, cov, views, tau=args.tau)

    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
