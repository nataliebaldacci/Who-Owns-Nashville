#!/usr/bin/env python3
"""
Discover U.S. localities with long-term residential rental licensing /
registration / proactive-inspection programs by searching the five big
municipal-code libraries plus city websites.

Strategy: every codified ordinance lives on a handful of hosts
(library.municode.com, ecode360.com, codelibrary.amlegal.com,
codebook.codepublishing.com). Running phrase searches scoped to those hosts is
effectively a national ordinance scan, and the result URL itself names the
municipality. Results land in a CSV of *candidates* — each row still needs the
verification checklist in METHODOLOGY.md before you cite it.

Run this on your own machine (the repo build environment has no open network):

    pip install requests beautifulsoup4
    python scrape_rental_license_cities.py discover -o candidates.csv
    python scrape_rental_license_cities.py probe cities.csv -o probed.csv

Modes:
  discover            dork every search term against every code-library host
  probe CITIES.CSV    for a list of cities (columns: city,state), search each
                      for a rental license/registration page on official sites

Search backends, tried in order:
  1. Google Programmable Search (reliable; set GOOGLE_API_KEY and GOOGLE_CSE_ID,
     free tier 100 queries/day, https://programmablesearchengine.google.com)
  2. DuckDuckGo HTML endpoint (no key; rate-limit yourself or it will block)

Endpoints and page structure drift; if parsing breaks, check the HTML in a
browser and adjust the selectors below.
"""

import argparse
import csv
import os
import re
import sys
import time
import urllib.parse

import requests

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("pip install requests beautifulsoup4")

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

# Vocabulary from METHODOLOGY.md §1 — different program models use different
# terms, so all of them must be searched. Ordered roughly by yield.
TERMS = [
    '"residential rental license"',
    '"rental dwelling license"',
    '"rental housing license"',
    '"rental license" inspection',
    '"rental registration program"',
    '"rental registry"',
    '"landlord registration"',
    '"proactive rental inspection"',
    '"rental inspection program"',
    '"systematic code enforcement"',
    '"certificate of rental suitability"',
    '"residential occupancy permit"',
    '"certificate of compliance" rental dwelling',
    '"fire certificate of occupancy" rental',
]

# Host-scoped dorks. The URL patterns let us pull muni + state straight out of
# the result link without fetching the page (except eCode360, whose URLs are
# opaque IDs — we fall back to the result title).
CODE_HOSTS = {
    "library.municode.com": re.compile(
        r"library\.municode\.com/([a-z]{2})/([^/]+)/"),
    "ecode360.com": None,  # opaque /XX1234 ids; muni name comes from title
    "codelibrary.amlegal.com": re.compile(
        r"codelibrary\.amlegal\.com/codes/([^/]+)/"),
    "codebook.codepublishing.com": re.compile(
        r"codebook\.codepublishing\.com/([A-Z]{2})/([^/]+)/"),
}

STR_NOISE = re.compile(r"short.?term|vacation rental|airbnb|transient", re.I)


def google_cse(query, key, cse_id, num=10):
    r = requests.get(
        "https://www.googleapis.com/customsearch/v1",
        params={"key": key, "cx": cse_id, "q": query, "num": num},
        timeout=30,
    )
    r.raise_for_status()
    return [(i.get("title", ""), i.get("link", ""), i.get("snippet", ""))
            for i in r.json().get("items", [])]


def ddg_html(query):
    r = requests.post(
        "https://html.duckduckgo.com/html/",
        data={"q": query},
        headers={"User-Agent": UA},
        timeout=30,
    )
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    out = []
    for res in soup.select(".result"):
        a = res.select_one("a.result__a")
        if not a:
            continue
        href = a.get("href", "")
        # DDG wraps links as /l/?uddg=<encoded>
        m = re.search(r"uddg=([^&]+)", href)
        if m:
            href = urllib.parse.unquote(m.group(1))
        snip = res.select_one(".result__snippet")
        out.append((a.get_text(" ", strip=True), href,
                    snip.get_text(" ", strip=True) if snip else ""))
    return out


