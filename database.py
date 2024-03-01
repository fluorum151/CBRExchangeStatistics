import sqlalchemy


def create_connect():
    engine = sqlalchemy.create_engine("mysql+mysqlconnector://root:erdtreeroot@localhost/cbrtest")
    return engine


def insert_db(engine, date, rate):
    with engine.connect() as connection:
        connection.execute(sqlalchemy.text("INSERT INTO usd (date, rate) VALUES (:date, :rate)"),
                           {"date": date, "rate": rate})
        connection.commit()


engine = create_connect()
insert_db(engine, '2006-11-11', '64.5675')

date1 = '17.01.2024'
date2 = date1[6:] + '-' + date1[3:5] + '-' + date1[0:2]
