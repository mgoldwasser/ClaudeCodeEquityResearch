"""
Lookahead-leak test suite for the --as-of retrofit.

Runs three layers:

  1. Helper unit tests
     - Exercise tools/_as_of.py (resolve, filter_by_date, epoch, parse errors)
       and the filter helpers inside tools/alt-data.py directly.
     - Pure-python, deterministic, no network.

  2. CLI contract tests
     - Subprocess each retrofitted tool to verify:
       - --as-of flag is accepted where supported
       - bad date strings exit 1
       - historical mode of Category C commands exits 2
       - live-mode invocation is preserved (zero-regression)
     - No network required; tests exercise surface only, not responses.

  3. Output vintage tests (network-gated)
     - Only run when RUN_NETWORK_TESTS=1 is set in the environment.
     - Hit real endpoints (SEC EDGAR, FRED CSV fallback, Yahoo Finance
       history) with --as-of=2021-06-01 and assert no data point with a
       date > as_of leaks into the tool output.

Run:
    python3 -m unittest tests/test_as_of.py -v
    RUN_NETWORK_TESTS=1 python3 -m unittest tests/test_as_of.py -v
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import unittest
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = REPO_ROOT / "tools"
PY = sys.executable

# Make tools/ importable so we can load _as_of and alt-data module-level helpers.
sys.path.insert(0, str(TOOLS_DIR))
import _as_of  # noqa: E402


def _load_alt_data_module():
    """Load tools/alt-data.py as a module (hyphen in filename blocks `import`)."""
    spec = importlib.util.spec_from_file_location("alt_data", TOOLS_DIR / "alt-data.py")
    mod = importlib.util.module_from_spec(spec)
    # Running the module-top-level code must not have side effects beyond defs.
    spec.loader.exec_module(mod)
    return mod


ALT_DATA = _load_alt_data_module()
AS_OF_DATE = "2021-06-01"
AS_OF = date(2021, 6, 1)


def _run(cmd, env_overrides=None, timeout=45):
    """Run a subprocess with a clean env + overrides, return (rc, stdout, stderr)."""
    env = os.environ.copy()
    env.pop("EQUITY_SWARM_AS_OF", None)
    if env_overrides:
        env.update(env_overrides)
    proc = subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout, proc.stderr


# ============================================================
# Layer 1 — Helper unit tests
# ============================================================

class AsOfResolveTests(unittest.TestCase):
    def test_resolve_none_in_live_mode(self):
        self.assertIsNone(_as_of.resolve(None))

    def test_resolve_cli_overrides_env(self):
        os.environ["EQUITY_SWARM_AS_OF"] = "2018-01-01"
        try:
            # CLI value wins.
            self.assertEqual(_as_of.resolve("2021-06-01"), AS_OF)
        finally:
            del os.environ["EQUITY_SWARM_AS_OF"]

    def test_resolve_env_var_fallback(self):
        os.environ["EQUITY_SWARM_AS_OF"] = "2021-06-01"
        try:
            self.assertEqual(_as_of.resolve(None), AS_OF)
        finally:
            del os.environ["EQUITY_SWARM_AS_OF"]

    def test_resolve_future_date_returns_live(self):
        self.assertIsNone(_as_of.resolve("2099-01-01"))

    def test_resolve_bad_date_exits(self):
        with self.assertRaises(SystemExit) as cm:
            _as_of.resolve("not-a-date")
        self.assertEqual(cm.exception.code, _as_of.EXIT_PARSE_ERROR)

    def test_resolve_pre_1990_rejected(self):
        with self.assertRaises(SystemExit) as cm:
            _as_of.resolve("1985-03-01")
        self.assertEqual(cm.exception.code, _as_of.EXIT_PARSE_ERROR)


class AsOfFilterTests(unittest.TestCase):
    def test_filter_by_date_drops_post_asof(self):
        records = [
            {"d": "2020-01-01"},
            {"d": "2021-06-01"},  # exactly as_of: KEEP
            {"d": "2021-06-02"},  # one day after: DROP
            {"d": "2025-01-01"},  # far after: DROP
        ]
        out = _as_of.filter_by_date(records, "d", AS_OF)
        dates = [r["d"] for r in out]
        self.assertEqual(dates, ["2020-01-01", "2021-06-01"])

    def test_filter_by_date_drops_undated_in_historical(self):
        records = [{"d": "2020-01-01"}, {"d": None}, {}]
        out = _as_of.filter_by_date(records, "d", AS_OF)
        self.assertEqual(len(out), 1)

    def test_filter_by_date_passthrough_in_live(self):
        records = [{"d": "2099-01-01"}]
        out = _as_of.filter_by_date(records, "d", None)
        self.assertEqual(out, records)

    def test_epoch_end_of_day(self):
        # 2021-06-01 23:59:59 UTC
        self.assertEqual(_as_of.epoch(AS_OF, end_of_day=True), 1622591999)

    def test_epoch_start_of_day(self):
        # 2021-06-01 00:00:00 UTC
        self.assertEqual(_as_of.epoch(AS_OF, end_of_day=False), 1622505600)

    def test_assert_live_only_no_op_in_live(self):
        # Must not raise.
        _as_of.assert_live_only("tool", "cmd", "reason", as_of=None)

    def test_assert_live_only_exits_in_historical(self):
        with self.assertRaises(SystemExit) as cm:
            _as_of.assert_live_only("tool", "cmd", "reason", as_of=AS_OF)
        self.assertEqual(cm.exception.code, _as_of.EXIT_CURRENT_ONLY)


class AltDataFilterHelperTests(unittest.TestCase):
    def test_filter_by_field_drops_post_asof(self):
        rows = [
            {"filingDate": "2021-05-30"},
            {"filingDate": "2021-06-01"},
            {"filingDate": "2021-06-02"},
            {"filingDate": "2022-01-01"},
        ]
        kept = ALT_DATA._filter_by_field(rows, "filingDate", AS_OF)
        self.assertEqual([r["filingDate"] for r in kept],
                         ["2021-05-30", "2021-06-01"])

    def test_filter_by_field_empty_field_dropped(self):
        rows = [{"filingDate": ""}, {"filingDate": None}, {"other": "x"}]
        self.assertEqual(ALT_DATA._filter_by_field(rows, "filingDate", AS_OF), [])

    def test_filter_by_field_live_passthrough(self):
        rows = [{"filingDate": "2099-01-01"}]
        self.assertEqual(ALT_DATA._filter_by_field(rows, "filingDate", None), rows)

    def test_historical_warning_live_returns_none(self):
        self.assertIsNone(ALT_DATA._historical_warning(None, "anything"))

    def test_historical_warning_historical_contains_date(self):
        w = ALT_DATA._historical_warning(AS_OF, "insider data")
        self.assertIn(AS_OF_DATE, w)
        self.assertIn("insider data", w)


# ============================================================
# Layer 2 — CLI contract tests (no network)
# ============================================================

class CLIContractTests(unittest.TestCase):
    """
    Verify each retrofitted tool:
      - accepts --as-of on help output
      - exits 1 on malformed --as-of
      - exits 2 on Category C hard-fail commands in historical mode
    No network is required: all tests short-circuit on flag parsing or
    the hard-fail gate before any fetch is attempted.
    """

    def _assert_help_has_as_of(self, cmd):
        rc, out, err = _run(cmd)
        combined = out + err
        self.assertIn("--as-of", combined,
                      f"{' '.join(cmd)} help should mention --as-of")

    # ---- shell tools ----

    def test_financial_data_help_exposes_asof(self):
        # financial-data.sh has no --help; `usage()` mentions --as-of via AS_OF.md
        # but the ground truth here is that a bad --as-of exits 1.
        rc, _, err = _run(["./tools/financial-data.sh", "ticker", "AAPL",
                           "--as-of", "not-a-date"])
        self.assertEqual(rc, 1, err)
        self.assertIn("invalid", err.lower())

    def test_market_data_stats_hard_fails_in_historical(self):
        rc, _, err = _run(["./tools/market-data.sh", "stats", "AAPL",
                           "--as-of", AS_OF_DATE])
        self.assertEqual(rc, 2, f"expected exit 2 (Category C), got {rc}\n{err}")
        self.assertIn("not supported", err)

    def test_market_data_quote_hard_fails_in_historical(self):
        rc, _, err = _run(["./tools/market-data.sh", "quote", "AAPL",
                           "--as-of", AS_OF_DATE])
        self.assertEqual(rc, 2)

    def test_market_data_profile_hard_fails_in_historical(self):
        rc, _, err = _run(["./tools/market-data.sh", "profile", "AAPL",
                           "--as-of", AS_OF_DATE])
        self.assertEqual(rc, 2)

    def test_env_var_triggers_hard_fail_without_flag(self):
        # Env var should flow into the hard-fail gate even with no CLI flag.
        rc, _, err = _run(
            ["./tools/market-data.sh", "stats", "AAPL"],
            env_overrides={"EQUITY_SWARM_AS_OF": AS_OF_DATE},
        )
        self.assertEqual(rc, 2, err)

    def test_bad_date_rejected_consistently(self):
        rc, _, err = _run(["./tools/market-data.sh", "history", "AAPL", "1y",
                           "--as-of", "06/01/2021"])
        self.assertEqual(rc, 1, err)

    # ---- python tools ----

    def test_alt_data_peers_accepts_asof(self):
        # peers is mostly static reference data; historical mode should still
        # return a structured envelope with as_of set. No network.
        rc, out, err = _run([PY, "./tools/alt-data.py", "peers", "AAPL",
                             "--as-of", AS_OF_DATE])
        self.assertEqual(rc, 0, err)
        doc = json.loads(out)
        self.assertEqual(doc["as_of"], AS_OF_DATE)
        self.assertIsNotNone(doc.get("historical_mode_warning"))
        # Unsafe sources must be flagged False.
        ys = doc["data_sources"]["yahoo_finance"]
        self.assertFalse(ys["as_of_safe"])

    def test_alt_data_ownership_summary_propagates_asof(self):
        rc, out, err = _run([PY, "./tools/alt-data.py", "ownership-summary",
                             "AAPL", "--as-of", AS_OF_DATE])
        self.assertEqual(rc, 0, err)
        doc = json.loads(out)
        self.assertEqual(doc["as_of"], AS_OF_DATE)
        # All three nested sub-calls must carry the same as_of.
        for sub in ("insider_trades", "institutional_holdings",
                    "short_interest"):
            self.assertEqual(doc[sub]["as_of"], AS_OF_DATE,
                             f"{sub} did not propagate as_of")
        # Retrieval priority must prefer SEC paths in historical mode.
        priority_0 = doc["retrieval_priority"][0]
        self.assertIn("edgar-enhanced.py", priority_0)
        self.assertIn("--as-of", priority_0)

    def test_alt_data_bad_date_exits_1(self):
        rc, _, err = _run([PY, "./tools/alt-data.py", "peers", "AAPL",
                           "--as-of", "June 1 2021"])
        self.assertEqual(rc, 1, err)

    def test_alt_data_live_mode_has_no_asof_artifacts(self):
        # Zero-regression: live mode must not emit historical envelope fields.
        rc, out, err = _run([PY, "./tools/alt-data.py", "peers", "MSFT"])
        self.assertEqual(rc, 0, err)
        doc = json.loads(out)
        self.assertIsNone(doc.get("as_of"))
        self.assertIsNone(doc.get("historical_mode_warning"))

    def test_edgar_enhanced_help_exposes_asof(self):
        rc, out, err = _run([PY, "./tools/edgar-enhanced.py", "filing",
                             "AAPL", "10-K", "--as-of", "not-a-date"])
        self.assertEqual(rc, 1, err)

    def test_transcript_fetcher_accepts_asof_flag(self):
        # search subcommand on a ticker short-circuits on validation,
        # or attempts network. Use validation failure to prove the flag is wired.
        rc, _, err = _run([PY, "./tools/transcript-fetcher.py", "search",
                           "AAPL", "--as-of", "garbage"])
        self.assertEqual(rc, 1, err)

    def test_macro_data_accepts_asof_flag(self):
        rc, _, err = _run([PY, "./tools/macro-data.py", "rates",
                           "--as-of", "garbage"])
        self.assertEqual(rc, 1, err)


# ============================================================
# Layer 3 — Output vintage tests (network-gated)
# ============================================================

NETWORK = os.environ.get("RUN_NETWORK_TESTS") == "1"


@unittest.skipUnless(NETWORK, "Set RUN_NETWORK_TESTS=1 to enable network tests")
class OutputVintageTests(unittest.TestCase):
    """
    Hit real endpoints and confirm that no post-as_of dated data leaks.
    """

    def _dates_in(self, obj, key_hint=("date", "filed", "period", "end",
                                       "filingDate", "transactionDate",
                                       "time", "lastUpdated")):
        """Yield all YYYY-MM-DD-looking strings that sit under plausibly
        date-valued keys in a deep JSON structure."""
        out = []

        def walk(x, parent_key=""):
            if isinstance(x, dict):
                for k, v in x.items():
                    walk(v, str(k))
            elif isinstance(x, list):
                for v in x:
                    walk(v, parent_key)
            else:
                if not isinstance(x, str) or len(x) < 10:
                    return
                s = x[:10]
                if (s[4] == "-" and s[7] == "-"
                        and s[:4].isdigit() and s[5:7].isdigit()
                        and s[8:10].isdigit()
                        and any(h.lower() in parent_key.lower()
                                for h in key_hint)):
                    out.append(s)

        walk(obj)
        return out

    def test_edgar_enhanced_filing_10k_is_vintage(self):
        rc, out, err = _run([PY, "./tools/edgar-enhanced.py", "filing",
                             "AAPL", "10-K", "--as-of", AS_OF_DATE])
        self.assertEqual(rc, 0, err)
        doc = json.loads(out)
        # The returned filing's date must be <= as_of.
        filing_date = doc.get("date") or doc.get("filing_date")
        self.assertTrue(filing_date and filing_date <= AS_OF_DATE,
                        f"Returned filing date {filing_date} leaks > {AS_OF_DATE}")

    def test_edgar_enhanced_financials_are_vintage(self):
        rc, out, err = _run([PY, "./tools/edgar-enhanced.py", "financials",
                             "AAPL", "--as-of", AS_OF_DATE])
        self.assertEqual(rc, 0, err)
        doc = json.loads(out)
        for d in self._dates_in(doc):
            self.assertLessEqual(d, AS_OF_DATE,
                                 f"Dated value {d} > as_of {AS_OF_DATE}")

    def test_financial_data_company_facts_vintage(self):
        rc, out, err = _run(["./tools/financial-data.sh", "company", "AAPL",
                             "--as-of", AS_OF_DATE])
        self.assertEqual(rc, 0, err)
        doc = json.loads(out)
        for d in self._dates_in(doc):
            self.assertLessEqual(d, AS_OF_DATE,
                                 f"Dated value {d} > as_of {AS_OF_DATE}")

    def test_market_data_history_bounded_by_asof(self):
        rc, out, err = _run(["./tools/market-data.sh", "history", "AAPL", "3y",
                             "--as-of", AS_OF_DATE])
        self.assertEqual(rc, 0, err)
        # Yahoo CSV: header + rows; row[0] is Date.
        lines = [ln for ln in out.strip().splitlines() if ln]
        self.assertGreater(len(lines), 1)
        for ln in lines[1:]:
            d = ln.split(",")[0]
            if len(d) == 10 and d[4] == "-":
                self.assertLessEqual(d, AS_OF_DATE,
                                     f"Quote row {d} leaks > {AS_OF_DATE}")

    def test_macro_data_fred_observations_bounded(self):
        # Without FRED_API_KEY the tool falls back to CSV (which does not
        # natively vintage, but passes coed=as_of to bound observation end).
        rc, out, err = _run([PY, "./tools/macro-data.py", "fred", "DGS10",
                             "--as-of", AS_OF_DATE])
        self.assertEqual(rc, 0, err)
        doc = json.loads(out) if out.strip().startswith("{") else None
        if not doc:
            self.skipTest("FRED fallback returned non-JSON")
        for d in self._dates_in(doc, key_hint=("date", "observation_end")):
            self.assertLessEqual(d, AS_OF_DATE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
