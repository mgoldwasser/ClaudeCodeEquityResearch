#!/usr/bin/env python3
"""
Batch Runner — Stock Universe Management & Batch Execution
Equity Research Swarm

Manages the stock database (data/stocks.json), filters by tags/sectors,
checks staleness, and generates batch run plans.

Usage:
    python tools/batch-runner.py list                                    # List all stocks
    python tools/batch-runner.py list --tag mag7                         # List Mag 7 stocks
    python tools/batch-runner.py list --sector Technology                # List tech stocks
    python tools/batch-runner.py list --tag ai --tag semiconductors      # Multiple tags (OR)
    python tools/batch-runner.py stale                                   # Show stocks needing refresh (>7 days)
    python tools/batch-runner.py stale --days 14                         # Custom staleness threshold
    python tools/batch-runner.py plan --tag mag7                         # Generate run plan for Mag 7
    python tools/batch-runner.py plan --sector Healthcare                # Generate run plan for healthcare
    python tools/batch-runner.py plan --stale                            # Generate plan for all stale stocks
    python tools/batch-runner.py plan --all                              # Generate plan for entire universe
    python tools/batch-runner.py add TICKER "Company Name" --sector X --tags tag1,tag2
    python tools/batch-runner.py remove TICKER
    python tools/batch-runner.py mark-complete TICKER                    # Mark stock as researched today
    python tools/batch-runner.py tags                                    # List all available tags
    python tools/batch-runner.py status                                  # Universe status dashboard
    python tools/batch-runner.py update-db                               # Refresh database metadata
"""

import json
import sys
import os
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Resolve paths relative to project root
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DB_PATH = PROJECT_ROOT / "data" / "stocks.json"
OUTPUT_DIR = PROJECT_ROOT / "output"

DEFAULT_STALENESS_DAYS = 7


def load_db():
    """Load the stock database."""
    if not DB_PATH.exists():
        print(f"Error: Stock database not found at {DB_PATH}")
        print("Create it with: python tools/batch-runner.py add TICKER 'Company Name' --sector X --tags tag1,tag2")
        sys.exit(1)
    with open(DB_PATH, 'r') as f:
        return json.load(f)


