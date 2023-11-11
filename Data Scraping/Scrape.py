from modules.selenium_module import WeatherScraper
from modules.scraping import list_all_station, click_dropdown_option
from datetime import datetime
import time
import requests
import csv

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]


def scrape_data(month_input, year_input):
    webscraper = WeatherScraper()
    all_possible_stations = list_all_station(webscraper)
    all_possible_stations = all_possible_stations[::-1]

    all_data = []
    for station_input in all_possible_stations:
        print(f'Processing station {station_input}')
    for station_input in all_possible_stations:
        print(f'Processing station {station_input}')

        is_station_available = click_dropdown_option(webscraper, 'cityname', station_input)
        time.sleep(2)

        is_year_available = click_dropdown_option(webscraper, 'year', year_input)
        if not is_year_available:
            print(f"Station {station_input} does not have weather data in {year_input}")
            continue
        time.sleep(3)

        is_month_available = click_dropdown_option(webscraper, 'month', month_input)
        if not is_month_available:
            print(f"Station {station_input} does not have weather data in {month_input} {year_input}")
            continue
        time.sleep(1)

        display_button = webscraper.get_element('id', 'display')
        display_button.click()
        time.sleep(2)

        download_link_parent_element = webscraper.get_element('class', 'download-link')
        csv_download_elements = webscraper.get_next_element('child', download_link_parent_element)[0]
        csv_download_url = csv_download_elements.get_attribute('href')
        print(f'Downloading from: {csv_download_url}')

        if csv_download_url:
            response = requests.get(csv_download_url)
            time.sleep(2)
            string_response = response.text
            splitted_resp = string_response.split('\n')
            if len(all_data) == 0:
                header = splitted_resp[0]
                header = header.split(',')
                all_data = [header]
            data = splitted_resp[1:]
            data = [el.split(',') for el in data]
            all_data.extend(data)

    filename = f"{month_input}_{year_input}_data.csv"
    with open(filename, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(all_data)

    webscraper.close_session()


if __name__ == '__main__':
    start_time = datetime.now()

    for year in range(2013, 2014):
        for month in MONTHS:
            if year == 2013 and month == "April":
                break
            print(f"Scraping data for {month} {year}")
            scrape_data(month, str(year))

    finish_time = datetime.now()
    duration = (finish_time - start_time).seconds
    print(f'The process took {str(duration)} seconds to complete')