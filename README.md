# Cross-Domain Error Dynamics

This project began with a question from two modeling projects: when models in unrelated domains miss, do their errors move together?

The early versions build increasingly structured synthetic examples: first a short descriptive comparison, then a longer synchronous baseline, lag scans, and residual-based scans. The later versions turn to inference: whether a correlation or selected lag remains meaningful once temporal dependence is taken seriously.

## Current version

### v6.0 – IID-permutation diagnostic under autocorrelated null data

Added September 14, 2026.

Version 6 tests the IID-permutation baseline from Version 5 under a setting where it should reject rarely: two independently generated AR(1) series. Each pair has 300 observations, an autoregressive coefficient of 0.85, and no cross-series relationship. For each pair, the script scans lags from `-10` to `+10`, records the largest absolute correlation, and assigns an IID-permutation p-value using 199 permutations of one series.

With the fixed seed used in the script, 6 of 12 independent pairs have an IID p-value below 0.05. The largest observed correlations range from `|r| = 0.080` to `|r| = 0.350`, at lags selected by the scan.

The diagnostic shows why the IID baseline needs to be checked separately from the lag scan. Permuting individual observations removes the serial structure of an AR(1) series, so its permutation distribution does not represent the null distribution of an autocorrelated series. This run is a diagnostic rather than an estimate of the rejection rate; the next step is a larger Monte Carlo experiment.

## Version history

| Version | Added | What changed |
|---|---|---|
| `v1.0` | August 13, 2026 | Compared four weekly soccer Brier-error observations with an illustrative finance proxy. Reported sample covariance `0.0080` and descriptive Pearson correlation `0.9854`. |
| `v2.0` | August 16, 2026 | Moved to 30-observation synthetic series, separate standardization, and overlapping rolling means. The synchronous correlation was `0.0258`. |
| `v3.0` | August 24, 2026 | Added a lag sweep, an injected two-step offset, and one-to-one shock alignment. |
| `v4.0` | August 28, 2026 | Moved the lag scan to standardized prediction residuals and injected opposite-signed shocks with a three-index offset. |
| `v5.0` | September 6, 2026 | Added a lag-0 IID permutation baseline alongside the exploratory lag scan. |
| `v5.1` | September 9, 2026 | Added paired moving-block resampling for synchronous-correlation and selected-lag stability checks. |
| `v6.0` | September 14, 2026 | Tests the IID-permutation approach on independent autocorrelated pairs and records how often the lag-scan statistic is declared significant. |

## Repository contents

| File | Purpose |
|---|---|
| `v1_0_synchronous_baseline.py` | Runs the original four-window descriptive comparison. |
| `v2_0_synchronous_simulation.py` | Runs the synthetic synchronous rolling-window baseline. |
| `v3_0_lag_scan_simulation.py` | Runs the exploratory lag scan and shock-alignment check. |
| `v4_0_residual_lag_scan.py` | Runs the exploratory lag scan on standardized prediction residuals. |
| `v5_0_iid_permutation_baseline.py` | Adds the lag-0 IID permutation baseline while retaining the exploratory lag scan. |
| `v5_1_paired_block_stability.py` | Runs paired moving-block checks for correlation and lag-selection stability. |
| `v6_0_false_positive_diagnostic.py` | Runs the IID-permutation diagnostic on independent AR(1) pairs. |
| `requirements.txt` | Lists the Python dependency required by the scripts. |

## Running the scripts

```bash
python -m pip install -r requirements.txt
python v1_0_synchronous_baseline.py
python v2_0_synchronous_simulation.py
python v3_0_lag_scan_simulation.py
python v4_0_residual_lag_scan.py
python v5_0_iid_permutation_baseline.py
python v5_1_paired_block_stability.py
python v6_0_false_positive_diagnostic.py
```

Later methodological changes will be added as new files so that the earlier baselines remain visible.
