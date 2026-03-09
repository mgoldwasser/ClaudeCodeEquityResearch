#!/usr/bin/env python3
"""
screening.py — Quantitative screening utilities for comparable company analysis.

Usage:
    python3 tools/screening.py calc-multiples --data <json_file>
    python3 tools/screening.py z-scores --data <json_file>
    python3 tools/screening.py rank --data <json_file> --method <composite|value|quality|momentum>
    python3 tools/screening.py sensitivity --wacc-range 8,12 --tgr-range 1,4 --base-fcf <fcf> --growth <g>

Input: JSON file with company data in the format:
{
    "companies": [
        {
            "ticker": "AAPL",
            "name": "Apple Inc.",
            "market_cap": 3000000,
            "enterprise_value": 2950000,
            "revenue_ntm": 400000,
            "ebitda_ntm": 140000,
            "net_income_ntm": 100000,
            "eps_ntm": 6.50,
            "eps_growth": 10.0,
            "fcf_ntm": 110000,
            "shares_diluted": 15400,
            "roic": 55.0,
            "ebitda_margin": 35.0,
            "net_margin": 25.0,
            "revenue_growth": 8.0,
            "net_debt": -50000,
            "price": 195.00,
            "price_3m_chg": 5.2,
            "estimate_revisions_3m": 2.1,
            "is_subject": false
        }
    ]
}
"""

import argparse
import json
import sys
import math
from typing import Dict, List, Optional


