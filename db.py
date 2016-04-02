from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import create_engine
from db_url import db_url
engine = create_engine(db_url)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)

def create_tables():
    import action
    import announcement
    Base.metadata.create_all(engine)
