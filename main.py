from dotenv import load_dotenv
from currency import Currency
import datetime
import os
import json


load_dotenv()
days_number = int(os.environ.get('DAYS_NUMBER'))

date2 = datetime.datetime.today()
date1 = date2 - datetime.timedelta(days=90)
date1 = date1.strftime("%d/%m/%Y")
date2 = date2.strftime("%d/%m/%Y")

CURRENCIES = json.loads(os.environ['CURRENCIES'])

if __name__ == '__main__':
    for curr in CURRENCIES:
        currency = Currency(curr[0], curr[1])
        currency.get_currency(date1, date2)
        currency.get_exchange_data()
        print(currency)
