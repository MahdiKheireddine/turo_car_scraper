# Turo Car Scraper

A Python web scraper for collecting car listings from Turo, extracting detailed information, and exporting data to CSV files. This project uses `selenium` with `undetected-chromedriver` to scrape the data and `BeautifulSoup` to parse the HTML.

## Features

- **Scrapes car listings**: Collects car details such as name, rating, number of trips, location, prices, and discount.
- **Visits individual car pages**: Extracts additional details such as options, description, and characteristics.
- **Saves data to CSV**: Exports the collected data to a CSV file for further analysis.

## Requirements

- Python 3.7+
- Install the required packages:
  ```bash
  pip install -r requirements.txt
