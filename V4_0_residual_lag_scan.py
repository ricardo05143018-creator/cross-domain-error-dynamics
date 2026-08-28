"""
v4: exploratory prediction-residual lag scan
Date: August 2026
"""

import numpy as np


def extract_prediction_residuals(predictions, actuals):
    predictions_array = np.array(predictions, dtype=np.float64)
    actuals_array = np.array(actuals, dtype=np.float64)

    if predictions_array.shape != actuals_array.shape:
        raise ValueError("Predictions and actuals must have the same shape.")

    # prediction residual: actuals - predictions
    return actuals_array - predictions_array


def calc_standardized_z(series):
    data = np.array(series, dtype=np.float64)

    if data.size == 0:
        raise ValueError("The series must not be empty.")

    std_dev = np.std(data)
    if std_dev == 0:
        return np.zeros_like(data)

    return (data - np.mean(data)) / std_dev


def apply_rolling_filter(data, window_size=5):
    array_data = np.array(data, dtype=np.float64)

    if window_size <= 0 or window_size > len(array_data):
        raise ValueError("Window size must be between 1 and the series length.")

    rolled = []
    for i in range(len(array_data) - window_size + 1):
        rolled.append(np.mean(array_data[i:i + window_size]))

    return np.array(rolled, dtype=np.float64)


def scan_lead_lag_structure(series_a, series_b, max_lag=5):
    series_a = np.array(series_a, dtype=np.float64)
    series_b = np.array(series_b, dtype=np.float64)

    if series_a.ndim != 1 or series_b.ndim != 1:
        raise ValueError("Both inputs must be one-dimensional series.")
    if len(series_a) != len(series_b):
        raise ValueError("The two series must have equal length.")
    if max_lag < 0:
        raise ValueError("Maximum lag must be non-negative.")

    lag_profiles = []

    # negative lag means series_b trails series_a
    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            x, y = series_a[:lag], series_b[-lag:]
        elif lag > 0:
            x, y = series_a[lag:], series_b[:-lag]
        else:
            x, y = series_a, series_b

        if len(x) > 2:
            std_x = np.std(x)
            std_y = np.std(y)

            if std_x == 0 or std_y == 0:
                continue

            correlation = float(np.corrcoef(x, y)[0, 1])
            lag_profiles.append((lag, correlation))

    if not lag_profiles:
        raise ValueError("No valid lag correlations could be computed.")

    return max(lag_profiles, key=lambda pair: abs(pair[1]))


def identify_statistical_shocks(series, threshold_z=2.0):
    if threshold_z < 0:
        raise ValueError("The z-score threshold must be non-negative.")

    return np.where(np.abs(series) > threshold_z)[0]


def execute_residual_lag_scan():
    print("Running exploratory prediction-residual lag scan...\n")
    np.random.seed(42)

    s_pred = 0.50 + np.random.normal(0, 0.05, 50)
    s_act = 0.55 + np.random.normal(0, 0.08, 50)

    f_pred = 0.02 + np.random.normal(0, 0.01, 50)
    f_act = 0.01 + np.random.normal(0, 0.05, 50)

    # induce opposite-signed shocks, with finance trailing soccer by three indices
    s_act[12:14] += 0.40
    f_act[15:17] -= 0.20

    s_err = extract_prediction_residuals(s_pred, s_act)
    f_err = extract_prediction_residuals(f_pred, f_act)

    s_norm = calc_standardized_z(s_err)
    f_norm = calc_standardized_z(f_err)

    s_roll = apply_rolling_filter(s_norm)
    f_roll = apply_rolling_filter(f_norm)

    optimal_lag, peak_r = scan_lead_lag_structure(s_roll, f_roll)

    soccer_shocks = identify_statistical_shocks(s_norm, threshold_z=2.0)
    finance_shocks = identify_statistical_shocks(f_norm, threshold_z=2.0)

    print("--- Residual Lag Scan Summary ---")
    print("Note: exploratory lag scan; selection bias is not corrected.")
    print("-" * 58)
    print(f"Rolling Windows per Series: {len(s_roll)}")
    print(f"Selected Lag:               {optimal_lag:+d} windows")
    print(f"Peak Correlation (r):       {peak_r:.4f}")
    print(f"Detected Soccer Shocks:     Indices {soccer_shocks}")
    print(f"Detected Finance Shocks:    Indices {finance_shocks}")
    print("=" * 58)


if __name__ == "__main__":
    execute_residual_lag_scan()
