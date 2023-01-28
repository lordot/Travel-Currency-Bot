import datetime as dt

import sqlalchemy as db


engine = db.create_engine('sqlite:///database.db')

connection = engine.connect()

metadata = db.MetaData()

currencies = db.Table('currencies', metadata,
                      db.Column('id', db.Integer, primary_key=True),
                      db.Column('name', db.Text, unique=True),
                      db.Column('rate', db.Float),
                      db.Column('updated', db.DateTime, onupdate=dt.datetime.now())
                      )

chats = db.Table('chats', metadata,
                 db.Column('chat_id', db.Integer, primary_key=True),
                 db.Column('currency', db.ForeignKey('currencies.id'))
                 )

metadata.create_all(engine)

insertion_query = currencies.insert().values([
    {'name': 'USD', 'rate': 70},
    {'name': 'IDR', 'rate': 15060},
    {'name': 'GEL', 'rate': 2.9},
])

add_query = currencies.insert().values([
    {'name': 'USD', 'rate': 70}
])

connection.execute(insertion_query)
# connection.execute(add_query)
connection.commit()
