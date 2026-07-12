"""Plottable table with in-cell graphs (python-graph-gallery "insert graphs in
cells" chapter). Columns render mini-plots inside their cells: a progress donut
and proportional bars with a background track and annotation. Turning numbers
into little plots makes a ranking table far quicker to read. Real data: the
largest Davidson operators (owner_leaderboard.json)."""
import matplotlib; matplotlib.use("Agg")
import os, json, functools
import matplotlib.pyplot as plt
import pandas as pd
from plottable import ColumnDefinition, Table
from plottable.plots import bar, progress_donut

WON_BLUE, WON_GOLD = "#1c458c", "#f0af1e"
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
rows = json.load(open(os.path.join(ROOT, "owner_leaderboard.json")))["rows"][:10]

df = pd.DataFrame([{
    "Operator": r["nm"],
    "Parcels": r["n"],
    "OOS share": round(100 * r.get("oos_n", 0) / max(r["n"], 1)),   # 0-100 -> donut
    "Avg value": round(r.get("val", 0) / max(r["n"], 1) / 1000),    # $000s -> bar
    "Units": r.get("du", 0),
} for r in rows]).set_index("Operator")

col_defs = [
    ColumnDefinition("Operator", textprops={"ha": "left", "weight": "bold"}, width=1.7),
    ColumnDefinition("Parcels", textprops={"ha": "center"}, width=0.6),
    ColumnDefinition("OOS share", width=0.9, plot_fn=progress_donut,
                     plot_kw={"is_pct": True, "color": WON_GOLD}, group="in-cell plots"),
    ColumnDefinition("Units", width=1.1,
                     plot_fn=functools.partial(bar, plot_bg_bar=True, color="#4fa0bd",
                                               annotate=True, xlim=(0, df["Units"].max())),
                     group="in-cell plots"),
    ColumnDefinition("Avg value", width=1.1,
                     plot_fn=functools.partial(bar, plot_bg_bar=True, color=WON_BLUE,
                                               annotate=True, xlim=(0, df["Avg value"].max())),
                     group="in-cell plots"),
]

plt.rcParams["font.family"] = ["DejaVu Sans"]
fig, ax = plt.subplots(figsize=(12, 7))
Table(df, column_definitions=col_defs, ax=ax, textprops={"fontsize": 13},
      row_dividers=True, footer_divider=True,
      row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))})
fig.text(0.06, 0.94, "DAVIDSON OPERATORS — READ-AT-A-GLANCE TABLE",
         fontsize=16, fontweight="bold")
fig.text(0.06, 0.905,
         "OOS share = progress donut   Units = bar   Avg value = bar (in $000s)",
         fontsize=10, color="#5a5a5a")
plt.savefig(os.path.join(os.path.dirname(__file__), "03_plottable_incell_plots.png"),
            dpi=150, bbox_inches="tight")
print("wrote 03_plottable_incell_plots.png")
