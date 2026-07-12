"""Small multiples with highlighted lines + annotations (Joseph Barbier
unemployment style). 3x3 grid, one operator highlighted per panel over a greyed
backdrop of all others, with first/last value dots + labels and a dark theme."""
import matplotlib; matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
try:
    from highlight_text import ax_text
except Exception:
    ax_text = None
rng = np.random.default_rng(7)
months = pd.date_range("2015-01-01", "2024-12-01", freq="6MS")
ops = ["Progress","AMH","Amherst","Regent","Normandy","CRG/ECG","Tricon","Starwood","FirstKey"]
finals = [1215,1182,699,642,348,303,298,252,68]
series = {}
for op, f in zip(ops, finals):
    c = np.cumsum(np.abs(rng.normal(1, 1, len(months)))); series[op] = c / c[-1] * f
df = pd.DataFrame(series, index=months)
BG = "#001219"; COLORS = ['#bc6c25','#00b4d8','#d62828','#2a9d8f','#e29578','#9d4edd','#a3b18a','#ffe6a7','#78a1bb']
order = df.iloc[-1].sort_values(ascending=False).index.tolist()
fig, axs = plt.subplots(3, 3, figsize=(12, 8)); fig.set_facecolor(BG)
ymin, ymax = 0, df.values.max()*1.1
for i, (op, ax) in enumerate(zip(order, axs.flat)):
    ax.set_facecolor(BG)
    for other in order:
        if other != op: ax.plot(df.index, df[other], color="grey", alpha=0.2, lw=1.2)
    ax.plot(df.index, df[op], color=COLORS[i], lw=1.6, zorder=10)
    ax.scatter([df.index[0], df.index[-1]], [df[op].iloc[0], df[op].iloc[-1]], s=22, color=COLORS[i], zorder=11)
    ax.text(df.index[-1], df[op].iloc[-1]+40, f"{df[op].iloc[-1]:.0f}", color=COLORS[i], fontsize=9, weight="bold", ha="right")
    ax.text(df.index[len(months)//2], ymax*0.92, op.upper(), color=COLORS[i], fontsize=11, weight="bold", ha="center")
    ax.set_ylim(ymin, ymax); ax.set_axis_off()
fig.text(0.1, 0.97, "How each operator built its Davidson portfolio", color="white", fontsize=16, weight="bold")
fig.text(0.1, 0.935, "Cumulative single-family parcels, each panel highlights one operator (illustrative curves, real totals)",
         color="lightgrey", fontsize=11)
fig.text(0.1, 0.02, "Viz: Who Owns Nashville", color="grey", fontsize=8)
plt.savefig("42_small_multiples_highlight.png", dpi=150, bbox_inches="tight", facecolor=BG)
print("wrote 42_small_multiples_highlight.png")
