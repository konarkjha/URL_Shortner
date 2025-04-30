from sqlalchemy import Column, Integer, String
from .database import Base

class URLMapping(Base):
    __tablename__ = "url_mappings"

    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, unique=True, index=True)
    short_url = Column(String, unique=True, index=True)