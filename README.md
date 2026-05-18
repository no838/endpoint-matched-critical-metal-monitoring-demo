# Endpoint-Matched Monitoring Demo

This repository is a minimal, public-safe demonstration package for the manuscript:

**Endpoint-matched monitoring of exchange and administrative shocks in critical-metal supply chains**

The package reproduces the schematic endpoint-matched monitoring figure and provides the small derived tables used to explain the claim-control logic. It is intentionally not a raw-data repository and does not redistribute raw London Metal Exchange records or third-party licensed data.

## Contents

```text
data/
  figure3_policy_framework_table_20260517.csv
  figure3_evidence_status_20260517.csv
  spc_case_selection_event_universe_20260517.csv
scripts/
  build_figure3.py
outputs/
  Figure_3_Endpoint_matched_policy_framework_20260517.svg
```

## What This Demo Shows

The demo separates:

- structural exposure screens;
- physical, administrative or exchange-rule gates;
- observable endpoint families;
- allowed claim ceilings;
- production or procurement actions.

The key principle is:

> Exposure identifies where a shock may matter; endpoint-matched evidence determines what can be claimed.

## Rebuild Figure 3

Create an environment with Python 3, `pandas` and `matplotlib`, then run:

```bash
python scripts/build_figure3.py
```

The script writes PNG, PDF and SVG files into `outputs/`.

## Data Boundary

The CSV files are derived demonstration tables prepared for the schematic and case-selection audit. They should not be interpreted as the complete empirical dataset for the manuscript.

Not included:

- raw LME warehouse, warrant or price files;
- raw customs downloads;
- restricted third-party source data;
- author metadata or manuscript submission forms.

Included:

- derived schematic table for the endpoint-matched monitoring workflow;
- derived evidence-status table for the claim ceiling;
- case-selection and event-universe audit table.

## License

No open-source license has been assigned yet. Until the authors choose a license, all rights are reserved.

