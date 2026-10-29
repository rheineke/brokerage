import datetime as dt


def split_download(lines, pos_fp, tx_fp):
    """Positions come first; after the first blank line, transactions."""
    out_fp = pos_fp
    for line in lines:
        if line == "\n":
            out_fp = tx_fp
        else:
            out_fp.write(line)


if __name__ == "__main__":
    date = dt.date(2018, 2, 22)
    # df = pd.read_csv(path)

    base_path = "/Users/rheineke/Downloads/"
    path = base_path + f"ofxdownload_{date:%m%d%Y}.csv"
    pos_path = base_path + f"ny529_pos_{date:%m%d%Y}.csv"
    tx_path = base_path + f"ny529_tx_{date:%m%d%Y}.csv"

    with open(path) as fp, open(pos_path, "w") as pos_fp, open(tx_path, "w") as tx_fp:
        split_download(fp, pos_fp, tx_fp)
