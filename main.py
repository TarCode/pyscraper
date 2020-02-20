import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import csv

URL = "https://www.property24.com/for-sale/cape-town/western-cape/432"

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(class_='p24_results')

listings = results.find_all('div', class_='js_resultTile')

processed_listings = []

for listing in listings:
    price = listing.find(class_='p24_price')
    title = listing.find(class_='p24_title')
    location = listing.find(class_='p24_location')
    description = listing.find(class_='p24_excerpt')
    area = listing.find(class_='p24_size')
    if title and location and price and area and description:
        title = title.text.strip()
        location = location.text.strip()
        price = price.text.strip()
        area = area.text.strip()
        description = description.text.strip()

        processed_listings.append({
            "title": title,
            "location": location,
            "price": unidecode(price),
            "description": unidecode(description),
            "area": area
        })
        print('***************************************************************')
        print(title + ' ' + location + ' ' + area + ' ' + price)

print(processed_listings)

with open('property-listings.csv', mode='w') as listings_file:
    writer = csv.writer(listings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for listing in processed_listings:
        writer.writerow([listing['title'], listing['location'], listing['area'], listing['price']])

