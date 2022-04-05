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
win_service = Service(r'C:\Users\ekpro\VS Code Projects\GOAT.com-Web-Scraper\chromedriver.exe')

driver = webdriver.Chrome(service=win_service, options=options)
driver.set_window_size(2048, 1080)
driver.set_window_position(1200, 200, windowHandle='current')



def on_the_hunt(query):

    # creates the site-friendly query string
    query = query.split()
    for i in range(len(query)*2):
        if i % 2 == 1:
            query.insert(i, '%20')
    query = ''.join(query)
    # ----------------------------------------

    driver.get(f'https://www.goat.com/search?query={query}')





if __name__ == '__main__':
    on_the_hunt('air jordan pro blue')
    driver.close()
