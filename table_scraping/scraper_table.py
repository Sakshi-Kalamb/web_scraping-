from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

print("Python is working! Selenium is ready!")

# Chrome options
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Uncomment if you don't want the browser to open
options.add_argument("--window-size=1920,1080")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")

# Create driver instance
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open website
driver.get("https://www.w3schools.com/html/html_tables.asp")
print(driver.title)  # should print the page title
time.sleep(3)  # wait for page to load

# Define TableScraper class
class TableScraper:
    def __init__(self, driver, table_id):
        self.driver = driver
        self.table_id = table_id
        self.data = []

    # Function to scrape table using XPath
    def scrape_table(self):
        # Locate table using XPath
        table = self.driver.find_element(By.XPATH, f"//table[@id='{self.table_id}']")
        rows = table.find_elements(By.XPATH, ".//tr")  # all rows
        
        for row in rows:
            cols = row.find_elements(By.XPATH, ".//td")  # all columns in each row
            cols_text = [col.text for col in cols]
            if cols_text:  # ignore empty header rows
                self.data.append(cols_text)

    # Convert scraped data to dataframe
    def to_dataframe(self, columns=None):
        df = pd.DataFrame(self.data, columns=columns)
        return df

    # Save dataframe to CSV
    def save_to_csv(self, df, filename):
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

# Initialize the scraper with the table ID
if __name__ == "__main__":
    table_id = "customers"
    columns = ["Company", "Contact", "Country"]

    scraper = TableScraper(driver, table_id)
    scraper.scrape_table()
    df = scraper.to_dataframe(columns)
    print(df)
    scraper.save_to_csv(df, "scraped_table_xpath.csv")

    driver.quit()  # close browser
