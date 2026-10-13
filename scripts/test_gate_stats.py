"""Tests for the skill's gate_stats.py. Run: python3 scripts/test_gate_stats.py"""

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(
    0, str(Path(__file__).resolve().parent.parent / "plugins/stemma/skills/stemma/scripts")
)
import gate_stats as g  # noqa: E402


class Wilson(unittest.TestCase):
    def test_known_value(self):
        # 8/10 at 95%: [0.490, 0.943] (standard Wilson score interval)
        lo, hi = g.wilson(8, 10)
        self.assertAlmostEqual(lo, 0.490, places=3)
        self.assertAlmostEqual(hi, 0.943, places=3)

    def test_bounds_at_extremes(self):
        lo, hi = g.wilson(0, 20)
        self.assertEqual(lo, 0.0)
        self.assertGreater(hi, 0.0)
        lo, hi = g.wilson(20, 20)
        self.assertEqual(hi, 1.0)
        self.assertLess(lo, 1.0)

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            g.wilson(5, 3)
        with self.assertRaises(ValueError):
            g.wilson(1, 10, confidence=0.93)


class RuleOfThree(unittest.TestCase):
    def test_exact_bound(self):
        self.assertAlmostEqual(g.rule_of_three(3), 0.6316, places=4)
        self.assertAlmostEqual(g.rule_of_three(100), 0.02951, places=4)

    def test_approaches_three_over_n(self):
        self.assertAlmostEqual(g.rule_of_three(300), 3 / 300, places=3)


class PairedBootstrap(unittest.TestCase):
    def test_clear_improvement_excludes_zero(self):
        pairs = [(0, 1)] * 15 + [(1, 1)] * 5
        r = g.paired_bootstrap(pairs)
        self.assertAlmostEqual(r["mean_diff"], 0.75)
        self.assertGreater(r["ci"][0], 0)
        self.assertEqual((r["wins"], r["losses"], r["ties"]), (15, 0, 5))

    def test_noise_includes_zero(self):
        pairs = [(0, 1), (1, 0)] * 5
        r = g.paired_bootstrap(pairs)
        self.assertLessEqual(r["ci"][0], 0)
        self.assertGreaterEqual(r["ci"][1], 0)

    def test_deterministic_with_seed(self):
        pairs = [(0.2, 0.5), (0.4, 0.3), (0.1, 0.9), (0.6, 0.6)]
        self.assertEqual(g.paired_bootstrap(pairs, seed=3), g.paired_bootstrap(pairs, seed=3))


class Cli(unittest.TestCase):
    def run_cli(self, argv):
        out = io.StringIO()
        with redirect_stdout(out):
            g.main(argv)
        return out.getvalue()

    def test_rate_reports_rule_of_three_on_zero_failures(self):
        text = self.run_cli(["rate", "30", "30"])
        self.assertIn("zero-event bound", text)

    def test_paired_from_csv(self):
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False) as f:
            f.write("case_id,baseline,candidate\na,0,1\nb,1,0\nc,0,1\nd,1,1\n")
        text = self.run_cli(["paired", f.name])
        self.assertIn("4 paired cases", text)
        self.assertIn("cannot distinguish", text)


if __name__ == "__main__":
    unittest.main()
