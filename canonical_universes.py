"""Who Owns Nashville — canonical universes and measures (machine-readable).

The single source of truth for how datasets are cut. Narrative spec: UNIVERSE.md.
Three universes (U1 framework / U2 developable / U3 deeds) share three measures
(M1 ownership type / M2 ZIP-occupancy & geography / M3 operator attribution).

    from canonical_universes import WHERE, is_entity, classify_owner, zip_match
    WHERE["framework"]                  # verbatim county where-clause
    classify_owner("MCH SFR NASHVILLE LLC")   # -> 'Entity'
    zip_match("37211", "37211")               # -> True (owner-occupied proxy)

Snapshot of record: July 6, 2026.
"""

# ---- Stage 1: sources -------------------------------------------------------
ENDPOINTS = {
    "cadastral": ("https://maps.nashville.gov/arcgis/rest/services/"
                  "Cadastral/Cadastral_Layers/MapServer/4"),
    "deeds": ("https://maps.nashville.gov/arcgis2/rest/services/"
              "Parcels/ParcelHistory/MapServer/2"),
    # per-parcel enrichment & cross-checks (SOAP): assessment history,
    # building characteristics, sales — NOT a universe, a verification source
    "parcel_service": "https://maps.nashville.gov/ParcelService/Search.asmx?WSDL",
}

# ---- Stage 2: universes (verbatim where-clauses) ----------------------------
# NB: the county stores unclassified land use as the literal string 'NULL'.
_USE_LIST = "('NULL','SINGLE FAMILY','ZERO LOT LINE','DUPLEX','RESIDENTIAL CONDO')"
_FEATURE_EXCL = "('Multistory Condo','Multistory Common Area','Open Space')"

WHERE = {
    # U1 — existing 1-2 unit homes (21st Century Housing Act framework)
    "framework": (
        f"(ducount = 1 OR ducount = 2) AND ludesc IN {_USE_LIST} "
        f"AND featuretype NOT IN {_FEATURE_EXCL}"
    ),
    # U2 — U1 plus vacant land (BTR / land-banking). LIKE 'VACANT%' also catches
    # the county's misspelling 'VACANT RESIENTIAL LAND' (~60 parcels).
    "developable": (
        f"(((ducount = 1 OR ducount = 2) AND ludesc IN {_USE_LIST}) "
        f"OR ludesc LIKE 'VACANT%') "
        f"AND featuretype NOT IN {_FEATURE_EXCL}"
    ),
    # U3 — every deed event (filterless at the universe level; measures below
    # are applied per event). Source: ENDPOINTS['deeds'].
    "deeds": "1=1",
}

EXPECTED = {   # July 6, 2026 snapshot — drift alarms, not gospel
    "all_parcels": 286_721,
    "framework": 205_933,
    "framework_entity": 16_769,       # M1 entity on U1 (funnel's 15-token query)
    "framework_out_of_state": 11_929,
    "framework_non_owner_occ": 42_632,
    "deed_events": 1_641_434,
    "deed_events_corporate": 199_158,  # M1 (23-token list) on U3
}

# Materialized U1 file of record (derive_canonical_framework.py on the
# 2026-07-07 baseline; fixed canonical classifier). The +134 vs the county's
# 205,933 is one-day snapshot drift; class deltas vs the funnel's published
# split are classifier-choice residue (funnel used the 15-token list and a
# looser bank test) — THESE are the authoritative local numbers.
CANONICAL_U1 = {
    "file": "Nashville_Framework_Homes_CANONICAL_2026-07-07.parquet",
    "rows": 206_067,
    "owner_split": {"Individual": 173_132, "Entity": 16_567, "Trust": 15_944,
                    "Government": 377, "Bank-Lender": 47},
    "landuse": {"SINGLE FAMILY": 156_644, "RESIDENTIAL CONDO": 36_936,
                "DUPLEX": 7_068, "ZERO LOT LINE": 5_419},
}

# ---- Stage 3 / M1: ownership type -------------------------------------------
# Canonical (Historical_Owners superset). The funnel's live query used a
# 15-token subset; new cuts use this list. Tokens with spaces/dots are
# significant ('% CO %' avoids matching COURT etc.).
ENTITY_TOKENS = [
    "LLC", "LLP", " LP", "L.P", " INC", "CORP", "LTD", "LIMITED",
    " CO ", "CO.", "COMPANY", "PARTNER", "ASSOC", "HOMES", "HOLDING",
    "CAPITAL", "INVEST", "FUND", "SOLUTION", "SFR", "ASSET", "BORROW", " JV",
]
# Word-boundary matters: tokens are matched inside a space-padded name, so
# " HUD " cannot hit HUDSON/HUDMON surnames and " BANK " cannot hit BANKS/
# EUBANKS (bugs surfaced by the 2026-07-13 baseline reconciliation).
GOVERNMENT_TOKENS = ["CITY OF", "HOUSING AUTH", "STATE OF", "COUNTY OF",
                     " HUD ", "MDHA", "UNITED STATES", "METROPOLITAN GOV",
                     "METRO GOV", "SECRETARY OF", "VETERANS AFFAIRS"]
# COMMUNITY PROPERTY (with or without the often-truncated 'TRUST') is a marital
# trust arrangement -> Trust; ' TR ' catches the county's clipped 'REV LIVING TR'.
TRUST_TOKENS = ["TRUST", "TRUSTEE", "REVOCABLE", "LIVING TR", "FAMILY TR",
                " TR ", "COMMUNITY PROPERTY"]
