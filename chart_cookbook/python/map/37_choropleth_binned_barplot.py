"""Choropleth + binned seaborn barplot legend (Sao Paulo HDI style, Vinicius Oike
/ Joseph Barbier). Davidson tracts shaded by institutional %; the inset horizontal
barplot bins the metric and shows each bin's share of residential parcels, labeled.
YlGnBu ramp. Optional pyfonts font (falls back offline)."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt, seaborn as sns, pandas as pd
import geopandas as gpd
from pypalettes import load_cmap

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
gdf = gpd.read_file(os.path.join(ROOT, "Davidson_Institutional_Pct_by_Tract.geojson"))
gdf = gdf[gdf["pct_institutional"].notna()].copy()
col = "pct_institutional"

# build the binned barplot dataset: residential parcels per institutional-% bin
bins = [0, 2, 5, 10, 15, 20, 30, 100]
labels = ["0-2%", "2-5%", "5-10%", "10-15%", "15-20%", "20-30%", "30%+"]
gdf["grp"] = pd.cut(gdf[col], bins=bins, include_lowest=True, labels=labels)
agg = gdf.groupby("grp", observed=True)["total_residential"].sum().reset_index()
agg["share"] = 100 * agg["total_residential"] / agg["total_residential"].sum()
agg["label"] = agg["share"].round(1).astype(str) + "%"

palette = "YlGnBu"
cmap = load_cmap(palette, cmap_type="continuous")
try:
    from pyfonts import load_google_font
    font = load_google_font("Roboto"); boldf = load_google_font("Roboto", weight="bold")
except Exception:
    font = boldf = None

fig, ax = plt.subplots(figsize=(10, 10), dpi=150); ax.axis("off")
gdf.plot(ax=ax, column=col, cmap=cmap, edgecolor="lightgrey", linewidth=0.2, alpha=0.92)

sub = ax.inset_axes(bounds=(0.60, 0.20, 0.16, 0.28), transform=fig.transFigure)
sub.set_axis_off()
sns.barplot(data=agg, x="share", y="grp", palette=palette, hue="grp", legend=False, ax=sub)
sub.axvline(x=0, color="black"); sub.invert_yaxis()
for i, r in agg.iterrows():
    xp = r["share"] - 5 if r["share"] > 8 else r["share"] + 1
    tc = "white" if i >= len(agg) - 2 else "black"
    sub.text(xp, i, r["label"], color=tc, size=7, va="center", **({"font": font} if font else {}))
    sub.text(-13, i, r["grp"], color="black", size=6, va="center", **({"font": font} if font else {}))

fig.text(0.5, 0.88, "Institutional Ownership in Davidson County", ha="center", size=22,
         **({"font": boldf} if boldf else {"weight": "bold"}))
fig.text(0.61, 0.49, "Residential parcels by institutional-% group", size=9,
         **({"font": font} if font else {}))
fig.text(0.62, 0.14, "Source: Metro Ownership Parcels · Who Owns Nashville", size=8,
         **({"font": font} if font else {}))
plt.savefig("37_choropleth_binned_barplot.png", dpi=150, bbox_inches="tight")
print("wrote 37_choropleth_binned_barplot.png")
