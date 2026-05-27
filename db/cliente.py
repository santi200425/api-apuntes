from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
database_url=os.getenv("DATABASE_URL")
# formato: mysql+pymysql://usuario:password@host/db
motor=create_engine(database_url)

base=declarative_base()
SessionLocal=sessionmaker(bind=motor)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()