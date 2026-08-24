import pandas as pd
import numpy as np

def returnRate(data):
    temp = data.dropna()
    years = (temp.index[-1] - temp.index[0]).days/365.25
    returnAll = temp.iloc[-1]/temp.iloc[0] - 1.0
    annualRet = (1.0 + returnAll)**(1.0/years) - 1.0
    return annualRet, returnAll