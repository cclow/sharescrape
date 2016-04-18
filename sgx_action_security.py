from sqlalchemy import Column, Integer, String, Date
from db import Base
from datetime import datetime

class SgxActionSecurity(Base):
    __tablename__ = "sgx_action_securities"

    id      = Column(Integer, primary_key=True)
    # CompanyName from sgx actions
    company_name = Column(String, unique=True)
    # symbol to make tp
    symbol  = Column(String)
