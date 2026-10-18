import datetime as dt

import pandas as pd

if __name__ == '__main__':
    date = dt.date(2018, 2, 22)
    # df = pd.read_csv(path)

    base_path = '/Users/rheineke/Downloads/'
    path = base_path + 'ofxdownload_{0:%m%d%Y}.csv'.format(date)
    pos_path = base_path + 'ny529_pos_{0:%m%d%Y}.csv'.format(date)
    tx_path = base_path + 'ny529_tx_{0:%m%d%Y}.csv'.format(date)

    with open(path) as fp, open(pos_path, 'w') as pos_fp, open(tx_path, 'w') as tx_fp:
        out_fp = pos_fp
        for line in fp:
            if line == '\n':
                out_fp = tx_fp
            else:
                out_fp.write(line)


