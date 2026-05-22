# Endpoint-Matched Critical-Metal Monitoring Demo

This repository is a minimal, public-safe demonstration package for the manuscript:

**Endpoint-matched monitoring of exchange and administrative shocks in critical-metal supply chains**

The package reproduces quantitative demonstration figures from derived, non-restricted tables. It is intentionally not a raw-data repository and does not redistribute raw London Metal Exchange records, raw customs downloads, or other third-party licensed data.

## Contents

```text
data/
  figure1_concentration_source_data_20260517.csv
  figure1_top5_source_profile_20260517.csv
  trade_exposure_to_lme_endpoint_bridge_20260517.csv
  figure2_benchmark_panel_source_20260517.csv
  lme_exact_label_null_auc_20260515.csv
  event_window_results_with_bh_q_20260517.csv
  lme_aluminium_premium_event_window_tests_20260516.csv
  tin_rkab_source_closure_event_panel_20260517.csv
scripts/
  build_quantitative_figures.py
outputs/
  Figure_1_Global_trade_exposure_demo.{png,pdf,svg}
  Figure_2_Exposure_vs_LME_deliverability_demo.{png,pdf,svg}
  Figure_3_Endpoint_matched_quantitative_evidence_demo.{png,pdf,svg}
```

## What This Demo Shows

The demo keeps the manuscript's evidence boundary intact:

- structural exposure screens identify candidate vulnerability;
- deliverability endpoints monitor exchange-rule shocks;
- spread and premium tests set the market-impact boundary;
- tin export tonnage supplies a bounded non-exchange trade-gate endpoint.

The governing principle is:

> Exposure identifies where a shock may matter; endpoint-matched evidence determines what can be claimed.

## Rebuild The Figures

Create an environment with Python 3, `pandas`, and `matplotlib`, then run:

```bash
python scripts/build_quantitative_figures.py
```

The script writes PNG, PDF, and SVG files into `outputs/`.

## Data Boundary

The CSV files are derived demonstration tables prepared for the quantitative figures. They should not be interpreted as the complete empirical dataset for the manuscript.

Not included:

- raw LME warehouse, warrant, off-warrant, or price files;
- raw customs downloads;
- restricted third-party source data;
- manuscript DOCX files, declarations, or submission forms.

Included:

- six-metal derived exposure summaries;
- derived LME benchmark tables;
- derived Cash-3M and aluminium premium limit tables;
- derived Indonesia tin monthly event panel.

## License

No open-source license has been assigned yet. Until the authors choose a license, all rights are reserved.
