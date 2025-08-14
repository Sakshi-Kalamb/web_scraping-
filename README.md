# Web Scraping Project

## Overview
This project demonstrates two types of web scraping:
1. **Scraping HTML tables** from websites.
2. **Extracting text from PDF files**.

The project is implemented in Python using libraries like:
- `selenium` for browser automation.
- `pandas` for handling data.
- `PyPDF2` or `pdfplumber` for reading PDF files.

---

## Theory

### 1. Scraping HTML Tables
Web scraping is the process of automatically extracting data from websites.  
For HTML tables, Selenium is used to:
- Launch a browser.
- Navigate to a page.
- Locate table elements.
- Read and store them in a structured format.

### 2. Extracting Text from PDF
PDF scraping involves reading PDF files programmatically and extracting their text content.  
We use `pdfplumber`/`PyPDF2` to:
- Open a PDF file.
- Read each page.
- Store extracted text in `.txt` files.

---

## Project Files
- `scrape_table.py` → Script to scrape HTML tables.
- `scrape_pdf.py` → Script to extract PDF text.
- `sample_data/` → Example output files.

---

## Installation
```bash
pip install -r requirements.txt
