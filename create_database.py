from models.database import create_db, Session
from models.currency import Currency
from models.chat import Chat


def create_database(load_data: bool = True):
    create_db()
    if load_data:
        _load_data(Session())


def _load_data(session: Session):
    idr = Currency(name='IDR', rate=15.230, api_url='test api URL')
    gel = Currency(name='GEL', rate=2.63, api_url='test api URL')
    thb = Currency(name='THB', rate=33.34, api_url='test api URL')
    usd = Currency(name='USD', rate=70, api_url='test api URL')
    session.add(idr)
    session.add(gel)
    session.add(thb)
    session.add(usd)
    session.commit()
    session.close()
