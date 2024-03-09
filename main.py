import datetime
import json
import os
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
    for curr in CURRENCIES:
        with Session(engine) as session:
            db_curr = database.create_currencies(session, curr[0], curr[1])
            session.commit()
            # session.close()
            currency = Currency(curr[0], curr[1])
            currency.get_currency(session, db_curr.name, date1, date2)
            currency.get_exchange_data()
            session.commit()
            session.close()
            print(currency)
