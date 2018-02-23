"""
https://www.ta-retirement.com/Default.aspx
https://ddol.divinvest.com/ddol/authenticated/reports/unitValues.html
https://ddol.divinvest.com/ddol/authenticated/reports/unitValuesDownload.html
"""
import argparse
import datetime as dt
import json
from collections import OrderedDict

import pandas as pd
import requests

DATE = 'Date'
FUND_NAME = 'Fund Name'

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
    # unit_value_url = 'https://ddol.divinvest.com/ddol/authenticated/reports/unitValuesDownload.html'
    # r = requests.get(unit_value_url)

    # with open('output/unitValues.html', 'w') as fp:
    #     fp.write(r.text)

    with open('configs/ta.json') as fp:
        config = json.load(fp, object_hook=OrderedDict)
    position_funds = config['positions']

    df = pd.read_csv(
        filepath_or_buffer='output/unitvalues-{0:%Y-%m-%d}.csv'.format(date),
        parse_dates=[DATE],
        index_col=[DATE, FUND_NAME]
    )

    fund_lbl = df.index.get_level_values(level=FUND_NAME).isin(position_funds)
    print(df.loc[fund_lbl])
