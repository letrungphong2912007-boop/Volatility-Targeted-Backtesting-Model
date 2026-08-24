import yfinance as yf
import pandas as pd
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent


def getData():
    path_data = DATA_DIR / "Tickers_List.csv"
    path_para = DATA_DIR / "Parameters.csv"
    parameters = pd.read_csv(path_para)
    ticker_list = pd.read_csv(path_data)
    ticker_list["weight"] = ticker_list["weight"]/ticker_list["weight"].sum()
    data = {}

    sy = int(parameters["Value"].iat[0])
    sm = int(parameters["Value"].iat[1])
    sd = int(parameters["Value"].iat[2])
    ey = int(parameters["Value"].iat[3])
    em = int(parameters["Value"].iat[4])
    ed = int(parameters["Value"].iat[5])
    interval = parameters["Value"].iat[6]

    start = datetime(sy, sm, sd)
    end = datetime(ey, em, ed)

    years = ((end - start).days + 1)/365.25


    for ticker in ticker_list["ticker"]:
        data[ticker] = yf.download(tickers = ticker, start = start, end = end, interval = interval, multi_level_index=False)

    return data, ticker_list, parameters, years
