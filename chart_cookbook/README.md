# chart_cookbook

A reference library of chart styles, in the spirit of the
[Python Graph Gallery](https://python-graph-gallery.com/), organized by the
gallery's categories and pre-loaded with **Who Owns Nashville sample data** so
each script runs on its own. Swap the sample `DataFrame` in any script for your
real data (e.g. `owner_leaderboard.json`, the tract GeoJSONs) to make a
publication figure.

Two flavors are included:

- **`python/`** — matplotlib / seaborn / plotly scripts that render a PNG (or an
  HTML for the interactive Sankey). Best for static figures and reports.
- **`chartjs/`** — the native-to-Chart.js types rebuilt in the HUD-style boxes,
  matching the interactive charts already used across the site. Open
  `chartjs/index.html` in a browser.

## Layout

```
chart_cookbook/
  python/
    ranking/        01_barplot  02_horizontal_barplot  03_lollipop  04_cleveland_dotplot
    part_of_whole/  05_stacked_barplot  06_treemap  07_donut
    evolution/      08_line  09_area  10_stacked_area
    distribution/   11_histogram  12_density_kde  13_boxplot  14_violin
    correlation/    15_scatter  16_bubble  17_correlogram_heatmap
    map/            18_choropleth  19_bubble_map        (need geopandas)
    flow/           20_sankey_plotly                    (plotly; PNG needs kaleido)
  chartjs/
    index.html      6 rebuilt in Chart.js (bar, horizontal bar, line+area,
                    stacked bar, bubble, doughnut)
  figures/
    cookbook_preview.png   contact sheet of all rendered Python figures
```

## House styles (color systems)

`styles/won_styles.py` holds four palettes you can drop onto any script. Call
`apply_style(name)` before creating the figure:

```python
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from styles.won_styles import apply_style, palette
apply_style("jchs")     # "won" | "hud" | "jchs" | "crs"
```

| Style | Colors | Source |
|---|---|---|
| `won`  | navy `#1c458c`, gold `#f0af1e`, blue `#4fa0bd` | Who Owns Nashville brand |
| `hud`  | HUD default-theme series | HUD county charts |
| `jchs` | slate `#508DA6`, burnt orange `#C14D00`, sage `#76AD99`, mustard `#E9C002`, plum `#653052` | Harvard Joint Center (State of the Nation's Housing) |
| `crs`  | steel blue `#2E75B6`, orange `#ED7D31`, grey, gold; tan `#D2D1AB` for stock bars | Congressional Research Service report figures |

`RAMPS` also holds JCHS + WON sequential ramps for choropleths. Run
`python style_showcase.py` to see the same charts in all styles side by side
(`figures/style_showcase.png`).

**CRS report figures** (`python/crs_reports/`) rebuild three signature CRS
looks: `crs_total_housing_units` (tan bars + blue ratio line, dual axis),
`crs_new_vs_existing` (stacked bars), and `crs_starts_by_type` (stacked area).

## Color-scheme libraries (thousands of palettes)

Beyond the four house styles, `styles/palettes.py` gives one call, `get()`,
that resolves any palette name across every major library:

```python
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from styles.palettes import get, CURATED
get("jchs")              # cookbook house style
get("Category10")        # Bokeh categorical
get("Set2", n=8)         # ColorBrewer (palettable)
get("Bold", n=10)        # CARTOColors (palettable)
get("Thermal", n=7)      # cmocean sequential (palettable)
get("viridis", n=6)      # any matplotlib colormap, sampled
get("Acadia")            # any of pypalettes' 2,500+ palettes
```

Resolution order: house styles → Bokeh → matplotlib colormap → palettable
(searched across ColorBrewer / CARTOColors / cmocean / Scientific / Tableau /
Wes Anderson / cubehelix) → pypalettes. `CURATED` maps housing tasks to good
picks (categorical operators, sequential choropleth, diverging change).

Browse them:
- `python styles/palette_reference.py` → `figures/palette_reference.png`
  (swatch sheet: house styles, categorical, sequential, diverging).
- `python styles/morethemes_demo.py` → `figures/morethemes_demo.png`
  (report-grade matplotlib themes: economist, wsj, ft, lumen …).

Install the libraries with `pip install -r requirements.txt` (palettable,
pypalettes, morethemes). Bokeh's Category10/20 are hardcoded, so bokeh itself
isn't required. `pyfonts` and `drawarrow` are optional (fonts / annotation
arrows) and listed commented-out in requirements.

## Running the Python scripts

```bash
pip install -r requirements.txt
cd python/ranking
python 01_barplot.py        # writes 01_barplot.png next to the script
```

Each script is standalone. The generated PNGs/HTML are git-ignored (they
regenerate on run); the contact sheet in `figures/` is committed as a preview.

## Which chart for which job

| Category       | Question it answers                        | Types here |
|----------------|--------------------------------------------|------------|
| Ranking        | Who has the most?                          | bar, horizontal bar, lollipop, Cleveland dot |
| Part of whole  | How is the total split?                    | stacked bar, treemap, donut |
| Evolution      | How did it change over time?               | line, area, stacked area |
| Distribution   | What's the spread of one variable?         | histogram, density, box, violin |
| Correlation    | How do two/three variables relate?         | scatter, bubble, correlogram |
| Map            | Where is it, geographically?               | choropleth, bubble map |
| Flow           | How does volume move between stages?        | Sankey |

## Notes

- **Maps** (`map/`) are wired to the repo's real GeoJSONs:
  - `18_choropleth.py` — static geopandas choropleth of institutional % by tract
    (JCHS orange ramp, quantile classes) from `Davidson_Institutional_Pct_by_Tract.geojson`.
  - `19_bubble_map.py` — block-group centroids sized by institutional count over
    the county outline.
  - `27_folium_choropleth.py` — interactive Leaflet map with hover tooltips -> HTML.
  - `29_bokeh_choropleth.py` — interactive Bokeh choropleth (LinearColorMapper +
    HoverTool; swap in `LogColorMapper` for skewed data) -> self-contained HTML.
  Need `geopandas folium mapclassify bokeh` (in requirements).
  - `32_palette_gallery.py` — the SAME block-group breakdown across ~36
    popular palettes (cmocean / CARTOColors / Scientific / ColorBrewer +
    matplotlib/seaborn); switch `BOUNDARY` to "block" for the finest cut.
  - `33_atlanta_style_choropleth.py` — dark-basemap tract choropleth (plasma
    bins, styled legend, scale bar); optional contextily dark tiles.
  - `34_folium_dark_interactive.py` — interactive Leaflet map (CartoDB dark
    tiles + hover), matching the site's ACS maps.
- **Boundary layers** — `styles/boundaries.py` registers every Davidson geography
  in the repo (census `tract` / `blockgroup`, plus local `community` /
  `council` / `zip`) and offers `aggregate_points(points, boundary)` to spatial-
  join any point layer onto any boundary and choropleth the result:
  - `30_boundaries_overview.py` — all five boundary sets side by side.
  - `31_choropleth_by_zip.py` — corporate parcels aggregated to ZIP codes.
- **Sankey** PNG export needs `kaleido` (`pip install kaleido`); without it the
  script still writes the interactive `.html`.
- Colors use the Who Owns Nashville palette (navy `#1c458c`, gold `#f0af1e`,
  blue `#4fa0bd`) plus the stable per-operator qualitative set.
- Chart styles are inspired by the Python Graph Gallery; the code here is
  original and uses this project's data and palette.
