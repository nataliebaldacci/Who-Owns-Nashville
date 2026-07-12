"""CRS 'New vs Existing Homes' style: stacked bars, blue = New, orange = Existing.
For Davidson: split each year's SF sales by parcel year-built vs sale year
(new = built within ~1-2 yrs of the transfer)."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt, numpy as np
from styles.won_styles import apply_style, palette
apply_style("crs"); c = palette("crs")
yrs = np.arange(2000, 2022)
existing = np.array([2050,2050,2100,2280,2200,2870,3480,3510,3120,2730,3020,2320,
                     1830,1880,1870,1770,1650,1470,1560,1400,1050,880])
new =      np.array([300,320,350,380,470,510,510,500,350,240,180,140,150,180,200,
                     230,260,290,340,320,300,390])
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.bar(yrs, new, color=c[4], label="New")
ax.bar(yrs, existing, bottom=new, color=c[1], label="Existing")
ax.set_ylabel("Thousands of Single-Family Units")
ax.set_title("New and Existing Single-Family Sales", fontweight="bold", loc="left")
ax.legend(loc="upper right", frameon=False); ax.grid(False); ax.set_axisbelow(True)
ax.yaxis.grid(True, color="#e6e6e6")
plt.xticks(yrs, rotation=90, fontsize=8)
plt.tight_layout(); plt.savefig("crs_new_vs_existing.png", dpi=150)
