from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os
import PyPDF2
import pandas as pd

class PDFXPathScraper:
    def __init__(self, download_dir="downloads"):
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)
        self.driver = None

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Remove if you want to see browser
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def find_pdf_link_and_download(self, url, xpath):
        self.driver.get(url)
        time.sleep(2)  # Wait for page load
        pdf_element = self.driver.find_element(By.XPATH, xpath)
        pdf_url = pdf_element.get_attribute("href")

        if pdf_url and pdf_url.endswith(".pdf"):
            pdf_name = os.path.join(self.download_dir, os.path.basename(pdf_url))
            r = requests.get(pdf_url)
            with open(pdf_name, "wb") as f:
                f.write(r.content)
            print(f"✅ PDF downloaded: {pdf_name}")
            return pdf_name
        else:
            print("❌ PDF link not found")
            return None

    def extract_pdf_to_csv(self, pdf_path, csv_path="extracted_text.csv"):
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            data = []
            for page_num in range(len(reader.pages)):
                text = reader.pages[page_num].extract_text() or ""
                data.append({"Page Number": page_num + 1, "Text": text})

        df = pd.DataFrame(data)
        df.to_csv(csv_path, index=False, encoding="utf-8")
        print(f"✅ Text saved to CSV: {csv_path}")

    def close(self):
        if self.driver:
            self.driver.quit()

if __name__ == "__main__":
    url = "https://www.africau.edu/images/default/sample.pdf"  # Example PDF link
    xpath = "//a[contains(@href, '.pdf')]"  # Find <a> tag with PDF

    scraper = PDFXPathScraper()
    scraper.setup_driver()
    pdf_path = scraper.find_pdf_link_and_download(url, xpath)

    if pdf_path:
        scraper.extract_pdf_to_csv(pdf_path)

    scraper.close()
