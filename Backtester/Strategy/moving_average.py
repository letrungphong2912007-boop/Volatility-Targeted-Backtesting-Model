import numpy as np
import pandas as pd


def maTrendFollowing(data, tickers, slowMa, fastMa):
    temp = data[tickers].copy()
    MA_table = []
    for col in tickers:
        temp["MA_slow"] = temp[col].rolling(window = slowMa).mean()
        temp["MA_fast"] = temp[col].rolling(window = fastMa).mean()
        temp["Signal"] = temp["MA_fast"] > temp["MA_slow"]
        temp["LogReturn"] = np.log(temp[col]/temp[col].shift(1))
        temp["LogReturn"].iat[0] = 0.0
        temp["Order"] = np.where(temp["Signal"] == True, "LONG", "EXIT")
        MA_table.append(temp[[col,"LogReturn", "Order"]])
    return MA_table



