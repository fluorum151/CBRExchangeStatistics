import os
from dotenv import load_dotenv
from currency import Currency
import arrow


load_dotenv()
days_number = int(os.environ.get('DAYS_NUMBER'))
date2 = current_date = arrow.now()
date1 = date2.shift(days=-days_number).format('DD/MM/YYYY')
date2 = date2.format('DD/MM/YYYY')

usd, eu, chf, gbp, jpy, cny, aud, cnd = (Currency('R01235', 'USD'),
                                         Currency('R01239', 'EU'),
                                         Currency('R01775', 'CHF'),
                                         Currency('R01035', 'GBP'),
                                         Currency('R01820', 'JPY'),
                                         Currency('R01375', 'CNY'),
                                         Currency('R01010', 'AUD'),
                                         Currency('R01350', 'CND'))

CURRENCIES = (usd, eu, chf, gbp, jpy, cny, aud, cnd)


if __name__ == '__main__':
    for currency in CURRENCIES:
        currency.get_currency(date1, date2)
        currency.get_exchange_data()
        print(currency)
