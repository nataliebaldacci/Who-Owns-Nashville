"""Heatmap + radial barcharts composite (Margaret Siple / TidyTuesday style,
Python port by Tomas Capretto). A dot-heatmap of each operator's property-type
mix, plus radial barplots for the top operators. Adapted to Davidson operators x
property types with synthetic proportions."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.colors as mcolors, matplotlib.pyplot as plt, numpy as np, pandas as pd

OPS = ["AMH","Amherst","CRG/ECG","Invitation","Normandy","Progress","Regent","Starwood","Tricon","Other"]
TYPES = ["sfr","btr","condo","duplex","land"]
rng = np.random.default_rng(7)
mat = rng.dirichlet(np.ones(len(TYPES))*1.5, size=len(OPS))
df = pd.DataFrame(mat, columns=TYPES); df["op"] = OPS
long = df.melt(id_vars="op", value_vars=TYPES, var_name="type", value_name="prop")
order = sorted(OPS, key=str.lower); order.remove("Other"); order.append("Other")
long["op"] = pd.Categorical(long["op"], categories=order, ordered=True)
long = long.sort_values("op", ascending=False)

COLORS = ["#0C2C84","#225EA8","#1D91C0","#41B6C4","#7FCDBB","#C7E9B4","#FFFFCC"]
cmap = mcolors.LinearSegmentedColormap.from_list("ylgnbu", COLORS, N=256)

def plot_heatmap(ax):
    for i, t in enumerate(TYPES):
        d = long[long["type"] == t]
        ax.scatter([i]*len(d), d["op"], color=cmap(d["prop"]), s=140)
    ax.set_frame_on(False); ax.grid(alpha=0.4); ax.set_axisbelow(True)
    ax.set_xticks(range(len(TYPES))); ax.set_xticklabels(TYPES)
    ax.tick_params(size=0, colors="0.3"); ax.set_xlabel("Property type", loc="right")

PAL = ["#81C4CA","#468D96","#103128","#E83D5F","#FA6E90","#FCB16D"]
def style_polar(ax):
    ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1); ax.set_frame_on(False)
    ax.set_xticklabels([]); ax.set_ylim([0, len(TYPES)+0.5]); ax.set_yticks(range(len(TYPES)+1))
    ax.set_yticklabels([]); ax.grid(alpha=0.4)

def plot_circular(axes):
    top6 = df.sort_values("sfr", ascending=False).head(6).reset_index(drop=True)
    for i, ax in enumerate(axes.ravel()):
        row = top6.iloc[i]; props = row[TYPES].values.astype(float) * 2*np.pi
        style_polar(ax)
        x = np.linspace(0, props, num=150); y = np.vstack([np.arange(len(props))]*150)
        ax.plot(x, y, lw=6, color=PAL[i], solid_capstyle="round")
        ax.set_title(row["op"], pad=8, color="0.3")
        for idx, t in enumerate(TYPES):
            ax.text(0, idx, t, color=PAL[i], ha="center", va="center", fontsize=9,
                    bbox={"facecolor":"w","edgecolor":PAL[i],"boxstyle":"round","pad":0.15})

fig = plt.figure(figsize=(14, 9)); fig.set_facecolor("w")
gs1 = fig.add_gridspec(1, 1, left=0.06, right=0.32, top=0.85, bottom=0.1)
plot_heatmap(fig.add_subplot(gs1[0]))
gs2 = fig.add_gridspec(3, 2, left=0.40, right=0.97, hspace=0.35, wspace=0.1, top=0.85, bottom=0.06)
axes = np.array([fig.add_subplot(g, projection="polar") for g in gs2])
plot_circular(axes)
fig.text(0.5, 0.94, "What property types do Davidson's top operators hold?", ha="center", size=17, weight="bold")
fig.text(0.5, 0.905, "Proportion of each property type per operator (illustrative)", ha="center", size=12, color="0.3")
fig.text(0.95, 0.03, "Who Owns Nashville", color="0.3", ha="right")
plt.savefig("39_heatmap_radial.png", dpi=150, bbox_inches="tight")
print("wrote 39_heatmap_radial.png")
