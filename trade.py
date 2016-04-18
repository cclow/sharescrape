from sqlalchemy import Column, Integer, String, Date
from db import Base
from datetime import datetime

class Trade(Base):
    __tablename__ = "trades"

    id      = Column(Integer, primary_key=True)

