import requests
from bs4 import BeautifulSoup
from unidecode import unidecode
import csv
import re

"""
    TODO: Enrich the dataset by getting bathrooms, parking spaces and pets/no pets
"""


def get_listings_per_page(url, number_of_pages):
    processed_listings = []
    for x in range(1, number_of_pages):
        print('PROCESSING PAGE %d... ' % x)
        real_url = url
        if number_of_pages > 1:
            real_url = url + '?page=' + str(x)

        page = requests.get(real_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(class_='resultsItemsContainer')
        listings = results.find_all('div', class_='infoHolder')

        for listing in listings:
            price = listing.find(class_='priceDescription')
            title = listing.find(class_='title')
            location = listing.find(class_='suburb')
            # bathrooms = listing.find(class_='p24_featureDetails', attrs={"title":'Bathrooms'})
            # parking = listing.find(class_='p24_featureDetails', attrs={"title":'Parking Spaces'})
            # area = listing.find(class_='p24_size')

            if title and location and price:
                title = title.text.strip()
                location = location.text.strip()
                price = price.text.strip()
                # area = area.text.strip()
                # bathrooms = bathrooms.text.strip()
                # parking = parking.text.strip()
                if "house" in title.lower() or "apartment" in title.lower():
                    processed_listings.append({
                        "bedrooms":  float(re.search(r'\d+', title).group()) if "bed" in title.lower() else 0,
                        "location": location,
                        # "area": float(re.search(r'\d+', area).group()),
                        # "bathrooms": bathrooms,
                        # "parking": parking,
                        "price":  float(re.search(r'\d+', unidecode(price).replace(" ", "")).group()) if price != 'Sold' else 0
                    })

    return processed_listings


URL = "https://www.privateproperty.co.za/for-sale/western-cape/cape-town/cape-town-city-bowl/cape-town-city-centre/436"

processed_listing_data = get_listings_per_page(URL, 9)

print(processed_listing_data)

with open('private-property-listings.csv', mode='w') as listings_file:
    fieldnames = ['bedrooms', 'location', 'price']
    writer = csv.DictWriter(listings_file, delimiter=',', quotechar='"', fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for prop_listing in processed_listing_data:
        writer.writerow(prop_listing)

