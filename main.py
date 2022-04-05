from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
from time import sleep

options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
macOS_service = Service('/Users/evankolberg/VS Code Projects/GOAT.com Web Scraper/chromedriver')
win_service = Service('C:\Users\ekpro\VS Code Projects\GOAT.com-Web-Scraper\chromedriver.exe')

driver = webdriver.Chrome(service=macOS_service, options=options)
driver.set_window_size(2048, 1080)
driver.set_window_position(1200, 200, windowHandle='current')


driver.get('https://goat.com')

sleep(3)

driver.close()
