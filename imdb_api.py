import requests
import pandas as pd

import os                        
from dotenv import load_dotenv

# Load the secret variables from the .env file
load_dotenv()

# Get the key from the environment
api_key = os.getenv("OMDB_API_KEY")


# 2. Let's search for movies from 2023
search_term = "2023" 
# The API endpoint we are hitting. We are using the "s" (search) parameter.
url = f"https://www.omdbapi.com/?apikey={api_key}&s={search_term}"

print("Asking the API waiter for data...")
response = requests.get(url)

# 3. Convert the JSON response into a Python dictionary
data = response.json()

# 4. Check if the API found anything
if data.get("Response") == "True":
    movies = data.get("Search")
    print(f"Found {len(movies)} movies!")
    
    # 5. Load straight into Pandas
    df = pd.DataFrame(movies)
    # noticed file has movies series and games, i only want movies so use pandas to filter.
    df = df[df['Type'] == 'movie']

    # Keep only the columns we care about
    df = df[['Title', 'Year', 'imdbID', 'Type']]

    print(df.to_string(index=False))  # Print whole df

    
    # Save to Excel
    df.to_excel('api_movies.xlsx', index=False)
    print("Successfully saved to api_movies.xlsx!")
else:
    print("Error from API:", data.get("Error"))