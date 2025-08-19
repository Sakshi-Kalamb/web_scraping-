from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime
import re

# ---------- SETUP CHROME ----------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary"
driver.get(url)

# ---------- WAIT FOR TABLES ----------
WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))

# ---------- HELPERS ----------
def format_date(date_str):
    """Strictly format date as YYYY-MM-DD."""
    if not date_str or date_str.strip() == "":
        return ""
    try:
        return datetime.datetime.strptime(date_str.strip(), "%B %d, %Y").strftime("%Y-%m-%d")
    except:
        return date_str.strip()

def is_header_row(cols):
    """Check if row is a header (contains 'Version', 'Release Date', or 'EOL')."""
    header_keywords = ["version", "release date", "eol"]
    for col in cols[:3]:
        if col.text.strip().lower() in header_keywords:
            return True
    return False

# ---------- SCRAPE ALL SECTIONS ----------
all_data = []

sections = driver.find_elements(By.CLASS_NAME, "text.baseComponent.parbase.section")

for section in sections:
    # Find all <p><b> inside section → each is a new software row
    p_b_elements = section.find_elements(By.CSS_SELECTOR, "p > b")
    p_b_texts = [el.text.strip() for el in p_b_elements]

    tables = section.find_elements(By.TAG_NAME, "table")
    current_software_name = p_b_texts[0] if p_b_texts else ""  # start with first <p><b> if exists

    for table in tables:
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) == 0:
                continue

            # Skip header rows
            if is_header_row(cols):
                continue

            # --- Check for p > b in row → NEW SOFTWARE ROW ---
            try:
                b_in_p = row.find_element(By.CSS_SELECTOR, "p > b")
                current_software_name = b_in_p.text.strip()
                continue  # skip row as it only contains the software name
            except:
                pass

            # --- Check for td > b (no <p>) → APPEND TO CURRENT SOFTWARE ---
            try:
                b_in_td = row.find_element(By.CSS_SELECTOR, "td > b")
                if current_software_name:
                    current_software_name += " + " + b_in_td.text.strip()
            except:
                pass

            # Scrape data columns
            version = cols[0].text.strip() if len(cols) > 0 else ""
            release_date = cols[1].text.strip() if len(cols) > 1 else ""
            eol_date = cols[2].text.strip() if len(cols) > 2 else ""

            # Skip empty rows
            if version == "" and release_date == "" and eol_date == "":
                continue

            all_data.append({
                "Software Name": current_software_name,
                "Version": version,
                "Release Date": format_date(release_date),
                "EOL Date": format_date(eol_date)
            })

# ---------- SAVE TO CSV ----------
df = pd.DataFrame(all_data)
df.to_csv("palo_alto_software_eol_all.csv", index=False)
print("✅ CSV saved as 'palo_alto_software_eol_all.csv'")

driver.quit()

