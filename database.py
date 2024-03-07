from dotenv import load_dotenv
from sqlalchemy import Date, Double, String, create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import os
import json

load_dotenv()
CURRENCIES = json.loads(os.environ['CURRENCIES'])


class Base(DeclarativeBase):
    pass


def create_connect():
    engine = create_engine("mysql+mysqlconnector://root:erdtreeroot@localhost/cbrtest")
    return engine


class Currency(Base):
    __tablename__ = "currencies"
    id: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(10))

    def __repr__(self) -> str:
        return f"Currency(id={self.id!r}, name={self.name!r})"


class ExchangeData(Base):
    __tablename__ = "exchange_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    currency_id = mapped_column(ForeignKey("currencies.id"))
    date: Mapped[str] = mapped_column(Date)
    exchange_rate: Mapped[float] = mapped_column(Double)

    def __repr__(self) -> str:
        return f"ExchangeData(id={self.id!r}, date={self.date!r}, rate={self.exchange_rate!r})"


def create_databases(engine):
    with Session(engine) as session:
        for curr in CURRENCIES:
            currency = Currency()
            currency.id = curr[0]
            currency.name = curr[1]
            session.add(currency)
        session.commit()
        session.close()


def insert_db(engine, date, rate):
    with Session(engine) as session:
        db_class = ExchangeData()
        db_class.exchange_rate = rate
        db_class.date = date
        session.add(db_class)
        session.commit()
        session.close()
