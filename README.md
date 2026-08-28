# Cross-Domain Error Dynamics

This project started with a simple question from two modeling projects: when models in unrelated domains miss, do their errors move together?

Version 1 made a four-window descriptive comparison. Version 2 replaced that small comparison with a longer synthetic synchronous baseline. Version 3 allowed one series to trail the other. Version 4 moves the comparison from the simulated series themselves to their prediction residuals.

## Current version

### v4.0 — Prediction-residual lag scan

Added August 28, 2026.

Version 4 generates predicted and actual series for both domains, then defines each residual as `actual - prediction`. It standardizes the two residual series separately, applies a five-observation rolling mean, and scans integer lags from `-5` through `+5` for the largest absolute correlation.

The simulation injects positive soccer residual shocks at indices 12–13 and negative finance residual shocks at 15–16. Under the convention used here, a negative lag means the finance series trails the soccer series. Because the injected shocks point in opposite directions, their aligned correlation is expected to be negative.

For the fixed simulation seed:

```text
Rolling Windows per Series: 46
Selected Lag:               -3 windows
Peak Correlation (r):       -0.6988
Detected Soccer Shocks:     Indices [12 13 24]
Detected Finance Shocks:    Indices [15 16 29]
```

The threshold detects the four injected shocks as well as background extremes at indices 24 and 29. These extra detections are left visible rather than treated as injected events. As in Version 3, the lag scan is exploratory: searching several lags and reporting the largest correlation introduces selection bias, so Version 4 does not attach a p-value or make an inferential claim.

## Version history

| Version | Added | What changed |
| --- | --- | --- |
| `v1.0` | August 13, 2026 | Compared four weekly soccer Brier-error observations with an illustrative finance proxy. Reported sample covariance `0.0080` and descriptive Pearson correlation `0.9854`. |
| `v2.0` | August 16, 2026 | Moved to 30-observation synthetic series, separate standardization, and overlapping rolling means. The synchronous correlation was `0.0258`. |
| `v3.0` | August 24, 2026 | Added a lag sweep, an injected two-step offset, and one-to-one shock alignment. |
| `v4.0` | August 28, 2026 | Moved the lag scan to standardized prediction residuals and injected opposite-signed shocks with a three-index offset. |

## Repository contents

| File | Purpose |
| --- | --- |
| `v1_0_synchronous_baseline.py` | Runs the original four-window descriptive comparison. |
| `v2_0_synchronous_simulation.py` | Runs the synthetic synchronous rolling-window baseline. |
| `v3_0_lag_scan_simulation.py` | Runs the exploratory lag scan and shock-alignment check. |
| `v4_0_residual_lag_scan.py` | Runs the exploratory lag scan on standardized prediction residuals. |
| `requirements.txt` | Lists the Python dependency required by the scripts. |

## Running the scripts

```bash
python -m pip install -r requirements.txt
python v1_0_synchronous_baseline.py
python v2_0_synchronous_simulation.py
python v3_0_lag_scan_simulation.py
python v4_0_residual_lag_scan.py
```

Later methodological changes will be added as new files so that the earlier baselines remain visible.
