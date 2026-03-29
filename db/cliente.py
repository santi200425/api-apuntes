from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# formato: mysql+pymysql://usuario:password@host/db
motor=create_engine("mysql+pymysql://root:ingeniero1@localhost/gestor_estudios")

base=declarative_base()
SessionLocal=sessionmaker(bind=motor)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()