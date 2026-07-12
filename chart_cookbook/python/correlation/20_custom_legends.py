"""Custom legends in Matplotlib — a reference sheet (python-graph-gallery style).
Six panels of the same scatter (corporate parcel size vs year built, colored by
property type) each showing a different legend treatment: default, custom
markers + loc, legend outside the axes, legend on top with ncol, styled title
and label text, and custom handles (facecolor / hatch / edgecolor) with a styled
legend patch. Real data: Davidson active corporate SFR detail (sampled)."""
import matplotlib; matplotlib.use("Agg")
import os, json
import numpy as np
import matplotlib.pyplot as plt

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
props = [f["properties"] for f in
         json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))["features"]]

rows = []
for p in props:
    sq, yb, pt = str(p.get("sqft", "")), str(p.get("ybuilt", "")), p.get("ptype")
    if sq.replace(".", "").isdigit() and yb.isdigit() and pt:
        rows.append((float(sq), int(yb), pt))
sqft = np.array([r[0] for r in rows]); year = np.array([r[1] for r in rows])
ptype = np.array([r[2] for r in rows])
# keep the three main types, sample for legibility
keep = np.isin(ptype, ["Single Family", "Condo", "Duplex"]) & (sqft < 6000) & (year > 1900)
sqft, year, ptype = sqft[keep], year[keep], ptype[keep]
rng = np.random.RandomState(0)
idx = rng.choice(len(sqft), size=min(1500, len(sqft)), replace=False)
sqft, year, ptype = sqft[idx], year[idx], ptype[idx]

TYPES = ["Single Family", "Condo", "Duplex"]
COLORS = ["#1B9E77", "#D95F02", "#7570B3"]
MARKERS = ["o", "^", "s"]

def scatter(ax, markers=False):
    for t, c, m in zip(TYPES, COLORS, MARKERS):
        s = ptype == t
        ax.scatter(sqft[s], year[s], label=t, s=22, color=c, alpha=0.6,
                   marker=(m if markers else "o"))
    ax.set_xlabel("Living area (sq ft)"); ax.set_ylabel("Year built")

fig, axes = plt.subplots(2, 3, figsize=(16, 10)); axes = axes.flatten()

# 1 — default legend
scatter(axes[0]); axes[0].legend(); axes[0].set_title("1. Default legend", loc="left", fontweight="bold")

# 2 — custom markers + loc
scatter(axes[1], markers=True); axes[1].legend(loc="lower right")
axes[1].set_title("2. Custom markers + loc='lower right'", loc="left", fontweight="bold")

# 3 — legend outside the axes (right)
scatter(axes[2]); axes[2].legend(loc="center left", bbox_to_anchor=(1.01, 0.5), frameon=False)
axes[2].set_title("3. Legend outside (bbox_to_anchor)", loc="left", fontweight="bold")

# 4 — legend on top, three columns
scatter(axes[3]); axes[3].legend(loc="lower center", ncol=3, bbox_to_anchor=(0.5, 1.08),
                                 frameon=False, columnspacing=0.8, handletextpad=0.2)
axes[3].set_title("4. On top, ncol=3", loc="left", fontweight="bold", y=1.12)

# 5 — styled title + label text
scatter(axes[5-1] if False else axes[4])
leg = axes[4].legend(loc="lower right", title="Property type", title_fontsize=12)
leg._legend_box.align = "left"
leg.get_title().set_color("#1c458c"); leg.get_title().set_weight("bold")
for text in leg.get_texts():
    text.set_color("#5a5a5a"); text.set_fontstyle("italic"); text.set_fontsize(11)
axes[4].set_title("5. Styled title + labels", loc="left", fontweight="bold")

# 6 — custom handles (facecolor / hatch / edgecolor) + styled patch
scatter(axes[5])
leg = axes[5].legend(loc="lower right", markerscale=1.6, labelspacing=1.2)
hatches = ["//", "xx", ".."]
for h, col, hatch in zip(leg.legend_handles, COLORS, hatches):
    h.set_edgecolor("#20303f"); h.set_facecolor(col); h.set_hatch(hatch); h.set_alpha(0.8)
leg.get_frame().set_facecolor("#eef4fb"); leg.get_frame().set_edgecolor("#4fa0bd")
leg.get_frame().set_linewidth(2)
axes[5].set_title("6. Custom handles + patch", loc="left", fontweight="bold")

fig.suptitle("Custom legends in Matplotlib — Davidson corporate parcels by property type",
             fontsize=16, fontweight="bold", x=0.02, ha="left")
fig.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(os.path.dirname(__file__), "20_custom_legends.png"), dpi=140)
print("wrote 20_custom_legends.png  (%d points)" % len(sqft))
