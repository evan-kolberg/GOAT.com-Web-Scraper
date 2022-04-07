from itertools import product
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
macOS_service = Service('/Users/evankolberg/VS Code Projects/GOAT.com Web Scraper/chromedriver')
win_service = Service('C:/Users/ekpro/VS Code Projects/GOAT.com-Web-Scraper/chromedriver.exe')

driver = webdriver.Chrome(service=macOS_service, options=options)
driver.set_window_size(2048, 1080)
driver.set_window_position(1200, 200, windowHandle='current')



def inquery(query):
    # creates the site-friendly query string
    query = query.split()
    for i in range(len(query)*2):
        if i % 2 == 1:
            query.insert(i, '%20')
    query = ''.join(query)
    # ----------------------------------------

    driver.get(f'https://www.goat.com/search?query={query}')


def crawler():
    link_queue = []

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for i in soup.findAll('div', {'data-qa': 'grid_cell_product'}):
        link_queue.append(f"https://goat.com{i.find(href=True)['href']}")

    # print(link_queue)

    for i in link_queue:
        driver.get(i)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        product_info = soup.find('div', {'data-qa': 'product_year'}).get_text().replace(soup.find('ol').get_text(), '')
        product_prices = soup.find('div', {'data-qa': 'buy_bar_desktop'}).get_text()

        print('\n', product_info)
        print(product_prices, '\n')


    


if __name__ == '__main__':
    inquery('air jordan pro')
    crawler()
    driver.quit()
