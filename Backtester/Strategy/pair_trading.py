import statsmodels.api as sm
import pandas as pd
import numpy as np

def pairTrading(data, ticker1, ticker2, window, upper, lower, Rmean, stop):
    temp = data[[ticker1, ticker2]].copy()

    alpha = [np.nan]*window
    beta = [np.nan]*window
    for i in range(window, len(temp)):
        #reset alpha and beta for each trading month (252/12 = 21)
        x = temp.iloc[i - window: i, 1] #ticker2
        y = temp.iloc[i - window: i, 0] #ticker1
        X = sm.add_constant(x)
        model = sm.OLS(y, X).fit()
        alpha.append(model.params[0])
        beta.append(model.params[1])
    spread = temp[ticker1] - alpha - beta*temp[ticker2]

    temp["z-score"] = (spread - spread.rolling(window = window).mean())/spread.rolling(window = window).std()
    status = "EXIT"
    order = []
    
    for date in data.index:
        Z = temp["z-score"].loc[date]

        if (status == "EXIT"):
            if (Z >= upper):
                status = "SHORT"
            elif (Z <= lower):
                status = "LONG"

        elif (status == "LONG"):
            if (Z >= upper):
                status = "SHORT"
            elif (Z > -Rmean):
                status = "EXIT"

        else:
            if (Z <= lower):
                status = "LONG"
            elif (Z < Rmean):
                status = "EXIT"

        if (abs(Z) >= stop):
            status = "EXIT"

        order.append(status)

    beta = pd.Series(beta, index = temp.index)
    ret1 = np.log(temp[ticker1]/temp[ticker1].shift(1))
    ret2 = np.log(temp[ticker2]/temp[ticker2].shift(1))
    pair_ret = (ret1 + ret2*beta.shift(1))/(1 + beta.shift(1))
    pair_ret.iat[0] = 0.0

    temp["Order"] = order
    return pd.DataFrame({
        ticker1: temp[ticker1],
        ticker2: temp[ticker2],
        "LogReturn": pair_ret,
        "Alpha": alpha,
        "Beta": beta,
        "Spread": spread,
        "Z": temp["z-score"],
        "Order": order
    })
    



