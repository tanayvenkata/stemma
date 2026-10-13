# SPDX-License-Identifier: MIT
"""Uncertainty for evaluation gates, computed rather than estimated in prose.

Standard library only. Run from anywhere:

  python3 gate_stats.py rate 3 40
      Pass rate with a Wilson 95% interval, plus the rule-of-three bound when
      there are no failures (or no passes).

  python3 gate_stats.py paired results.csv
      Paired comparison of two configurations on the same cases. The CSV has a
      header and one row per case: case_id,baseline,candidate (scores or 0/1).
      Reports the mean difference with a percentile bootstrap 95% interval
      (cases resampled), and wins, losses, and ties.

Options: --confidence 0.9 (default 0.95), --resamples N (default 10000),
--seed N (default 0).
"""

import argparse
import csv
import math
import random
import statistics
import sys

Z = {0.80: 1.2816, 0.90: 1.6449, 0.95: 1.9600, 0.99: 2.5758}


def z_for(confidence):
    if confidence not in Z:
        raise ValueError(f"confidence must be one of {sorted(Z)}")
    return Z[confidence]


def wilson(successes, n, confidence=0.95):
    """Wilson score interval for a binomial proportion."""
    if n <= 0 or not 0 <= successes <= n:
        raise ValueError("need 0 <= successes <= n and n > 0")
    z = z_for(confidence)
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def rule_of_three(n, confidence=0.95):
    """Upper bound on an event rate when it was seen 0 times in n trials.

    Uses the exact one-sided binomial bound 1 - (1 - confidence) ** (1 / n);
    the rule of three, 3 / n at 95%, approximates it once n is above about 30.
    """
    if n <= 0:
        raise ValueError("n must be positive")
    return 1 - (1 - confidence) ** (1 / n)


def paired_bootstrap(pairs, confidence=0.95, resamples=10000, seed=0):
    """Mean of candidate - baseline over cases, with a percentile bootstrap CI."""
    if len(pairs) < 2:
        raise ValueError("need at least two paired cases")
    diffs = [c - b for b, c in pairs]
    rng = random.Random(seed)
    n = len(diffs)
    means = sorted(
        sum(diffs[rng.randrange(n)] for _ in range(n)) / n for _ in range(resamples)
    )
    alpha = (1 - confidence) / 2
    lo = means[int(math.floor(alpha * resamples))]
    hi = means[min(resamples - 1, int(math.ceil((1 - alpha) * resamples)) - 1)]
    return {
        "n": n,
        "mean_diff": statistics.fmean(diffs),
        "ci": (lo, hi),
        "wins": sum(d > 0 for d in diffs),
        "losses": sum(d < 0 for d in diffs),
        "ties": sum(d == 0 for d in diffs),
    }


def read_pairs(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows or not {"baseline", "candidate"} <= set(rows[0]):
        raise ValueError("CSV needs columns case_id,baseline,candidate")
    return [(float(r["baseline"]), float(r["candidate"])) for r in rows]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--confidence", type=float, default=0.95)
    parser.add_argument("--resamples", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=0)
    sub = parser.add_subparsers(dest="cmd", required=True)
    rate = sub.add_parser("rate")
    rate.add_argument("passes", type=int)
    rate.add_argument("n", type=int)
    paired = sub.add_parser("paired")
    paired.add_argument("csv")
    args = parser.parse_args(argv)
    pct = round(args.confidence * 100)

    if args.cmd == "rate":
        lo, hi = wilson(args.passes, args.n, args.confidence)
        print(f"pass rate {args.passes}/{args.n} = {args.passes / args.n:.3f}")
        print(f"Wilson {pct}% interval: [{lo:.3f}, {hi:.3f}]")
        if args.passes == args.n:
            print(f"0 failures in {args.n}: failure rate below {rule_of_three(args.n, args.confidence):.3f} at {pct}% (exact zero-event bound; about 3/n, the rule of three, for large n)")
        elif args.passes == 0:
            print(f"0 passes in {args.n}: pass rate below {rule_of_three(args.n, args.confidence):.3f} at {pct}% (exact zero-event bound; about 3/n, the rule of three, for large n)")
    else:
        r = paired_bootstrap(read_pairs(args.csv), args.confidence, args.resamples, args.seed)
        lo, hi = r["ci"]
        print(f"{r['n']} paired cases: mean difference (candidate - baseline) {r['mean_diff']:+.3f}")
        print(f"bootstrap {pct}% interval: [{lo:+.3f}, {hi:+.3f}]")
        print(f"wins {r['wins']}, losses {r['losses']}, ties {r['ties']}")
        if lo <= 0 <= hi:
            print("the interval includes 0: the data cannot distinguish the configurations")


if __name__ == "__main__":
    sys.exit(main())
