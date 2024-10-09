import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_model import Base, Platform

def get_amazon_price(session, url):
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", 
        "Accept-Encoding":"gzip, deflate",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT":"1",
        "Connection":"close",
        "Upgrade-Insecure-Requests":"1"
    }
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    try:
        price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()

    except AttributeError:
        price = ""	
    print(price)
    
    exit()
    # price = soup.find('span', {'id': 'priceblock_ourprice'}).text
    # return price

def add_platforms():
    platforms = ['Amazon', 'Worten', 'Fnac']
    for platform_name in platforms:
        platform = Platform(name=platform_name)
        session.add(platform)
    session.commit()

add_platforms()

if __name__ == "__main__":
    
    # 1. Define DB if not defined
    engine = create_engine('sqlite:///prices.db')
    Base.metadata.create_all(engine)

    SessionDB = sessionmaker(bind=engine)
    db_session = SessionDB()

    session = requests.Session()
    url = 'https://www.amazon.es/-/pt/dp/B0C1H3KJ2C/'
    #print(get_amazon_price(session, url))

    # 2. Fetch the products to be searched

    # 3. Web-scrapping each of the sites (multi-threadding)

    # 4. Load data into DB

 