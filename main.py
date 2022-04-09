from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from bs4 import BeautifulSoup


options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36')
options.add_experimental_option('excludeSwitches', ['enable-logging'])    # disables annoying chrome flag errors
options.add_argument('--window-position=0,0')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')
options.add_argument('--proxy-server="direct://"')
options.add_argument('--proxy-bypass-list=*')
options.add_argument('--incognito')
driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()), options=options)


def inquery(query):
    # creates the site-friendly query string
    query = query.split()
    for i in range(len(query)*2):
        if i % 2 == 1:
            query.insert(i, '%20')
    query = ''.join(query)

    driver.get(f'https://www.goat.com/search?query={query}')


def crawler():
    link_queue = []

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for i in soup.findAll('div', {'data-qa': 'grid_cell_product'}):
        link_queue.append(f"https://goat.com{i.find(href=True)['href']}")

    for i in link_queue:
        prices = []
        counter = 0

        driver.get(i)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # gets the name of the product
        product_info = soup.find('div', {'data-qa': 'product_year'}).get_text().replace(soup.find('ol').get_text(), '')

        # for shoes, it iterates through all the available sizes
        if soup.find('div', {'data-swiper-slide-index':0}): # tests if it is infact shoes
            while True:
                if soup.find('div', {'data-swiper-slide-index':counter}):
                    data = soup.find('div', {'data-swiper-slide-index':counter}).get_text()
                    data = data[:data.find('$')] + ' ' + data[data.find('$'):]
                    if data.find('C') != -1: # checks to see if the price on the site actually says Currently Unavailable
                            data = data[:data.find('C')] + ' ' + data[data.find('C'):]
                    prices.append(data.upper())
                    counter += 1
                else:
                    break
        else:
            # for other things, NOT shoes, with the names of sizes
            if soup.find('div', {'data-qa': 'buy_bar_item_desktop'}):
                for i in soup.findAll('div', {'data-qa': 'buy_bar_item_desktop'}):
                    data = i.get_text()
                    data = data[:data.find('$')] + ' ' + data[data.find('$'):]
                    if data.find('C') != -1: # checks to see if the price on the site actually says Currently Unavailable
                        data = data[:data.find('C')] + ' ' + data[data.find('C'):]
                    prices.append(data.upper())

        # if there are no prices
        if len(prices) == 0:
            prices.append('Need to add support for this structure')
        

        print(f'\n{product_info}')
        print(f'{prices}\n')
    


if __name__ == '__main__':
    inquery(input('\nSearch at https://goat.com:  '))
    crawler()
    driver.quit()
