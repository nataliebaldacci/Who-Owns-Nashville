# Finding Cities with Long-Term Residential Rental Licensing Programs

**Goal:** Build a national inventory of localities that license, register, or
proactively inspect *long-term* residential rentals (the Chester, PA model —
not short-term/Airbnb permitting).

Seeded 2026-07. Companion files:

- `cities_rental_licensing_seed.csv` — starter dataset (~40 programs, each with a source URL and a `verify` flag)
- `scrape_rental_license_cities.py` — discovery scraper (run locally; this repo's build environment blocks outbound fetches)
- `../Rental_License_Programs_Nationwide.html` — rendered reference page

---

## 1. Taxonomy — know what you're looking for

Programs fall into four models. Ordinances use wildly different vocabulary, so
searching for one phrase ("rental license") misses most of them.

| Model | What it is | Typical vocabulary |
|---|---|---|
| **Rental licensing** | A revocable license is a *precondition* to renting; denial/revocation is the enforcement lever (Chester, Minneapolis, Baltimore, Denver) | "rental license", "rental dwelling license", "residential rental license", "rental housing license", "business license — rental" |
| **Registration/registry** | Owner must file contact + unit info; usually no pass/fail gate (NYC HPD, Portland, Spokane, Nashville's § 16.24.030) | "rental registration", "rental registry", "landlord registration", "property registration" |
| **Periodic inspection / certificate** | Recurring code inspection produces a certificate of occupancy/compliance for rentals (Rochester NY, Ann Arbor, St. Paul, LA SCEP) | "certificate of occupancy — rental", "certificate of compliance", "proactive rental inspection", "systematic code enforcement", "rental inspection program", "residential occupancy permit", "fire certificate of occupancy" |
| **State-level programs** | Statewide registration/licensing/inspection (NJ landlord registration + 5-yr multiple-dwelling inspections; FL DBPR apartment licensing; TN § 66-28-107 for Davidson Co.) | statutes, not ordinances |

Exclude: short-term rental permits, rent-control registries *alone* (though LA,
Berkeley, SF pair them with inspection programs worth capturing).

## 2. Fastest route: mine the aggregators first

Someone has already surveyed much of this. Harvest their city lists before
scraping anything:

1. **Local Housing Solutions** — policy library page "Rental registries" and the
   case study "Exploring Rental Registries Across U.S. Localities"
   (localhousingsolutions.org). Names cities and design details.
2. **National League of Cities** — Local Policy Hub, "Proactive Rental
   Inspection" page (nlc.org): city examples with ordinance links.
3. **Center for Community Progress** — blog/reports on proactive rental
   inspection (communityprogress.org).
4. **ChangeLab Solutions** — *A Guide to Proactive Rental Inspection Programs*
   (PDF) surveys dozens of programs with ordinance citations.
5. **MRSC (WA)** — "Rental Housing Registries" insight pages catalog Washington
   cities (Seattle, Tacoma, Tukwila, Bellingham, Pasco, Spokane...).
6. **HUD / PD&R and Abt reports** on rental registries and code enforcement.
7. **Advocacy scans** — PolicyLink, Emory/ChangeLab preemption maps,
   supportdemocracy.org "State Preemption of Local Equitable Housing Policies".
8. **Industry side** — landlord associations (RHAWA, apartment associations)
   publish "compliance guides" that are effectively inventories of programs
   they oppose; so do rental-compliance vendors (Deckard, Granicus/Host
   Compliance blogs).

## 3. Ordinance full-text search (the scalable method)

Nearly every codified municipal code lives in one of five commercial libraries.
Full-text search across them *is* the national scan:

| Library | URL pattern | Coverage |
|---|---|---|
| Municode (CivicPlus) | `library.municode.com/{state}/{muni}` | ~4,000 munis, strong South/Southeast |
| American Legal | `codelibrary.amlegal.com/codes/{muni}` | ~2,000, strong Midwest (OH, IL) |
| General Code eCode360 | `ecode360.com/{id}` | ~3,000, strong Northeast (NY, NJ, PA) |
| Code Publishing Co. | `codebook.codepublishing.com/{ST}/{Muni}` | strong West (WA, OR, CA) |
| Sterling Codifiers | now folded into Code Publishing | mountain West |

Two ways to query them:

- **Search-engine dorks** (what the script automates), e.g.:
  - `site:ecode360.com "residential rental license"`
  - `site:library.municode.com "rental registration program"`
  - `site:codelibrary.amlegal.com "rental dwelling license"`
  - `site:codebook.codepublishing.com "rental housing inspection"`
  The result URL itself usually names the municipality and state.
- **Each library's own search box** supports phrase search across all clients
  (Municode's site search and eCode360's "search all codes" both work; grab the
  network request in browser DevTools if you want to script it directly).

Run every vocabulary term from § 1 against every library. Expect hundreds of
hits in PA/NY/NJ/MN/IA — licensing is near-universal among small Northeastern
boroughs; the interesting finds are mid-size and large cities.

## 4. Other search channels

- **News dorks:** `"rental registry" OR "rental license" ordinance council approved`
  restricted to the past 1–2 years surfaces brand-new programs (e.g., 2024–26
  adoptions) before aggregators catch them.
- **Legistar/council-agenda search:** many cities run Granicus Legistar
  (`{city}.legistar.com`); searching "rental registration" across Legistar
  instances finds pending ordinances.
- **State municipal leagues** (League of Minnesota Cities, PA State Association
  of Boroughs, etc.) publish model rental-licensing ordinances and member
  surveys.
- **Court dockets:** landlord groups sue over these programs; the complaints
  enumerate program details (e.g., Pittsburgh's registration litigation).

## 5. Preemption screen — where programs *can't* exist

Before crediting or expecting a program, check the state:

- **Indiana** — Ind. Code 36-1-20-4.1 caps registration fees (~$5) and
  restricts inspection programs; pre-July 1984 programs (Bloomington, West
  Lafayette) grandfathered.
- **Wisconsin** — 2015 Act 176 and 2017 Act 317 sharply limit local rental
  registration and inspection (Milwaukee's program survives only in narrowed
  form).
- **North Carolina** — G.S. 160D-1207 bars general rental registration/permits;
  only "problem property" targeting allowed (killed Raleigh's PROP).
- **Georgia** — state law bars local registration of residential rental
  property (verify current citation, O.C.G.A. tit. 44 ch. 7).
- **Tennessee** — *no general ban.* Davidson County registration is
  state-authorized (Tenn. Code Ann. § 66-28-107). Watch the legislature; STR
  preemption fights show the appetite.
- Always re-check: preemption bills move every session (AZ, TX, FL, OH, MT have
  all seen attempts).

The preemption map is itself a finding for the Nashville series: it shows which
program designs survive hostile legislatures (targeted/problem-property
programs, fee-capped registries, state-authorized carve-outs like Davidson's).

## 6. Verification checklist (per city, before it enters the dataset)

1. Find the **ordinance text** in the code library (not just a city webpage).
2. Confirm scope: does it cover long-term rentals generally (not just STR,
   vacant property, or multifamily 3+)?
3. Record: model (license/registration/inspection), unit scope, renewal cycle,
   inspection cycle, fee structure, local-agent requirement, penalty, year
   enacted, administering department.
4. Confirm the program is **operating** (fee schedule or application form on
   the city site dated within ~2 years) — several ordinances are dead letters.
5. Note litigation/preemption status.

## 7. Suggested record schema

See header row of `cities_rental_licensing_seed.csv`:
`city, state, program_name, model, scope, cycle, fee_notes, year, authority, url, notes, verify`

`verify=Y` means the row came from a secondary source or memory and needs the
§ 6 checklist run against primary sources before you cite it.
