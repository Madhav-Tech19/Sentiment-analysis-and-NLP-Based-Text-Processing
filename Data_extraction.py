import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

input_file = 'input.xlsx'
data = pd.read_excel(input_file)

# Prepare output folder
output_folder = 'articles'
os.makedirs(output_folder, exist_ok=True)

# Function to extract article text
def extract_article(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract article title
            title = soup.find('h1').get_text(strip=True)

            # Extract article text
            paragraphs = soup.find_all('p')
            text = "\n".join([p.get_text(strip=True) for p in paragraphs])

            return title, text
        else:
            print(f"Failed to fetch URL: {url} (Status Code: {response.status_code})")
            return None, None
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return None, None

# Loop through URLs and save articles
for _, row in data.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    
    title, text = extract_article(url)
    
    if title and text:
        content = f"{title}\n\n{text}"
        
        # Save to text file
        output_path = os.path.join(output_folder, f"{url_id}.txt")
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Saved article {url_id}.txt")
    else:
        print(f"Skipping URL_ID {url_id}")

print("Extraction completed!")
