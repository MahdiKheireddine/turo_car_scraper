import argparse
from scraper.turo_scraper import TuroScraper

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Scrape Turo car listings for a specified location and date range.')
    parser.add_argument('location', type=str, help='Location for car rentals')
    parser.add_argument('start_date', type=str, help='Start date for car rentals (MM/DD/YYYY)')
    parser.add_argument('end_date', type=str, help='End date for car rentals (MM/DD/YYYY)')
    args = parser.parse_args()

    # Assign the arguments to variables
    location = args.location
    start_date = args.start_date
    end_date = args.end_date

    # Create an instance of TuroScraper and start scraping
    scraper = TuroScraper(location, start_date, end_date)
    scraper.scrape()

if __name__ == "__main__":
    main()
