import re
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime

# --- Setup Chrome ---
options = Options()
options.headless = False  # True for headless
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- Open the Palo Alto EOL page ---
url = "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/hardware-end-of-life-dates"
driver.get(url)

# --- Wait until the table loads ---
wait = WebDriverWait(driver, 20)
table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))

# --- Extract table rows ---
rows = table.find_elements(By.TAG_NAME, "tr")

# --- Prepare lists ---
vendor_list = []
product_name_list = []
eol_date_list = []     # Clean YYYY-MM-DD (string for CSV)
eol_date_xlsx = []     # True datetime.date objects for Excel
resource_list = []
recommended_list = []

# --- Strict YYYY-MM-DD parser ---
def parse_iso(date_str):
    if not date_str:
        return None
    s = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str.strip())
    for fmt in ("%m/%d/%Y", "%b %d, %Y", "%B %d, %Y", "%d-%b-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(s, fmt).date()  # ✅ only date object
        except:
            continue
    return None  # unrecognized → None

# --- Loop rows (skip header) ---
for row in rows[1:]:
    cells = row.find_elements(By.TAG_NAME, "td")
    if len(cells) >= 6:
        vendor_list.append("Palo Alto")
        product_name_list.append(cells[0].text.strip())

        dt = parse_iso(cells[2].text.strip())
        if dt:
            eol_date_list.append(dt.strftime("%Y-%m-%d"))  # CSV as string
            eol_date_xlsx.append(dt)                       # Excel true date
        else:
            eol_date_list.append("")
            eol_date_xlsx.append(None)

        # Resource link
        try:
            resource_list.append(cells[3].find_element(By.TAG_NAME, "a").get_attribute("href"))
        except:
            resource_list.append("")
        recommended_list.append(cells[5].text.strip())

# --- DataFrames ---
df_csv = pd.DataFrame({
    "vendor": vendor_list,
    "productName": product_name_list,
    "EOL Date": eol_date_list,   # plain text YYYY-MM-DD
    "resource": resource_list,
    "Recommended replacement": recommended_list
})

df_xlsx = pd.DataFrame({
    "vendor": vendor_list,
    "productName": product_name_list,
    "EOL Date": eol_date_xlsx,   # true date
    "resource": resource_list,
    "Recommended replacement": recommended_list
})

# --- Save CSV (YYYY-MM-DD strings, no apostrophe) ---
df_csv.to_csv("palo_alto_eol_products.csv", index=False, quoting=csv.QUOTE_MINIMAL)

# --- Save XLSX with yyyy-mm-dd date format ---
with pd.ExcelWriter("palo_alto_eol_products.xlsx", engine="xlsxwriter") as writer:
    df_xlsx.to_excel(writer, index=False, sheet_name="data")
    wb  = writer.book
    ws  = writer.sheets["data"]
    date_fmt = wb.add_format({"num_format": "yyyy-mm-dd"})
    date_col = df_xlsx.columns.get_loc("EOL Date")
    ws.set_column(date_col, date_col, 12, date_fmt)

print("✅ Done. Extracted all products with 5 columns. Dates are YYYY-MM-DD (no time, no apostrophe).")

# --- Close driver ---
driver.quit()
