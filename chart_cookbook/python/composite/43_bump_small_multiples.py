"""Multi-panel highlighted bump/ranking lineplots (Abdoul Madjid water-rankings
style). One panel per operator; each highlights that operator's RANK trajectory
(by parcels acquired per period) over a greyed backdrop, inverted y-axis so rank
1 sits on top, with '#N in YYs' labels on the first panel."""
import matplotlib; matplotlib.use("Agg")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import rankdata
rng = np.random.default_rng(11)
ops = ["Progress","AMH","Amherst","Regent","Normandy","CRG/ECG","Tricon","Starwood","FirstKey"]
decades = [2000, 2005, 2010, 2015, 2020]
rows=[]
for op in ops:
    trend = rng.uniform(20, 400, len(decades)) * rng.uniform(0.5, 2)
    for d, v in zip(decades, np.sort(trend)):
        rows.append((op.upper(), d, v))
df = pd.DataFrame(rows, columns=["op","decade","nb"])
df["rank"] = df.groupby("decade")["nb"].transform(lambda x: rankdata(-x))
OPS = df["op"].unique()
def add_label(x, y, fs, ax):
    ax.annotate(f"#{int(y)} in\n{str(int(x))[2:]}s", xy=(x, y-0.4), ha="center", va="bottom", fontsize=fs, zorder=12)
def plot_one(country, ax, annotate):
    for c in OPS:
        d = df[df["op"] == c]; x = d["decade"].values; y = d["rank"].values
        if c == country:
            ax.plot(x, y, color="#0b53c1", lw=2.4, zorder=10)
            ax.scatter(x, y, fc="w", ec="#0b53c1", s=55, lw=2.2, zorder=12)
            if annotate: add_label(x[0], y[0], 9, ax); add_label(x[-1], y[-1], 9, ax)
        else:
            ax.plot(x, y, color="#BFBFBF", lw=1.4)
    ax.set_yticks([]); ax.set_xticks(decades)
    ax.set_xticklabels(["00s","05","10","15","20s"], fontsize=9)
    ax.tick_params(bottom=False); ax.set_frame_on(False)
    ax.set_title(country, fontsize=13, fontweight=500)
fig, axes = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(13, 8))
for idx, (ax, op) in enumerate(zip(axes.ravel(), OPS)):
    plot_one(op, ax, annotate=(idx == 0))
axes.ravel()[0].invert_yaxis()
fig.subplots_adjust(wspace=0.1, left=0.03, right=0.97, bottom=0.10, top=0.82)
fig.text(0.5, 0.92, "RANKING OPERATORS BY PARCELS ACQUIRED, BY PERIOD", ha="center", fontsize=20, fontweight="bold")
fig.text(0.97, 0.04, "Illustrative ranking · Who Owns Nashville", ha="right", fontsize=8)
fig.set_facecolor("#f9fbfc")
plt.savefig("43_bump_small_multiples.png", dpi=150, bbox_inches="tight", facecolor="#f9fbfc")
print("wrote 43_bump_small_multiples.png")
