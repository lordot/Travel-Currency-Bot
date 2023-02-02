from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from database import Base


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    rate = Column(Float)
    api_url = Column(String)
    updated = Column(DateTime, onupdate=datetime.now())
    chat = relationship('Chat')

    def __init__(self, name: str, api_url: str):
        self.name = name
        self.api_url = api_url
