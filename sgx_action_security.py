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

def update_action_security():
    from sqlalchemy import func
    from db import Session
    from action import Action
    session = Session()
    for security in session.query(SgxActionSecurity).filter(
            SgxActionSecurity.symbol != None):
        for action in session.query(Action).filter(Action.symbol == None).filter(
                func.upper(Action.company_name) == security.company_name):
            action.symbol = security.symbol
    session.commit()
