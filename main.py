# This is a sample Python script.
import xml.etree.ElementTree as ET

import requests

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# USD - R01235 EU - R01239 CHF - R01775 GBP - R01035
# JPY - R01820 CNY  - R01375 AUD  - R01010 CND - R01350
#


class Currency:
    def __init__(self, cbr_id, curr_name):
        self.cbr_id = cbr_id
        self.name = curr_name
        self.curr_dict = {}
        self.max_rate_date = ''
        self.min_rate_date = ''
        self.max_rate = 0
        self.min_rate = 0
        self.rate_avg = 0

    def __str__(self):
        return f'''
        {self.name}:
        Высший курс за период: {self.max_rate} - {self.max_rate_date}
        Низший курс за период: {self.min_rate} - {self.min_rate_date}
        Средний курс за период: {self.rate_avg}'''


usd, eu, chf, gbp, jpy, cny, aud, cnd = (Currency('R01235', 'USD'),
                                         Currency('R01239', 'EU'),
                                         Currency('R01775', 'CHF'),
                                         Currency('R01035', 'GBP'),
                                         Currency('R01820', 'JPY'),
                                         Currency('R01375', 'CNY'),
                                         Currency('R01010', 'AUD'),
                                         Currency('R01350', 'CND'))

CURRENCIES = (usd, eu, chf, gbp, jpy, cny, aud, cnd)


def get_currency(currency):
    response = requests.get("https://www.cbr.ru/scripts/XML_dynamic.asp?"
                            "date_req1=19/12/2023&date_req2=19/02/2024&VAL_NM_RQ=" + currency.cbr_id)

    string_xml = response.content
    tree = ET.fromstring(string_xml)

    for value in tree:  # .iter('Value'):
        # print(value.attrib['Date'] + ' ' + value[1].text)  # + ' \n')
        currency.curr_dict[value.attrib['Date']] = float(value[1].text.replace(',', '.'))


def get_exchange_data(currency):
    currency.max_rate_date = max(currency.curr_dict, key=currency.curr_dict.get)
    currency.min_rate_date = min(currency.curr_dict, key=currency.curr_dict.get)
    currency.max_rate = currency.curr_dict[currency.max_rate_date]
    currency.min_rate = currency.curr_dict[currency.min_rate_date]
    currency.rate_avg = sum(currency.curr_dict.values()) / len(currency.curr_dict)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for i in CURRENCIES:
        get_currency(i)
        get_exchange_data(i)
        print(i)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
