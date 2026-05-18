#!/usr/bin/env python3
"""Rebuild the endpoint-matched monitoring schematic from demo CSV files.

This script intentionally uses only derived, non-restricted demonstration
tables. It does not read raw LME records, raw customs downloads or manuscript
workbooks.
"""

from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import pandas as pd


STATUS_COLORS = {
    "supported": "#2a9d8f",
    "ready_with_boundary": "#74a57f",
    "boundary_null": "#e9c46a",
    "blocked": "#b56576",
    "framework": "#5b8def",
}

STATUS_LABELS = {
    "supported": "supported",
    "ready_with_boundary": "ready\nboundary",
    "boundary_null": "boundary\nnull",
    "blocked": "blocked",
    "framework": "framework",
}


def wrap(text: object, width: int = 26) -> str:
    return "\n".join(textwrap.wrap(str(text), width=width, break_long_words=False))


def read_csv(path: Path, required: set[str]) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path)
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{path.name} missing required columns: {missing}")
    return df


def draw_box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str,
    facecolor: str,
    edgecolor: str = "#4f5b66",
    fontsize: float = 8.5,
    weight: str = "normal",
) -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.018,rounding_size=0.018",
        linewidth=0.8,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        fontweight=weight,
        color="#1f2933",
    )


def plot_figure(framework: pd.DataFrame, evidence: pd.DataFrame, out_dir: Path, stem: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.titleweight": "bold",
            "axes.edgecolor": "#2b2b2b",
            "axes.linewidth": 0.8,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
        }
    )

    fig = plt.figure(figsize=(13.2, 8.6), constrained_layout=False)
    gs = fig.add_gridspec(nrows=2, ncols=1, height_ratios=[1.45, 1.0], hspace=0.22)

    ax1 = fig.add_subplot(gs[0])
    ax1.axis("off")
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.text(
        0.0,
        1.04,
        "a  Endpoint-matched monitoring workflow",
        fontsize=12,
        fontweight="bold",
        ha="left",
        va="bottom",
    )

    cols = [
        ("risk_question", "Risk question", 0.0, 0.19),
        ("shock_or_gate", "Shock or gate", 0.2, 0.23),
        ("observable_endpoint", "Observable endpoint", 0.44, 0.23),
        ("allowed_claim", "Allowed claim", 0.68, 0.16),
        ("policy_use", "Production action", 0.85, 0.15),
    ]

    for _, label, x, w in cols:
        ax1.text(x + w / 2, 0.965, label, ha="center", va="center", fontsize=9, fontweight="bold", color="#25313c")

    row_h = 0.165
    y0 = 0.78
    for i, row in framework.sort_values("step_order").iterrows():
        y = y0 - i * row_h
        status = str(row["status"])
        color = STATUS_COLORS.get(status, "#bfc7d5")
        pale = {"supported": "#d6efec", "framework": "#dbe8ff", "boundary_null": "#fff1cf"}.get(status, "#f2f4f7")
        for key, _, x, w in cols:
            draw_box(ax1, x, y, w, row_h * 0.72, wrap(row[key], 22), pale, edgecolor=color, fontsize=7.0)
        for _, _, x, w in cols[:-1]:
            ax1.annotate(
                "",
                xy=(x + w + 0.011, y + row_h * 0.36),
                xytext=(x + w + 0.0005, y + row_h * 0.36),
                arrowprops=dict(arrowstyle="-|>", color="#4f5b66", lw=0.9),
            )

    ax2 = fig.add_subplot(gs[1])
    ax2.axis("off")
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    ax2.text(
        0.0,
        1.04,
        "b  Current evidence status and claim ceiling",
        fontsize=12,
        fontweight="bold",
        ha="left",
        va="bottom",
    )

    headers = [
        ("Evidence layer", 0.0, 0.22),
        ("Status", 0.25, 0.13),
        ("Support", 0.42, 0.28),
        ("Claim ceiling", 0.74, 0.26),
    ]
    for label, x, _ in headers:
        ax2.text(x, 0.93, label, fontsize=9, fontweight="bold", ha="left", va="center", color="#25313c")

    y = 0.82
    for _, row in evidence.iterrows():
        status = str(row["status"])
        color = STATUS_COLORS.get(status, "#bfc7d5")
        ax2.text(0.0, y, wrap(row["evidence_layer"], 28), fontsize=8, ha="left", va="center", color="#1f2933")
        draw_box(
            ax2,
            0.25,
            y - 0.035,
            0.13,
            0.055,
            STATUS_LABELS.get(status, status),
            facecolor=color + "22",
            edgecolor=color,
            fontsize=6.8,
            weight="bold",
        )
        ax2.text(0.42, y, wrap(row["support"], 38), fontsize=7.5, ha="left", va="center", color="#1f2933")
        ax2.text(0.74, y, wrap(row["claim_ceiling"], 36), fontsize=7.5, ha="left", va="center", color="#1f2933")
        ax2.plot([0.0, 0.96], [y - 0.06, y - 0.06], color="#d6d8db", lw=0.7)
        y -= 0.135

    fig.suptitle(
        "Endpoint-matched monitoring prevents overclaiming",
        x=0.05,
        y=0.985,
        ha="left",
        fontsize=14,
        fontweight="bold",
    )
    fig.text(
        0.05,
        0.025,
        "Source: derived demonstration tables only. Green marks supported endpoint evidence; yellow marks boundary/null evidence; red marks blocked claims.",
        fontsize=7.5,
        color="#4b5563",
    )

    for ext in ["png", "pdf", "svg"]:
        fig.savefig(out_dir / f"{stem}.{ext}", dpi=320, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    parser.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parents[1] / "outputs")
    parser.add_argument("--stem", default="Figure_3_Endpoint_matched_policy_framework_demo")
    args = parser.parse_args()

    framework = read_csv(
        args.data_dir / "figure3_policy_framework_table_20260517.csv",
        {
            "step_order",
            "risk_question",
            "shock_or_gate",
            "observable_endpoint",
            "allowed_claim",
            "policy_use",
            "status",
        },
    )
    evidence = read_csv(
        args.data_dir / "figure3_evidence_status_20260517.csv",
        {"evidence_layer", "claim_id", "status", "support", "claim_ceiling"},
    )
    plot_figure(framework, evidence, args.out_dir, args.stem)
    print(f"Wrote figure files to {args.out_dir}")


if __name__ == "__main__":
    main()
