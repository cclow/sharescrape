from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://localhost/invest")

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