BANK_TOKENS = [" BANK ", "MORTGAGE", "LENDER", "FEDERAL NATIONAL",
               "FANNIE MAE", "FREDDIE MAC", "FEDERAL HOME LOAN"]


def _norm(name):
    """County-style normalization: uppercase, punctuation to spaces, padded."""
    out = "".join(c if c.isalnum() or c == "." else " " for c in (name or "").upper())
    return f" {' '.join(out.split())} "


def classify_owner(name):
    """M1: Individual / Entity / Trust / Bank-Lender / Government."""
    n = _norm(name)
    if any(t in n for t in GOVERNMENT_TOKENS):
        return "Government"
    if any(t in n for t in TRUST_TOKENS):
        return "Trust"
    if any(t in n for t in BANK_TOKENS):
        return "Bank-Lender"
    if any((t if t.strip(" .") != t else t) in n or t in n for t in ENTITY_TOKENS):
        return "Entity"
    return "Individual"


def is_entity(name):
    """M1 shorthand: business entity (not gov / trust / bank)."""
    return classify_owner(name) == "Entity"


# ---- Stage 3 / M2: occupancy & geography ------------------------------------
DAVIDSON_ZIPS = {"37013", "37072", "37076", "37080", "37115", "37138", "37189",
                 "37228"} | {f"372{i:02d}" for i in range(1, 22)}  # 37201-37221


def zip_match(owner_zip, parcel_zip):
    """Owner-occupancy proxy: owner mailing ZIP equals parcel ZIP (first 5)."""
    a, b = str(owner_zip or "")[:5], str(parcel_zip or "")[:5]
    return bool(a) and a == b


def is_out_of_county(owner_zip):
    return str(owner_zip or "")[:5] not in DAVIDSON_ZIPS


def is_out_of_state(state_code):
    return (state_code or "").strip().upper() != "TN"


# ---- Stage 4 / M3: operator attribution --------------------------------------
# The shell-resolution chain lives in the pipeline (see
# Methodology_Corporate_Landlords.html). Vocabulary rule enforced here:
INSTITUTIONAL_MEANS = ("attributed to a named operator via the resolution "
                       "chain (M3); NEVER a raw M1 entity count")


if __name__ == "__main__":
    tests = [
        ("MCH SFR NASHVILLE LLC", "Entity"),
        ("PROGRESS RESIDENTIAL BORROWER 7, LLC", "Entity"),
        ("AMH 2015-2 BORROWER LLC", "Entity"),
        ("SMITH, JOHN & MARY", "Individual"),
        ("SMITH FAMILY TRUST", "Trust"),
        ("METROPOLITAN GOVERNMENT OF NASHVILLE", "Government"),
        ("FIRST HORIZON BANK", "Bank-Lender"),
        ("JONES LIVING TR", "Trust"),
        ("OPENDOOR PROPERTY TRUST I", "Trust"),   # known edge: trust token wins
        ("YAMASA CO., LTD", "Entity"),
        # regression cases from the 2026-07-13 baseline reconciliation
        ("HUDSON SFR PROPERTY HOLDINGS II LLC", "Entity"),
        ("HUDSON TAYLOR & MADISON", "Individual"),
        ("HUDSON FAMILY TRUST", "Trust"),
        ("HUDMON STANTON CHARLES", "Individual"),
        ("BANKS DANIEL & KRISTEN", "Individual"),
        ("EUBANKS BRYSON NICHOLAS & HUNT MILLER", "Individual"),
        ("FIRST HORIZON BANK", "Bank-Lender"),
        ("SECRETARY OF VETERANS AFFAIRS", "Government"),
        ("SECRETARY OF HOUSING AND URBAN DEVELOPME", "Government"),
        ("LAIRD COMMUNITY PROPERTY TRUST", "Trust"),
        ("BLUMENTHAL TENNESSEE COMMUNITY PROPERTY", "Trust"),
        ("THOMAS JEFF & MARY FAMILY REV LIVING TR", "Trust"),
        ("CRESPO FREDDIE O & KAREN A TRUSTEES", "Trust"),
        ("TRACELAND FARM LP", "Entity"),
        ("NASHBORO VILLAGE NINETEEN CONDOMINIUM ASSOCIATION", "Entity"),
        ("NASHVILLE METRO HOLDINGS LLC", "Entity"),
        ("DANG HAI & TRAN LOAN ANH", "Individual"),
        ("FEDERAL HOME LOAN MORTGAGE CORP", "Bank-Lender"),
        ("METROPOLITAN GOVERNMENT OF NASHVILLE", "Government"),
    ]
    ok = True
    for name, want in tests:
        got = classify_owner(name)
        flag = "" if got == want else "  <-- MISMATCH"
        if got != want:
            ok = False
        print(f"{name:45} -> {got:12} (want {want}){flag}")
    print()
    print("zip_match('37211','37211') ->", zip_match("37211", "37211"))
    print("is_out_of_county('30303')  ->", is_out_of_county("30303"))
    print("is_out_of_state('AZ')      ->", is_out_of_state("AZ"))
    print("37205 in DAVIDSON_ZIPS     ->", "37205" in DAVIDSON_ZIPS)
    print("\nWHERE['framework'] =", WHERE["framework"][:80], "...")
    print("self-test:", "PASS" if ok else "SEE MISMATCHES ABOVE")
