from models.database import create_db, Session
from models.currency import Currency
from models.chat import Chat


def create_database(load_data: bool = True):
    create_db()
    if load_data:
        _load_data(Session())


def _load_data(session: Session):
    idr = Currency(name='IDR', rate=15000, api_url='test api URL')
    gel = Currency(name='GEL', rate=2.3, api_url='test api URL')
    session.add(idr)
    session.add(gel)
    session.commit()
    session.close()
