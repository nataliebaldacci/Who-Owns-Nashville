"""Stacked-area small-multiples arranged as a map (Erin Davis 'viral map' style).
One mini stacked-area per Davidson council district, positioned at the district
centroid, showing ownership-composition-over-time. Synthetic composition."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt, numpy as np
import geopandas as gpd
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
dist = gpd.read_file(os.path.join(ROOT, "Davidson_Council_Districts.geojson")).to_crs(4326)
outline = gpd.read_file(os.path.join(ROOT, "Davidson_County_Boundary.geojson")).to_crs(4326)
years = np.arange(2010, 2025); rng = np.random.default_rng(3)
colors = ["#4fa0bd", "#f0af1e", "#1c458c"]  # owner-occ / individual-investor / corporate

fig, ax = plt.subplots(figsize=(11, 11)); ax.axis("off")
outline.plot(ax=ax, color="#f7f7f7", edgecolor="#c8c7c7", linewidth=0.6)
dist.boundary.plot(ax=ax, color="#e0e0e0", linewidth=0.4)
x0, y0, x1, y1 = ax.get_xlim()[0], ax.get_ylim()[0], ax.get_ylim()[1], ax.get_xlim()[1]
xmin, xmax = ax.get_xlim(); ymin, ymax = ax.get_ylim()
for _, r in dist.iterrows():
    c = r.geometry.representative_point()
    fx = (c.x - xmin) / (xmax - xmin); fy = (c.y - ymin) / (ymax - ymin)
    ia = ax.inset_axes([fx-0.028, fy-0.022, 0.056, 0.044])
    base = rng.uniform(0.5, 0.8)
    oo = np.clip(base - np.linspace(0, 0.25, len(years)) + rng.normal(0, 0.02, len(years)), 0.1, 0.95)
    corp = np.clip(np.linspace(0.03, 0.22, len(years)) + rng.normal(0, 0.02, len(years)), 0, 0.5)
    ind = np.clip(1 - oo - corp, 0, 1)
    ia.stackplot(years, oo, ind, corp, colors=colors)
    ia.axis("off"); ia.set_ylim(0, 1)
fig.text(0.5, 0.93, "Ownership composition over time, by council district", ha="center", size=16, weight="bold")
fig.text(0.5, 0.90, "Each mini chart is one district; blue=owner-occ, gold=individual investor, navy=corporate (illustrative)",
         ha="center", size=10, color="#666")
plt.savefig("40_stacked_area_tilemap.png", dpi=140, bbox_inches="tight")
print("wrote 40_stacked_area_tilemap.png")
