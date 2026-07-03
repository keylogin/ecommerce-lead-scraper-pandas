# E-commerce Lead Generation Scraper & Data Pipeline

A high-performance Python automated pipeline designed to extract, filter, and clean e-commerce store data. This tool utilizes multi-threading for fast live website validation and leverages the Pandas library to deliver a 100% duplicate-free, structured B2B outreach dataset.

## 🚀 Key Features
* **Advanced Multi-Threading:** Uses `concurrent.futures` to dynamically validate website status codes and live domains concurrently, reducing execution time by up to 80%.
* **Smart Data Extraction:** Built with `BeautifulSoup` to parse structure, isolate brands, and target direct contact form URLs (`/contact`, `/pages/contact-us`) for automated form-filling outreach.
* **Pandas Data Cleaning:** Automated data wrangling pipeline that drops missing values (NaNs), standardizes text formats, normalizes domain URLs, and guarantees 0% brand duplication.
* **Outreach-Ready Output:** Generates clean, production-ready `.csv` and `.json` files optimized for instant integration into CRM or Cold Email platforms.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Data Extraction:** BeautifulSoup4, Requests
* **Data Architecture & Processing:** Pandas
* **Concurrency:** Concurrent.futures (ThreadPoolExecutor)

## 📊 Data Schema Delivered
The final pipeline outputs a structured table containing:
1. **Brand Name** (Normalized and formatted)
2. **Website URL** (Live, secure HTTPS links)
3. **Contact Page URL** (Direct route for outreach)
4. **Verification Status** (Live status check verified as of July 2026)

## ⚙️ Quick Start
1. Clone the repository:
   ```bash
   git clone [https://github.com/keylogin/ecommerce-lead-scraper-pandas.git](https://github.com/YOUR_USERNAME/ecommerce-lead-scraper-pandas.git)

2.   Install dependencies:
Bash

pip install pandas beautifulsoup4 requests

3. Run the pipeline:
Bash

python scraper.py
