import pandas as pd
import numpy as np

def sharpeRatio(data, riskfree):
    temp = data.copy()
    rf = riskfree/252
    daily_return = temp.pct_change()
    excess_ret = daily_return - rf
    sr = round(np.sqrt(252)*np.mean(excess_ret)/np.std(excess_ret), 6)
    return sr