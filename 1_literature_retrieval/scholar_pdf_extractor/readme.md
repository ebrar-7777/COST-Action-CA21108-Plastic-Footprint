# Script 2: Google Scholar PDF Extractor (`scholar_pdf_extractor.py`)

## Overview

This script uses Selenium WebDriver to search Google Scholar for polymer-specific carbon footprint literature, 
automatically downloads available PDF articles, and extracts CO₂ emission values using regex pattern matching on the full text of each PDF.

## Purpose

Automated full-text extraction of carbon footprint values from academic PDFs retrieved via Google Scholar. 
This script complements the web snippet scraper (Script 1) by accessing the complete article content rather than search result previews only.

## How It Works

1. For each polymer, a Google Scholar search query is constructed with CO₂-related keywords and a `filetype:pdf` filter.
2. Selenium (headless Chrome) navigates Google Scholar and retrieves article links.
3. For each article, the script attempts to download the PDF directly.
4. Successfully downloaded PDFs are parsed using PyMuPDF (`fitz`) to extract text.
5. Regex patterns identify CO₂ emission values in formats such as:
   - `X.XX kg CO2e/kg`
   - `X.XX kg CO2 per kg`
   - `X.XX kg CO2eq`
6. Extracted values are saved per-polymer to individual CSV files.

## Polymers Searched

polypropylene (PP), polystyrene (PS), polyethylene terephthalate (PET), polyethylene (PE), 
high-density polyethylene (HDPE), low-density polyethylene (LDPE), polycarbonate (PC), 
polyvinyl chloride (PVC), polyester (PES), silicone, acetal/polyoxymethylene (POM), nitrile and latex. 
## Output (raw)

- `{Polymer_Name}_f_value.csv` — One CSV file per polymer with columns: `Polymer`, `Carbon Footprint`, `URL`

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DEFINE_MAX_ARTICLE` | 20 | Maximum number of articles to process per polymer | #configurable

## Requirements

```
selenium>=4.10.0
webdriver-manager>=4.0.0
requests>=2.28.0
PyMuPDF>=1.22.0
pandas>=1.5.0
```

### System Requirements

Google Chrome browser installed
ChromeDriver (automatically managed by `webdriver-manager`)

## Usage

```bash
pip install selenium webdriver-manager requests PyMuPDF pandas
python scholar_pdf_extractor.py
```

## Regex Patterns Used

The following patterns are used to identify CO₂ values in PDF text:

| Pattern | Example Match |
|---------|--------------|
| `\b[\d.,]+\s*kg\s*CO2e?/kg\b` | `2.42 kg CO2e/kg` |
| `\b[\d.,]+\s*CO2e?/kg\b` | `3.78 CO2e/kg` |
| `\b[\d.,]+\s*kg\s*CO2\s*per\s*kg\b` | `4.04 kg CO2 per kg` |
| `\b[\d.,]+\s*kg\s*of\s*CO2\b` | `2.72 kg of CO2` |
| `\b[\d.,]+\s*kg\s*CO2eq\b` | `9.17 kg CO2eq` |

## Limitations

Depends on Google Scholar HTML structure (subject to change).
PDF download success depends on open-access availability; paywalled articles are skipped (HTTP 403).
Extracted values are not contextually validated, so we have performed manual validation.
Headless Chrome is used to reduce detection, but Google Scholar may still impose rate limits or CAPTCHAs.

## Ethical Considerations

The script runs in headless mode with anti-detection measures disabled (`--disable-blink-features=AutomationControlled`).
Random delays and retry logic are implemented to minimise server load.
Downloaded PDFs are deleted after processing.
All data was used solely for academic research purposes.
