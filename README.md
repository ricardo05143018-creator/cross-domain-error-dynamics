# Cross-Domain Error Dynamics

This project began with a question from two modeling projects: when models in unrelated domains miss, do their errors move together?

The first versions explored that question with synthetic examples, starting with synchronous comparisons and then moving to lag scans and residual-based tests. The later versions focused on inference: whether an observed correlation or selected lag still means anything when the series are temporally dependent.

## Project status

**Complete — September 19, 2026.**

Version 7 is the final version of this project. Earlier versions are kept in the repository to show how the analysis changed over time.

## Related Research Paper

This project is closely connected to my independent research paper, *Correcting Selection Bias in Lag-Optimized Time Series Dependence Tests*, which examines statistical inference after lag selection under serial dependence.

- [Read the Paper (PDF)](https://github.com/ricardo05143018-creator/lag-optimized-time-series-tests/blob/main/paper/Lag_Optimized_Time_Series_Tests.pdf)
- [Paper & Reproducibility Code](https://github.com/ricardo05143018-creator/lag-optimized-time-series-tests)

## Final version

### v7.0 – Monte Carlo Type-I error check for IID-permutation lag scans

Added September 19, 2026.

Version 7 extends the autocorrelated-null diagnostic from Version 6 into a Monte Carlo experiment. Each trial generates two independent AR(1) series with 300 observations and an autoregressive coefficient of 0.85, so there is no cross-series relationship but substantial serial dependence within each series.

For each pair, the script scans lags from `-10` to `+10` and records the largest absolute correlation. The IID-permutation null repeats the same lag scan after randomly permuting one series, so the permutation statistic incorporates the lag-selection step while failing to preserve serial dependence.

With the fixed seeds used in the script, the illustrative independent pair produces a maximum scanned correlation of `r = -0.2252` at lag `-2` and an IID max-scan permutation p-value of `0.0020`.

The Monte Carlo experiment then repeats the procedure for 100 independently generated AR(1) pairs, using 200 permutations per trial. The IID-permutation test rejects 69 of the 100 true-null trials at `alpha = 0.05`, giving an empirical Type-I error rate of `0.690` with a Monte Carlo standard error of `0.0462`.

Repeating the lag scan inside each permutation accounts for selection over the scanned lags. It does not solve the second problem: IID permutation destroys the serial dependence in the original series. Under this autocorrelated null, the resulting test is therefore badly miscalibrated.

This is where the project ends: the lag-selection issue is included in the null procedure, but the IID assumption still fails under serial dependence.

## Version history

| Version | Added              | What changed                                                                                                                                                               |
| ------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `v1.0`  | August 13, 2026    | Compared four weekly soccer Brier-error observations with an illustrative finance proxy. Reported sample covariance `0.0080` and descriptive Pearson correlation `0.9854`. |
| `v2.0`  | August 16, 2026    | Moved to 30-observation synthetic series, separate standardization, and overlapping rolling means. The synchronous correlation was `0.0258`.                               |
| `v3.0`  | August 24, 2026    | Added a lag sweep, an injected two-step offset, and one-to-one shock alignment.                                                                                            |
| `v4.0`  | August 28, 2026    | Moved the lag scan to standardized prediction residuals and injected opposite-signed shocks with a three-index offset.                                                     |
| `v5.0`  | September 6, 2026  | Added a lag-0 IID permutation baseline alongside the exploratory lag scan.                                                                                                 |
| `v5.1`  | September 9, 2026  | Added paired moving-block resampling for synchronous-correlation and selected-lag stability checks.                                                                        |
| `v6.0`  | September 14, 2026 | Tested the IID-permutation approach on independent autocorrelated pairs and showed that it can produce small p-values under a true null.                                   |
| `v7.0`  | September 19, 2026 | Extended the autocorrelated-null diagnostic to a Monte Carlo Type-I error experiment while repeating the full lag scan inside each permutation.                            |

## Repository contents

| File                                | Purpose                                                                                     |
| ----------------------------------- | ------------------------------------------------------------------------------------------- |
| `v1_0_synchronous_baseline.py`      | Runs the original four-window descriptive comparison.                                       |
| `v2_0_synchronous_simulation.py`    | Runs the synthetic synchronous rolling-window baseline.                                     |
| `v3_0_lag_scan_simulation.py`       | Runs the exploratory lag scan and shock-alignment check.                                    |
| `v4_0_residual_lag_scan.py`         | Runs the exploratory lag scan on standardized prediction residuals.                         |
| `v5_0_iid_permutation_baseline.py`  | Adds the lag-0 IID permutation baseline while retaining the exploratory lag scan.           |
| `v5_1_paired_block_stability.py`    | Runs paired moving-block checks for correlation and lag-selection stability.                |
| `v6_0_false_positive_diagnostic.py` | Runs the initial IID-permutation diagnostic on independent AR(1) pairs.                     |
| `v7_0_lag_selection_simulation.py`  | Estimates the Type-I error of an IID-permutation max-lag test under an autocorrelated null. |
| `requirements.txt`                  | Lists the Python dependency required by the scripts.                                        |

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
python v7_0_lag_selection_simulation.py
```
