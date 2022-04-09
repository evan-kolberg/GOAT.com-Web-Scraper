from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import os

os.environ['WDM_LOG_LEVEL'] = '0'    # prevents webdriver manager from printing, it is quite annoying tbh

ua = UserAgent(verify_ssl=False)

options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')    # helps go undetected
options.add_argument(f'--user-agent={ua}')
options.add_argument('--window-size=960,540')
options.add_argument('--incognito')    # doesn't save cookies after session
driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

# adds extra protection against getting detected
stealth(driver,
        languages=['en-US', 'en'],
        vendor='Google Inc.',
        platform='Win32',
        webgl_vendor='Intel Inc.',
        renderer='Intel Iris OpenGL Engine',
        fix_hairline=True)

driver.set_window_position(0, 0, windowHandle='current')


def inquery(query):
    # creates the site-friendly query string
    query = query.split()
    for i in range(len(query)*2):
        if i % 2 == 1:
            query.insert(i, '%20')
    query = ''.join(query)

    driver.get(f'https://www.goat.com/search?query={query}')


def data_hound():
    link_queue = []

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for i in soup.findAll('div', {'data-qa': 'grid_cell_product'}):
        link_queue.append(f"https://goat.com{i.find(href=True)['href']}")
    print('\n')

    for i in link_queue:
        prices = []
        counter = 0

        driver.get(i)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # gets the product info
        try:
            product_info = soup.find('div', {'data-qa': 'product_year'}).get_text().replace(soup.find('ol').get_text(), '')
        except AttributeError:    # cannot convert NoneType to text, because no text was loaded
            print(soup.find('body').get_text())
            driver.quit()

        # product structure 1
        if soup.find('div', {'data-swiper-slide-index':0}):
            while True:
                if soup.find('div', {'data-swiper-slide-index':counter}):
                    data = soup.find('div', {'data-swiper-slide-index':counter}).get_text()
                    if 'Currently Unavailable' in data:
                            data = data[:data.find('C')] + ' ' + data[data.find('C'):]
                    else:
                        data = data[:data.find('$')] + ' ' + data[data.find('$'):]
                    prices.append(data.upper())
                    counter += 1
                else:
                    break

        # product structure 2
        elif soup.find('div', {'data-qa': 'buy_bar_item_desktop'}):
            for i in soup.findAll('div', {'data-qa': 'buy_bar_item_desktop'}):
                data = i.get_text()
                if 'Currently Unavailable' in data:
                    data = data[:data.find('C')] + ' ' + data[data.find('C'):]
                else:
                    data = data[:data.find('$')] + ' ' + data[data.find('$'):]
                if len(data) > 1:
                    prices.append(data.upper())

        # product structure 3
        elif soup.find('div', {'class': 'swiper-slide'}):
            for i in soup.findAll('div', {'class': 'swiper-slide'}):
                data = i.get_text()
                if 'Currently Unavailable' in data:
                    data = data[:data.find('C')] + ' ' + data[data.find('C'):]
                else:
                    data = data[:data.find('$')] + ' ' + data[data.find('$'):]
                if len(data) > 1:
                    prices.append(data.upper())

        # if no matching structures are present
        else: 
            if len(prices) == 0:
                prices.append('No structure found within webpage')

        print(f'{product_info}')
        print(f'{prices}\n')
    


if __name__ == '__main__':
    inquery(input('\nSearch at https://goat.com:  '))
    data_hound()
    driver.quit()
