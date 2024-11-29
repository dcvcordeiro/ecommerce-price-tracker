import os
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from lxml import etree

import database
from data_model import ProductPlatform

def parser(url, xpath):
    
    # Configure Chrome options
    options = Options()
    options.add_argument('--headless=new')
    driver = Chrome(options=options)
    driver.set_page_load_timeout(10)

    driver.get(url)
    html = driver.page_source

    driver.quit()

    soup = BeautifulSoup(html, 'html.parser')
    dom = etree.HTML(str(soup))
    
    price = dom.xpath(xpath)[0].text
    return price

def sanitize_price(price_str):

    price = price_str.replace("\xa0","") #replaces &nbsp;
    price = price.strip(" ").split("€")[0] # This can cause issues if value is on the right side of the currency symbol
    price = price.replace(" ","")
    price = price.replace(",", ".")
    return float(price)

def update_prices():
    db_session = database.get_database_session()
    product_mapping = db_session.query(ProductPlatform).all()

    for mapping in product_mapping:
        xpath_env = f"{mapping.platform.name.upper()}_PRICE_XPATH"
        xpath = os.getenv(xpath_env)
        price = parser(mapping.url, xpath)
        product_price = sanitize_price(price)
            
        database.add_price(db_session, mapping.id, product_price)


if __name__ == "__main__":
    
   update_prices()