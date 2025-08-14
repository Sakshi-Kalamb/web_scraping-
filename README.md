# Web Srapping

## Web Scraping Toolkit

This repository contains scripts and examples for web scraping tasks using Python, including:

- Selenium scraping (dynamic web pages)

- HTML table scraping → CSV/Excel

- PDF text extraction → TXT

- Single image download using XPath

⚠️ Make sure you respect websites’ terms of service. Scrape responsibly.

## 📁 Repository Structure
web-scraping-toolkit/  
├─ README.md  
├─ requirements.txt  
├─ pdf_scraping/  
│  ├─ scraper_pdf.py        
│  └─ sample.pdf.pdf    
│  └─ output_pdf_text.csv 
├─ table_scraping/  
│  ├─ scraper_table.py  
│  ├─ output_table.py  


## ⚡ Features

1. Selenium Scraping  
Scrape dynamic content (quotes, text, authors) from a website.  

2. Table Scraping  
Extract HTML tables from any webpage and save as CSV or Excel.  

3. PDF Text Extraction  
Extract text from local or downloaded PDFs.  

4. Image Scraping by XPath  
Download a single image using its XPath.  

## 🛠 Installation

1. Clone the repository:  
```python 
git clone <your-repo-url>
cd web-scraping-toolkit
```

2. Create virtual environment and activate:  
```python
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```


3. Install required libraries:  
```python
pip install -r requirements.txt
```


requirements.txt
```python
selenium
webdriver-manager
pandas
beautifulsoup4
lxml
requests
pdfplumber
PyPDF2
```
### 🔧 Usage
1.  Selenium Scraper  

Scrapes quotes from a website and saves CSV:
```python
python scripts/selenium_scraper.py
```
2.  Table Scraper

Extracts HTML tables from a webpage:
```python
python scripts/table_scraper.py
```
3.   PDF Text Extraction  

Extracts text from a PDF:
```python
python scripts/pdf_to_text.py
```
4. Image Scraper (XPath)  

Downloads a single image from a page:
```python
python scripts/image_by_xpath.py
```
## 📌 Notes

- Place PDFs in data/pdfs/ before extracting text.

- Outputs (CSV, TXT, Images) will be saved in data/outputs/.

- For headless Selenium, uncomment options.add_argument("--headless") in the script.

- Always scrape responsibly.

## 📚 References

- Selenium Documentation
- Pandas Documentation
- pdfplumber Documentation


