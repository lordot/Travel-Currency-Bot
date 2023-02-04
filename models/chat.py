from sqlalchemy import Column, Integer, ForeignKey

from models.database import Base


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer, ForeignKey('currencies.id'))

    def __init__(self, id: int, currency_id):
        self.id = id
        self.currency_id = currency_id
