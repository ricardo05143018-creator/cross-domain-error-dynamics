"""
v5: naive IID permutation baseline
Date: September 2026
"""

import numpy as np


def extract_prediction_residuals(predictions, actuals):
    predictions = np.array(predictions, dtype=np.float64)
    actuals = np.array(actuals, dtype=np.float64)

    if predictions.shape != actuals.shape:
        raise ValueError("Predictions and actuals must have the same shape.")

    # prediction residual: actuals - predictions
    return actuals - predictions


def align_observable_sequences(series_a, series_b):
    if len(series_a) != len(series_b):
        raise ValueError("The two time series must have equal length.")
    return np.array(series_a, dtype=np.float64), np.array(series_b, dtype=np.float64)


def apply_rolling_mean_filter(series, window=5):
    return np.array([
        np.mean(series[i:i + window])
        for i in range(len(series) - window + 1)
    ], dtype=np.float64)


def scan_lag_correlation(series_a, series_b, max_lag=10):
    results = []
    best_lag = 0
    best_corr = 0.0
    best_abs = -1.0

    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            a = series_a[:lag]
            b = series_b[-lag:]
        elif lag > 0:
            a = series_a[lag:]
            b = series_b[:-lag]
        else:
            a, b = series_a, series_b

        if len(a) > 3:
            corr = np.corrcoef(a, b)[0, 1]
            results.append((lag, corr))
            if abs(corr) > best_abs:
                best_abs = abs(corr)
                best_corr = corr
                best_lag = lag

    return results, (best_lag, best_corr)


def run_synchronous_permutation_test(series_a, series_b, n_permutations=500):
    observed_corr = np.corrcoef(series_a, series_b)[0, 1]
    null_distribution = []

    for _ in range(n_permutations):
        shuffled_b = np.random.permutation(series_b)
        null_corr = np.corrcoef(series_a, shuffled_b)[0, 1]
        null_distribution.append(null_corr)

    nulls = np.array(null_distribution)
    p_val = (1 + np.sum(np.abs(nulls) >= abs(observed_corr))) / (n_permutations + 1)

    return observed_corr, np.mean(nulls), np.std(nulls), p_val


def execute_baseline_analysis():
    print("Initializing IID permutation baseline...\n")
    np.random.seed(42)

    soccer_pred = 0.6 + np.random.normal(0, 0.05, 60)
    soccer_act = 0.6 + np.random.normal(0, 0.08, 60)
    finance_pred = 0.5 + np.random.normal(0, 0.04, 60)
    finance_act = 0.5 + np.random.normal(0, 0.10, 60)

    soccer_error = extract_prediction_residuals(soccer_pred, soccer_act)
    finance_error = extract_prediction_residuals(finance_pred, finance_act)

    s, f = align_observable_sequences(soccer_error, finance_error)
    s_roll = apply_rolling_mean_filter(s)
    f_roll = apply_rolling_mean_filter(f)

    _, best_lag_info = scan_lag_correlation(s_roll, f_roll)
    observed_corr, null_mean, null_std, p_val = run_synchronous_permutation_test(s_roll, f_roll)

    print("--- Exploratory Lag Scan ---")
    print("Descriptive only; the permutation p-value below is for lag 0.")
    print("-" * 55)
    print(f"Optimal Scanned Lag:       {best_lag_info[0]:+d} windows (r = {best_lag_info[1]:.4f})")

    print("\n--- Naive IID Permutation Baseline (Lag 0) ---")
    print("Warning: Overlapping rolling means violate exchangeability. This naive test is a")
    print("historical baseline to motivate later corrections, not a valid final inference.")
    print("-" * 55)
    print(f"Synchronous Observed r:    {observed_corr:.4f}")
    print(f"Permutation Null Mean (r): {null_mean:.4f}")
    print(f"Permutation Null Std Dev:  {null_std:.4f}")
    print(f"Synchronous Two-Sided p:   {p_val:.4f}")
    print("=" * 55)


if __name__ == "__main__":
    execute_baseline_analysis()
