"""
v5.1: paired moving-block stability check
Date: September 2026
"""

import math
import numpy as np


def _get_moving_block_indices(n, block_size=15):
    if block_size <= 0 or block_size >= n:
        raise ValueError("Block size must be positive and smaller than sequence length.")

    indices = []
    num_blocks = math.ceil(n / block_size)

    for _ in range(num_blocks):
        start = np.random.randint(0, n - block_size + 1)
        indices.extend(range(start, start + block_size))

    return np.array(indices[:n])


def run_paired_block_bootstrap_corr(series_a, series_b, n_bootstrap=500, block_size=15):
    bootstrap_corrs = []
    n = len(series_a)

    for _ in range(n_bootstrap):
        idx = _get_moving_block_indices(n, block_size)
        a_sample = np.array(series_a)[idx]
        b_sample = np.array(series_b)[idx]
        bootstrap_corrs.append(np.corrcoef(a_sample, b_sample)[0, 1])

    return np.array(bootstrap_corrs)


def audit_paired_lag_stability(series_a, series_b, max_lag=10, n_bootstrap=300, block_size=15):
    lag_distribution = []
    n = len(series_a)

    for _ in range(n_bootstrap):
        idx = _get_moving_block_indices(n, block_size)
        a = np.array(series_a)[idx]
        b = np.array(series_b)[idx]

        best_lag = 0
        best_corr = 0.0
        best_abs = -1.0

        for lag in range(-max_lag, max_lag + 1):
            if lag < 0:
                a_shift, b_shift = a[:lag], b[-lag:]
            elif lag > 0:
                a_shift, b_shift = a[lag:], b[:-lag]
            else:
                a_shift, b_shift = a, b

            if len(a_shift) > 3:
                corr = np.corrcoef(a_shift, b_shift)[0, 1]
                if abs(corr) > best_abs:
                    best_abs = abs(corr)
                    best_corr = corr
                    best_lag = lag

        lag_distribution.append(best_lag)

    return np.array(lag_distribution)


def execute_stability_check(series_a, series_b):
    series_a = np.array(series_a, dtype=np.float64)
    series_b = np.array(series_b, dtype=np.float64)

    if len(series_a) != len(series_b):
        raise ValueError("The two time series must have equal length.")

    print("Executing paired moving-block stability check...\n")

    observed_corr = np.corrcoef(series_a, series_b)[0, 1]
    corr_dist = run_paired_block_bootstrap_corr(series_a, series_b, block_size=15)
    corr_mean, corr_std = np.mean(corr_dist), np.std(corr_dist)

    print("--- Paired Block Bootstrap (Synchronous Correlation) ---")
    print(f"Observed Synchronous r:  {observed_corr:.4f}")
    print(f"Resampled Mean r:        {corr_mean:.4f}")
    print(f"Resampled Std Dev:       {corr_std:.4f}")

    lag_dist = audit_paired_lag_stability(series_a, series_b, block_size=15)

    # Safely compute mode without hardcoding array boundaries
    vals, counts = np.unique(lag_dist, return_counts=True)
    lag_mode = vals[np.argmax(counts)]
    lag_stability = np.std(lag_dist)

    print("\n--- Paired Lag Stability ---")
    print(f"Modal Selected Lag:      {lag_mode:+d} windows")
    print(f"Lag Standard Deviation:  {lag_stability:.4f}")

    print("\n" + "=" * 65)
    print("Scope:")
    print("This is a descriptive stability check, not a null calibration.")
    print("The resampling uses a shared block index, preserving the observed")
    print("cross-series relationship rather than imposing independence.")
    print("=================================================================\n")


if __name__ == "__main__":
    np.random.seed(42)
    s_err, f_err = [0.0], [0.0]
    for _ in range(99):
        s_err.append(0.6 * s_err[-1] + np.random.normal(0, 1))
        f_err.append(0.5 * f_err[-1] + np.random.normal(0, 1))

    execute_stability_check(np.array(s_err), np.array(f_err))
