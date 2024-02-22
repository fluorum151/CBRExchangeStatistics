from currencyclass import Currency

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
    for i in CURRENCIES:
        i.get_currency()
        i.get_exchange_data()
        print(i)
