# Davidson County rent and affordability, HUD administrative data (2017-2026)

Findings from the HUD User Fair Market Rent and Income Limits series for Davidson County, TN
(HUD entity `4703799999`, Nashville-Davidson–Murfreesboro–Franklin MSA). All figures are HUD
administrative values, not survey estimates.

## Findings

**Rents rose faster than incomes.** The two-bedroom Fair Market Rent in the Nashville metro
climbed from $959 in 2017 to $1,730 in 2026, an 80 percent increase over nine years. The
one-bedroom FMR more than doubled, rising from $780 to $1,578 (102 percent). Median family
income rose from $68,700 to $116,100 over the same period (69 percent). Rent growth outpaced
income growth by roughly eleven percentage points. The two-bedroom FMR peaked at $1,827 in 2025
before HUD reduced it about 5 percent for 2026.

**A minimum-cost unit now exceeds what a very-low-income household can pay.** At the 2026
two-bedroom FMR of $1,730 per month, a household must earn about $69,200 per year to keep rent
at 30 percent of income. HUD sets the 2026 extremely-low-income limit (30 percent of area median)
for a four-person household at $34,850. That household can afford about $871 per month. Renting a
two-bedroom unit at the Fair Market Rent would consume roughly 60 percent of its income, a monthly
shortfall of about $859 against the 30 percent standard.

**Rent varies almost threefold within the county.** Across the 125 Davidson ZIP codes with 2026
Small Area Fair Market Rents, the two-bedroom value ranges from $970 (ZIP 37110) to $2,600
(ZIP 37135), a 2.7-to-1 gradient inside a single county. This intra-county spread is the reason
the ZIP-to-tract crosswalk matters: it allows the rent gradient to be mapped against the
institutional-ownership geography.

## Methods

**Data.** Fair Market Rents and Income Limits were retrieved from the HUD User Datasets API for
Davidson County across program years 2017 through 2026. Metro-level values were used for the
county rent series; ZIP-level Small Area Fair Market Rents were used for the within-county spread.
Income Limits provide the area median family income and the extremely-low (30 percent), very-low
(50 percent), and low (80 percent) limits by household size.

**The affordability calculation.** The 30 percent standard treats housing as affordable when it
consumes no more than 30 percent of a household's income; a household paying more is cost burdened,
and one paying more than 50 percent is severely cost burdened. Two quantities follow directly:

1. *Income required for a unit.* The annual income at which a given rent equals 30 percent of income
   is the monthly rent times twelve, divided by 0.30. For the 2026 two-bedroom FMR:
   `$1,730 x 12 / 0.30 = $69,200`.

2. *What a household can afford.* The monthly rent a household can pay at the 30 percent standard is
   its annual income times 0.30, divided by twelve. For the 2026 four-person extremely-low-income
   limit: `$34,850 x 0.30 / 12 = $871`.

The shortfall is the difference between the Fair Market Rent and the affordable payment
(`$1,730 - $871 = $859` per month), and the burden share is the Fair Market Rent as a fraction of
the household's income (`$1,730 x 12 / $34,850 = 59.6 percent`). The four-person household is used
because HUD reports the two-bedroom FMR and the four-person income limit as the standard pairing for
a modest family unit; the same arithmetic applies to any bedroom size and household size.

**Percent changes** are computed as the ratio of the last year to the first year minus one. Nominal
dollars are used throughout; the series is not inflation-adjusted.

## Citations

- U.S. Dep't of Hous. & Urban Dev., *Fair Market Rents*, https://www.huduser.gov/portal/datasets/fmr.html
  (data via https://www.huduser.gov/hudapi/public/fmr/data/4703799999).
- U.S. Dep't of Hous. & Urban Dev., *Small Area Fair Market Rents*,
  https://www.huduser.gov/portal/datasets/fmr/smallarea/index.html.
- U.S. Dep't of Hous. & Urban Dev., *Income Limits*, https://www.huduser.gov/portal/datasets/il.html
  (data via https://www.huduser.gov/hudapi/public/il/data/4703799999).
- 42 U.S.C. § 1437a(a)(1) (setting tenant contribution in assisted housing at 30 percent of monthly
  adjusted income; the statutory basis for the 30 percent affordability standard).
- U.S. Dep't of Hous. & Urban Dev., *CHAS: Background and Data Documentation*,
  https://www.huduser.gov/portal/datasets/cp.html (defining cost burden as housing costs above
  30 percent of income and severe cost burden as above 50 percent).
