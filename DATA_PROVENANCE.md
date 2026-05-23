# Data Provenance

Generated: 2026-05-23

This demo package contains only derived demonstration tables copied from the local SPC submission workspace. The files were selected because they reproduce the quantitative public-safe figures without redistributing raw or restricted records.

## Included Files

| File | Role | Redistribution boundary |
|---|---|---|
| `data/figure1_concentration_source_data_20260517.csv` | Six-metal exposure summary | Derived exposure table |
| `data/figure1_top5_source_profile_20260517.csv` | Top-source profile by metal | Derived exposure table |
| `data/trade_exposure_to_lme_endpoint_bridge_20260517.csv` | Exposure-to-deliverability bridge | Derived bridge table |
| `data/figure2_benchmark_panel_source_20260517.csv` | LME benchmark AUC summary | Derived benchmark table |
| `data/lme_exact_label_null_auc_20260515.csv` | Exact permutation null AUC draws | Derived null table |
| `data/event_window_results_with_bh_q_20260517.csv` | Cash-3M event-window q values | Derived event-window table |
| `data/lme_aluminium_premium_event_window_tests_20260516.csv` | Aluminium premium boundary tests | Derived event-window table |
| `data/tin_rkab_source_closure_event_panel_20260517.csv` | Indonesia tin monthly endpoint panel | Derived endpoint table |
| `scripts/build_quantitative_figures.py` | Public-safe figure builder | Reads only included derived CSV files |

## Excluded Files

The following inputs are deliberately excluded from this public-safe demo:

- raw London Metal Exchange data;
- raw customs or trade downloads;
- restricted third-party data;
- manuscript DOCX files;
- declarations, title pages, or submission forms;
- local path inventories or other machine-specific records.

## Claim Boundary

These demo files support only the bounded monitoring logic shown in the manuscript:

> endpoint families should be matched to shock channels before escalating a critical-metal supply-chain statement.

They do not support a universal predictive risk score, broad causal price transmission claim, or permit-level administrative causality claim.
