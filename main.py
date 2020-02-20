import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import csv


def get_listings_per_page(url, number_of_pages):
    processed_listings = []
    for x in range(1, number_of_pages):
        print('PROCESSING PAGE %d... ' % x)
        real_url = url
        if number_of_pages > 1:
            real_url = url + '/p' + str(x)

        page = requests.get(real_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(class_='p24_results')
        listings = results.find_all('div', class_='js_resultTile')

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

    return processed_listings


URL = "https://www.property24.com/for-sale/cape-town/western-cape/432"

processed_listing_data = get_listings_per_page(URL, 20)

print(processed_listing_data)

with open('property-listings.csv', mode='w') as listings_file:
    writer = csv.writer(listings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for l in processed_listing_data:
        writer.writerow([l['title'], l['location'], l['area'], l['price']])

