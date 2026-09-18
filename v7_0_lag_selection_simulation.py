"""
v7: Monte Carlo Type-I error check for IID-permutation lag scans
Date: September 2026
"""

import math
import numpy as np


def generate_ar1(n=300, phi=0.85, burn_in=500, seed=None):
    rng = np.random.default_rng(seed)
    series = [rng.normal(0, 1.0)]
    for _ in range(n + burn_in - 1):
        series.append(phi * series[-1] + rng.normal(0, 1.0))
    return np.array(series[burn_in:], dtype=np.float64)


def evaluate_lag_selection(a, b, max_lag=10, n_permutations=0, seed=None):
    best_lag = 0
    best_corr = 0.0
    best_abs = -1.0

    # Re-scan all lags within each permutation
    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            aa, bb = a[:lag], b[-lag:]
        elif lag > 0:
            aa, bb = a[lag:], b[:-lag]
        else:
            aa, bb = a, b

        if len(aa) > 5:
            c = np.corrcoef(aa, bb)[0, 1]
            if abs(c) > best_abs:
                best_abs = abs(c)
                best_corr = c
                best_lag = lag

    if n_permutations <= 0:
        return best_lag, best_corr, None

    rng = np.random.default_rng(seed)
    null_max_scores = []

    for _ in range(n_permutations):
        b_shuffled = rng.permutation(b)
        local_max_abs = -1.0

        for lag in range(-max_lag, max_lag + 1):
            if lag < 0:
                aa, bb = a[:lag], b_shuffled[-lag:]
            elif lag > 0:
                aa, bb = a[lag:], b_shuffled[:-lag]
            else:
                aa, bb = a, b_shuffled

            if len(aa) > 5:
                c_null = np.corrcoef(aa, bb)[0, 1]
                if abs(c_null) > local_max_abs:
                    local_max_abs = abs(c_null)

        null_max_scores.append(local_max_abs)

    null_max_scores = np.array(null_max_scores)
    p_val = (1 + np.sum(null_max_scores >= best_abs)) / (n_permutations + 1)

    return best_lag, best_corr, p_val


def execute_simulation():
    print("Initializing lag-scan simulation for autocorrelated series...\n")

    print("--- Illustrative Independent Pair ---")
    a_single = generate_ar1(n=300, phi=0.85, seed=42)
    b_single = generate_ar1(n=300, phi=0.85, seed=101)

    best_lag, best_corr, p_val = evaluate_lag_selection(
        a_single, b_single, max_lag=10, n_permutations=500, seed=999
    )

    print(f"Max Scanned Correlation : {best_corr:.4f} (at lag {best_lag:+d})")
    print(f"IID Max-Scan Permutation p : {p_val:.4f}\n")

    print("--- Monte Carlo Type-I Error Check ---")
    n_trials = 100
    n_perms = 200
    print(f"Running {n_trials} independent trials (H0 is true, alpha=0.05)...")

    false_positives = 0
    mc_rng = np.random.default_rng(777)

    for i in range(n_trials):
        a_mc = generate_ar1(n=300, phi=0.85, seed=int(mc_rng.integers(0, 1000000)))
        b_mc = generate_ar1(n=300, phi=0.85, seed=int(mc_rng.integers(0, 1000000)))

        _, _, p_mc = evaluate_lag_selection(
            a_mc, b_mc, max_lag=10, n_permutations=n_perms, seed=int(mc_rng.integers(0, 1000000))
        )

        if p_mc < 0.05:
            false_positives += 1

    empirical_size = false_positives / n_trials
    se = math.sqrt(empirical_size * (1 - empirical_size) / n_trials)

    print(f"Empirical False Positive Rate : {empirical_size:.3f} ({false_positives}/{n_trials})")
    print(f"Monte Carlo Standard Error    : {se:.4f}")
    print(f"(Expected rate ~ 0.05 if the null distribution were correctly calibrated)\n")

    print("-" * 65)
    print("Observation:")
    print("The IID permutation does not preserve serial dependence.")
    print("In this simulation, the IID-permutation max-lag test rejects far above the nominal level.")
    print("-" * 65)


if __name__ == "__main__":
    execute_simulation()