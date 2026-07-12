"""Animated stacked-area chart with text that highlights key events (Joseph
Barbier "space objects" style). A GIF that grows a two-band stacked area of the
cumulative corporate SFR footprint in Davidson County by home vintage (built
pre-2000 vs 2000+), with a big background year, a running description that types
itself out, and black-lollipop event callouts that appear one at a time. Real
per-parcel acquisition data. Saved with matplotlib's PillowWriter (no external
imagemagick needed). Set DPI higher for a crisper final render."""
import matplotlib; matplotlib.use("Agg")
import os, json, math, textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
try:
    from highlight_text import fig_text, ax_text
    HL = True
except Exception:
    HL = False

DPI = 60  # bump to 120 for a crisp (slower) render
plt.rcParams["figure.dpi"] = DPI; plt.rcParams["savefig.dpi"] = DPI
COLORS = ["#4fa0bd", "#1c458c"]          # pre-2000, 2000+
BG = "#fef9ef"

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
props = [f["properties"] for f in
         json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))["features"]]
recs = []
for p in props:
    a, yb = str(p.get("acq", ""))[:4], str(p.get("ybuilt", ""))
    if a.isdigit() and yb.isdigit() and 2010 <= int(a) <= 2025:
        recs.append((int(a), "Built 2000+" if int(yb) >= 2000 else "Built pre-2000"))
df = pd.DataFrame(recs, columns=["year", "vintage"])
per_year = df.groupby(["year", "vintage"]).size().unstack(fill_value=0)
per_year = per_year.reindex(range(df.year.min(), df.year.max() + 1), fill_value=0)
cum = per_year.cumsum()[["Built pre-2000", "Built 2000+"]]
years = cum.index.to_numpy()

# reference figures for the running description
total = int(cum.iloc[-1].sum())
new_share = 100 * cum.iloc[-1]["Built 2000+"] / total
description = (f"Between {years[0]} and {years[-1]}, corporate operators assembled "
              f"{total:,} single-family parcels across Davidson County. "
              f"{new_share:.0f}% of that footprint is housing built since 2000 - "
              f"the build-to-rent and newer scattered stock that operators favored "
              f"as the buying accelerated after 2018.")

# events: (year, label)
events = [(2012, "Institutional buyers\nenter Nashville <2012>"),
          (2020, "Pandemic buying\nsurge <2020>"),
          (2021, "Acquisitions peak <2021>"),
          (2023, "Rate hikes slow\nthe buying <2023>")]

fig, ax = plt.subplots(figsize=(12, 8))
fig.set_facecolor(BG); ax.set_facecolor(BG)
FRAMES = len(years)

def update(frame):
    ax.clear(); ax.set_facecolor(BG)
    sub = cum.iloc[:frame + 1]
    ax.stackplot(sub.index, sub["Built pre-2000"], sub["Built 2000+"], colors=COLORS)
    ymax = cum.iloc[:frame + 1].sum(axis=1).max() * 1.9 or 1
    ax.set_ylim(0, ymax); ax.set_xlim(years[0], years[-1])
    ax.set_xticks([]); ax.spines[["top", "right", "bottom"]].set_visible(False)
    year = years[frame]

    if HL:
        fig_text(0.15, 0.90, f"{years[0]} - {year}", ha="left", va="center",
                 fontsize=46, fontweight="bold", alpha=0.10, fig=fig)
        fig_text(0.13, 0.85, "The corporate footprint by vintage:\n"
                 "<Built pre-2000> and <Built 2000+>", ha="left", va="top", fontsize=18,
                 highlight_textprops=[{"color": COLORS[0], "fontweight": "bold"},
                                      {"color": COLORS[1], "fontweight": "bold"}], fig=fig)
        # running description types itself out
        eff = FRAMES - 3
        nch = math.ceil(len(description) * (frame / eff)) if frame < eff else len(description)
        wrapped = "\n".join(textwrap.fill(par, width=64) for par in description[:nch].split("\n"))
        fig_text(0.135, 0.70, wrapped, ha="left", va="top", fontsize=12, fig=fig)
        fig_text(0.9, 0.02, "Graph: <Who Owns Nashville>   Data: <Davidson County parcels>",
                 ha="right", va="bottom", fontsize=7,
                 highlight_textprops=[{"fontweight": "bold"}, {"fontweight": "bold"}], fig=fig)
    else:
        ax.set_title(f"{years[0]} - {year}", loc="left", fontsize=16)

    # one-at-a-time event lollipops
    ev_years = [e[0] for e in events] + [years[-1] + 1]
    for i, (eyr, label) in enumerate(events):
        if eyr <= year < ev_years[i + 1] and eyr in cum.index:
            h = cum.loc[eyr].sum()
            ax.plot((eyr, eyr), (0, h), color="black", zorder=10, lw=1.2)
            ax.scatter(eyr, h, color="black", s=70, zorder=11)
            if HL:
                ax_text(eyr - 0.3, h * 1.08 + ymax * 0.04, label, fontsize=11,
                        ha="left", va="bottom",
                        highlight_textprops=[{"fontweight": "bold"}], ax=ax)
    return ax

ani = FuncAnimation(fig=fig, func=update, frames=FRAMES, interval=200)
out = os.path.join(os.path.dirname(__file__), "34_animated_stacked_area.gif")
ani.save(out, writer=PillowWriter(fps=2))
print("wrote 34_animated_stacked_area.gif  (%d frames, %d parcels)" % (FRAMES, total))
