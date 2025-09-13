# PyScraper

A Python web scraper specifically designed for extracting property listing data from Property24.com in Cape Town, South Africa.

## Overview

PyScraper is a targeted web scraping tool that extracts structured property data from Property24.com listings. It processes multiple pages of property listings and exports the data to CSV format for analysis and research purposes.

## Features

- **Property24.com Integration**: Specifically designed to scrape Property24 property listings
- **Multi-page Processing**: Automatically processes multiple pages of listings
- **Data Extraction**: Extracts key property details including:
  - Number of bedrooms
  - Property type (house/apartment)
  - Location
  - Area (square meters)
  - Number of bathrooms
  - Parking spaces
  - Price
- **Data Cleaning**: Handles text normalization with unidecode
- **CSV Export**: Exports structured data to CSV format
- **Error Handling**: Filters out incomplete listings and handles price variations (POA)

## Installation

### Prerequisites
- Python 3.6+
- pip package manager

### Setup
```bash
git clone https://github.com/TarCode/pyscraper.git
cd pyscraper
pip install -r requirements.txt
```

### Dependencies
```bash
pip install requests beautifulsoup4 unidecode
```

Or install from requirements.txt:
```txt
requests>=2.25.1
beautifulsoup4>=4.9.3
unidecode>=1.2.0
```

## Usage

### Basic Usage

The scraper is currently configured to scrape Cape Town property listings:

```python
python main.py
```

This will:
1. Scrape 418 pages of Property24 Cape Town listings
2. Extract property details from each listing
3. Save the results to `property-listing.csv`

### Customizing the Target

To scrape different areas or property types, modify the URL in `main.py`:

```python
# Current URL (Cape Town for-sale properties)
URL = "https://www.property24.com/for-sale/cape-town/western-cape/432"

# Examples for other areas:
# URL = "https://www.property24.com/for-sale/johannesburg/gauteng/1613"  # Johannesburg
# URL = "https://www.property24.com/to-rent/cape-town/western-cape/432"  # Cape Town rentals
```

### Adjusting Page Count

Modify the number of pages to scrape:

```python
# Scrape fewer pages for testing
processed_listing_data = get_listings_per_page(URL, 5)  # Only 5 pages

# Scrape more pages
processed_listing_data = get_listings_per_page(URL, 500)  # 500 pages
```

## Code Structure

### Main Function: `get_listings_per_page(url, number_of_pages)`

This function handles the core scraping logic:

**Parameters:**
- `url` (string): Base URL of the Property24 search results
- `number_of_pages` (int): Number of pages to scrape

**Returns:**
- List of dictionaries containing property data

**Process:**
1. Iterates through each page (URL pattern: `/p{page_number}`)
2. Parses HTML using BeautifulSoup
3. Extracts property details using CSS selectors
4. Filters for houses and apartments only
5. Cleans and normalizes extracted data
6. Returns structured property data

### Data Fields Extracted

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `bedrooms` | float | Number of bedrooms | 3.0 |
| `type` | string | Property type | "house" or "apartment" |
| `location` | string | Property location | "Claremont, Cape Town" |
| `area` | float | Property size (m²) | 120.0 |
| `bathrooms` | string | Number of bathrooms | "2" |
| `parking` | string | Parking spaces | "1" |
| `price` | float | Property price (ZAR) | 2500000.0 |

### Data Processing Features

- **Text Normalization**: Uses `unidecode` to handle special characters
- **Price Handling**: Converts prices to float, handles "POA" (Price on Application) as 0
- **Filtering**: Only includes properties with complete data sets
- **Type Detection**: Automatically categorizes as "house" or "apartment" based on title

## Output

The scraper generates a CSV file (`property-listing.csv`) with the following structure:

```csv
bedrooms,type,location,area,bathrooms,parking,price
3.0,house,"Claremont, Cape Town",150.0,2,2,2800000.0
2.0,apartment,"Sea Point, Cape Town",85.0,1,1,1950000.0
```

## Example Output Data

```python
[
    {
        "bedrooms": 3.0,
        "type": "house",
        "location": "Claremont, Cape Town",
        "area": 150.0,
        "bathrooms": "2",
        "parking": "2",
        "price": 2800000.0
    },
    {
        "bedrooms": 2.0,
        "type": "apartment", 
        "location": "Sea Point, Cape Town",
        "area": 85.0,
        "bathrooms": "1",
        "parking": "1",
        "price": 1950000.0
    }
]
```

## Limitations & Considerations

### Current Limitations
- **Single Website**: Currently only works with Property24.com
- **Fixed Selectors**: Uses hardcoded CSS selectors specific to Property24's structure
- **No Rate Limiting**: No built-in delays between requests
- **Error Handling**: Limited error handling for network issues

### Best Practices
- **Respect Terms of Service**: Ensure compliance with Property24's robots.txt and terms of service
- **Rate Limiting**: Consider adding delays between requests to avoid overwhelming the server
- **Data Validation**: Always validate scraped data before analysis

### TODO Items
The code includes a TODO note about enriching the dataset:
```python
"""
    TODO: Enrich the dataset by getting bathrooms, parking spaces and pets/no pets
"""
```
*Note: Bathrooms and parking spaces are already implemented. Pet policy extraction could be added as a future enhancement.*

## CSS Selectors Used

The scraper uses these Property24-specific CSS selectors:

- `.p24_results`: Main results container
- `.js_resultTile`: Individual listing container
- `.p24_price`: Property price
- `.p24_title`: Property title
- `.p24_location`: Property location
- `.p24_featureDetails[title='Bathrooms']`: Bathroom count
- `.p24_featureDetails[title='Parking Spaces']`: Parking count
- `.p24_size`: Property area

## Potential Enhancements

1. **Configuration File**: Add YAML/JSON configuration for URLs and parameters
2. **Multiple Websites**: Extend to support other property websites
3. **Database Export**: Add SQLite/PostgreSQL export options
4. **Image Scraping**: Extract property images
5. **Geolocation**: Add GPS coordinates extraction
6. **Rate Limiting**: Implement respectful request throttling
7. **Error Recovery**: Add retry logic for failed requests
8. **Data Validation**: Implement comprehensive data validation
9. **Logging**: Add detailed logging for debugging
10. **Command Line Interface**: Add CLI arguments for customization

## Legal Considerations

**Important**: This tool is for educational and research purposes. When using this scraper:

- Respect website terms of service
- Check and comply with robots.txt
- Implement appropriate delays between requests
- Don't overwhelm servers with rapid requests
- Use scraped data responsibly and ethically


## Changelog

### [Current Version]
- Property24.com Cape Town scraping functionality
- Multi-page processing (up to 418 pages)
- CSV export with property details
- Data cleaning and normalization
- Property type filtering (houses and apartments only)
