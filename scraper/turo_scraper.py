import time
import urllib.parse
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from .utils import initialize_driver, save_to_csv

class TuroScraper:
    def __init__(self, location, start_date, end_date):
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.location_encoded = urllib.parse.quote(location)
        self.url = self.construct_url()
        self.car_data_list = []

    def construct_url(self):
        # Construct the Turo URL with the provided parameters
        return (f"https://turo.com/fr/fr/search?country=FR&defaultZoomLevel=11&deliveryLocationType=city&"
                f"endDate={self.end_date}&endTime=10%3A00&isMapSearch=false&itemsPerPage=200&"
                f"latitude=48.8575475&location={self.location_encoded}&locationType=CITY&"
                "pickupType=ALL&placeId=ChIJD7fiBh9u5kcRYJSMaMOCCwQ&region=IDF&"
                f"sortType=RELEVANCE&startDate={self.start_date}&startTime=10%3A00&"
                "useDefaultMaximumDistance=true")

    def scrape(self):
        # Initialize the WebDriver for scrolling and collecting data
        driver = initialize_driver()
        all_divs = self.scroll_and_collect(driver)
        driver.quit()

        # Process the collected data
        self.process_data(all_divs)

        # Visit individual car pages to extract additional details
        driver = initialize_driver()
        self.extract_additional_details(driver)
        driver.quit()

        # Save the data to a CSV file
        save_to_csv(self.car_data_list, self.location, self.start_date, self.end_date)

    def scroll_and_collect(self, driver):
        # Scroll down the page and collect car listings
        all_divs = {}
        try:
            driver.get(self.url)
            time.sleep(10)  # Allow the page to load

            scroll_container = driver.find_element(By.CSS_SELECTOR, 'div[data-test-id="virtuoso-scroller"]')

            for _ in range(3):  # Adjust the number of scrolls as needed
                listing_container = driver.find_element(By.CSS_SELECTOR, 'div[data-test-id="virtuoso-item-list"]')
                cars_divs = listing_container.find_elements(By.XPATH, "./div")
                for car in cars_divs:
                    car_id = car.get_attribute("data-index")
                    if car_id not in all_divs:
                        all_divs[int(car_id)] = car.get_attribute('outerHTML')
                scroll_container.send_keys(Keys.PAGE_DOWN)
                time.sleep(0.2)  # Adjust the wait time as needed

        except Exception as e:
            print(f"Error during initial scraping: {e}")

        return {k: all_divs[k] for k in sorted(all_divs.keys())}

    def process_data(self, sorted_all_divs):
        # Use BeautifulSoup to parse the HTML and extract car details
        for car_html in sorted_all_divs.values():
            try:
                soup = BeautifulSoup(car_html, 'html.parser')
                car_info_element = soup.find('div', {'data-testid': 'SearchResultWrapper'}).find('div').find('a').find('div').find_all('div', recursive=False)[1]

                car_name = self.extract_car_name(car_info_element)
                car_location = self.extract_car_location(car_info_element)
                car_rating, number_of_trips = self.extract_car_rating_and_trips(car_info_element)
                total_price, discount, price = self.extract_car_prices(car_info_element)
                car_link = self.extract_car_link(soup)

                self.car_data_list.append({
                    'Car Name': car_name,
                    'Car Rating': car_rating,
                    'Number of Trips': number_of_trips,
                    'Car placement': car_location,
                    'Total price': total_price,
                    'Discount': discount,
                    'Price': price,
                    'Link': car_link
                })
            except Exception as e:
                print(f"Error extracting car details: {e}")

    def extract_car_name(self, car_info_element):
        # Extract the car name
        car_name_element = car_info_element.find_all('div')[0].find_all('div')[0].find_all('div')[0]
        return car_name_element.text

    def extract_car_location(self, car_info_element):
        # Extract the car location
        car_location_element = car_info_element.find_all('div')[0].find_all('div', recursive=False)[2].find('p')
        return car_location_element.text

    def extract_car_rating_and_trips(self, car_info_element):
        # Extract the car rating and number of trips
        voyages = car_info_element.find_all('div')[0].find_all('div', recursive=False)[1]
        if voyages.find('p', recursive=False):
            return 0, 0
        else:
            car_rating = voyages.find('div').find('div').find('div').find('p').text
            number = voyages.find('div').find('div').find('p', recursive=False).text
            number_of_trips = re.findall(r'\d+', number)[0]
            return car_rating, number_of_trips

    def extract_car_prices(self, car_info_element):
        # Extract the car prices
        prices_element = car_info_element.find('div', {'data-testid': 'price-details-container'}).find('div', {'data-testid': 'vehicle-discount-and-daily-price'})
        child_elements = prices_element.find_all(recursive=False)
        num_child_elements = len(child_elements)
        if num_child_elements > 1:
            discount_text = prices_element.find_all('div')[0].find('p').text
            discount = re.findall(r'\d+', discount_text)[0]
            total_price_text = prices_element.find('span', class_='css-1mtd86-StyledText-TotalPrice').text
            total_price = re.findall(r'\d+', total_price_text)[0]
            price_text = prices_element.find('span', class_='css-1vmc2vr-StyledText').text
            price = re.findall(r'\d+', price_text)[0]
        else:
            price_text = prices_element.find('span').text
            price = re.findall(r'\d+', price_text)[0]
            total_price = price
            discount = 0
        return total_price, discount, price

    def extract_car_link(self, soup):
        # Extract the car link
        car_link = soup.find('div', {'data-testid': 'SearchResultWrapper'}).find('div').find('a').get('href')
        return "https://turo.com" + car_link

    def extract_additional_details(self, driver):
        # Visit individual car pages to extract additional details
        try:
            for car in self.car_data_list:
                try:
                    driver.get(car['Link'])
                    time.sleep(2)  # Adjust as needed
                    car_soup = BeautifulSoup(driver.page_source, 'html.parser')

                    main_div = car_soup.find('div', {'data-testid': 'row'}).find_all('div', recursive=False)[0].find('div')
                    divs = main_div.find_all('div', recursive=False)

                    car['Options'] = self.extract_car_options(divs)
                    car['Description'] = self.extract_car_description(divs)
                    car['Caracteristique'] = self.extract_car_caracteristiques(divs)

                except Exception as e:
                    print(f"Error extracting details from car page: {e}")

        finally:
            driver.quit()

    def extract_car_options(self, divs):
        # Extract car options
        options_div = divs[1].find('div')
        options = ""
        if options_div:
            option_elements = options_div.find_all('div', recursive=False)
            for option_element in option_elements:
                option = option_element.find('div').find('p').text
                options = option if options == "" else options + " - " + option
        return options if options else 'N/A'

    def extract_car_description(self, divs):
        # Extract car description
        description_element = divs[3].find('div').find_all('div', recursive=False)[1].find('div').find_all('div', recursive=False)[0].find('div').find('div').find('p')
        return description_element.text

    def extract_car_caracteristiques(self, divs):
        # Extract car characteristics
        caracterstiques_div = divs[3].find('section').find('div').find_all('div', recursive=False)[1].find('div').find('div').find('div').find('div')
        caracterstiques = ""
        if caracterstiques_div:
            caracterstiques_elements = caracterstiques_div.find_all('div', recursive=False)
            for caracterstiques_element in caracterstiques_elements:
                caracterstique = caracterstiques_element.find('div').find('div').find('p').text
                caracterstiques = caracterstique if caracterstiques == "" else caracterstiques + " - " + caracterstique
        return caracterstiques if caracterstiques else 'N/A'
