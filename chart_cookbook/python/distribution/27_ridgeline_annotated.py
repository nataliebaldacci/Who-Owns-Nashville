"""Annotated ridgeline with quantile bands + legend inset (rent-by-adjective
style, Ansgar Wolsing / Joseph Barbier). Sale-price distribution by buyer type,
each row filled by quantile band, mean dot, global mean line, and an inset
mini-chart that explains the encoding."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt, seaborn as sns, numpy as np, pandas as pd
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

rng = np.random.default_rng(11)
groups = ["Individual","Trust","Local investor","Corporate","REIT","iBuyer"]
means = [310,360,400,440,470,505]
df = pd.concat([pd.DataFrame({"grp":g,"price":rng.normal(m,70,900).clip(60)})
                for g,m in zip(groups,means)])
order = df.groupby("grp")["price"].mean().sort_values().index.tolist()
gmean = df["price"].mean()
bands = ["#E7E5CB","#C2D6A4","#9BC184","#C2D6A4","#E7E5CB"]; darkgrey="#525252"

fig, axs = plt.subplots(nrows=len(order), ncols=1, figsize=(8, 7)); axs = axs.flatten()
for i, g in enumerate(order):
    sub = df[df["grp"]==g]
    sns.kdeplot(sub["price"], fill=True, ax=axs[i], color="grey", edgecolor="lightgrey", bw_adjust=1)
    axs[i].axvline(gmean, color=darkgrey, linestyle="--")
    q = np.percentile(sub["price"], [2.5,10,25,75,90,97.5]).tolist()
    ymax = axs[i].get_ylim()[1]
    for j in range(len(q)-1):
        axs[i].fill_between([q[j], q[j+1]], 0, ymax*0.18, color=bands[j])
    axs[i].scatter([sub["price"].mean()], [ymax*0.09], color="black", s=10, zorder=5)
    axs[i].text(sub["price"].min()-40, 0, g.upper(), ha="right", fontsize=9, color=darkgrey, va="bottom")
    axs[i].set_xlim(0, 800); axs[i].set_ylim(0, ymax); axs[i].set_ylabel(""); axs[i].set_axis_off()

fig.text(0.5, 0.92, "SALE PRICE BY BUYER TYPE — DAVIDSON COUNTY", ha="center", fontsize=15, weight="bold")
fig.text(0.5, 0.055, "Sale price ($000s)", ha="center", fontsize=12)
fig.text(0.30, 0.885, "Mean (dashed = overall mean)", ha="center", fontsize=9, color=darkgrey)

# legend inset explaining the quantile bands
sub = inset_axes(axs[0], width="42%", height="330%", loc=1)
sub.set_xticks([]); sub.set_yticks([])
bs = df[df["grp"]=="Corporate"]["price"]
sns.kdeplot(bs, fill=True, ax=sub, color="grey", edgecolor="lightgrey")
q = np.percentile(bs, [2.5,10,25,75,90,97.5]).tolist(); ym = sub.get_ylim()[1]
for j in range(len(q)-1):
    sub.fill_between([q[j], q[j+1]], 0, ym*0.18, color=bands[j])
sub.scatter([bs.mean()], [ym*0.09], color="black", s=10)
sub.text(bs.min(), ym*0.9, "Legend", fontsize=11, weight="bold")
sub.text(bs.mean(), ym*0.5, "mean", fontsize=6, ha="center")
sub.text(bs.quantile(0.5), -ym*0.06, "50% of prices", fontsize=6, ha="center")
sub.set_ylim(-ym*0.1, ym*1.05)
plt.savefig("distribution/27_ridgeline_annotated.png".split("/")[-1], dpi=150, bbox_inches="tight")
print("wrote 27_ridgeline_annotated.png")
