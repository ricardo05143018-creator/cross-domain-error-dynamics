"""
v2: synthetic synchronous time-series baseline
Date: August 2026
"""

import math
import numpy as np


def calc_standardized_z(series):
    array_data = np.array(series, dtype=np.float64)
    std_dev = np.std(array_data)
    if std_dev == 0:
        return np.zeros_like(array_data)
    return (array_data - np.mean(array_data)) / std_dev

def apply_rolling_mean_filter(data_stream, window_size=4, stride=1):
    if window_size <= 0 or window_size > len(data_stream):
        raise ValueError("Window size must be between 1 and the series length.")
    if stride <= 0:
        raise ValueError("Stride must be strictly positive.")

    rolled_series = []
    pointer = 0
    while pointer + window_size <= len(data_stream):
        window_chunk = data_stream[pointer: pointer + window_size]
        rolled_series.append(np.mean(window_chunk))
        pointer += stride
    return np.array(rolled_series, dtype=np.float64)


def compute_synchronous_corr(series_a, series_b):
    mean_a = np.mean(series_a)
    mean_b = np.mean(series_b)

    covariance = np.sum((series_a - mean_a) * (series_b - mean_b))
    var_a = np.sum((series_a - mean_a) ** 2)
    var_b = np.sum((series_b - mean_b) ** 2)

    if var_a == 0 or var_b == 0:
        return 0.0
    return float(covariance / math.sqrt(var_a * var_b))


def execute_alignment_baseline():
    print("Running synchronous simulation...\n")

    # generate synthetic series with a shared anomaly at index 12
    np.random.seed(101)
    raw_soccer = 0.64 + np.random.normal(0, 0.05, 30)
    raw_finance = 0.50 + np.random.normal(0, 0.25, 30)

    raw_soccer[12] += 0.15
    raw_finance[12] += 0.80

    # transform raw inputs into standardized risk profiles
    z_soccer = calc_standardized_z(raw_soccer)
    z_finance = calc_standardized_z(raw_finance)

    smooth_soccer = apply_rolling_mean_filter(z_soccer, window_size=4)
    smooth_finance = apply_rolling_mean_filter(z_finance, window_size=4)

    r_val = compute_synchronous_corr(smooth_soccer, smooth_finance)

    print("--- Synchronous Simulation Results ---")
    print(f"Processed Rolled Windows: {len(smooth_soccer)}")
    print(f"Synchronous Baseline r:   {r_val:.4f}")
    print("-" * 42)
    print("Observation: In this run, one shared anomaly does not produce strong correlation after smoothing.")
    print("=" * 42)


if __name__ == "__main__":
    execute_alignment_baseline()