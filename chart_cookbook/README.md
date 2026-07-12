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

- **Maps** (`map/`) need `geopandas` (`pip install geopandas`) and point at the
  GeoJSON layers already in the repo root (e.g.
  `Davidson_Institutional_Pct_by_Tract.geojson`, `Davidson_County_Boundary.geojson`).
- **Sankey** PNG export needs `kaleido` (`pip install kaleido`); without it the
  script still writes the interactive `.html`.
- Colors use the Who Owns Nashville palette (navy `#1c458c`, gold `#f0af1e`,
  blue `#4fa0bd`) plus the stable per-operator qualitative set.
- Chart styles are inspired by the Python Graph Gallery; the code here is
  original and uses this project's data and palette.
