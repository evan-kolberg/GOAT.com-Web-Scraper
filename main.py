from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup

user_agent = '''Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) 
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Mobile Safari/537.36'''

options = FirefoxOptions()
options.set_preference('--general.useragent.override', user_agent)
options.add_argument('--width=960')
options.add_argument('--height=540')
driver = Firefox(service=Service(GeckoDriverManager().install()), options=options)


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
            print('Structure 1')
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
            print('Structure 2')
            for i in soup.findAll('div', {'data-qa': 'buy_bar_item_desktop'}):
                data = i.get_text()
                if 'Currently Unavailable' in data:
                    data = data[:data.find('C')] + ' ' + data[data.find('C'):]
                else:
                    data = data[:data.find('$')] + ' ' + data[data.find('$'):]
                prices.append(data.upper())

        # product structure 3
        elif soup.find('div', {'class': 'swiper-slide'}):
            print('Structure 3')
            for i in soup.findAll('div', {'class': 'swiper-slide'}):
                data = i.get_text()
                if 'Currently Unavailable' in data:
                    data = data[:data.find('C')] + ' ' + data[data.find('C'):]
                else:
                    data = data[:data.find('$')] + ' ' + data[data.find('$'):]
                if not len(data) <= 1:
                    prices.append(data.upper())

        # if no matching structures are present
        else: 
            if len(prices) == 0:
                prices.append('Need to add support for this structure')

        print(f'{product_info}')
        print(f'{prices}\n')
    


if __name__ == '__main__':
    inquery(input('\nSearch at https://goat.com:  '))
    data_hound()
    driver.quit()
