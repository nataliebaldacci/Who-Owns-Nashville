"""Scatter with regression fit + auto-positioned labels (Claus Wilke corruption
style). Block groups: income (x) vs institutional rate (y), log fit, colored by
poverty tercile, extreme points auto-labeled with adjustText."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import numpy as np, geopandas as gpd
import matplotlib.pyplot as plt
from adjustText import adjust_text
from sklearn.linear_model import LinearRegression
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
bg = gpd.read_file(os.path.join(ROOT, "institutional_by_blockgroup.geojson"))
bg = bg[(bg["inc"] > 0) & (bg["rate"].notna()) & (bg["res"] > 30)].copy()
x, y = bg["inc"].values.astype(float), bg["rate"].values.astype(float)
terc = np.digitize(bg["pov"], np.quantile(bg["pov"], [0.33, 0.66]))
COLS = np.array(["#56B4E9", "#E69F00", "#D55E00"])[terc]
fig, ax = plt.subplots(figsize=(11, 7.5))
ax.scatter(x, y, s=bg["res"]/4, color=COLS, alpha=0.55, edgecolor="white", zorder=10)
lr = LinearRegression().fit(np.log(x.reshape(-1,1)), y)
xp = np.linspace(x.min(), x.max(), 200)
ax.plot(xp, lr.predict(np.log(xp.reshape(-1,1))), color="#696969", lw=3)
TEXTS=[]
extreme = bg.sort_values("rate", ascending=False).head(8)
for _, r in extreme.iterrows():
    TEXTS.append(ax.text(r["inc"], r["rate"], str(r["bg"])[-4:], size=9))
adjust_text(TEXTS, arrowprops=dict(arrowstyle="-", lw=0.8), ax=ax)
for sp in ["top","right","left"]: ax.spines[sp].set_visible(False)
ax.grid(axis="y", alpha=0.4); ax.tick_params(length=0)
ax.set_xlabel("Median household income ($)"); ax.set_ylabel("Institutional rate (%)")
ax.set_title("Corporate ownership vs neighborhood income (log fit)", weight="bold", loc="left")
plt.tight_layout(); plt.savefig("19_scatter_regression_labels.png", dpi=150)
print("wrote 19_scatter_regression_labels.png")
