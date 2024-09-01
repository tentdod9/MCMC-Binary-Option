from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
from thai_date import parse_thai_date

def settrade_scraping(symbol="TDEX"):
    # Set up the Chrome driver using webdriver_manager
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    # Open the URL with Selenium
    url1 = f"https://www.settrade.com/th/equities/quote/{symbol.upper()}/historical-trading"
    url2 = f"https://www.settrade.com/th/equities/etf/quote/{symbol.upper()}/historical-trading"
    # print(url1)
    driver.get(url1)
    if driver.current_url == "https://www.settrade.com/th/error/404":
        driver.quit()
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.maximize_window()
        driver.get(url2)
    # Optional: wait for the content to load
    driver.implicitly_wait(10)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(0.5)
        # Calculate new scroll height and compare with the last height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    display_option_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div/div/div[1]/div[4]/div[1]/div/div[2]/div/div[1]')
    display_option_button.click()
    show_all_option = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div[3]/div[2]/div/div/div/div[1]/div[4]/div[1]/div/div[2]/div/div[3]/ul/li[5]/span/div')
    show_all_option.click()
    time.sleep(1)
    # Extract page content using Selenium
    page_source = driver.page_source

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Close the driver
    driver.quit()
    # Find the table
    # table = soup.find('table')
    table = soup.find('table', {'class': 'table b-table table-custom-field table-custom-field--cnc table-hover-underline b-table-no-border-collapse'})

    # Extract the table headers
    header_elements = table.find_all('th')
    headers = [header.text.strip().split('\n        (Click to sort Ascending)')[0] for header in header_elements]

    # Extract the table rows
    rows = []

    for row in table.find('tbody').find_all('tr'):  # Skip the header row
        cells = row.find_all('td')
        # print(cells)
        row_data = [cell.text.strip() for cell in cells]
        # print(row_data)
        row_data[0] = parse_thai_date(row_data[0])
        rows.append(row_data)

    return headers[:8], [_[:8] for _ in rows]

# Create a DataFrame
# df = pd.DataFrame(rows, columns=headers)
# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 1000)
# pd.set_option('display.colheader_justify', 'center')
#
# # Display the DataFrame
# print(headers)
# print(df.head())

if __name__ == '__main__':
    settrade_scraping(symbol="M")