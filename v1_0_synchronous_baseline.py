"""
v1: four-window descriptive comparison
Date: August 2026
"""

import math
import numpy as np

# weekly synchronized tracking matrix (2026 observation window)
soccer_errors = {
    "2026-W27": 0.6956,
    "2026-W28": 0.6710,
    "2026-W29": 0.6439,
    "2026-W30": 0.6512
}

# illustrative finance proxy used for the initial descriptive comparison
illustrative_finance_proxy = {
    "2026-W27": 1.2400,
    "2026-W28": 0.9800,
    "2026-W29": 0.5200,
    "2026-W30": 0.5500
}


def compute_pearson_baseline(x_arr, y_arr):
    n = len(x_arr)
    x_mean, y_mean = np.mean(x_arr), np.mean(y_arr)
    cov_sum = np.sum((x_arr - x_mean) * (y_arr - y_mean))
    var_x = np.sum((x_arr - x_mean) ** 2)
    var_y = np.sum((y_arr - y_mean) ** 2)

    if var_x == 0 or var_y == 0 or n <= 1:
        return 0.0, 0.0

    # sample covariance with an n - 1 denominator
    sample_cov = cov_sum / (n - 1)
    return float(cov_sum / math.sqrt(var_x * var_y)), float(sample_cov)


def evaluate_synchronous_alignment():
    weeks = sorted(soccer_errors.keys())
    print("Evaluating descriptive alignment profiles...\n")
    print("Window   | Soccer Brier Error | Illustrative Finance Proxy")
    print("-" * 58)

    soccer, finance = [], []
    for w in weeks:
        soccer.append(soccer_errors[w])
        finance.append(illustrative_finance_proxy[w])
        print(f"{w} |        {soccer_errors[w]:.4f}         |          {illustrative_finance_proxy[w]:.4f}")
    print("-" * 58)

    r_coeff, sample_cov = compute_pearson_baseline(np.array(soccer), np.array(finance))

    print("\n--- Synchronous Baseline Report ---")
    print(f"Observation Windows (N): {len(weeks)}")
    print(f"Sample Covariance:       {sample_cov:.4f}")
    print(f"Descriptive Pearson r (N={len(weeks)}; no inference): {r_coeff:.4f}")
    print("=" * 55)


if __name__ == "__main__":
    evaluate_synchronous_alignment()