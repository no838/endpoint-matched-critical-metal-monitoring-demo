#!/usr/bin/env python3
"""Build the public-safe quantitative figures used in the demo package.

This script uses only derived demonstration tables stored under ``data/``.
It does not read raw London Metal Exchange files, raw customs downloads, or
restricted third-party datasets.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(exist_ok=True)

plt.rcParams.update(
    {
        "font.family": "DejaVu Serif",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 8.5,
        "figure.dpi": 220,
        "savefig.dpi": 300,
    }
)

COLORS = {
    "exposure": "#355C7D",
    "top5": "#5C9EAD",
    "target": "#C44E52",
    "control": "#5B8E7D",
    "stock": "#7A8DA3",
    "null": "#B9C2D0",
    "threshold": "#2A2A2A",
    "tin": "#A05A2C",
}


def save(fig: plt.Figure, stem: str) -> None:
    for ext in ("png", "pdf", "svg"):
        fig.savefig(OUT_DIR / f"{stem}.{ext}", bbox_inches="tight")
    plt.close(fig)


def build_figure1() -> None:
    exposure = pd.read_csv(DATA_DIR / "figure1_concentration_source_data_20260517.csv")
    top5 = pd.read_csv(DATA_DIR / "figure1_top5_source_profile_20260517.csv")
    exposure = exposure.sort_values("top1_source_share", ascending=False).reset_index(drop=True)
    metals = exposure["metal_label"].tolist()
    x = np.arange(len(metals))

    pivot = (
        top5.assign(share_pct=top5["share_pct"].round(2))
        .pivot(index="sourceDesc", columns="metal_label", values="share_pct")
        .fillna(0)
    )
    row_order = pivot.max(axis=1).sort_values(ascending=False).head(12).index
    pivot = pivot.loc[row_order, metals]

    fig = plt.figure(figsize=(10.8, 5.6))
    gs = GridSpec(1, 2, width_ratios=[1.05, 1.15], wspace=0.3, figure=fig)
    ax1 = fig.add_subplot(gs[0, 0])
    width = 0.34
    ax1.bar(x - width / 2, exposure["top1_source_share"] * 100, width=width, color=COLORS["exposure"], label="Top-1 source share")
    ax1.bar(x + width / 2, exposure["top5_source_share"] * 100, width=width, color=COLORS["top5"], label="Top-5 source share")
    ax1.set_xticks(x)
    ax1.set_xticklabels(metals, rotation=25, ha="right")
    ax1.set_ylabel("Share of import-source value (%)")
    ax1.set_title("a  Source concentration differs sharply across metals", loc="left")
    ax1.grid(axis="y", alpha=0.18, linewidth=0.6)
    ax1.legend(frameon=False, loc="upper left")

    ax2 = fig.add_subplot(gs[0, 1])
    im = ax2.imshow(pivot.values, cmap="Blues", aspect="auto", vmin=0, vmax=max(10, pivot.values.max()))
    ax2.set_xticks(np.arange(len(metals)))
    ax2.set_xticklabels(metals, rotation=25, ha="right")
    ax2.set_yticks(np.arange(len(pivot.index)))
    ax2.set_yticklabels(pivot.index)
    ax2.set_title("b  Top-source composition is metal-specific", loc="left")
    cbar = fig.colorbar(im, ax=ax2, fraction=0.046, pad=0.04)
    cbar.set_label("Source share (%)")
    save(fig, "Figure_1_Global_trade_exposure_demo")


def build_figure2() -> None:
    bridge = pd.read_csv(DATA_DIR / "trade_exposure_to_lme_endpoint_bridge_20260517.csv")
    bench = pd.read_csv(DATA_DIR / "figure2_benchmark_panel_source_20260517.csv")
    if "metal_label" not in bridge.columns:
        bridge["metal_label"] = bridge["metal"].str.title()

    fig = plt.figure(figsize=(10.8, 5.4))
    gs = GridSpec(1, 2, width_ratios=[1.05, 0.95], wspace=0.32, figure=fig)

    ax1 = fig.add_subplot(gs[0, 0])
    for _, row in bridge.iterrows():
        is_target = row["lme_deliverability_status"] == "direct_endpoint_positive"
        color = COLORS["target"] if is_target else COLORS["control"]
        ax1.scatter(
            row["russia_source_share_import"] * 100,
            row["lme_direct_russian_share_max"] * 100,
            s=85,
            color=color,
            edgecolor="black",
            linewidth=0.4,
        )
        ax1.text(row["russia_source_share_import"] * 100 + 0.25, row["lme_direct_russian_share_max"] * 100 + 0.35, row["metal_label"], fontsize=8.5)
    ax1.axvline(5.0, color="#9A9A9A", linestyle="--", linewidth=0.9)
    ax1.set_xlabel("Russia source share in global trade exposure (%)")
    ax1.set_ylabel("Maximum LME Russian-origin share (%)")
    ax1.set_title("a  Trade exposure and deliverability are distinct layers", loc="left")
    ax1.grid(alpha=0.18, linewidth=0.6)

    ax2 = fig.add_subplot(gs[0, 1])
    bench = bench.copy()
    bench["type"] = np.where(bench["benchmark"].str.contains("Aggregate"), "Generic stock", "Matched deliverability")
    y = np.arange(len(bench))[::-1]
    colors = [COLORS["target"] if t == "Matched deliverability" else COLORS["stock"] for t in bench["type"]]
    ax2.barh(y, bench["auc"], color=colors, height=0.62)
    ax2.set_yticks(y)
    ax2.set_yticklabels(bench["benchmark"])
    ax2.set_xlim(0, 1.05)
    ax2.set_xlabel("AUC in locked nine-label benchmark universe")
    ax2.set_title("b  Matched deliverability defeats generic stock screens", loc="left")
    ax2.grid(axis="x", alpha=0.18, linewidth=0.6)
    save(fig, "Figure_2_Exposure_vs_LME_deliverability_demo")


def build_figure3() -> None:
    null_df = pd.read_csv(DATA_DIR / "lme_exact_label_null_auc_20260515.csv")
    bench = pd.read_csv(DATA_DIR / "figure2_benchmark_panel_source_20260517.csv")
    cash = pd.read_csv(DATA_DIR / "event_window_results_with_bh_q_20260517.csv")
    premium = pd.read_csv(DATA_DIR / "lme_aluminium_premium_event_window_tests_20260516.csv")
    tin = pd.read_csv(DATA_DIR / "tin_rkab_source_closure_event_panel_20260517.csv")
    tin["month_date"] = pd.to_datetime(tin["month_date"])

    cash = cash.copy()
    cash["window_label"] = cash["pre_n"].astype(int).astype(str) + "d"
    q_summary = cash.groupby("window_label", as_index=False)["bh_q_18_tests"].min()
    premium_summary = (
        premium.assign(window_label=premium["pre_n_trading_days"].astype(int).astype(str) + "d")
        .groupby("window_label", as_index=False)["empirical_two_sided_p"]
        .min()
        .rename(columns={"empirical_two_sided_p": "min_p"})
    )

    fig = plt.figure(figsize=(11.2, 8.4))
    gs = GridSpec(2, 2, wspace=0.28, hspace=0.34, figure=fig)

    ax1 = fig.add_subplot(gs[0, 0])
    vals = null_df.loc[null_df["benchmark"] == "origin_endpoint_annual_mean_share", "null_auc"]
    ax1.hist(vals, bins=np.linspace(0.15, 0.85, 15), color=COLORS["null"], edgecolor="white")
    ax1.axvline(1.0, color=COLORS["target"], linewidth=1.4)
    ax1.set_xlim(0.1, 1.02)
    ax1.set_xlabel("AUC under exact target-label permutation")
    ax1.set_ylabel("Assignments")
    ax1.set_title("a  Exact permutation null", loc="left")

    ax2 = fig.add_subplot(gs[0, 1])
    plot_bench = bench.iloc[[0, 3]].copy()
    plot_bench["label"] = ["Matched origin/warrant endpoint", "Generic aggregate-stock benchmark"]
    ax2.bar(plot_bench["label"], plot_bench["auc"], color=[COLORS["target"], COLORS["stock"]], width=0.58)
    ax2.set_ylim(0, 1.08)
    ax2.set_ylabel("Observed AUC")
    ax2.set_title("b  Benchmark AUC separation", loc="left")
    ax2.tick_params(axis="x", labelrotation=12)

    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(q_summary["window_label"], q_summary["bh_q_18_tests"], marker="o", color=COLORS["target"], label="Minimum Cash-3M BH q")
    ax3.axhline(0.05, color=COLORS["threshold"], linestyle="--", linewidth=0.9, label="0.05 reference")
    ax3.scatter(premium_summary["window_label"], premium_summary["min_p"], color=COLORS["stock"], marker="D", s=42, label="Minimum aluminium premium p")
    ax3.set_ylabel("q or p value")
    ax3.set_ylim(0, 1.02)
    ax3.set_title("c  Market-impact boundary evidence", loc="left")
    ax3.legend(frameon=False, loc="upper left")

    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(tin["month_date"], tin["hs8001_primary_tonnes"], color=COLORS["tin"], marker="o", linewidth=1.8)
    ax4.axvspan(pd.Timestamp("2024-01-01"), pd.Timestamp("2024-02-29"), color=COLORS["target"], alpha=0.08)
    ax4.axvspan(pd.Timestamp("2024-03-01"), pd.Timestamp("2024-04-30"), color=COLORS["top5"], alpha=0.08)
    ax4.set_ylabel("HS8001 export tonnage")
    ax4.set_title("d  Indonesia tin trade-gate endpoint", loc="left")
    ax4.tick_params(axis="x", rotation=25)
    save(fig, "Figure_3_Endpoint_matched_quantitative_evidence_demo")


def main() -> None:
    build_figure1()
    build_figure2()
    build_figure3()
    print(f"[OK] wrote outputs to {OUT_DIR}")


if __name__ == "__main__":
    main()
