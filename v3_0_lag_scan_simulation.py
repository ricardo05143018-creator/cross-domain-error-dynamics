"""
v3: exploratory lag scan and shock alignment
Date: August 2026
"""

import math
import numpy as np


def calc_standardized_z(values):
    array_data = np.array(values, dtype=np.float64)
    std_dev = np.std(array_data)
    if std_dev == 0:
        return np.zeros_like(array_data)
    return (array_data - np.mean(array_data)) / std_dev


def apply_rolling_mean_filter(data, window_size=4, stride=1):
    if window_size <= 0 or window_size > len(data):
        raise ValueError("Window size must be between 1 and the series length.")
    if stride <= 0:
        raise ValueError("Stride must be strictly positive.")

    result = []
    index = 0
    while index + window_size <= len(data):
        result.append(np.mean(data[index:index + window_size]))
        index += stride
    return np.array(result, dtype=np.float64)


def scan_lag_correlation(series_a, series_b, max_lag=10):
    lag_profiles = []

    # negative lag means series_b trails series_a
    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            x = series_a[:lag]
            y = series_b[-lag:]
        elif lag > 0:
            x = series_a[lag:]
            y = series_b[:-lag]
        else:
            x = series_a
            y = series_b

        if len(x) > 2:
            mean_x, mean_y = np.mean(x), np.mean(y)
            cov = np.sum((x - mean_x) * (y - mean_y))
            var_x = np.sum((x - mean_x) ** 2)
            var_y = np.sum((y - mean_y) ** 2)

            corr = float(cov / math.sqrt(var_x * var_y)) if var_x > 0 and var_y > 0 else 0.0
            lag_profiles.append((lag, corr))

    return lag_profiles, max(lag_profiles, key=lambda x: abs(x[1]))


def identify_statistical_shocks(series, threshold_z=2.0):
    mean = np.mean(series)
    std = np.std(series)

    shocks = []
    for i, value in enumerate(series):
        if std > 0 and abs(value - mean) / std > threshold_z:
            shocks.append(i)

    return shocks


def compute_shock_alignment_score(shocks_a, shocks_b, tolerance=1):
    if tolerance < 0:
        raise ValueError("Tolerance must be non-negative.")

    shocks_a = sorted(shocks_a)
    b_available = sorted(shocks_b)

    if not shocks_a or not b_available:
        return 0.0

    # match each shock at most once
    matched = 0
    for a in shocks_a:
        for b in b_available:
            if abs(a - b) <= tolerance:
                matched += 1
                b_available.remove(b)
                break

    return float(2 * matched / (len(shocks_a) + len(shocks_b)))


def execute_lag_scan_analysis():
    print("Running exploratory lag scan simulation...\n")
    np.random.seed(42)

    soccer_stream = 0.60 + np.random.normal(0, 0.05, 50)
    finance_stream = 0.50 + np.random.normal(0, 0.10, 50)

    soccer_stream[12:14] += 0.30
    finance_stream[14:16] += 0.60

    s_norm = calc_standardized_z(soccer_stream)
    f_norm = calc_standardized_z(finance_stream)

    s_roll = apply_rolling_mean_filter(s_norm)
    f_roll = apply_rolling_mean_filter(f_norm)

    _, best_lag = scan_lag_correlation(s_roll, f_roll, max_lag=5)

    s_shocks = identify_statistical_shocks(s_norm)
    f_shocks = identify_statistical_shocks(f_norm)
    score = compute_shock_alignment_score(s_shocks, f_shocks, tolerance=2)

    mean_s, mean_f = np.mean(s_roll), np.mean(f_roll)
    cov = np.sum((s_roll - mean_s) * (f_roll - mean_f))
    base_corr = cov / math.sqrt(
        np.sum((s_roll - mean_s) ** 2) *
        np.sum((f_roll - mean_f) ** 2)
    )

    print("--- Lag Scan Profile Analysis ---")
    print("Note: exploratory lag scan; selection bias is not corrected.")
    print("-" * 42)
    print(f"Base Correlation (Lag 0): {base_corr:.4f}")
    print(f"Selected Lag:             {best_lag[0]:+d} windows")
    print(f"Peak Scanned Correlation: {best_lag[1]:.4f}")
    print(f"Shock Alignment Score:    {score:.4f}")
    print("=" * 42)


if __name__ == "__main__":
    execute_lag_scan_analysis()
