# Cross-Domain Error Dynamics

This project started with a simple question from two modeling projects: when models in unrelated domains miss, do their errors move together?

The first version made a four-window descriptive comparison. Version 2 moves to a longer synthetic setting so that the same question can be checked without treating the initial four-point correlation as evidence of a broader relationship.

## Current version

### v2.0 — Synthetic synchronous time-series baseline

Added August 16, 2026.

Version 2:

- generates two 30-observation synthetic series with independent noise;
- injects one shared anomaly at index 12;
- standardizes each series separately;
- applies an overlapping four-observation rolling mean with stride 1; and
- calculates the synchronous Pearson correlation across the resulting 27 windows.

For the fixed simulation seed, the processed correlation is `0.0258`. In this run, the single injected anomaly does not produce strong global synchronous alignment. This remains a descriptive simulation rather than a hypothesis test.

## Version history

| Version | Added | What changed |
| --- | --- | --- |
| `v1.0` | August 13, 2026 | Compared four weekly soccer Brier-error observations with an illustrative finance proxy. Reported sample covariance `0.0080` and descriptive Pearson correlation `0.9854`; no inferential claim. |
| `v2.0` | August 16, 2026 | Replaced the four stored values with 30-observation synthetic series, separate standardization, and overlapping rolling means. |

## Repository contents

| File | Purpose |
| --- | --- |
| `v1_0_synchronous_baseline.py` | Runs the original four-window descriptive comparison. |
| `v2_0_synchronous_simulation.py` | Runs the synthetic synchronous rolling-window simulation. |
| `requirements.txt` | Lists the Python dependency required by both scripts. |

## Running the scripts

```bash
python -m pip install -r requirements.txt
python v1_0_synchronous_baseline.py
python v2_0_synchronous_simulation.py
```

Expected Version 2 summary:

```text
Processed Rolled Windows: 27
Synchronous Baseline r:   0.0258
```

## Interpretation

The high four-window correlation in Version 1 does not persist in the longer synthetic baseline. That contrast is the point of the second version: a visually striking alignment in a very small comparison can disappear once the setup changes. Version 2 still does not estimate a real cross-domain relationship, and its overlapping windows are used only for descriptive exploration.

Later methodological changes will be added as new files so that the earlier baselines remain visible.
