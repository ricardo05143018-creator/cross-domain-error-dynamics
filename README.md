# Cross-Domain Error Dynamics

This project started with a simple question from two modeling projects: when models in unrelated domains miss, do their errors move together?

Version 1 is only a first check. It compares four weekly soccer Brier-error observations with an illustrative finance proxy and reports their synchronous covariance and correlation. The proxy is constructed rather than drawn from an empirical market dataset, so this release is a descriptive baseline rather than evidence of a general relationship.

## Current release

### v1.0 — Four-window descriptive baseline

Initial public release: August 13, 2026

The baseline:

- aligns four weekly windows from 2026-W27 through 2026-W30;
- calculates sample covariance using an `n - 1` denominator;
- calculates the Pearson correlation across the aligned windows; and
- makes no hypothesis test, causal claim, or population-level inference.

With only four observations and an illustrative comparison series, the result is a starting observation rather than evidence of general cross-domain dependence.

## Repository contents

| File | Purpose |
| --- | --- |
| `v1_0_synchronous_baseline.py` | Runs the four-window comparison and prints the descriptive results. |
| `requirements.txt` | Lists the Python dependency required to run the script. |

## Running the baseline

```bash
python -m pip install -r requirements.txt
python v1_0_synchronous_baseline.py
```

Expected summary:

```text
Observation Windows (N): 4
Sample Covariance:       0.0080
Descriptive Pearson r (N=4; no inference): 0.9854
```

## Interpretation

The large descriptive correlation describes these four aligned values only. It should not be read as a validated relationship between soccer forecasting error and financial risk. I will add later methodological changes as new versions and keep the earlier releases visible.
