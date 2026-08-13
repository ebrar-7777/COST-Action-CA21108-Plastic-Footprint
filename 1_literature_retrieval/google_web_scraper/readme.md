# Script 1: Google Web Scraper (`google_web_scraper.py`)

## Overview

This script performs automated web searches via the Google Search API to retrieve carbon footprint values (kg CO₂e/kg) for specified polymer types. 
It parses search result snippets to extract numeric CO₂ emission data and saves the results to a CSV file.

## Purpose

Initial broad-scope data collection for polymer-specific emission factors from publicly available web sources. 
This script served as the first stage of a two-pronged literature retrieval strategy described in the Methods section.

## How It Works

1. For each polymer in the predefined list, the script constructs a Google Search query (e.g., `"co2 emissions per kg of Polypropylene polymer"`).
2. It retrieves up to 5 pages of search results per polymer.
3. For each result, the snippet text is parsed to identify numeric values followed by CO₂-related units (e.g., `kg CO2e/kg`, `million tons`).
4. Results containing extractable CO₂ values are saved to a CSV file.

## Polymers Searched

polypropylene (PP), polystyrene (PS), polyethylene terephthalate (PET), 
polyethylene (PE), high-density polyethylene (HDPE), low-density polyethylene (LDPE), 
polycarbonate (PC), polyvinyl chloride (PVC), 
polyester (PES), silicone, acetal/polyoxymethylene (POM), nitrile and latex. 

## Output (raw)

- `query_dbv2_queryv2.csv` — CSV file with columns: `polymer`, `co2_value`, `link`

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `MAX_PAGES` | 5 | Maximum number of Google Search result pages per polymer | #configurable
| `QUERY_LIST` | See source | Search query templates with `{polymer}` placeholder |
| `PL_LIST` | See source | List of polymer names to search |

## Requirements

```
requests>=2.28.0
beautifulsoup4>=4.11.0
```

## Usage

```bash
pip install requests beautifulsoup4
python google_web_scraper.py
```

## Limitations

- Relies on Google Search HTML structure, which may change over time.
- Extracts values from search snippets only (not full article text).
- Rate-limited with random delays (2–5 seconds between requests) to avoid blocking.
- Retrieved values require manual screening for relevance and accuracy.

## Ethical Considerations

The script includes polite rate limiting (`wait_for_random_time`) to minimise server load. 
All data was used solely for academic research purposes.
