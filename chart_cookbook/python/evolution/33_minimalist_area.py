"""Minimalist two-color area chart (Joseph Barbier "Japan population" style).
One line + filled area, split into a green segment (positive) and a red segment
(negative) around a zero baseline, with the axes stripped off, min/max callouts,
inline year labels down the middle, a highlight_text title/subtitle, and a
drawarrow arrow to the turning point. Real Davidson data: the year-over-year
change in corporate SFR acquisitions — the buying spree builds, then reverses
after 2021."""
import matplotlib; matplotlib.use("Agg")
import os, json, collections
import numpy as np
import matplotlib.pyplot as plt

# graceful fallbacks for the optional font/annotation libraries
try:
    from pyfonts import load_google_font
    FONT = load_google_font("Libre Baskerville")
    BOLD = load_google_font("Libre Baskerville", weight="bold")
    DIGIT = load_google_font("Lato", weight="bold")
except Exception:
    FONT = BOLD = DIGIT = None
def fp(f):  # font kwarg helper
    return {"font": f} if f is not None else {}
try:
    from highlight_text import fig_text, ax_text
    HL = True
except Exception:
    HL = False
try:
    from drawarrow import ax_arrow
    ARROW = True
except Exception:
    ARROW = False

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
props = [f["properties"] for f in
         json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))["features"]]
by_year = collections.Counter()
for p in props:
    a = str(p.get("acq", ""))[:4]
    if a.isdigit() and 2013 <= int(a) <= 2025:
        by_year[int(a)] += 1
years = sorted(by_year)
counts = [by_year[y] for y in years]
# year-over-year change (delta): positive = accelerating, negative = pulling back
xs = np.array(years[1:], dtype=float)
dv = np.diff(counts).astype(float)
# start of the longest run of down-years = when the pullback set in
neg = dv < 0
best_len = best_start = run_len = run_start = 0
for i, v in enumerate(neg):
    if v:
        if run_len == 0: run_start = i
        run_len += 1
        if run_len > best_len: best_len, best_start = run_len, run_start
    else:
        run_len = 0
flag_year = int(xs[best_start])

GREEN, RED = "#335c67", "#9e2a2b"
fig, ax = plt.subplots(dpi=200, figsize=(10, 7))
ax.set_axis_off()

# smooth line, then two-color fill by sign of the value (the tutorial's core idea)
ax.plot(xs, dv, color="#333333", lw=1.4, zorder=3)
ax.fill_between(xs, dv, 0, where=dv >= 0, interpolate=True, alpha=0.35, color=GREEN)
ax.fill_between(xs, dv, 0, where=dv < 0, interpolate=True, alpha=0.35, color=RED)

imax = int(np.argmax(dv)); imin = int(np.argmin(dv))
ax.scatter(xs[imax], dv[imax], color=GREEN, s=20)
ax.text(xs[imax] - 0.3, dv[imax] + 25, f"+{dv[imax]:.0f}", size=8, color=GREEN, ha="right", **fp(DIGIT))
ax.scatter(xs[imin], dv[imin], color=RED, s=20)
ax.text(xs[imin], dv[imin] - 60, f"{dv[imin]:.0f}", size=8, color=RED, ha="center", **fp(DIGIT))
ax.plot([xs[0], xs[-1]], [0, 0], color="black", lw=0.6)
for y in xs:
    ax.text(y, 25, f"{int(y)}", size=7, ha="center", **fp(BOLD))

if HL:
    fig_text(0.13, 0.86, "Corporate buying went\ninto <reverse> after 2021",
             highlight_textprops=[{"font": BOLD, "color": RED}] if BOLD else [{"color": RED}],
             fontsize=22, ha="left", va="top", **fp(FONT))
    fig_text(0.13, 0.70, "Year-over-year change in corporate SFR acquisitions, Davidson County",
             fontsize=10, ha="left", va="top", alpha=0.55, **fp(FONT))
    ax_text(xs[0], min(dv) - 120, "<Data>: Davidson County parcel records\n<Graph>: Who Owns Nashville",
            ax=ax, fontsize=6, ha="left",
            highlight_textprops=[{"font": BOLD}] * 2 if BOLD else [{}, {}], **fp(FONT))
else:
    ax.set_title("Corporate buying went into reverse after 2021", fontsize=16, color=RED, loc="left")

if ARROW:
    ax_arrow(tail_position=(flag_year + 1.4, -260),
             head_position=(flag_year, -20), ax=ax,
             color="black", width=0.5, head_width=2, head_length=5, radius=-0.25)
    ax.text(flag_year + 1.5, -300, f"{flag_year}: the pace of\nbuying first fell",
            fontsize=8, ha="left", **fp(FONT))

plt.savefig(os.path.join(os.path.dirname(__file__), "33_minimalist_area.png"),
            dpi=200, bbox_inches="tight")
print("wrote 33_minimalist_area.png  (turn=%d, max=+%d, min=%d)"
      % (flag_year, dv[imax], dv[imin]))
