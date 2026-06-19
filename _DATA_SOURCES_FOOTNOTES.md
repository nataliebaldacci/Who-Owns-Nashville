# Data Sources — Who Owns Nashville?

Every map on this site draws from primary Metro Nashville government data. Citations below (Bluebook government-dataset form).

---

**Permit Records (Landlord Registration).** Metro Gov't of Nashville & Davidson Cnty., Dep't of Codes & Building Safety, *ePermits Landlord Registration Records* (caseTypeID 176, PSLANDLORD), https://epermits.nashville.gov/. The program imposes a $10 annual registration term on landlords operating one or more dwelling units up to a quadplex, per the case-type rule, https://epermits.nashville.gov/api/permit/1.0/CaseType?$filter=caseTypeID%20eq%20176, codified at Metro Code § 16.33.170 (Required registration), https://library.municode.com/tn/metro_government_of_nashville_and_davidson_county/codes/code_of_ordinances?nodeId=CD_TIT16BUCO_CH16.33REIN_16.33.170RERE, implementing Tenn. Code Ann. § 66-28-107, https://tca.bagel.legal/Title_66_Property#66-28-107. Registration cases: https://epermits.nashville.gov/api/permit/1.0/Case?$filter=caseTypeID%20eq%20176.

**Tax Parcels (Property Type / Characteristics).** Metro Gov't of Nashville & Davidson Cnty., *Cadastral Parcels*, ArcGIS REST Services Directory, Layer 4, https://maps.nashville.gov/arcgis/rest/services/Cadastral/Cadastral_Layers/MapServer/4/ (filtered to non-owner-occupied small residential parcels: `OwnZip <> PropZip AND DUCount > 0 AND DUCount < 3 AND LUDesc IN ('SINGLE FAMILY','ZERO LOT LINE','DUPLEX','RESIDENTIAL CONDO') AND FeatureType NOT IN ('Multistory Condo','Multistory Common Area','Open Space')`). This single-family scope tracks the federal definition of a *single-family home* — a structure with 2 or fewer dwelling units, excluding manufactured homes. Homes Are For People, Not Corporations, H. Res. 1299, 119th Cong. tit. X § 1001(3), https://www.govinfo.gov/content/pkg/BILLS-119hres1299ih/html/BILLS-119hres1299ih.htm.

**Ownership Records (Owner).** Metro Gov't of Nashville & Davidson Cnty., *Parcel Ownership History*, ArcGIS REST Services Directory, Layer 2, https://maps.nashville.gov/arcgis2/rest/services/Parcels/ParcelHistory/MapServer/2.

---

*Notes.* The ePermits endpoints require a browser `User-Agent` header. The cadastral filter above is the canonical non-owner-occupied single-family universe used across these maps. A reader can paste any of these URLs to reproduce the underlying records.
