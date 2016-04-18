from sqlalchemy import Column, Integer, String, Date
from db import Base
from datetime import datetime

class Action(Base):
    __tablename__ = "actions"

    id          = Column(Integer, primary_key=True)
    sgx_key     = Column(Integer, unique=True)
    type        = Column(String)
    company_name = Column(String)
    ex_date     = Column(Date)
    record_date = Column(Date)
    paid_date   = Column(Date)
    notes       = Column(String)
    siblings    = Column(String)
    symbol      = Column(String)

    def __repr__(self):
        return "<Action(sgx_key='%d', type='%s', company='%s', ex_date='%s', notes='%s')>" % (self.sgx_key, self.type, self.company_name, datetime.strftime(self.ex_date, "%d-%m-%Y"), self.notes)
