# Cross-Domain Error Dynamics

This project started with a simple question from two modeling projects: when models in unrelated domains miss, do their errors move together?

Version 1 made a four-window descriptive comparison. Version 2 replaced that small comparison with a longer synthetic synchronous baseline. Version 3 asks a different question: can an alignment become clearer after allowing one series to trail the other?

## Current version

### v3.0 — Exploratory lag scan and shock alignment

Added August 24, 2026.

Version 3 generates two 50-observation synthetic series and injects two-step-offset shocks: the first series at indices 12–13 and the second at 14–15. After separate standardization and a four-observation rolling mean, it scans integer lags from `-5` through `+5` and selects the largest absolute correlation.

Under the convention used here, a negative lag means the second series trails the first. The script also identifies unsmoothed observations beyond two standard deviations and matches shocks one-to-one within a tolerance of two indices.

For the fixed simulation seed:

```text
Base Correlation (Lag 0): 0.1278
Selected Lag:             -2 windows
Peak Scanned Correlation: 0.7339
Shock Alignment Score:    1.0000
```

The injected offset is recovered, but the lag scan is exploratory. Searching several lags and then reporting the largest correlation introduces selection bias, so Version 3 does not attach a p-value or make an inferential claim.

## Version history

| Version | Added | What changed |
| --- | --- | --- |
| `v1.0` | August 13, 2026 | Compared four weekly soccer Brier-error observations with an illustrative finance proxy. Reported sample covariance `0.0080` and descriptive Pearson correlation `0.9854`. |
| `v2.0` | August 16, 2026 | Moved to 30-observation synthetic series, separate standardization, and overlapping rolling means. The synchronous correlation was `0.0258`. |
| `v3.0` | August 24, 2026 | Added a lag sweep, an injected two-step offset, and one-to-one shock alignment. |

## Repository contents

| File | Purpose |
| --- | --- |
| `v1_0_synchronous_baseline.py` | Runs the original four-window descriptive comparison. |
| `v2_0_synchronous_simulation.py` | Runs the synthetic synchronous rolling-window baseline. |
| `v3_0_lag_scan_simulation.py` | Runs the exploratory lag scan and shock-alignment check. |
| `requirements.txt` | Lists the Python dependency required by the scripts. |

## Running the scripts

```bash
python -m pip install -r requirements.txt
python v1_0_synchronous_baseline.py
python v2_0_synchronous_simulation.py
python v3_0_lag_scan_simulation.py
```

Later methodological changes will be added as new files so that the earlier baselines remain visible.
