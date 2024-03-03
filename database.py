from sqlalchemy import Column, Table, Date, Double, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, registry


class Base(DeclarativeBase):
    pass


mapper_registry = registry()


def create_connect():
    engine = create_engine("mysql+mysqlconnector://root:erdtreeroot@localhost/cbrtest")
    return engine


def create_table(engine, name):
    table = Table(
        name, mapper_registry.metadata,
        Column('date', Date, primary_key=True),
        Column('rate', Double),
    )
    mapper_registry.metadata.create_all(engine)
    return table


def create_class(table):
    class Currency:
        pass

    mapper_registry.map_imperatively(Currency, table)
    return Currency()


def insert_db(engine, table, date, rate):
    with Session(engine) as session:
        db_class = create_class(table)
        db_class.date = date
        db_class.rate = rate
        session.add(db_class)
        session.commit()
        session.close()
