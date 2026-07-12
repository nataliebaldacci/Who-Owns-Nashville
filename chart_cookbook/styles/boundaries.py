"""
Registry of Davidson County boundary layers available in the repo, so any
cookbook map can aggregate a metric to whichever geography you need.

    from styles.boundaries import load, BOUNDARIES, aggregate_points
    zips = load("zip")                       # GeoDataFrame (EPSG:4326)
    gdf  = aggregate_points("Davidson_Corporate_Ownership_CLEAN.geojson", "zip")
"""
import os
import geopandas as gpd

_ROOT = os.path.join(os.path.dirname(__file__), "..", "..")

# name -> (geojson file, unique-id field, human label field)
BOUNDARIES = {
    "county":     ("Davidson_County_Boundary.geojson",           "OBJECTID",        "OBJECTID"),
    "tract":      ("Davidson_Institutional_Pct_by_Tract.geojson","GEOCODE",         "TRACTCE"),
    "blockgroup": ("institutional_by_blockgroup.geojson",        "bg",              "bg"),
    "community":  ("Davidson_Community_Planning_Areas.geojson",  "CommunityNumber", "CommunityName"),
    "council":    ("Davidson_Council_Districts.geojson",         "DISTRICT",        "DistrictName"),
    "zip":        ("Davidson_Zipcodes.geojson",                  "ZipCode",         "POName"),
}


def path(name):
    return os.path.join(_ROOT, BOUNDARIES[name][0])


def load(name):
    """Load a boundary layer as a GeoDataFrame in EPSG:4326."""
    return gpd.read_file(path(name)).to_crs(4326)


def aggregate_points(points_geojson, boundary, how="count", value=None):
    """Spatial-join a point layer onto a boundary and return the boundary
    GeoDataFrame with an added 'metric' column (count of points per area, or
    mean/sum of `value`). `points_geojson` is a filename in the repo root."""
    bnd = load(boundary)
    idf, lab = BOUNDARIES[boundary][1], BOUNDARIES[boundary][2]
    pts = gpd.read_file(os.path.join(_ROOT, points_geojson)).to_crs(4326)
    joined = gpd.sjoin(pts, bnd[[idf, lab, "geometry"]], predicate="within", how="inner")
    if how == "count":
        agg = joined.groupby(idf).size().rename("metric")
    else:
        agg = getattr(joined.groupby(idf)[value], how)().rename("metric")
    out = bnd.merge(agg, on=idf, how="left")
    out["metric"] = out["metric"].fillna(0)
    return out
