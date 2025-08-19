
# Troemner OIML Calibration Weight Sets Scraper

This script scrapes **all products** from:
https://www.troemner.com/Calibration-Weights/Balance-Calibration-Weights/OIML-Calibration-Weight-Sets/c/3944

It produces a table with these **6 columns**:
- `vendor` (fixed: `troemner`)
- `productName` (product title — what you highlighted in red)
- `model` (model/SKU — what you highlighted in blue)
- `description` (short description if available)
- `productURL` (link to the product page)
- `cost` (price if visible)

Output files:
- `troemner_oiml_weight_sets.csv`
- `troemner_oiml_weight_sets.xlsx`

---

## 1) Prerequisites

- Windows 10/11 with **Python 3.10+**
- **Google Chrome** installed
- **VS Code** (optional but recommended)

> The script uses `webdriver-manager` to auto-install the matching **ChromeDriver**.

---

## 2) Setup

Create a folder for the project (e.g., `troemner-scraper`) and put these three files in it:

- `scraper.py`
- `requirements.txt`
- `README.md` (this file)

Then open a terminal in that folder and run:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

---

## 3) Run the scraper

```bash
python scraper.py
```

The browser runs **headless** (no window). To watch it, edit `scraper.py` and set `HEADLESS = False`.

---

## 4) How it works (step-by-step)

1. **Launch Chrome** via Selenium with a realistic user-agent.
2. **Open the category URL** and auto-accept common cookie banners.
3. **Load all products** by trying three patterns:
   - Click **Load more** button if present.
   - Click **Next** pagination if present.
   - Perform **infinite scroll** fallback to trigger lazy loading.
4. **Collect product cards/links** from the grid using robust XPath patterns.
5. **Parse each card** for basic fields (name, model, description, price, URL).
6. **Deduplicate** rows (some grids repeat items).
7. **Open each product page** to **enrich** missing fields (title, model/SKU, price, description) using multiple common selectors.
8. **Save results** to CSV and Excel.

---

## 5) Customize (if the site changes)

- Change `CATEGORY_URL` at the top of `scraper.py`.
- If your **blue/red highlights** refer to specific selectors, update these areas:
  - **Product Name (listing)**: search for the XPath list under `parse_card_basic` → `name_el`.
  - **Model (listing)**: XPath list under `parse_card_basic` → `model_el`.
  - **Title/Model (detail page)**: XPath lists under `parse_detail_page`.

The script already tries many common class names: `name`, `title`, `sku`, `code`, `model`, `price`, `description`, etc.

---

## 6) Tips for getting all 162 models

- Let the script finish; it attempts to load all products before collecting.
- If your page uses **filters** or **pagination**, make sure everything is visible on the main listing. The script clicks "Load More" and "Next" if present.
- If products are grouped into sets with multiple **variants**, the detail-page step increases your chances of capturing the **model/SKU** value.

---

## 7) Troubleshooting

- **No products found**: Set `HEADLESS = False` and watch the page. Update XPaths in `collect_product_cards` if needed.
- **Cookie or region wall**: Manually accept it once with `HEADLESS = False`, or adjust the `accept_cookies_if_any` selectors.
- **Access denied / bot protection**: Add small delays or run slower networks; you can also add a small `time.sleep(1)` inside loops.
- **ChromeDriver mismatch**: `webdriver-manager` should handle it automatically. Ensure Chrome is up to date.

---

## 8) Data columns you get

| vendor    | productName | model | description | productURL | cost |
|-----------|-------------|-------|-------------|------------|------|
| troemner  | ...         | ...   | ...         | ...        | ...  |

If any fields are missing at listing level, the detail-page enrichment usually fills them.

---

## 9) License

Use this code for personal/educational purposes. Respect the website's Terms of Use.
