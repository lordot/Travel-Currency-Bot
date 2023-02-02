from sqlalchemy import Column, Integer, ForeignKey

from database import Base


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True)
    currency = Column(Integer, ForeignKey('currencies.id'))

