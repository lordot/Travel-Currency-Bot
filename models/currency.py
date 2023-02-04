from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from models.database import Base


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    rate = Column(Float)
    api_url = Column(String)
    updated = Column(DateTime, onupdate=datetime.now())
    chats = relationship('Chat', backref='currency')

    def __init__(self, name: str, rate: float, api_url: str):
        self.name = name
        self.api_url = api_url
        self.rate = rate
