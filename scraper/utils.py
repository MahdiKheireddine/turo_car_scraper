import csv
import re
import undetected_chromedriver as uc

def initialize_driver():
    options = uc.ChromeOptions()
    options.headless = False  # Set to True to run in headless mode
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options)
    driver.maximize_window()
    return driver

def save_to_csv(car_data_list, location, start_date, end_date):
    formatted_location = re.sub(r'[^\w\s]', '', location).replace(' ', '_')
    formatted_start_date = start_date.replace('/', '-')
    formatted_end_date = end_date.replace('/', '-')
    csv_file = f"data/car_listings_{formatted_location}_{formatted_start_date}_to_{formatted_end_date}.csv"
    
    csv_columns = ['Car Name', 'Car Rating', 'Number of Trips', 'Car placement', 'Total price', 'Discount', 'Price', 'Link', 'Description', 'Options', 'Caracteristique']
    
    try:
        with open(csv_file, mode='w', newline='', encoding='latin-1', errors='replace') as file:
            writer = csv.DictWriter(file, fieldnames=csv_columns)
            writer.writeheader()
            for data in car_data_list:
                writer.writerow(data)
        print(f"Data successfully saved to {csv_file}")
    except IOError as e:
        print(f"I/O error: {e}")
