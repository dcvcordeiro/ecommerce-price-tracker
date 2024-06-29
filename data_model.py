from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    product_platforms = relationship('ProductPlatform', backref='product')

class Platform(Base):
    __tablename__ = 'platforms'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    product_platforms = relationship('ProductPlatform', backref='platform')

class ProductPlatform(Base):
    __tablename__ = 'product_platform'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    platform_id = Column(Integer, ForeignKey('platforms.id'), nullable=False)
    url = Column(String, nullable=False)
    price_history = relationship('PriceHistory', backref='product_platform')

class PriceHistory(Base):
    __tablename__ = 'price_history'
    id = Column(Integer, primary_key=True)
    product_platform_id = Column(Integer, ForeignKey('product_platform.id'), nullable=False)
    price = Column(Float, nullable=False)
    date_checked = Column(DateTime, default=datetime.datetime.utcnow)

