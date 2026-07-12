"""Table with great_tables (python-graph-gallery great_tables chapter). The gt-
inspired API builds a titled, footnoted, cell-highlighted table and exports it as
a self-contained HTML (and PNG when a Chromium/webshot backend is available).
Shows title/subtitle (tab_header), a source note in markdown (tab_source_note),
per-column formatting (fmt_number / fmt_percent), a spanner, and a highlighted
top cell. Real data: the largest Davidson operators (owner_leaderboard.json)."""
import os, json
import pandas as pd
from great_tables import GT, md, style, loc

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
rows = json.load(open(os.path.join(ROOT, "owner_leaderboard.json")))["rows"][:10]
df = pd.DataFrame([{
    "Operator": r["nm"],
    "Parcels": r["n"],
    "Units": r.get("du", 0),
    "OOS": r.get("oos_n", 0) / max(r["n"], 1),   # fraction -> fmt_percent
    "AvgValue": r.get("val", 0) / max(r["n"], 1),
} for r in rows])

gt = (
    GT(df, rowname_col="Operator")
    .tab_header(title="Largest corporate operators in Davidson County",
                subtitle="Single-family holdings, ranked by parcels")
    .tab_spanner(label="Holdings", columns=["Parcels", "Units"])
    .tab_spanner(label="Profile", columns=["OOS", "AvgValue"])
    .fmt_number(columns=["Parcels", "Units"], decimals=0, use_seps=True)
    .fmt_percent(columns="OOS", decimals=0)
    .fmt_currency(columns="AvgValue", currency="USD", decimals=0)
    .cols_label(OOS="Out-of-state", AvgValue="Avg. value")
    .data_color(columns="Parcels", palette=["#eff3ff", "#08519c"])
    .tab_source_note(source_note=md("**Source:** Who Owns Nashville, Davidson County "
                                    "parcel and assessor records"))
    .tab_style(style=style.fill(color="#fff3cd"),
               locations=loc.body(rows=[0]))
    .tab_options(table_font_size="13px", heading_title_font_size="18px")
)

HERE = os.path.dirname(__file__)
html = os.path.join(HERE, "04_great_tables.html")
open(html, "w").write(gt.as_raw_html())
print("wrote 04_great_tables.html  (open in a browser; or `gt.gtsave(...)` "
      "with a Chromium backend to get a PNG)")
