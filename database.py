from sqlalchemy import create_engine, exists
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv 
from data_model import Base, Platform

load_dotenv() 

def add_platforms(db_session):
    platforms = os.getenv("PLATFORMS").split()

    for platform_name in platforms:
        platform = Platform(name=platform_name)
        db_session.add(platform)
    db_session.commit()

def get_database_session():
    db = os.getenv("DATABASE")
    engine = create_engine(f'sqlite:///{db}')

    if not os.path.exists(db):
        Base.metadata.create_all(engine)
        
    SessionDB = sessionmaker(bind=engine)

    session_db = SessionDB()

    # Check if the Platform table is empty and if it is populate 
    if not session_db.query(exists().where(Platform.id != None)).scalar():
        add_platforms(db_session)

    return db_session

if "__main__" == __name__: 
    # 1. Define DB if not defined

    #add_platforms(db_session)
    #query_plaform(db_session))
    db_session = get_database_session()


    