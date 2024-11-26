import requests
from bs4 import BeautifulSoup

import database
from data_model import ProductPlatform

def get_amazon_price(session, url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", 
        "Accept-Encoding":"gzip, deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
        "DNT":"1",
        "Connection":"close",
        "Upgrade-Insecure-Requests":"1"
    }
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    try:
        lateral_box_div = soup.find("div", attrs={'class': 'a-box-group'})
        price = lateral_box_div.find("span", attrs={'class':'a-offscreen'})
        price= float(price.string.strip("€").replace(",", "."))
    except Exception as e:
        price = -1
    return price

def update_prices():
    db_session = database.get_database_session()
    request_session = requests.Session()
    product_mapping = db_session.query(ProductPlatform).all()

    for mapping in product_mapping:
        if mapping.platform.name == "Amazon":
            product_price = get_amazon_price(request_session, mapping.url)
        else:
            product_price = -1
        if product_price == -1:
            continue
        database.add_price(db_session, mapping.id, product_price)


if __name__ == "__main__":
    
   update_prices()