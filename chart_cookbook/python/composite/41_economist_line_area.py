"""Economist-style two-panel line + stacked area (child-labour chart style) with
flexitext titles and a red top bar. Left: institutional rate over time by tier.
Right: parcel counts by tier stacked. Illustrative."""
import matplotlib; matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
from flexitext import flexitext
from matplotlib import lines, patches
BLUE="#076FA1"; GREEN="#2FC1D3"; BROWN="#AD8C97"; GREY="#C7C9CB"; RED="#E3120B"
year=[2012,2016,2020,2024]
rate=[[2.1,3.4,5.2,7.1],[1.2,2.0,3.1,4.0],[0.4,0.9,1.6,2.3]]  # Big4 / other-corp / local
counts=[[65,120,210,320],[90,150,240,300],[40,70,120,160],[300,260,210,180]]
COLORS=[BLUE,GREEN,BROWN]
fig, axes = plt.subplots(1, 2, figsize=(13, 7.2)); fig.subplots_adjust(left=0.05,right=0.97,top=0.80,bottom=0.12); fig.set_facecolor("w")
def cust(ax):
    ax.set_axisbelow(True); ax.grid(axis="y", color="#A8BAC4", lw=1.0)
    ax.set_xticks(year); ax.set_xticklabels(year, fontsize=12)
    for sp in ["right","top","left"]: ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_lw(1.2)
for pct,c in zip(rate,COLORS):
    axes[0].plot(year,pct,color=c,lw=4); axes[0].scatter(year,pct,fc=c,s=70,ec="white",lw=1.2,zorder=5)
cust(axes[0]); axes[0].set_ylim(0,8); axes[0].set_xlim(2011,2025)
axes[0].text(2012,7.2,"Big-4 REIT",color=BLUE,weight="bold"); axes[0].text(2012,4.2,"Other corporate",color=GREEN,weight="bold"); axes[0].text(2012,2.4,"Local investor",color=BROWN,weight="bold")
flexitext(0.05,0.965,"<size:16><weight:bold>Institutional rate,</> % of SF parcels</>", va="top", ax=axes[0])
axes[1].stackplot(year, counts, colors=COLORS+[GREY], lw=1.5, edgecolor="white")
cust(axes[1]); axes[1].set_ylim(0,1000); axes[1].set_xlim(2011,2025)
flexitext(0.55,0.965,"<size:16><weight:bold>Parcels by tier,</> count</>", va="top", ax=axes[1])
fig.text(0.05,0.90,"Corporate ownership is rising", fontsize=20, weight="bold")
fig.text(0.05,0.855,"Davidson County single-family parcels (illustrative)", fontsize=13)
fig.add_artist(lines.Line2D([0,1],[1,1], lw=3, color=RED, solid_capstyle="butt"))
fig.add_artist(patches.Rectangle((0,0.975),0.05,0.025, color=RED))
plt.savefig("41_economist_line_area.png", dpi=150, bbox_inches="tight")
print("wrote 41_economist_line_area.png")
