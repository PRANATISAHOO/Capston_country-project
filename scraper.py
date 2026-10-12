import requests
from bs4 import BeautifulSoup 

URL = "https://www.scrapethissite.com/pages/simple/"

def scrape_countries(limit =20):
    response = requests.get(URL, timeout=20)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    country_blocks = soup.select("div.country")
    countries = []
    for block in country_blocks[:limit]:
        name = block.select_one('.country-name')
        capital = block.select_one('.country-capital')
        population = block.select_one('.country-population')
        area = block.select_one('.country-area')
        countries.append({
            "country_name":name.get_text(strip=True),
            "capital":capital.get_text(strip=True),
            "population":int(population.get_text(strip=True)),
            "area":float(area.get_text(strip=True))
        })
    return countries

if __name__ == "__main__":
    data = scrape_countries()
    print(f"Scraped {len(data)} countries")
    for country in data:
        print(country)
