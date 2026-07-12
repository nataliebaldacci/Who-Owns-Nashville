"""Line chart with labels at the end of each line (Cedric Scherer Big Mac style).
Operator cumulative acquisitions over time; highlighted operators colored + end-
labeled with leader lines, the rest greyed."""
import matplotlib; matplotlib.use("Agg")
import numpy as np, matplotlib.pyplot as plt
years = np.arange(2013, 2025)
rng = np.random.default_rng(5)
ops = {"Progress":1215,"AMH":1182,"Amherst":699,"Tricon":298,"Starwood":252,"FirstKey":68}
GREY = "#bfbfbf"; COLORS = ["#7F3C8D","#11A579","#3969AC","#E68310"]
highlight = ["Progress","AMH","Amherst","Tricon"]
fig, ax = plt.subplots(figsize=(12, 7)); fig.set_facecolor("#fafafa"); ax.set_facecolor("#fafafa")
series = {}
for name, final in ops.items():
    curve = np.clip(np.cumsum(rng.uniform(0, final/8, len(years))), 0, None)
    curve = curve / curve[-1] * final; series[name] = curve
for name, curve in series.items():
    if name not in highlight:
        ax.plot(years, curve, color=GREY, lw=1.2, alpha=0.6)
label_y = {}
for i, name in enumerate(highlight):
    ax.plot(years, series[name], color=COLORS[i], lw=2.2)
    label_y[name] = series[name][-1]
for i, name in enumerate(highlight):
    y = label_y[name]
    ax.plot([years[-1], years[-1]+0.4], [y, y], color=COLORS[i], lw=1, ls="dashed", alpha=0.6)
    ax.text(years[-1]+0.5, y, name, color=COLORS[i], fontsize=13, weight="bold", va="center")
for sp in ["top","right"]: ax.spines[sp].set_visible(False)
ax.set_xlim(2013, 2026); ax.set_ylabel("Cumulative parcels acquired")
fig.text(0.09, 0.95, "How the big operators grew their Davidson portfolios", size=15, weight="bold")
fig.text(0.09, 0.91, "Cumulative single-family parcels acquired, 2013-2024 (illustrative curves, real totals)", size=10, color="#555")
plt.tight_layout(rect=[0,0,1,0.9]); plt.savefig("29_line_end_labels.png", dpi=150)
print("wrote 29_line_end_labels.png")
