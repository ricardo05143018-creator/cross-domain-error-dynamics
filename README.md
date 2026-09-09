# Cross-Domain Error Dynamics

This project started with a simple question from two modeling projects: when models in unrelated domains miss, do their errors move together?

Version 1 made a four-window descriptive comparison. Version 2 replaced that small comparison with a longer synthetic synchronous baseline. Version 3 allowed one series to trail the other. Version 4 moved the comparison from the simulated series themselves to their prediction residuals. Version 5 added an IID permutation baseline at lag 0 while keeping the lag scan descriptive. Version 5.1 adds paired moving-block resampling to examine the stability of the observed correlation and selected lag.

## Current version

### v5.1 – Paired moving-block stability check

Added September 9, 2026.

Version 5.1 focuses on resampling stability. It generates two autocorrelated synthetic series and resamples them using shared moving-block indices. Applying the same sampled indices to both series preserves their pairing while retaining short-range temporal structure within each block.

Two quantities are tracked across the resamples. The first is the synchronous correlation. The second is the lag selected by scanning integer offsets from `-10` through `+10` for the largest absolute correlation.

For the fixed simulation seed:

```text
Observed Synchronous r:  0.0635
Resampled Mean r:        0.0079
Resampled Std Dev:       0.1009

Modal Selected Lag:      -2 windows
Lag Standard Deviation:  5.0792
```

The wide lag distribution indicates that the selected lag is not especially stable in this simulation. Because both series are resampled with the same block indices, the procedure preserves their observed cross-series relationship rather than constructing an independence null.

## Version history

| Version | Added | What changed |
|---|---|---|
| `v1.0` | August 13, 2026 | Compared four weekly soccer Brier-error observations with an illustrative finance proxy. Reported sample covariance `0.0080` and descriptive Pearson correlation `0.9854`. |
| `v2.0` | August 16, 2026 | Moved to 30-observation synthetic series, separate standardization, and overlapping rolling means. The synchronous correlation was `0.0258`. |
| `v3.0` | August 24, 2026 | Added a lag sweep, an injected two-step offset, and one-to-one shock alignment. |
| `v4.0` | August 28, 2026 | Moved the lag scan to standardized prediction residuals and injected opposite-signed shocks with a three-index offset. |
| `v5.0` | September 6, 2026 | Added a lag-0 IID permutation baseline alongside the exploratory lag scan. |
| `v5.1` | September 9, 2026 | Added paired moving-block resampling for synchronous-correlation and selected-lag stability checks. |

## Repository contents

| File | Purpose |
|---|---|
| `v1_0_synchronous_baseline.py` | Runs the original four-window descriptive comparison. |
| `v2_0_synchronous_simulation.py` | Runs the synthetic synchronous rolling-window baseline. |
| `v3_0_lag_scan_simulation.py` | Runs the exploratory lag scan and shock-alignment check. |
| `v4_0_residual_lag_scan.py` | Runs the exploratory lag scan on standardized prediction residuals. |
| `v5_0_iid_permutation_baseline.py` | Adds the lag-0 IID permutation baseline while retaining the exploratory lag scan. |
| `v5_1_paired_block_stability.py` | Runs paired moving-block checks for correlation and lag-selection stability. |
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
```

Later methodological changes will be added as new files so that the earlier baselines remain visible.
