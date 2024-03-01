import xml.etree.ElementTree as ElementTree
import requests
import database


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

    def get_exchange_data(self):
        self.max_rate_date = max(self.curr_dict, key=self.curr_dict.get)
        self.min_rate_date = min(self.curr_dict, key=self.curr_dict.get)
        self.max_rate = self.curr_dict[self.max_rate_date]
        self.min_rate = self.curr_dict[self.min_rate_date]
        self.rate_avg = sum(self.curr_dict.values()) / len(self.curr_dict)

    def get_currency(self, date1, date2):
        response = requests.get(f"https://www.cbr.ru/scripts/XML_dynamic.asp?"
                                f"date_req1={date1}&date_req2={date2}&VAL_NM_RQ={self.cbr_id}")

        string_xml = response.content
        tree = ElementTree.fromstring(string_xml)
        db_engine = database.create_connect()

        for value in tree:
            date = value.attrib['Date']
            db_date = date[6:] + '-' + date[3:5] + '-' + date[0:2]
            rate = float(value[1].text.replace(',', '.'))
            self.curr_dict[date] = rate
            database.insert_db(db_engine, db_date, rate)

