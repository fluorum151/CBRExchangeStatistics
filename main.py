import datetime
import json
import os

import sqlalchemy
from dotenv import load_dotenv
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
            currency.get_currency(session, currency.name, date1, date2)
            currency.get_exchange_data()
            session.commit()
            print(currency)