def search(query):
    key, cse = os.getenv("GOOGLE_API_KEY"), os.getenv("GOOGLE_CSE_ID")
    if key and cse:
        try:
            return google_cse(query, key, cse)
        except Exception as e:
            print(f"  google cse failed ({e}); falling back to ddg",
                  file=sys.stderr)
    return ddg_html(query)


def muni_from_url(url, title):
    """Return (state, municipality) best guess from a code-library URL."""
    for host, pat in CODE_HOSTS.items():
        if host not in url:
            continue
        if pat:
            m = pat.search(url)
            if m:
                g = m.groups()
                if host == "codelibrary.amlegal.com":
                    return ("", g[0].replace("_", " ").title())
                return (g[0].upper(), g[1].replace("_", " ").title())
        # eCode360 and pattern misses: titles look like
        # "Rental Property | Town of Penn, PA" or "City of X, NY ..."
        m = re.search(r"(?:of|Of)\s+([A-Z][\w .'-]+?),\s*([A-Z]{2})\b", title)
        if m:
            return (m.group(2), m.group(1).strip())
        return ("", title[:60])
    return None


def discover(out_path, limit, sleep):
    seen, rows = set(), []
    queries = [f"site:{h} {t}" for h in CODE_HOSTS for t in TERMS]
    if limit:
        queries = queries[:limit]
    print(f"{len(queries)} queries")
    for q in queries:
        print(f"> {q}")
        try:
            results = search(q)
        except Exception as e:
            print(f"  search failed: {e}", file=sys.stderr)
            time.sleep(sleep * 3)
            continue
        for title, url, snippet in results:
            if STR_NOISE.search(title + " " + snippet):
                continue
            hit = muni_from_url(url, title)
            if not hit:
                continue
            state, muni = hit
            k = (state, muni.lower())
            if k in seen:
                continue
            seen.add(k)
            rows.append({"state": state, "municipality": muni,
                         "matched_term": q, "title": title, "url": url,
                         "snippet": snippet[:300]})
        time.sleep(sleep)
    write_csv(out_path, rows,
              ["state", "municipality", "matched_term", "title", "url",
               "snippet"])
    print(f"{len(rows)} candidate municipalities -> {out_path}")


def probe(cities_path, out_path, sleep):
    rows = []
    with open(cities_path, newline="", encoding="utf-8") as f:
        cities = list(csv.DictReader(f))
    for c in cities:
        city, state = c["city"], c["state"]
        q = (f'"{city}" "{state}" ("rental license" OR "rental registration" '
             f'OR "rental inspection program")')
        print(f"> {city}, {state}")
        try:
            results = search(q)
        except Exception as e:
            print(f"  search failed: {e}", file=sys.stderr)
            time.sleep(sleep * 3)
            continue
        best = next(
            (r for r in results
             if re.search(r"\.gov|\.us|municode|ecode360|amlegal|"
                          r"codepublishing", r[1])
             and not STR_NOISE.search(r[0] + r[2])),
            None)
        rows.append({"city": city, "state": state,
                     "evidence_title": best[0] if best else "",
                     "evidence_url": best[1] if best else "",
                     "snippet": (best[2][:300] if best else ""),
                     "has_candidate": "Y" if best else "N"})
        time.sleep(sleep)
    write_csv(out_path, rows,
              ["city", "state", "has_candidate", "evidence_title",
               "evidence_url", "snippet"])
    print(f"{len(rows)} cities probed -> {out_path}")


def write_csv(path, rows, fields):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    sub = p.add_subparsers(dest="mode", required=True)
    d = sub.add_parser("discover", help="dork code libraries for programs")
    d.add_argument("-o", "--out", default="candidates.csv")
    d.add_argument("--limit", type=int, default=0,
                   help="cap number of queries (for testing)")
    pr = sub.add_parser("probe", help="check a specific list of cities")
    pr.add_argument("cities", help="CSV with columns: city,state")
    pr.add_argument("-o", "--out", default="probed.csv")
    p.add_argument("--sleep", type=float, default=4.0,
                   help="seconds between queries (be polite; DDG blocks fast "
                        "clients)")
    a = p.parse_args()
    if a.mode == "discover":
        discover(a.out, a.limit, a.sleep)
    else:
        probe(a.cities, a.out, a.sleep)


if __name__ == "__main__":
    main()
