
# OLX Used Cars Web Scraper — Tangerang Area

A Python project that scrapes **used car listings** from [OLX Indonesia](https://www.olx.co.id/) specifically for the **Tangerang** region.  
It extracts key car details such as title, price, fuel type, transmission, engine capacity, mileage, location, and description, then saves them into **CSV** and **SQLite** formats.

---

## Tech Stack
- **Selenium** – Automates Chrome for scrolling and loading pages  
- **BeautifulSoup** – Parses HTML content from OLX pages  
- **Pandas** – Organizes and exports data  
- **SQLite3** – Saves structured data locally  

---

## Features
- Keyword-based search (e.g., *toyota*, *honda*, etc.)  
- Auto scroll & "Load more" click handling  
- Data filtering for **Tangerang** listings only  
- CSV & SQLite output  
- Error handling for smooth scraping  

---

## How to Run
1. Clone this repo:
```bash
git clone https://github.com/username/olx-tangerang-scraper.git
cd olx-tangerang-scraper
```
2. Install dependencies:
```bash
pip install selenium beautifulsoup4 pandas
```
3. Download the matching **ChromeDriver**: https://chromedriver.chromium.org/downloads  
4. Run the script:
```bash
python olx_scraper_tangerang.py
```
5. Enter your search keyword when prompted.  
Output files:
- `data_olx_tangerang.csv`
- `data_olx_tangerang.db` (table: `mobil_olx_tangerang`)

---

## Data Columns
| Column | Description |
|--------|--------------|
| title | Ad title |
| fuel | Fuel type |
| price | Car price |
| engine | Engine capacity |
| location | Seller’s area |
| transmission | Manual / Automatic |
| odometer | Mileage |
| description | Seller notes |

---

## Notes
- Avoid rapid scraping to prevent being rate-limited.  
- If OLX updates its HTML structure, selectors may need adjustment.  
- Intended for **educational & research purposes only**.

---

## ✍️ Author
**Brian Naufal**  
