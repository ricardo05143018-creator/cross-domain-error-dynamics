# Cross-Domain Error Dynamics

This project started with a simple question from two modeling projects: when models in unrelated domains miss, do their errors move together?

Version 1 made a four-window descriptive comparison. Version 2 replaced that small comparison with a longer synthetic synchronous baseline. Version 3 allowed one series to trail the other. Version 4 moved the comparison from the simulated series themselves to their prediction residuals. Version 5 added a naive IID permutation baseline at lag 0 while keeping the lag scan descriptive.

## Current version

### v5.0 – Naive IID permutation baseline

Added September 6, 2026.

Version 5 keeps the prediction-residual setup from Version 4. It generates predicted and actual series for both domains, forms the two residual series, applies a five-observation rolling mean, and scans integer lags from `-10` through `+10` for the largest absolute correlation.

The fixed simulation does not inject a shared cross-domain shock. The lag scan remains exploratory, while a two-sided IID permutation test is added separately at lag 0 by repeatedly shuffling one rolled series.

For the fixed simulation seed:

```text
Optimal Scanned Lag:       +10 windows (r = -0.4349)

Synchronous Observed r:    -0.0197
Permutation Null Mean (r): 0.0030
Permutation Null Std Dev:  0.1350
Synchronous Two-Sided p:   0.8603
```

The permutation p-value applies only to the synchronous lag-0 correlation, not to the selected peak from the lag scan. Because the five-observation rolling windows overlap, the rolled observations are not exchangeable. The IID permutation test is therefore kept as a naive baseline rather than treated as valid final inference.

## Version history

| Version | Added | What changed |
| --- | --- | --- |
| `v1.0` | August 13, 2026 | Compared four weekly soccer Brier-error observations with an illustrative finance proxy. Reported sample covariance `0.0080` and descriptive Pearson correlation `0.9854`. |
| `v2.0` | August 16, 2026 | Moved to 30-observation synthetic series, separate standardization, and overlapping rolling means. The synchronous correlation was `0.0258`. |
| `v3.0` | August 24, 2026 | Added a lag sweep, an injected two-step offset, and one-to-one shock alignment. |
| `v4.0` | August 28, 2026 | Moved the lag scan to standardized prediction residuals and injected opposite-signed shocks with a three-index offset. |
| `v5.0` | September 6, 2026 | Added a naive IID permutation baseline at lag 0 while leaving the lag scan exploratory and making the exchangeability limitation explicit. |

## Repository contents

| File | Purpose |
| --- | --- |
| `v1_0_synchronous_baseline.py` | Runs the original four-window descriptive comparison. |
| `v2_0_synchronous_simulation.py` | Runs the synthetic synchronous rolling-window baseline. |
| `v3_0_lag_scan_simulation.py` | Runs the exploratory lag scan and shock-alignment check. |
| `v4_0_residual_lag_scan.py` | Runs the exploratory lag scan on standardized prediction residuals. |
| `v5_0_iid_permutation_baseline.py` | Adds the naive lag-0 IID permutation baseline while retaining the exploratory lag scan. |
| `requirements.txt` | Lists the Python dependency required by the scripts. |

## Running the scripts

```bash
python -m pip install -r requirements.txt
python v1_0_synchronous_baseline.py
python v2_0_synchronous_simulation.py
python v3_0_lag_scan_simulation.py
python v4_0_residual_lag_scan.py
python v5_0_iid_permutation_baseline.py
```

Later methodological changes will be added as new files so that the earlier baselines remain visible.
