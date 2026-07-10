
pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
import time

def scrape_quotes(url):
    # 1. Define a User-Agent header (helps avoid getting blocked by identifying your scraper as a standard browser)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print(f"Scraping: {url}...\n")
    
    try:
        # 2. Send an HTTP GET request to the URL
        response = requests.get(url, headers=headers)
        
        # Raise an exception if the request was unsuccessful (e.g., 404 or 500 error)
        response.raise_for_status()
        
        # 3. Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 4. Find the specific HTML elements containing the data
        # On quotes.toscrape.com, each quote is wrapped in a <div class="quote">
        quotes_elements = soup.find_all('div', class_='quote')
        
        scraped_data = []
        
        # 5. Extract text from the elements
        for element in quotes_elements:
            # Extract the quote text (span with class "text")
            text = element.find('span', class_='text').get_text(strip=True)
            
            # Extract the author (small tag with class "author")
            author = element.find('small', class_='author').get_text(strip=True)
            
            # Save the extracted data into a dictionary
            scraped_data.append({
                'quote': text,
                'author': author
            })
            
        return scraped_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

# --- Main Execution ---
if __name__ == "__main__":
    target_url = 'http://quotes.toscrape.com/'
    
    # Run the scraper
    results = scrape_quotes(target_url)
    
    # Print the results
    if results:
        print("--- Extracted Quotes ---")
        for i, item in enumerate(results, 1):
            print(f"{i}. {item['quote']}")
            print(f"   - {item['author']}\n")
            
        # Be polite to the server by adding a small delay if scraping multiple pages
        time.sleep(1)
