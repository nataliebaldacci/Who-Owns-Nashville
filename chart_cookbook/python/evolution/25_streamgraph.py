"""Streamgraph — EVOLUTION. Stacked area with a wiggle baseline (flowing)."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt, numpy as np
from styles.won_styles import apply_style, palette
apply_style("jchs"); c = palette("jchs")
yrs = np.arange(2015, 2025)
prog = [60,110,180,260,340,300,250,220,200,190]
amh  = [80,130,190,250,320,280,210,180,170,160]
amh2 = [40,70,120,170,230,190,150,120,110,100]
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.stackplot(yrs, prog, amh, amh2, labels=["Progress","AMH","Amherst"],
             colors=c[:3], baseline="wiggle", alpha=.9)
ax.set_title("Acquisitions by Operator (streamgraph)", fontweight="bold")
ax.legend(loc="upper left", frameon=True); ax.set_yticks([])
plt.tight_layout(); plt.savefig("25_streamgraph.png", dpi=150)
