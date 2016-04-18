from sqlalchemy import Column, Integer, String, DateTime
from db import Base
from datetime import datetime

class Announcement(Base):
    __tablename__ = "announcements"

    id          = Column(Integer, primary_key=True)
    sgx_key     = Column(String, unique=True)
    broadcast_time = Column(DateTime)
    issuer_name = Column(String)
    security_name = Column(String)
    group_code  = Column(String)
    category_code = Column(String)
    category_name = Column(String)
    title       = Column(String)
    siblings    = Column(String)
    symbol      = Column(String)

    def __repr__(self):
        return "<Announcement(security='%s', broadcast_time='%s', category='%s', title='%s')>" % (self.security_name, datetime.strftime(self.broadcast_time, "%d %b %Y %H:%M:%S"), self.category_name, self.title)
