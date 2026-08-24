import pandas as pd
import numpy as np

def meanReversion(data, tickers, upper, lower, Rmean, stop):
    temp = data[tickers].copy()
    MR_table = [] 
    for col in tickers:
        temp["z-score"] = (temp[col] - temp[col].rolling(window = 50).mean())/temp[col].rolling(window = 50).std()
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
        temp["LogReturn"] = np.log(temp[col]/temp[col].shift(1))
        temp["LogReturn"].iat[0] = 0.0
        temp["Order"] = order
        MR_table.append(temp[[col, "LogReturn", "Order"]])
    return MR_table


    



