"""morethemes demo — the same bar chart in four report-grade themes.
Run: python styles/morethemes_demo.py  ->  figures/morethemes_demo.png
morethemes ships 17 themes (mt.ALL_THEMES): economist, wsj, ft, nord,
lumen, minimal, urban, nature, ... Fonts fall back to defaults if the
theme's font isn't installed locally."""
import matplotlib; matplotlib.use("Agg")
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import matplotlib.pyplot as plt
import morethemes as mt

ops = ["Progress", "AMH", "Amherst", "Regent"]; parcels = [1215, 1182, 699, 642]
themes = ["economist", "wsj", "ft", "lumen"]
fig, axes = plt.subplots(2, 2, figsize=(11, 7))
for ax, name in zip(axes.flat, themes):
    with plt.rc_context(mt.get_rcparams(name)):
        ax.bar(ops, parcels, color=plt.rcParams["axes.prop_cycle"].by_key()["color"][:4])
        ax.set_title(f"morethemes: {name}", fontweight="bold")
        ax.set_facecolor(plt.rcParams["axes.facecolor"])
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)
fig.suptitle("morethemes — report-grade matplotlib themes", fontsize=13, fontweight="bold")
plt.tight_layout(rect=[0, 0, 1, .97])
plt.savefig(os.path.join(os.path.dirname(__file__), "..", "figures", "morethemes_demo.png"), dpi=130)
print("wrote figures/morethemes_demo.png")
