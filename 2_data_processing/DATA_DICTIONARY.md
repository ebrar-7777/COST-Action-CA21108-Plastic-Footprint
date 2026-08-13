# Data dictionary

This file documents (a) the input layout `plastic_footprint.py` expects and (b) every
column it writes. The laboratory-level survey records themselves are not redistributed
with this repository — see *About the survey data* in the [README](../README.md).

---

## Input — `survey_data_anonymised.csv`

One row per participating laboratory (53 rows in the published study), 44 columns.

This layout describes the file the analysis expects, but note that `plastic_footprint.py`
is written for the specific survey dataset of this study: some free-text entries are
interpreted record by record, keyed to their row position in the file. Matching the layout
alone is not sufficient to reuse the script on other data — see the README.

| Column | Type | Description |
|---|---|---|
| `Lab_ID` | string | Laboratory identifier, `Lab_01` … `Lab_53`. A sequential pseudonym assigned by survey response order; it carries no other meaning. |
| `Country` | string | Country of the laboratory (22 distinct values in the study). |
| `ITC_status` | `ITC` / `non-ITC` | Whether the country is a COST Inclusiveness Target Country. 29 ITC, 24 non-ITC. |
| `Working_with_cell_cultures` | string | Free-text answer to the screening question. |
| `Purchase_{1..10}_item` | string | Free-text name of the consumable, as written by the respondent (e.g. `10 ml serological pipette`). Empty when the laboratory reported fewer than *n* purchases. |
| `Purchase_{1..10}_brand` | string | Free-text manufacturer/supplier. Not used in the calculation; retained for transparency. |
| `Purchase_{1..10}_boxes` | string | Free-text number of boxes or packs purchased over the six-month period. |
| `Purchase_{1..10}_items_per_box` | string | Free-text number of items per box. |

The four quantity/item fields are deliberately kept as **raw free text**. Respondents
wrote things like `100 tips (5 × 20 racks)`, `15–50 mL` or `two boxes`; parsing those
strings is part of the method and is implemented in `plastic_footprint.py`
(`compute_total_items`, `match_consumable`), so the raw strings must remain auditable.

**Personal data.** The original survey also collected each respondent's full name,
institutional affiliation, free-text comments and a co-authorship preference. All four are
personal data under the GDPR and were removed before any release, replaced by `Lab_ID` and
by `Country` / `ITC_status` — the only geographic granularity the analysis uses. Country
and ITC status were resolved once from the affiliation text before the identifying columns
were dropped, so the pipeline reads them straight from the file and never handles
affiliation text. This removes no information from the analysis: the reported statistics
(12,603.6 kg plastic; 42,813.6 kg CO₂e; U = 188, p = 0.0044; U = 182, p = 0.0031) are
computed entirely from the columns above.

Note that the free-text purchase fields do name **brands and suppliers** (Eppendorf, VWR,
and so on). These are commercial product identifiers rather than personal data, and are
retained because the consumable matching depends on them being auditable.

---

## Published output — `output_data/country_summary.csv`

22 rows, one per country. This is the file included in this repository, and it is the same
data as Supplementary Data 3 of the article.

| Column | Description |
|---|---|
| `country` | Country name |
| `itc_status` | `ITC` or `non-ITC` |
| `n_labs` | Number of participating laboratories in that country |
| `total_plastic_kg` | Total plastic mass over the six-month period (kg) |
| `total_co2e_kg` | Corresponding carbon footprint (kg CO₂e) |
| `mean_plastic_kg`, `mean_co2e_kg` | Per-laboratory means for that country |

## Published output — figures

These are the published versions of the article figures.

| File | Content |
|---|---|
| `fig1_polymer_distribution.png` | Mass and carbon-footprint share of each polymer type (article Fig. 1) |
| `fig2_emission_factors.png` | Literature-derived average emission factors per polymer, mean ± s.e.m. (article Fig. 2) |
| `fig3_itc_vs_nonitc_boxplot.png` | Laboratory plastic use and CO₂e, ITC vs non-ITC, log scale (article Fig. 3) |
| `fig4_europe_map.png` | Geographic distribution of the participating laboratories and their carbon footprints (article Fig. 4) |

---

## Intermediate output — laboratory level (not redistributed)

`plastic_footprint.py` also writes two laboratory-level files. They are produced locally
when the script is run with an input file, and are **not** part of the public release.

### `output_data/lab_summary.csv` — one row per laboratory

| Column | Description |
|---|---|
| `row_index` | 0-based row number in the input file |
| `lab_id` | Laboratory identifier |
| `country`, `itc_status` | As above |
| `total_plastic_kg` | Total plastic mass attributed to that laboratory over six months (kg) |
| `total_co2e_kg` | Corresponding carbon footprint (kg CO₂e) |

This is the file `mann_whitney_u_test.py` reads.

### `output_data/lab_detailed_audit.csv` — one row per reported purchase

The full audit trail from raw survey text to kilograms (424 rows in the published study).

| Column | Description |
|---|---|
| `row_index`, `lab_id`, `country`, `itc_status` | Laboratory identification |
| `purchase_num` | 1–10, which purchase slot this row came from |
| `raw_item_name`, `raw_boxes`, `raw_items` | The respondent's original free text, unmodified |
| `matched_consumable` | The entry matched in the built-in consumable database, or `UNMATCHED` |
| `polymer` | Polymer assigned to the item (PP, PS, PET, …) |
| `weight_per_piece_g` | Unit mass used for that consumable (g) |
| `total_items` | Number of items after parsing boxes × items-per-box |
| `plastic_kg`, `co2e_kg` | Mass and emissions for the item body |
| `cap_polymer`, `cap_weight_g`, `cap_kg`, `cap_co2e_kg` | The same for a separate cap or lid, where the consumable has one (e.g. centrifuge tubes) |
| `calc_notes` | How this row was interpreted — the reason for every non-obvious decision |
