from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

year = input("Enter the year you want (ex: 2000): ")
url = f"https://www.imdb.com/search/title/?release_date={year}-01-01,{year}-12-31&title_type=feature"

print(f"Fetching data for {year} using a real browser...")

with sync_playwright() as p:
    # Launch invisible Chromium browser and hide the fact that it's a bot
    browser = p.chromium.launch(
        headless=True, 
        args=['--disable-blink-features=AutomationControlled']
    ) 
    page = browser.new_page()
    
    print("Navigating to IMDb...")
    page.goto(url, wait_until="domcontentloaded")
    
    print("Waiting 5 seconds for WAF challenge...")
    page.wait_for_timeout(5000) 
    
    # Save the screenshot and HTML for debugging
    page.screenshot(path="debug_screenshot.png")
    html_content = page.content()
    
    with open("debug_playwright.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    
    browser.close()

print("Screenshot and HTML saved for debugging.")

# Parse the HTML
soup = BeautifulSoup(html_content, "html.parser")

# Find the movie titles (IMDb's h3 class)
movieList = soup.find_all('h3', class_='ipc-title__text')

# Check if we got blocked
if len(movieList) == 0:
    print("\n🚨 ERROR: Found 0 movies. Amazon's AWS WAF likely blocked us with a 403 Forbidden.")
    print("Check debug_screenshot.png and debug_playwright.html to see what happened.")
else:
    print(f"Found {len(movieList)} movies on the page!")
    
    movies = []
    i = 1
    
    for tag in tqdm(movieList):
        raw_text = tag.text
        # Clean the text to remove the index (e.g., "1. ")
        movie_title = raw_text.split('. ', 1)[1] if '. ' in raw_text else raw_text
        movies.append({'Index': i, 'Movie': movie_title})
        i += 1

    # Save to Excel
    df = pd.DataFrame(movies)
    df.to_excel(f'movies_{year}.xlsx', index=False)
    print(f"Successfully saved {len(movies)} movies to movies_{year}.xlsx!")