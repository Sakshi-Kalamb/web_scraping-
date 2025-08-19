from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import datetime

print("🚀 Troemner scraper started!")

# Setup Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
# options.add_argument("--headless")  # Uncomment to run without opening browser

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Target URL
URL = "https://www.troemner.com/Calibration-Weights/Balance-Calibration-Weights/OIML-Calibration-Weight-Sets/c/3944"
driver.get(URL)
time.sleep(5)

SCROLL_PAUSE = 2  # pause between scrolls
last_count = 0

print("🔄 Starting to scroll and load all products. This may take a few minutes...")

while True:
    # Scroll down slowly
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(SCROLL_PAUSE)
    
    # Click Load More button if it appears
    try:
        load_more = driver.find_element(By.CSS_SELECTOR, "a.btn-loadMore, button.btn-loadMore")
        driver.execute_script("arguments[0].click();", load_more)
        print("🖱️ Clicked Load More button")
        time.sleep(3)  # wait for products to load
    except:
        pass

    # Count products
    product_rows = driver.find_elements(By.CSS_SELECTOR, "li.product-item")
    current_count = len(product_rows)
    
    # Print progress
    print(f"📦 Products loaded so far: {current_count}")
    
    # Stop only when count stops increasing
    if current_count == last_count:
        # Extra wait in case slow loading
        time.sleep(5)
        product_rows = driver.find_elements(By.CSS_SELECTOR, "li.product-item")
        current_count = len(product_rows)
        if current_count == last_count:
            break
    else:
        last_count = current_count

print(f"🎯 Finished loading all products! Total found: {len(product_rows)}")

# Extract data
data = []
for i, row in enumerate(product_rows, start=1):
    try:
        product_name = row.find_element(By.CSS_SELECTOR, "h3.title a").text.strip()
        product_url = row.find_element(By.CSS_SELECTOR, "h3.title a").get_attribute("href")

        try:
            model = row.find_element(By.CSS_SELECTOR, "span.code").text.strip().replace("(", "").replace(")", "")
        except:
            model = "N/A"

        try:
            cost_text = row.find_element(By.CSS_SELECTOR, ".product-price, .price").text.strip()
            # ✅ Extract only the actual price starting with $
            cost_parts = [part for part in cost_text.split() if part.startswith("$")]
            cost = cost_parts[0] if cost_parts else "N/A"
        except:
            cost = "N/A"

        try:
            description = row.find_element(By.CSS_SELECTOR, "div.description.product-description").text.strip()
        except:
            description = "N/A"

        data.append({
            "vendor": "troemner",
            "productName": product_name,
            "model": model,
            "description": description,
            "productURL": product_url,
            "cost": cost
        })

        print(f"✅ Scraped {i}: {product_name} | {cost}")

    except Exception as e:
        print(f"⚠️ Skipped a product due to error: {e}")
        continue

# Save CSV
filename = f"troemner_products_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
df = pd.DataFrame(data)
df.to_csv(filename, index=False, encoding="utf-8-sig")
print(f"💾 Data saved to {filename}")

driver.quit()
