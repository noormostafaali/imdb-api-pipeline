import requests # A library for making HTTP requests
from bs4 import BeautifulSoup #bs4 is the package, and BeautifulSoup is a class inside it

import pandas as pd # referring to the pandas library as pd to save time typing
from tqdm import tqdm #A simple library that draws a progress bar in your terminal (helwa dyh)

# what i learned here : .venve , what it is a local folder inside my projects instead of one giant one 
"""
Imagine you are working on two Data Science projects:

Project A was written in 2021 and requires pandas==1.0 and numpy==1.18.

Project B is a new project you just started and requires pandas==2.2 and numpy==2.0.

If you install everything globally on your computer, Python can only have one
 version of a package installed at a time. If you install the new version for
   Project B, Project A will instantly break and crash because the old code doesn't 
   work with the new library updates

# ( baisically its like isolating the packages so that Project A's tools don't fight with Project B's tools)

"""

# what i learned when commiting here : pip freeze > requirements.txt magically creates a file that lists every library you installed and its exact version. It's how you tell other developers (or recruiters) what to install 


year = input("Enter the year you want ( ex: 2000 ): ")

# 2. The NEW IMDb URL
url = f"https://www.imdb.com/search/title/?release_date={year}-01-01,{year}-12-31&title_type=feature"
#show movies released between Jan 1st and Dec 31st of that year []
"""
"How would I get the URL without you?"
This is the most important question you've asked so far. In the real world,
nobody hands you the URL. You have to reverse-engineer the website. Here is how you do it:

Go to the website in your browser: Open https://www.imdb.com.

Use the UI to find the data: Click on "Advanced Search", or use their filter for "Release Date"
 and set it to 2023.

Look at the URL bar: As soon as you apply the filter, look at the address bar at the top of your 
browser. You will see the URL change to something like:
https://www.imdb.com/search/title/?release_date=2023-01-01,2023-12-31&title_type=feature

Identify the pattern: You look at that URL and say, "Okay, the URL takes parameters (release_date).
 If I change 2023 to 2024, does the page change?" Yes. So now you know how to construct the URL 
 dynamically using an f-string.

(Advanced trick: Right-click on the page, click Inspect, go to the Network tab, and refresh the page. 
You can see exactly what URLs your browser is requesting behind the scenes)"""

# 3. Disguise our script as a real Chrome browser
"""headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}
# to make the website think its a  real human chrome browser not a bot ( trying to not instatly get banned)
"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0'
}

print(f" Fetching data for {year}...") # the f before , is  f-string 
"""
whats f string ? (formatted string literal)
It tells Python, "Hey, look inside the {} brackets
 and insert the value of those variables.
"""
"""
# 4
response = requests.get(url, headers=headers)
#response holds the entire raw HTML code of the IMDb webpage as a giant string

# till now , maaya the hmtl but its EVERHTING i want smth specific 

# ADDING DEBUG LINES
print(f"Status Code: {response.status_code}")
print(f"First 500 chars of response: {response.text[:500]}")
"""

# 4. Use a Session instead of a direct request
session = requests.Session()
response = session.get(url, headers=headers)

# --- Debug Lines ---
print(f"Status Code: {response.status_code}")
print(f"Length of HTML: {len(response.text)} chars")

# now to use BeautifulSoup to act as a highlighter.

# Temporary debug line: save the HTML to a file
with open("debug_page.html", "w", encoding="utf-8") as file:
    file.write(response.text)

# 5. Parse the HTML
soup = BeautifulSoup(response.text, "html.parser") #This parses the string into a Python object (a tree) , 3amla zay DOM f java 


# 6. Find all movie containers
movieList = soup.find_all('div', class_='ipc-metadata-list-summary-item') # kol el div tags with ipc-metadata-list-summary-item
"""
How did I get that class name?
 I went to IMDb on my browser, right-clicked on a movie title,
clicked Inspect, and looked at the HTML structure. The <div> 
wrapping every movie has that specific class
"""

print(f"Found {len(movieList)} movies on the page!")

# len prints length of the list  # c starts at 1 not 0 



"""
Why is IMDb giving us a 202 and empty text?
When you visit a site with Chrome, your browser and the server do a complex "handshake". The browser sends a TLS fingerprint (a unique signature of how Chrome talks to the network), and a bunch of headers (Accept-Language, Sec-Fetch, etc.).

When Python's requests library asks for a page, it sends a very basic fingerprint. Amazon's security (AWS WAF) looks at it and says, "You say you're Chrome, but your fingerprint says you're a Python script. Nice try. Here's a 202 with an empty body to waste your time."

3. The Attack Plan
We are going to upgrade our script to look exactly like a real browser. We will:

Use a requests.Session() (this handles cookies automatically, just like a real browser).

Add all the extra headers Chrome normally sends
"""

