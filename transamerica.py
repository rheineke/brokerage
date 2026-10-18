"""
https://www.ta-retirement.com/Default.aspx
https://secure.transamerica.com/login/sign-in/login.html?requestUrl=/pkmslogout&token=Unknown
https://secure.transamerica.com/ddol/authenticated/reports/unitValues.html
https://secure.transamerica.com/ddol/authenticated/reports/unitValuesDownload.html
https://secure.transamerica.com/ddol/authenticated/reports/unitValuesDownload.html?submitted=true
"""
import argparse
import datetime as dt
import json
from collections import OrderedDict

import pandas as pd
import requests

DATE = 'Date'
FUND_NAME = 'Fund Name'

BASE_URL = 'https://secure.transamerica.com'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'date',
        default=dt.date.today,
        type=lambda s: dt.datetime.strptime(s, '%Y-%m-%d').date()
    )
    args = parser.parse_args()

    date = args.date

    # date = dt.date(2017, 11, 24)
    # Credentials live in configs/login.json, which is git-ignored
    with open('configs/login.json') as fp:
        login = json.load(fp)
    with open('configs/ta.json') as fp:
        config = json.load(fp, object_hook=OrderedDict)

    # Login attempt
    s = requests.Session()

    login_result = s.post(
        url=BASE_URL + '/login/sign-in/login.html?TAM_OP=login',
        data={
            'username': login['username'],
            'password': login['password'],
            'login-form-type': 'pwd',
        }
    )

    # Unit value
    unit_value_result = s.post(
        url=BASE_URL + '/ddol/authenticated/reports/unitValuesDownload.html',
        data={'submitted': 'true'}
    )

    # with open('output/unitValues.html', 'w') as fp:
    #     fp.write(r.text)

    position_funds = config['positions']

    df = pd.read_csv(
        filepath_or_buffer='output/unitvalues-{0:%Y-%m-%d}.csv'.format(date),
        parse_dates=[DATE],
        index_col=[DATE, FUND_NAME]
    )

    fund_lbl = df.index.get_level_values(level=FUND_NAME).isin(position_funds)
    print(df.loc[fund_lbl])
