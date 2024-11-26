from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import json
from dotenv import load_dotenv

from data_model import Base, Product, Platform, ProductPlatform, PriceHistory

load_dotenv() 

def get_database_session():
    db = os.getenv("DATABASE")
    engine = create_engine(f'sqlite:///{db}')
    SessionDB = sessionmaker(bind=engine)
    session_db = SessionDB()
    
    if not os.path.exists(db):
        Base.metadata.create_all(engine)
        setup_db(session_db)

    return session_db

def setup_db(session_db):

    with open(os.getenv("DATABASE_INIT"), "r") as fp:
        products = json.load(fp)
    
    for product in products:
        product_id = add_product(session_db, product["name"])
        for platform, url in product["platformsURL"].items():
            platform_id = add_platform(session_db, platform)
            add_map_product_platform(session_db, product_id, platform_id, url)


def add_product(session_db, product_name):
    product = session_db.query(Product).filter_by(name=product_name).first()
    
    if not product:
        product = Product(name=product_name)
        session_db.add(product)
        session_db.commit()

    return product.id
    
def add_platform(session_db, platform_name):
    platform = session_db.query(Platform).filter_by(name=platform_name).first()
    
    if not platform:
        platform = Platform(name=platform_name)
        session_db.add(platform)
        session_db.commit()

    return platform.id

def add_map_product_platform(session_db, product_id, platform_id, url):
    mapping = session_db.query(ProductPlatform).filter_by(product_id=product_id, platform_id=platform_id).first()

    if not mapping:
        mapping = ProductPlatform(product_id=product_id, platform_id=platform_id, url=url)
        session_db.add(mapping)
    else:
        mapping.url = url
    session_db.commit()

def add_price(session_db, mapping_id, product_price):
    price_row = PriceHistory(product_platform_id = mapping_id, price=product_price)
    session_db.add(price_row)
    session_db.commit()