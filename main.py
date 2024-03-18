import datetime
import json
import os

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import and_
from sqlalchemy.orm import Session
from currency import Currency
import database


load_dotenv()
days_number = int(os.environ.get('DAYS_NUMBER'))

date2 = datetime.datetime.today()
date1 = date2 - datetime.timedelta(days=days_number)
date1 = date1.strftime("%d/%m/%Y")
date2 = date2.strftime("%d/%m/%Y")

CURRENCIES = json.loads(os.environ['CURRENCIES'])

if __name__ == '__main__':
    engine = database.create_connect()
    database.create_classes(engine)
    with Session(engine) as session:
        for curr in CURRENCIES:
            currency_exists = session.query(sqlalchemy.exists().where(database.Currency.name == curr[1])).scalar()
            if not currency_exists:
                database.create_currency(session, curr[0], curr[1])

            currency = Currency(curr[0], curr[1])
            currency.get_currency(date1, date2)
            for value in currency.tree:
                currency.parse_currency(value)
            currency.get_exchange_data()

            for date, rate in currency.curr_dict.items():
                db_date = date[6:] + '-' + date[3:5] + '-' + date[0:2]
                record_exists = session.query(sqlalchemy.exists()
                                              .where(and_(database.ExchangeData.currency == currency.name,
                                                          database.ExchangeData.date == db_date))).scalar()
                if not record_exists:
                    database.insert_db(session, currency.name, rate, db_date)
                session.commit()
            print(currency)
