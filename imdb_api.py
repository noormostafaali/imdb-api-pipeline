import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load from the .env file
load_dotenv()

# Get the key from the env
api_key = os.getenv("OMDB_API_KEY")

# 1. Ask the user for the year
year = input("Enter year: (ex :2023): ")

# 2. Use the 'y=' parameter (Year of release) instead of 's=' (Title search)
# We also add '&type=movie' so it only returns movies!

"""
why ?????
Here is the trade-off:

Filtering at the API (&type=movie): The server does the work. 
It guarantees you get 10 movies.

Filtering in Pandas (df[df['Type'] == 'movie']): Your computer does the work.
 You download 10 random results, and if 3 of them are TV series, you filter
 them out and end up with 7 movies.
 
"""
url = f"https://www.omdbapi.com/?apikey={api_key}&y={year}&type=movie"

print(f"Asking the API waiter for movies released in {year}...")
response = requests.get(url)

# 3. Convert the JSON response into a Python dictionary
data = response.json()

# 4. Check if the API found anything
if data.get("Response") == "True":
    movies = data.get("Search")
    print(f"Found {len(movies)} movies!")
    
    # 5. Load straight into Pandas
    df = pd.DataFrame(movies)

    # Keep only the columns we care about
    df = df[['Title', 'Year', 'imdbID', 'Type']]

    print(df.to_string(index=False))  # Print whole df
    
    # Save to Excel
    filename = f'movies_{year}.xlsx'
    df.to_excel(filename, index=False)
    print(f"Successfully saved to {filename}!")
else:
    print("Error from API:", data.get("Error"))