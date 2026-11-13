# IMDb Data Pipeline: Scraping vs. API

## Project Overview
The goal of this project was to build a data pipeline to fetch movie data. This repository documents the journey from attempting traditional web scraping to pivoting to a professional API solution.

## The Journey
1. **Attempt 1: Web Scraping (Failed)**
   I initially tried to scrape IMDb using `requests` and `BeautifulSoup`. I quickly encountered a `202 Accepted` followed by a `403 Forbidden` from Amazon's AWS WAF (Web Application Firewall).
2. **Attempt 2: Headless Browser (Failed)**
   I tried using `Playwright` (a headless Chromium browser) to bypass the JavaScript challenge. IMDb's security successfully detected the bot and blocked the request. 
   *(See `scraper_v1_requests_failed.py` and `scraper_failed_imdb_playwright.py` for the code and my learning notes).*
3. **Attempt 3: The API Pivot (Success!)**
   I realized that IMDb's Terms of Service prohibit scraping, and that APIs are the industry standard for Data Science. I pivoted to the OMDb API, which provides clean, structured JSON data.

## Technologies Used
*   **Python 3**
*   **requests** (HTTP library)
*   **pandas** (Data manipulation)
*   **python-dotenv** (Environment variable management)
*   **OMDb API** (Movie data source)

## How to Run the Final Script
1. Clone the repository.
2. Create a `.env` file in the root directory and add your OMDb API key: 
   `OMDB_API_KEY=your_api_key_here`
3. Install the required packages:
   `pip install -r requirements.txt`
4. Run the script:
   `python imdb_api.py`

## Key Learnings
*   Understood the difference between scraping HTML and consuming JSON APIs.
*   Learned how to protect API keys using `.env` files and `.gitignore`.
*   Practiced data cleaning and filtering using Pandas DataFrames.