def save_db(db):
    """Save the stock database."""
    db['_metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(DB_PATH, 'w') as f:
        json.dump(db, f, indent=2)


def is_stale(stock, days=DEFAULT_STALENESS_DAYS):
    """Check if a stock's research is stale."""
    if stock.get('last_researched') is None:
        return True
    try:
        last = datetime.strptime(stock['last_researched'], '%Y-%m-%d')
        return (datetime.now() - last).days > days
    except (ValueError, TypeError):
        return True


def days_since_research(stock):
    """Get days since last research, or None if never researched."""
    if stock.get('last_researched') is None:
        return None
    try:
        last = datetime.strptime(stock['last_researched'], '%Y-%m-%d')
        return (datetime.now() - last).days
    except (ValueError, TypeError):
        return None


def filter_stocks(db, tags=None, sector=None, stale_only=False, stale_days=DEFAULT_STALENESS_DAYS):
    """Filter stocks by tags, sector, and staleness."""
    stocks = db.get('stocks', [])

    if tags:
        stocks = [s for s in stocks if any(t in s.get('tags', []) for t in tags)]

    if sector:
        stocks = [s for s in stocks if s.get('sector', '').lower() == sector.lower()]

    if stale_only:
        stocks = [s for s in stocks if is_stale(s, stale_days)]

    return stocks


def check_existing_output(ticker):
    """Check if output already exists for a ticker."""
    if not OUTPUT_DIR.exists():
        return None
    for f in OUTPUT_DIR.iterdir():
        if f.name.startswith(f"{ticker}-research-note-") and f.suffix == '.md':
            return f.name
    return None


# ─── Commands ───────────────────────────────────────────────────────────────

def cmd_list(args):
    """List stocks, optionally filtered."""
    db = load_db()
    stocks = filter_stocks(db, tags=args.tag, sector=args.sector)

    if not stocks:
        print("No stocks match the filter criteria.")
        return

    # Header
    print(f"\n{'Ticker':<8} {'Name':<35} {'Sector':<22} {'Tags':<40} {'Last Researched':<16} {'Status'}")
    print("─" * 130)

    for s in sorted(stocks, key=lambda x: x['ticker']):
        ticker = s['ticker']
        name = s.get('name', '')[:34]
        sector = s.get('sector', '')[:21]
        tags = ', '.join(s.get('tags', []))[:39]
        last = s.get('last_researched') or 'Never'
        days = days_since_research(s)

        if days is None:
            status = "⬜ Not researched"
        elif days <= DEFAULT_STALENESS_DAYS:
            status = f"✅ Fresh ({days}d ago)"
        else:
            status = f"⚠️  Stale ({days}d ago)"

        print(f"{ticker:<8} {name:<35} {sector:<22} {tags:<40} {last:<16} {status}")

    print(f"\nTotal: {len(stocks)} stocks")


def cmd_stale(args):
    """Show stocks needing refresh."""
    db = load_db()
    days = args.days if args.days else DEFAULT_STALENESS_DAYS
    stale = filter_stocks(db, stale_only=True, stale_days=days)

    if not stale:
        print(f"\nAll stocks are fresh (researched within {days} days).")
        return

    never_researched = [s for s in stale if s.get('last_researched') is None]
    outdated = [s for s in stale if s.get('last_researched') is not None]

    if never_researched:
        print(f"\n📋 Never Researched ({len(never_researched)} stocks):")
        for s in sorted(never_researched, key=lambda x: x['ticker']):
            print(f"  {s['ticker']:<8} {s.get('name', '')}")

    if outdated:
        print(f"\n⚠️  Stale (>{days} days) ({len(outdated)} stocks):")
        for s in sorted(outdated, key=lambda x: days_since_research(x) or 0, reverse=True):
            d = days_since_research(s)
            print(f"  {s['ticker']:<8} {s.get('name', ''):<35} Last: {s['last_researched']} ({d}d ago)")

    print(f"\nTotal needing refresh: {len(stale)}")


def cmd_plan(args):
    """Generate a batch run plan."""
    db = load_db()

    if args.all:
        stocks = db.get('stocks', [])
    elif args.stale:
        days = args.days if args.days else DEFAULT_STALENESS_DAYS
        stocks = filter_stocks(db, stale_only=True, stale_days=days)
    else:
        stocks = filter_stocks(db, tags=args.tag, sector=args.sector)

    if not stocks:
        print("No stocks match the criteria. Nothing to run.")
        return

    tickers = [s['ticker'] for s in sorted(stocks, key=lambda x: x['ticker'])]

    print(f"\n# Batch Run Plan")
    print(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"# Stocks: {len(tickers)}")

    if args.tag:
        print(f"# Filter: tags = {', '.join(args.tag)}")
    if args.sector:
        print(f"# Filter: sector = {args.sector}")
    if args.stale:
        print(f"# Filter: stale (>{args.days or DEFAULT_STALENESS_DAYS} days)")

    print(f"# Tickers: {', '.join(tickers)}")
    print()

    # Generate the claude command for batch execution
    print("## Execution Commands")
    print()
    print("### Option 1: Sequential (one at a time)")
    print("```bash")
    for t in tickers:
        print(f'claude "Run the full-research-note workflow for {t}. Follow the CLAUDE.md orchestration protocol."')
    print("```")
    print()

    print("### Option 2: Batch instruction (recommended)")
    ticker_list = ', '.join(tickers)
    print("```bash")
    print(f'claude "Run the full-research-note workflow for the following stocks sequentially: {ticker_list}. For each stock, follow the CLAUDE.md orchestration protocol. After completing each stock, run tools/batch-runner.py mark-complete [TICKER] to update the database. Process cross-stock notes between stocks."')
    print("```")
    print()

    # Per-stock status
    print("## Stock Status")
    print()
    print(f"{'Ticker':<8} {'Name':<35} {'Last Researched':<16} {'Existing Output'}")
    print("─" * 85)
    for s in sorted(stocks, key=lambda x: x['ticker']):
        existing = check_existing_output(s['ticker']) or "None"
        last = s.get('last_researched') or 'Never'
        print(f"{s['ticker']:<8} {s.get('name', '')[:34]:<35} {last:<16} {existing}")

    print()
    print(f"Estimated time: ~{len(tickers) * 15}-{len(tickers) * 25} minutes ({len(tickers)} stocks × 15-25 min each)")


def cmd_add(args):
    """Add a stock to the database."""
    db = load_db()

    # Check for duplicate
    existing = [s for s in db['stocks'] if s['ticker'] == args.ticker.upper()]
    if existing:
        print(f"Error: {args.ticker.upper()} already exists in the database.")
        print(f"  Name: {existing[0].get('name')}")
        print(f"  Tags: {', '.join(existing[0].get('tags', []))}")
        return

    tags = [t.strip() for t in args.tags.split(',')] if args.tags else []

    stock = {
        "ticker": args.ticker.upper(),
        "name": args.name,
        "sector": args.sector or "Unknown",
        "industry": args.industry or "Unknown",
        "tags": tags,
        "last_researched": None
    }

    db['stocks'].append(stock)
    save_db(db)
    print(f"Added {args.ticker.upper()} ({args.name}) to stock database.")
    print(f"  Sector: {stock['sector']}")
    print(f"  Tags: {', '.join(tags) if tags else 'None'}")


def cmd_remove(args):
    """Remove a stock from the database."""
    db = load_db()
    ticker = args.ticker.upper()

    original_count = len(db['stocks'])
    db['stocks'] = [s for s in db['stocks'] if s['ticker'] != ticker]

    if len(db['stocks']) == original_count:
        print(f"Error: {ticker} not found in database.")
        return

    save_db(db)
    print(f"Removed {ticker} from stock database.")


def cmd_mark_complete(args):
    """Mark a stock as researched today."""
    db = load_db()
    ticker = args.ticker.upper()
    today = datetime.now().strftime('%Y-%m-%d')

    found = False
    for s in db['stocks']:
        if s['ticker'] == ticker:
            s['last_researched'] = today
            found = True
            break

    if not found:
        print(f"Error: {ticker} not found in database.")
        return

    save_db(db)
    print(f"Marked {ticker} as researched on {today}.")


def cmd_tags(args):
    """List all available tags with stock counts."""
    db = load_db()

    # Count tags
    tag_counts = {}
    for s in db.get('stocks', []):
        for t in s.get('tags', []):
            tag_counts[t] = tag_counts.get(t, 0) + 1

    # Get definitions
    tag_defs = db.get('tag_definitions', {})

    print(f"\n{'Tag':<22} {'Count':<8} {'Description'}")
    print("─" * 80)

    for tag in sorted(tag_counts.keys()):
        desc = tag_defs.get(tag, '')
        print(f"{tag:<22} {tag_counts[tag]:<8} {desc}")

    print(f"\nTotal tags: {len(tag_counts)}")
    print(f"Total stocks: {len(db.get('stocks', []))}")


def cmd_status(args):
    """Show universe status dashboard."""
    db = load_db()
    stocks = db.get('stocks', [])
    total = len(stocks)

    if total == 0:
        print("Stock database is empty.")
        return

    never = sum(1 for s in stocks if s.get('last_researched') is None)
    fresh = sum(1 for s in stocks if not is_stale(s) and s.get('last_researched') is not None)
    stale = total - never - fresh

    # Sector breakdown
    sectors = {}
    for s in stocks:
        sec = s.get('sector', 'Unknown')
        sectors[sec] = sectors.get(sec, 0) + 1

    # Tag popularity
    tag_counts = {}
    for s in stocks:
        for t in s.get('tags', []):
            tag_counts[t] = tag_counts.get(t, 0) + 1

    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    print(f"\n{'='*60}")
    print(f"  STOCK UNIVERSE STATUS DASHBOARD")
    print(f"  Database: {DB_PATH}")
    print(f"  Last updated: {db.get('_metadata', {}).get('last_updated', 'Unknown')}")
    print(f"{'='*60}")
    print()
    print(f"  Total stocks:        {total}")
    print(f"  ✅ Fresh:             {fresh} ({fresh/total*100:.0f}%)")
    print(f"  ⚠️  Stale (>{DEFAULT_STALENESS_DAYS}d):     {stale} ({stale/total*100:.0f}%)")
    print(f"  ⬜ Never researched:  {never} ({never/total*100:.0f}%)")
    print()

    print(f"  SECTORS:")
    for sec in sorted(sectors.keys()):
        bar = "█" * sectors[sec]
        print(f"    {sec:<25} {sectors[sec]:>3}  {bar}")
    print()

    print(f"  TOP TAGS:")
    for tag, count in top_tags:
        bar = "█" * count
        print(f"    {tag:<22} {count:>3}  {bar}")
    print()

    # Staleness details
    if stale > 0 or never > 0:
        print(f"  NEEDS ATTENTION:")
        needing = [s for s in stocks if is_stale(s)]
        for s in sorted(needing, key=lambda x: x['ticker'])[:10]:
            d = days_since_research(s)
            status = f"{d}d ago" if d is not None else "Never"
            print(f"    {s['ticker']:<8} {status}")
        if len(needing) > 10:
            print(f"    ... and {len(needing) - 10} more")
    print()


def cmd_update_db(args):
    """Refresh database metadata and check for completed research in output/."""
    db = load_db()
    updated = 0

    if OUTPUT_DIR.exists():
        for s in db['stocks']:
            output_file = check_existing_output(s['ticker'])
            if output_file and s.get('last_researched') is None:
                # Extract date from filename: TICKER-research-note-YYYY-MM-DD.md
                try:
                    date_part = output_file.replace(f"{s['ticker']}-research-note-", "").replace(".md", "")
                    datetime.strptime(date_part, '%Y-%m-%d')
                    s['last_researched'] = date_part
                    updated += 1
                    print(f"  Updated {s['ticker']}: last_researched = {date_part} (from output file)")
                except ValueError:
                    pass

    save_db(db)
    print(f"\nDatabase refreshed. {updated} stocks updated from output files.")
    print(f"Last updated: {db['_metadata']['last_updated']}")


# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Stock Universe Management & Batch Execution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/batch-runner.py list --tag mag7           # List Magnificent Seven
  python tools/batch-runner.py list --sector Healthcare  # List healthcare stocks
  python tools/batch-runner.py stale                     # Show stale stocks (>7 days)
  python tools/batch-runner.py plan --tag mag7           # Generate run plan for Mag 7
  python tools/batch-runner.py plan --stale              # Plan for all stale stocks
  python tools/batch-runner.py add PLTR "Palantir" --sector Technology --tags ai,software,government
  python tools/batch-runner.py mark-complete AAPL        # Mark as researched today
  python tools/batch-runner.py status                    # Dashboard view
        """
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # list
    p_list = subparsers.add_parser('list', help='List stocks')
    p_list.add_argument('--tag', action='append', help='Filter by tag (can specify multiple)')
    p_list.add_argument('--sector', help='Filter by sector')

    # stale
    p_stale = subparsers.add_parser('stale', help='Show stale stocks')
    p_stale.add_argument('--days', type=int, help=f'Staleness threshold in days (default: {DEFAULT_STALENESS_DAYS})')

    # plan
    p_plan = subparsers.add_parser('plan', help='Generate batch run plan')
    p_plan.add_argument('--tag', action='append', help='Filter by tag')
    p_plan.add_argument('--sector', help='Filter by sector')
    p_plan.add_argument('--stale', action='store_true', help='Only stale stocks')
    p_plan.add_argument('--all', action='store_true', help='All stocks')
    p_plan.add_argument('--days', type=int, help=f'Staleness threshold (default: {DEFAULT_STALENESS_DAYS})')

    # add
    p_add = subparsers.add_parser('add', help='Add a stock')
    p_add.add_argument('ticker', help='Stock ticker')
    p_add.add_argument('name', help='Company name')
    p_add.add_argument('--sector', help='Sector')
    p_add.add_argument('--industry', help='Industry')
    p_add.add_argument('--tags', help='Comma-separated tags')

    # remove
    p_remove = subparsers.add_parser('remove', help='Remove a stock')
    p_remove.add_argument('ticker', help='Stock ticker')

    # mark-complete
    p_mark = subparsers.add_parser('mark-complete', help='Mark stock as researched today')
    p_mark.add_argument('ticker', help='Stock ticker')

    # tags
    subparsers.add_parser('tags', help='List all tags')

    # status
    subparsers.add_parser('status', help='Universe status dashboard')

    # update-db
    subparsers.add_parser('update-db', help='Refresh database from output files')

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    commands = {
        'list': cmd_list,
        'stale': cmd_stale,
        'plan': cmd_plan,
        'add': cmd_add,
        'remove': cmd_remove,
        'mark-complete': cmd_mark_complete,
        'tags': cmd_tags,
        'status': cmd_status,
        'update-db': cmd_update_db,
    }

    commands[args.command](args)


if __name__ == '__main__':
    main()
