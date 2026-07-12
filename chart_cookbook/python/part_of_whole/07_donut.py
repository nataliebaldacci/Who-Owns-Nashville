"""
Donut chart — PART OF WHOLE
Use sparingly (few categories). Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({
    "type": ["Individual", "Corporate", "Trust", "Bank/Lender", "Government"],
    "owners": [844084, 62114, 22775, 3696, 2270],
})
colors = ["#4fa0bd", "#e6194b", "#911eb4", "#16a085", "#8a94a0"]

fig, ax = plt.subplots(figsize=(6.5, 6.5))
ax.pie(df["owners"], labels=df["type"], colors=colors, autopct="%1.1f%%",
       pctdistance=0.82, wedgeprops={"width": 0.38, "edgecolor": "white"})
ax.set_title("Owner Type — Share of All Owners", fontweight="bold")
plt.tight_layout()
plt.savefig("07_donut.png", dpi=150)
