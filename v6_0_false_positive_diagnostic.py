"""
v6: IID-permutation diagnostic under autocorrelated null data
Date: September 2026
"""

import numpy as np


def generate_ar1(n=300, phi=0.85, burn_in=500, rng=None):
    if rng is None:
        rng = np.random.default_rng()

    series = [rng.normal(0, 1.0)]
    for _ in range(n + burn_in - 1):
        series.append(phi * series[-1] + rng.normal(0, 1.0))

    return np.array(series[burn_in:], dtype=np.float64)


def scan_max_abs_correlation(a, b, max_lag=10):
    best_lag = 0
    best_corr = 0.0
    best_abs = -1.0

    for lag in range(-max_lag, max_lag + 1):
        if lag < 0:
            aa, bb = a[:lag], b[-lag:]
        elif lag > 0:
            aa, bb = a[lag:], b[:-lag]
        else:
            aa, bb = a, b

        corr = np.corrcoef(aa, bb)[0, 1]

        if abs(corr) > best_abs:
            best_abs = abs(corr)
            best_corr = corr
            best_lag = lag

    return best_lag, best_corr, best_abs


def iid_permutation_p_value(a, b, max_lag=10, n_permutations=199, rng=None):
    if rng is None:
        rng = np.random.default_rng()

    _, _, observed_max = scan_max_abs_correlation(a, b, max_lag)
    null_maxima = []

    # Use naive IID permutation as a baseline under autocorrelated data
    for _ in range(n_permutations):
        _, _, null_max = scan_max_abs_correlation(
            a, rng.permutation(b), max_lag
        )
        null_maxima.append(null_max)

    null_maxima = np.array(null_maxima)
    return (1 + np.sum(null_maxima >= observed_max)) / (n_permutations + 1)


def run_diagnostic():
    rng = np.random.default_rng(2026)

    n_pairs = 12
    alpha = 0.05
    rejections = 0

    print("naive IID-permutation diagnostic for independent AR(1) pairs\n")

    for pair_id in range(1, n_pairs + 1):
        a = generate_ar1(rng=rng)
        b = generate_ar1(rng=rng)

        lag, corr, _ = scan_max_abs_correlation(a, b)
        p_value = iid_permutation_p_value(a, b, rng=rng)

        if p_value < alpha:
            rejections += 1

        print(
            f"Pair {pair_id:02d}: "
            f"max r = {corr:+.3f} at lag {lag:+d}, "
            f"IID p = {p_value:.3f}"
        )

    print("\n" + "-" * 60)
    print(f"Naive IID rejections: {rejections}/{n_pairs}")
    print(
        "This is a small diagnostic, not a calibrated size estimate. "
        "The next version repeats the check over a larger Monte Carlo run."
    )


if __name__ == "__main__":
    run_diagnostic()