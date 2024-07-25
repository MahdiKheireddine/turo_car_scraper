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

## Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/turo_car_scraper.git
   cd turo_car_scraper
   pip install -r requirements.txt

 2. **Run the scraper:**
    ```bash
    python main.py "location" "start_date" "end_date"
    
  Replace "location", "start_date", and "end_date" with your desired values. For example:
    ```bash
    python main.py "Paris" "07/25/2024" "07/30/2024"

      


