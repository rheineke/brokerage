import io
import json
from pathlib import Path

import pandas as pd

import nysaves529
import transamerica

CONFIG = Path(__file__).parent.parent / "configs" / "ta.json"

UNIT_VALUES = """\
Date,Fund Name,Unit Value
2017-11-24,Transamerica Stable Value Account,12.34
2017-11-24,Janus Triton Ret Acct,45.67
2017-11-24,Vanguard REIT Index Ret Acct,23.45
"""


def test_split_download_puts_transactions_after_blank_line():
    lines = ["pos header\n", "pos 1\n", "\n", "tx header\n", "tx 1\n"]
    pos, tx = io.StringIO(), io.StringIO()
    nysaves529.split_download(lines, pos, tx)
    assert pos.getvalue() == "pos header\npos 1\n"
    assert tx.getvalue() == "tx header\ntx 1\n"


def test_position_values_keeps_held_funds(tmp_path):
    path = tmp_path / "unitvalues-2017-11-24.csv"
    path.write_text(UNIT_VALUES)
    df = transamerica.read_unit_values(path)
    held = transamerica.position_values(df, json.loads(CONFIG.read_text())["positions"])
    funds = held.index.get_level_values(transamerica.FUND_NAME)
    assert list(funds) == [
        "Transamerica Stable Value Account",
        "Vanguard REIT Index Ret Acct",
    ]
    assert held.index.get_level_values(transamerica.DATE)[0] == pd.Timestamp(
        "2017-11-24"
    )


def test_config_positions_are_known_funds():
    config = json.loads(CONFIG.read_text())
    assert set(config["positions"]) <= set(config["tickers"])
