import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import fitz  # PyMuPDF
import re
import os
import pandas as pd

DEFINE_MAX_ARTICLE = 20  # Article count. If you want, you can change it.

# Configure Selenium Chrome driver
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128")
chrome_options.add_argument("--headless")  # Runs Chrome in headless mode.
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def get_articles(driver, polymer):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "gs_res_ccl_mid"))
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        driver.quit()
        return 0

    results = driver.find_elements(By.XPATH, '//div[@class="gs_r gs_or gs_scl"]')
    filename_value = polymer.replace(" ", "_") + "_f_value.csv"

    added_count = 0
    for result in results[:10]:  # Google Scholar : 10, Science Direct : 25  (configurable)
        try:
            title_element = result.find_element(By.XPATH, './/h3[@class="gs_rt"]/a')
            link = title_element.get_attribute('href')

            output_path = 'downloaded_file.pdf'
            downloaded_pdf_path = download_pdf(link, output_path)
            if downloaded_pdf_path:
                carbon_footprint = extract_values_from_pdf(downloaded_pdf_path)
                if carbon_footprint:
                    carbon_value = ', '.join(carbon_footprint)
                    new_row = {'Polymer': polymer, 'Carbon Footprint': carbon_value, 'URL': link}
                    if os.path.isfile(filename_value):
                        df = pd.read_csv(filename_value)
                        new_df = pd.DataFrame([new_row])
                        df = pd.concat([df, new_df], ignore_index=True)
                    else:
                        df = pd.DataFrame([new_row])

                    df.to_csv(filename_value, index=False)
                    print(f"Row added to '{filename_value}'")
                    added_count += 1

                    os.remove(downloaded_pdf_path)
        except Exception as e:
            print(f"Error processing result: {str(e)}")

    return added_count

def download_pdf(url, output_path, retries=3):
    for i in range(retries):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                return output_path
            elif response.status_code == 403:
                print(f"Failed to download PDF 403: {url}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error downloading PDF: {e}")
            time.sleep(5)
    raise Exception(f"Failed to download PDF after {retries} retries")

def extract_values_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    values = []

    patterns = [
        r'\b[\d.,]+\s*kg\s*CO2e?\/kg\b',
        r'\b[\d.,]+\s*CO2e?\/kg\b',
        r'\b[\d.,]+\s*kg\s*CO2\s*per\s*kg\b',
        r'\b[\d.,]+\s*CO2\s*per\s*kg\b',
        r'\b[\d.,]+\s*kg\s*of\s*CO2\b',
        r'\b[\d.,]+\s*kg\s*CO2\b',
        r'\b[\d.,]+\s*kg\s*CO2eq\b',
        r'\b[\d.,]+\s*CO2eq\b'
    ]

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text = page.get_text()
        for pattern in patterns:
            matches = re.findall(pattern, text)
            values.extend([str(match.replace(',', '')) for match in matches])

    pdf_document.close()
    return values

def search_carbon_footprint_selenium(polymer):
    search_query = f"{polymer} AND kg-CO2e/kg OR CO2e/kg OR CO2-per-kg OR kg-of-CO2 OR kg/CO2 OR kg-CO2eq AND filetype:pdf"

    page_idx = 0
    article_idx = 0
    while article_idx <= DEFINE_MAX_ARTICLE + 1:
        driver_url = f"https://scholar.google.com/scholar?start={str(page_idx*10)}&q={search_query}"
        driver.get(driver_url)
        article_idx += get_articles(driver, polymer)
        page_idx += 1

polymers = [
    "Polypropylene AND Low-Density",
    "Polypropylene AND High-Density",
    "Polystyrene",
    "Polycarbonate",
    "Polypropylene",
    "Silicone",
    "Polyethylene AND LD",
    "Polyethylene AND HD",
    "Polyethylene",
    "Acetal",
    "Polyester",
    "Borosilicate glass",
    "Polyethylene Terephthalate",
    "Polyvinyl chloride",
    "Nitrile"
]

all_data = {}

for polymer in polymers:
    data = search_carbon_footprint_selenium(polymer)