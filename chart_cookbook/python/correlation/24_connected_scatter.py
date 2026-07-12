"""Connected scatter — CORRELATION. Two variables tracked over time (path)."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt
from styles.won_styles import apply_style, palette
apply_style("crs"); c = palette("crs")
years = list(range(2016, 2025))
starts = [3.4, 3.6, 3.9, 3.6, 3.9, 4.0, 3.1, 2.7, 2.7]
price  = [240, 260, 285, 300, 330, 380, 430, 460, 470]
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(starts, price, "-o", color=c[0], lw=1.5)
for x, y, yr in zip(starts, price, years):
    ax.annotate(str(yr), (x, y), fontsize=8, xytext=(4, 4), textcoords="offset points")
ax.set_xlabel("SF permits (000s)"); ax.set_ylabel("Median price ($000s)")
ax.set_title("Permits vs Price, Year by Year", fontweight="bold")
plt.tight_layout(); plt.savefig("24_connected_scatter.png", dpi=150)
