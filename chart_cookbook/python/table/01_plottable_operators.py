"""Publication-ready table with plottable (Fortune Uwha liveability-table style).
Top Davidson operators with color-coded circled metric cells (per-column
colormap), grouped columns, title/subtitle/footer. Uses real owner_leaderboard
data. NOTE: this is a color-coded figure-table; house-style report tables stay
booktabs/Garamond per _HOUSE_STYLE.md."""
import matplotlib; matplotlib.use("Agg")
import os, json, matplotlib, matplotlib.pyplot as plt, pandas as pd
from plottable import ColumnDefinition, Table
from plottable.cmap import normed_cmap

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
rows = json.load(open(os.path.join(ROOT, "owner_leaderboard.json")))["rows"][:12]
df = pd.DataFrame([{
    "Operator": r["nm"],
    "Parcels": r["n"],
    "TN %": round(100*r.get("tn_n",0)/max(r["n"],1)),
    "OOS %": round(100*r.get("oos_n",0)/max(r["n"],1)),
    "Avg $000s": round((r.get("val",0)/max(r["n"],1))/1000),
    "Units": r.get("du",0),
    "Acres": round(r.get("acres",0)),
} for r in rows]).set_index("Operator")

circ = {"ha":"center","bbox":{"boxstyle":"circle","pad":0.35}}
def cd(name, group, cmap="PiYG"):
    return ColumnDefinition(name=name, width=0.8, textprops=circ,
                            cmap=normed_cmap(df[name], cmap=getattr(matplotlib.cm, cmap), num_stds=2.2),
                            group=group)
col_defs = [
    ColumnDefinition(name="Operator", textprops={"ha":"left","weight":"bold"}, width=1.8),
    cd("Parcels","Holdings","Blues"), cd("Units","Holdings","Blues"), cd("Acres","Holdings","Blues"),
    cd("TN %","Geography","PiYG"), cd("OOS %","Geography","PiYG_r"),
    cd("Avg $000s","Value","YlOrBr"),
]
plt.rcParams["font.family"]=["DejaVu Sans"]
fig, ax = plt.subplots(figsize=(14, 8))
Table(df, column_definitions=col_defs, row_dividers=True, footer_divider=True, ax=ax,
      textprops={"fontsize":13}, row_divider_kw={"linewidth":1,"linestyle":(0,(1,5))},
      col_label_divider_kw={"linewidth":1,"linestyle":"-"})
plt.text(0.5, 0.93, "DAVIDSON COUNTY — LARGEST CORPORATE OPERATORS", transform=fig.transFigure,
         ha="center", fontsize=17, fontweight="bold")
plt.text(0.5, 0.905, "Holdings, in-state vs out-of-state share, average parcel value, dwelling units and acreage.",
         transform=fig.transFigure, ha="center", fontsize=12, color="gray")
plt.text(0.5, 0.07, "Source: Metro Ownership Parcels (owner_leaderboard) · Who Owns Nashville",
         transform=fig.transFigure, ha="center", fontsize=11)
fig.savefig("01_plottable_operators.png", facecolor="white", dpi=170, bbox_inches="tight")
print("wrote 01_plottable_operators.png")