def load_data(filepath: str) -> Dict:
    """Load company data from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def calc_multiples(companies: List[Dict]) -> List[Dict]:
    """Calculate valuation multiples for each company."""
    results = []
    for c in companies:
        ev = c.get('enterprise_value', 0)
        mc = c.get('market_cap', 0)

        multiples = {
            'ticker': c['ticker'],
            'name': c.get('name', ''),
            'is_subject': c.get('is_subject', False),
            'market_cap': mc,
            'enterprise_value': ev,
        }

        # EV/EBITDA
        ebitda = c.get('ebitda_ntm', 0)
        multiples['ev_ebitda'] = round(ev / ebitda, 1) if ebitda and ebitda > 0 else None

        # P/E
        eps = c.get('eps_ntm', 0)
        price = c.get('price', 0)
        multiples['pe'] = round(price / eps, 1) if eps and eps > 0 else None

        # EV/Revenue
        rev = c.get('revenue_ntm', 0)
        multiples['ev_revenue'] = round(ev / rev, 1) if rev and rev > 0 else None

        # PEG
        growth = c.get('eps_growth', 0)
        pe = multiples.get('pe')
        multiples['peg'] = round(pe / growth, 2) if pe and growth and growth > 0 else None

        # EV/FCF
        fcf = c.get('fcf_ntm', 0)
        multiples['ev_fcf'] = round(ev / fcf, 1) if fcf and fcf > 0 else None

        # FCF Yield
        multiples['fcf_yield'] = round((fcf / mc) * 100, 1) if fcf and mc and mc > 0 else None

        # Growth and profitability
        multiples['revenue_growth'] = c.get('revenue_growth')
        multiples['ebitda_margin'] = c.get('ebitda_margin')
        multiples['net_margin'] = c.get('net_margin')
        multiples['roic'] = c.get('roic')

        results.append(multiples)

    return results


def calc_statistics(values: List[float]) -> Dict:
    """Calculate summary statistics for a list of values."""
    if not values:
        return {'median': None, 'mean': None, 'std_dev': None, 'p25': None, 'p75': None, 'min': None, 'max': None}

    sorted_vals = sorted(values)
    n = len(sorted_vals)

    mean = sum(sorted_vals) / n
    variance = sum((x - mean) ** 2 for x in sorted_vals) / n if n > 1 else 0
    std_dev = math.sqrt(variance)

    # Median
    if n % 2 == 0:
        median = (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
    else:
        median = sorted_vals[n // 2]

    # Percentiles (simple method)
    p25_idx = max(0, int(n * 0.25) - 1)
    p75_idx = min(n - 1, int(n * 0.75))

    return {
        'median': round(median, 2),
        'mean': round(mean, 2),
        'std_dev': round(std_dev, 2),
        'p25': round(sorted_vals[p25_idx], 2),
        'p75': round(sorted_vals[p75_idx], 2),
        'min': round(sorted_vals[0], 2),
        'max': round(sorted_vals[-1], 2),
        'count': n
    }


def z_scores(companies: List[Dict]) -> Dict:
    """Calculate z-scores for the subject company relative to comps."""
    multiples_data = calc_multiples(companies)

    # Separate subject from comps
    subject = None
    comps = []
    for m in multiples_data:
        if m.get('is_subject'):
            subject = m
        else:
            comps.append(m)

    if not subject:
        return {'error': 'No subject company identified (set is_subject: true)'}

    metrics = ['ev_ebitda', 'pe', 'ev_revenue', 'peg', 'ev_fcf']
    z_results = {}

    for metric in metrics:
        comp_values = [c[metric] for c in comps if c.get(metric) is not None]
        if not comp_values or subject.get(metric) is None:
            z_results[metric] = {'z_score': None, 'percentile': None, 'stats': None}
            continue

        stats = calc_statistics(comp_values)
        if stats['std_dev'] and stats['std_dev'] > 0:
            z = (subject[metric] - stats['median']) / stats['std_dev']
        else:
            z = 0

        # Approximate percentile
        below = sum(1 for v in comp_values if v <= subject[metric])
        percentile = round((below / len(comp_values)) * 100)

        outlier_flag = None
        if abs(z) > 2:
            direction = 'above' if z > 0 else 'below'
            outlier_flag = f"OUTLIER: {subject['ticker']} trades at {subject[metric]}x {metric.replace('_', '/').upper()}, " \
                           f"which is {abs(z):.1f} standard deviations {direction} the comp group median of {stats['median']}x"

        z_results[metric] = {
            'subject_value': subject[metric],
            'z_score': round(z, 2),
            'percentile': percentile,
            'stats': stats,
            'outlier_flag': outlier_flag
        }

    return {
        'subject': subject['ticker'],
        'comp_count': len(comps),
        'z_scores': z_results
    }


def composite_rank(companies: List[Dict], method: str = 'composite') -> List[Dict]:
    """
    Rank companies by composite score.

    Methods:
        composite: Equal-weighted valuation + quality + momentum
        value: Valuation metrics only (lower multiple = better)
        quality: Quality metrics only (higher ROIC/margin = better)
        momentum: Price and estimate momentum only
    """
    multiples_data = calc_multiples(companies)
    n = len(multiples_data)

    # Calculate percentile ranks for each metric
    def percentile_rank(values_with_idx, lower_is_better=True):
        """Rank values and return percentile scores (0-100, higher is better)."""
        valid = [(i, v) for i, v in values_with_idx if v is not None]
        if not valid:
            return {i: 50 for i, _ in values_with_idx}  # default to median

        sorted_valid = sorted(valid, key=lambda x: x[1], reverse=not lower_is_better)
        ranks = {}
        for rank, (idx, _) in enumerate(sorted_valid):
            ranks[idx] = round(((len(sorted_valid) - rank) / len(sorted_valid)) * 100)

        # Fill None values with median rank
        for i, v in values_with_idx:
            if i not in ranks:
                ranks[i] = 50

        return ranks

    # Valuation scores (lower multiple = better = higher score)
    ev_ebitda_ranks = percentile_rank([(i, m.get('ev_ebitda')) for i, m in enumerate(multiples_data)], lower_is_better=True)
    pe_ranks = percentile_rank([(i, m.get('pe')) for i, m in enumerate(multiples_data)], lower_is_better=True)

    # Quality scores (higher = better)
    roic_ranks = percentile_rank([(i, m.get('roic')) for i, m in enumerate(multiples_data)], lower_is_better=False)
    margin_ranks = percentile_rank([(i, m.get('ebitda_margin')) for i, m in enumerate(multiples_data)], lower_is_better=False)

    # Momentum scores (higher = better)
    price_mom_ranks = percentile_rank(
        [(i, companies[i].get('price_3m_chg')) for i in range(n)],
        lower_is_better=False
    )
    est_rev_ranks = percentile_rank(
        [(i, companies[i].get('estimate_revisions_3m')) for i in range(n)],
        lower_is_better=False
    )

    results = []
    for i, m in enumerate(multiples_data):
        val_score = (ev_ebitda_ranks[i] + pe_ranks[i]) / 2
        qual_score = (roic_ranks[i] + margin_ranks[i]) / 2
        mom_score = (price_mom_ranks[i] + est_rev_ranks[i]) / 2

        if method == 'value':
            composite = val_score
        elif method == 'quality':
            composite = qual_score
        elif method == 'momentum':
            composite = mom_score
        else:  # composite
            composite = (val_score + qual_score + mom_score) / 3

        results.append({
            'ticker': m['ticker'],
            'name': m.get('name', ''),
            'is_subject': m.get('is_subject', False),
            'valuation_score': round(val_score, 1),
            'quality_score': round(qual_score, 1),
            'momentum_score': round(mom_score, 1),
            'composite_score': round(composite, 1)
        })

    # Sort by composite score (higher = better)
    results.sort(key=lambda x: x['composite_score'], reverse=True)

    # Add rank
    for rank, r in enumerate(results, 1):
        r['rank'] = rank

    return results


def sensitivity_table(wacc_range: tuple, tgr_range: tuple, base_fcf: float,
                      growth_rate: float, years: int = 5, shares: float = 1.0,
                      net_debt: float = 0.0) -> Dict:
    """
    Generate a WACC vs. terminal growth rate sensitivity table.

    Args:
        wacc_range: (min_wacc, max_wacc) as percentages
        tgr_range: (min_tgr, max_tgr) as percentages
        base_fcf: Base year free cash flow ($M)
        growth_rate: Annual FCF growth rate (%) for explicit forecast period
        years: Number of explicit forecast years
        shares: Diluted shares outstanding (M)
        net_debt: Net debt ($M, positive = debt exceeds cash)
    """
    wacc_min, wacc_max = wacc_range
    tgr_min, tgr_max = tgr_range

    # Generate 5 steps for each
    wacc_steps = [wacc_min + i * (wacc_max - wacc_min) / 4 for i in range(5)]
    tgr_steps = [tgr_min + i * (tgr_max - tgr_min) / 4 for i in range(5)]

    table = {}
    for wacc_pct in wacc_steps:
        wacc = wacc_pct / 100
        row = {}
        for tgr_pct in tgr_steps:
            tgr = tgr_pct / 100

            if wacc <= tgr:
                row[f"{tgr_pct:.1f}%"] = "N/A"
                continue

            # Project FCFs
            fcfs = []
            fcf = base_fcf
            for yr in range(1, years + 1):
                fcf = fcf * (1 + growth_rate / 100)
                pv = fcf / ((1 + wacc) ** yr)
                fcfs.append(pv)

            # Terminal value
            terminal_fcf = fcf * (1 + tgr)
            tv = terminal_fcf / (wacc - tgr)
            pv_tv = tv / ((1 + wacc) ** years)

            # Enterprise value
            ev = sum(fcfs) + pv_tv

            # Equity value per share
            equity_value = ev - net_debt
            price_per_share = equity_value / shares if shares > 0 else 0

            tv_pct = round((pv_tv / ev) * 100, 1) if ev > 0 else 0

            row[f"{tgr_pct:.1f}%"] = {
                'price': round(price_per_share, 2),
                'ev': round(ev, 0),
                'tv_pct': tv_pct
            }

        table[f"{wacc_pct:.1f}%"] = row

    return {
        'wacc_values': [f"{w:.1f}%" for w in wacc_steps],
        'tgr_values': [f"{t:.1f}%" for t in tgr_steps],
        'table': table,
        'assumptions': {
            'base_fcf': base_fcf,
            'fcf_growth_rate': growth_rate,
            'forecast_years': years,
            'shares_diluted': shares,
            'net_debt': net_debt
        }
    }


def print_sensitivity_table(result: Dict):
    """Pretty-print sensitivity table."""
    wacc_vals = result['wacc_values']
    tgr_vals = result['tgr_values']
    table = result['table']

    # Header
    header = f"{'WACC':<10}" + "".join(f"{'TGR ' + t:>12}" for t in tgr_vals)
    print(header)
    print("-" * len(header))

    for wacc in wacc_vals:
        row = f"{wacc:<10}"
        for tgr in tgr_vals:
            cell = table[wacc][tgr]
            if cell == "N/A":
                row += f"{'N/A':>12}"
            else:
                price = cell['price']
                tv_flag = "*" if cell['tv_pct'] > 50 else ""
                row += f"${price:>10.2f}{tv_flag}"
        print(row)

    print("\n* Terminal value > 50% of enterprise value")


def main():
    parser = argparse.ArgumentParser(description='Quantitative screening utilities')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # calc-multiples
    p_mult = subparsers.add_parser('calc-multiples', help='Calculate valuation multiples')
    p_mult.add_argument('--data', required=True, help='Path to JSON data file')

    # z-scores
    p_z = subparsers.add_parser('z-scores', help='Calculate z-scores vs comp group')
    p_z.add_argument('--data', required=True, help='Path to JSON data file')

    # rank
    p_rank = subparsers.add_parser('rank', help='Composite ranking')
    p_rank.add_argument('--data', required=True, help='Path to JSON data file')
    p_rank.add_argument('--method', default='composite',
                        choices=['composite', 'value', 'quality', 'momentum'],
                        help='Ranking method')

    # sensitivity
    p_sens = subparsers.add_parser('sensitivity', help='WACC vs TGR sensitivity table')
    p_sens.add_argument('--wacc-range', required=True, help='WACC range as min,max (e.g., 8,12)')
    p_sens.add_argument('--tgr-range', required=True, help='Terminal growth range as min,max (e.g., 1,4)')
    p_sens.add_argument('--base-fcf', required=True, type=float, help='Base year FCF ($M)')
    p_sens.add_argument('--growth', required=True, type=float, help='Annual FCF growth rate (%)')
    p_sens.add_argument('--years', default=5, type=int, help='Forecast years (default: 5)')
    p_sens.add_argument('--shares', required=True, type=float, help='Diluted shares (M)')
    p_sens.add_argument('--net-debt', default=0, type=float, help='Net debt ($M)')
    p_sens.add_argument('--format', default='json', choices=['json', 'table'], help='Output format')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'calc-multiples':
        data = load_data(args.data)
        result = calc_multiples(data['companies'])
        print(json.dumps(result, indent=2))

    elif args.command == 'z-scores':
        data = load_data(args.data)
        result = z_scores(data['companies'])
        print(json.dumps(result, indent=2))

    elif args.command == 'rank':
        data = load_data(args.data)
        result = composite_rank(data['companies'], method=args.method)
        print(json.dumps(result, indent=2))

    elif args.command == 'sensitivity':
        wacc_min, wacc_max = map(float, args.wacc_range.split(','))
        tgr_min, tgr_max = map(float, args.tgr_range.split(','))
        result = sensitivity_table(
            wacc_range=(wacc_min, wacc_max),
            tgr_range=(tgr_min, tgr_max),
            base_fcf=args.base_fcf,
            growth_rate=args.growth,
            years=args.years,
            shares=args.shares,
            net_debt=args.net_debt
        )
        if args.format == 'table':
            print_sensitivity_table(result)
        else:
            print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
