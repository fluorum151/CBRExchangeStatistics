from dotenv import load_dotenv
from sqlalchemy import Date, Double, String, create_engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, relationship
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
    date: Mapped[str] = mapped_column(Date)
    exchange_rate: Mapped[float] = mapped_column(Double)
    # currency_name: Mapped[str] = mapped_column(ForeignKey("currencies.name"))

    def __repr__(self) -> str:
        return f"ExchangeData(id={self.id!r}, date={self.date!r}, rate={self.exchange_rate!r})"


def create_classes(engine):
    Base.metadata.create_all(engine)


def create_currencies(session, cbr_id, name):
    curr_class = Currency()
    curr_class.id = cbr_id
    curr_class.name = name
    session.add(curr_class)


def insert_db(session, date, rate):
    db_class = ExchangeData()
    db_class.exchange_rate = rate
    db_class.date = date
    session.add(db_class)

