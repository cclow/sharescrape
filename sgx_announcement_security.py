from sqlalchemy import Column, Integer, String, Date, UniqueConstraint
from db import Base
from datetime import datetime

class SgxAnnouncementSecurity(Base):
    __tablename__ = "sgx_announcement_securities"

    id      = Column(Integer, primary_key=True)
    # issuer and security names from sgx announcements
    issuer_name = Column(String)
    security_name = Column(String)
    # symbol to make tp
    symbol  = Column(String)
