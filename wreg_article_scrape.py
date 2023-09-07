
import requests
from bs4 import BeautifulSoup

# URL to be scraped
URL = "https://wreg.com/news/local/"

# Send a GET request to the URL
response = requests.get(URL)
response.raise_for_status()  # Raise an exception if there's an error

# Parse the HTML content of the page with BeautifulSoup
html = response.text
soup = BeautifulSoup(html, 'html.parser')

def extract_articles(section_soup, is_trending=False):
    # Function to extract article details from a section of the page
    return [{
        'title': title_link.get_text(strip=True),  # Extract the article title
        'link': title_link['href'],  # Extract the article link
        'time_posted': None if is_trending else (timestamp := article.select_one("time")) and timestamp['datetime']  # Extract the time the article was posted
    } for article in section_soup.select("article.article-list__article" + ("--is-slat" if is_trending else ""))
        if (title_link := article.select_one(("h3.article-list__article-title a" if is_trending else "a.article-list__article-link")))]

# Select the sections of the page to scrape
sections = soup.select("section.article-list.article-list--story-grid.article-list-headline-with-featured-image-and-images")
all_articles = {}

for section in sections:
    # Extract the heading of each section
    heading = section.select_one("h2.article-list__heading").get_text(strip=True)
    # Extract the articles from each section
    all_articles[heading] = extract_articles(section)

# print count of articles in each section
for heading, articles in all_articles.items():
    print(f"{heading}: {len(articles)}")

# Extract the trending articles
trending_section = soup.select_one("section.article-list.article-list--trending")
all_articles["Trending Stories"] = extract_articles(trending_section, is_trending=True)

# Print the extracted data
for heading, articles in all_articles.items():
    print(f"Section: {heading}")
    for article in articles:
        print(f"Title: {article['title']}")
        print(f"Link: {article['link']}")
        print(f"Time Posted: {article['time_posted']}")
        print('-'*50)
    print('='*100)
