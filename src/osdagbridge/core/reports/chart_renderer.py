"""Render report charts in an isolated process.

Matplotlib's native text renderer can segfault when called from the report
worker thread while the Qt/OpenCascade UI is active. Keeping Matplotlib in a
short-lived child process isolates its native libraries from the desktop app.
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from osdagbridge.core.reports.styles import CHART


def _render(spec):
    import matplotlib

    matplotlib.use("Agg")
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure

    kind = spec["kind"]
    if kind == "ur":
        values = spec["values"]
        labels = spec["labels"]
        fig = Figure(figsize=CHART["ur_size"], dpi=CHART["dpi"], facecolor="white")
        ax = fig.subplots()
        valid = [(i, value) for i, value in enumerate(values) if value is not None]
        if valid:
            ax.bar(
                [i for i, _ in valid], [value for _, value in valid],
                color=[CHART["accent"] if value <= CHART["threshold"] else CHART["fail"] for _, value in valid],
                width=CHART["bar_width"],
            )
            for i, value in valid:
                ax.text(i, value, f"{value:.2f}", ha="center", va="bottom", fontsize=9)
        display_labels = [
            f"{label}\nNo design data" if value is None else label
            for label, value in zip(labels, values)
        ]
        ax.axhline(
            CHART["threshold"],
            color=CHART["threshold_color"],
            linestyle="--",
            linewidth=1.3,
            label=f"UR = {CHART['threshold']:.1f} limit",
        )
        max_ur = max((value for value in values if value is not None), default=1.0)
        ax.set_ylim(0, max(CHART["threshold"] * 1.15, max_ur * 1.15))
        ax.set_xticks(list(range(len(labels))), display_labels)
        ax.set_ylabel("Utilization Ratio (UR = Demand / Capacity)")
        ax.grid(axis="y", alpha=CHART["grid_alpha"])
        ax.legend(loc="upper right", frameon=False)
    elif kind == "steel":
        labels = spec["labels"]
        values = spec["values"]
        fig = Figure(figsize=CHART["material_size"], dpi=CHART["dpi"], facecolor="white")
        ax = fig.subplots()
        bars = ax.bar(labels, values, color=CHART["accent"])
        ax.set_ylabel("Weight (MT)")
        ax.set_title("Structural Steel Quantities")
        ax.set_ylim(top=max(values, default=0) * (1 + CHART["label_headroom"]) or 1)
        missing_labels = spec.get("missing_labels", [])
        if missing_labels:
            ax.set_xlabel("No quantity data for: " + ", ".join(missing_labels), fontsize=8)
        ax.grid(axis="y", linestyle=":", alpha=CHART["material_grid_alpha"])
        ax.bar_label(bars, fmt="%.2f", padding=4)
    elif kind == "concrete_rebar":
        fig = Figure(figsize=CHART["material_size"], dpi=CHART["dpi"], facecolor="white")
        axes = fig.subplots(1, 2)
        for ax, title, value, unit in (
            (axes[0], "Concrete Deck", spec.get("concrete"), "Volume (m$^3$)"),
            (axes[1], "Deck Reinforcement", spec.get("rebar"), "Weight (MT)"),
        ):
            ax.set_title(title)
            ax.set_ylabel(unit)
            ax.grid(axis="y", linestyle=":", alpha=CHART["material_grid_alpha"])
            if value is None:
                ax.text(0.5, 0.5, "Quantity unavailable", ha="center", va="center", transform=ax.transAxes)
                ax.set_xticks([])
            else:
                bars = ax.bar([title], [value], color=CHART["info"])
                ax.set_ylim(top=value * (1 + CHART["label_headroom"]) or 1)
                ax.bar_label(bars, fmt="%.2f", padding=4)
    else:
        raise ValueError(f"Unknown chart type: {kind}")

    FigureCanvasAgg(fig)
    fig.tight_layout()
    fig.savefig(sys.stdout.buffer, format="png", bbox_inches="tight", facecolor="white")


def render_chart_png(spec):
    """Return PNG bytes produced by an isolated Matplotlib process."""
    with tempfile.TemporaryDirectory(prefix="osdagbridge-mpl-") as mpl_config_dir:
        env = os.environ.copy()
        env["MPLBACKEND"] = "Agg"
        env["MPLCONFIGDIR"] = mpl_config_dir
        result = subprocess.run(
            [sys.executable, os.path.abspath(__file__)],
            input=json.dumps(spec).encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(f"Chart rendering failed: {result.stderr.strip()}")
        if not result.stdout:
            raise RuntimeError("Chart rendering returned an empty image")
        return result.stdout


if __name__ == "__main__":
    os.environ.setdefault("MPLBACKEND", "Agg")
    _render(json.load(sys.stdin))
