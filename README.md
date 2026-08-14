<div align="center">

# Carbon Emissions from Cell-Culture Plastics Across Europe

**Analysis code for a 53-laboratory, 22-country survey of single-use plastic consumption
and its carbon footprint in cell-culture research**

[![COST Action](https://img.shields.io/badge/COST%20Action-CA21108%20NETSKINMODELS-1f4e79)](https://www.cost.eu/actions/CA21108/)
[![Code licence](https://img.shields.io/badge/code-BSD--3--Clause-blue)](LICENSE)
[![Data licence](https://img.shields.io/badge/data-CC%20BY%204.0-lightgrey)](LICENSE-DATA)
[![Python](https://img.shields.io/badge/python-3.12-3776ab)](https://www.python.org/)


<img src="2_data_processing/output_data/fig4_europe_map.png" width="760" alt="Carbon footprint of participating laboratories across Europe">

<sub>Geographic distribution of the 53 participating laboratories and their carbon footprints</sub>

</div>

---

This repository is the *Code availability* resource for the associated article. It contains
the complete analysis pipeline: literature-based emission factors, the consumable-matching
and mass/CO₂e calculation, and the statistical comparison reported in the paper.

The work is based upon **COST Action CA21108 — NETSKINMODELS** (*European network for skin
engineering and modeling*), supported by **COST (European Cooperation in Science and
Technology)**, [www.cost.eu](https://www.cost.eu/). The survey was carried out within
**Working Group 3**.

> COST is a funding agency for research and innovation networks. Our Actions help connect
> research initiatives across Europe and enable scientists to grow their ideas by sharing
> them with their peers.

---

## Pipeline

```
      Literature (Life-Cycle Assessment Studies)
                     │
   [1]  literature Retrieval  ──►  Polymer Emission Factors (kg CO₂e per kg)
                     │
                     ▼
   Procurement Survey  ──►  [2] Data Processing  ──►  Per-Laboratory Mass & CO₂e
   (53 labs, 6 months)       plastic_footprint.py     country_summary.csv
                                                            │
                                                            ▼
                                     [3]  Statistics — mann_whitney_u_test.py
                                          ITC vs non-ITC comparison
```

## What is in this repository

```
├── 1_literature_retrieval/       Emission factors from the LCA literature
│   ├── google_web_scraper/
│   └── scholar_pdf_extractor/
├── 2_data_processing/            Consumable matching, mass and CO₂e calculation
│   ├── plastic_footprint.py
│   ├── DATA_DICTIONARY.md        Required input layout + output columns
│   └── output_data/              Country-level results, article figures
├── 3_statistical_analysis/
│   └── mann_whitney_u_test.py    ITC vs non-ITC comparison
├── CITATION.cff
├── LICENSE                       BSD 3-Clause — code
├── LICENSE-DATA                  CC BY 4.0 — country-level data and figures
└── requirements.txt
```

### 1 · Automated literature retrieval — [`1_literature_retrieval/`](1_literature_retrieval)

Two complementary strategies for collecting polymer-specific emission factors from
published life-cycle assessments.

| Script | What it does |
|---|---|
| [`google_web_scraper.py`](1_literature_retrieval/google_web_scraper) | Queries web search per polymer and parses result snippets for kg CO₂e/kg values. |
| [`scholar_pdf_extractor.py`](1_literature_retrieval/scholar_pdf_extractor) | Selenium + PyMuPDF; downloads Google Scholar PDFs and extracts emission values from the full text by regular expression. |

Candidate values retrieved this way were then **screened and averaged manually** — the
scrapers are a search aid, not an automatic source of the published numbers. The final
emission factors, with their references and variability ranges, are Supplementary Data 1
and 2 of the article and are hard-coded in `plastic_footprint.py`.

### 2 · Data processing — [`2_data_processing/`](2_data_processing)

[`plastic_footprint.py`](2_data_processing/plastic_footprint.py) is the core script. It
maps each reported consumable to a polymer type and unit mass using a built-in consumable
database, parses the free-text quantity fields, and computes plastic mass and carbon
footprint per laboratory, per country and per polymer.

Because respondents described consumables in free text, the matching logic has to make explicit decisions. 
Every one of them is recorded in the calc_notes field of the audit output, one entry per reported purchase, 
so each of the 424 records can be traced back to the text the respondent actually wrote. 
That audit file is generated when the script is run; 
it is at laboratory level and is therefore not redistributed here (see About the survey data).

The column layout the script expects, and every column it writes, are documented in
[`DATA_DICTIONARY.md`](2_data_processing/DATA_DICTIONARY.md).

### 3 · Statistical analysis — [`3_statistical_analysis/`](3_statistical_analysis)

[`mann_whitney_u_test.py`](3_statistical_analysis/mann_whitney_u_test.py) — two-sided
Mann–Whitney *U* test of the differences in plastic consumption and carbon footprint
between laboratories in COST Inclusiveness Target Countries (ITC) and non-ITC
laboratories. It reads the data-processing output directly, so there is one source of
truth and no duplicated dataset.

---

## About the survey data

The published results in [`2_data_processing/output_data/`](2_data_processing/output_data)
are **country-level aggregates and the article figures**. The aggregates are the same data
as Supplementary Data 3 of the article, and the figures are the published versions of
Figures 1–4.

The **laboratory-level records are not redistributed here.** The survey collected each
respondent's name, institutional affiliation, free-text comments and a co-authorship
preference; those fields are personal data under the GDPR and were removed before any
release. Even after removal, a per-laboratory row remains linkable to an institution in
countries represented by a single laboratory, so the laboratory-level files are kept out
of the public release entirely. Country and ITC status are the only geographic granularity
the analysis uses, and they are published in full.

Consequently the pipeline in this repository is **auditable but not self-running**: the
code, the consumable database, the emission factors and the aggregate results are all
here, but reproducing the per-laboratory numbers requires the input file. Researchers who
need it for verification should contact the corresponding authors.

Note also that `plastic_footprint.py` is specific to the survey dataset of this study.
Respondents described their purchases in free text, and a number of entries had to be
interpreted individually; those interpretations are written into the script, keyed to the
position of the record in the survey file, and each one is documented in the `calc_notes`
field of the audit output. Applying the pipeline to a different dataset therefore means
reviewing those sections rather than simply swapping the input file.

---

## Running the code

```bash
git clone https://github.com/ebrar-7777/COST-Action-CA21108-Plastic-Footprint.git
cd COST-Action-CA21108-Plastic-Footprint
pip install -r requirements.txt

cd 2_data_processing          && python3 plastic_footprint.py
cd ../3_statistical_analysis  && python3 mann_whitney_u_test.py
```

Paths are resolved relative to each script, so nothing needs editing.The literature
scrapers additionally need `requests`, `beautifulsoup4`, `selenium`, `webdriver-manager`,
`PyMuPDF` and a local Google Chrome installation.

Both scripts exit with an explanatory message if their input file is absent — see
*About the survey data* above.

### Published values

| Quantity | Value |
|---|---|
| Total plastic consumption (53 labs, 6 months) | **12,603.6 kg** |
| Total carbon footprint | **42,813.6 kg CO₂e** |
| Plastic — ITC vs non-ITC | median 43.2 vs 127.1 kg &nbsp;·&nbsp; **U = 188, p = 0.0044** |
| CO₂e — ITC vs non-ITC | median 182.2 vs 484.4 kg CO₂e &nbsp;·&nbsp; **U = 182, p = 0.0031** |
| Coverage | 29 ITC / 24 non-ITC laboratories, 22 countries |

These are exactly the values this code produces: code → data → statistics are internally
consistent, and they are the authoritative numbers.

---

## Licence

| | |
|---|---|
| **Code** (`*.py`) | BSD 3-Clause Licence — see [`LICENSE`](LICENSE) |
| **Data and figures** (`output_data/`) | Creative Commons Attribution 4.0 International — see [`LICENSE-DATA`](LICENSE-DATA) |

Both allow reuse with attribution, in line with COST's commitment to FAIR research
outputs. The BSD 3-Clause non-endorsement clause additionally prevents the COST Action's
name being used to promote derived work.


## Acknowledgements

This article is based upon work from COST Action CA21108 NETSKINMODELS, supported by COST
(European Cooperation in Science and Technology). We thank the 53 participating
laboratories for contributing their procurement records.

<div align="center">
<sub>COST Action CA21108 · NETSKINMODELS · Working Group 3</sub>
</div>
