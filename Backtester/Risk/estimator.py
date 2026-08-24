import numpy as np
import pandas as pd
from arch import arch_model


def rollingStd(data, window = 63):
    temp = data.copy()
    ret = temp["LogReturn"]
    std = ret.rolling(window = window).std()*np.sqrt(252)
    return std

def weightedRollingStd(data, window = 63, lambDa = 0.94):
    temp = data.copy()
    ret = temp["LogReturn"]
    std = [np.nan]*(window - 1)
    std.append(ret.iloc[0:window].std())
    for i in range(window, len(temp)):
        var = lambDa*std[-1]**2 + (1 - lambDa)*ret.iloc[i]**2
        std.append(np.sqrt(var))
    std = pd.Series(std, index = temp.index)
    std = std*np.sqrt(252)
    return std

def volRogerSatchell(data, window = 63):
    temp = data.copy()
    h = temp["High"]
    l = temp["Low"]
    o = temp["Open"]
    c = temp["Close"]

    tempRs = np.log(h/c)*np.log(h/o) + np.log(l/c)*np.log(l/o)
    
    temp["RS"] = tempRs.rolling(window = window).mean()
    std = np.sqrt(temp["RS"]*252)
    return std

def volYangZhang(data, window = 63):
    k = 0.34/(1.34 +(window+1)/(window-1))
    #overnight
    temp = data.copy()
    o = temp["Open"]
    c = temp["Close"]

    temp["RS"] = volRogerSatchell(temp, window)**2/252

    overnight = np.log(o/c.shift(1))
    temp["Overnight"] = overnight.rolling(window = window).std()**2

    otc = np.log(c/o)
    temp["Otc"] = otc.rolling(window = window).std()**2

    temp["YZ"] = temp["Overnight"] + k*temp["Otc"] + (1 - k)*temp["RS"]
    std = np.sqrt(temp["YZ"]*252)
    return std

def garchVol(data, window = 500, refit = 21): 
    temp = data.copy()
    temp = pd.DataFrame(temp)
    temp["returnRate"] = temp["LogReturn"]*100
    temp["returnRate"] = temp["returnRate"].fillna(0)
    alpha = [np.nan]*window
    beta = [np.nan]*window
    omega = [np.nan]*window
    mean = [np.nan]*window

    m, a, b, o = 0, 0, 0, 0
    for i in range(window, len(temp)):
        if((i - window)%refit == 0):
            series = temp["returnRate"].iloc[i - window:i]
            res = arch_model(
                series,
                mean = "Constant",
                vol = "GARCH",
                p = 1,
                q = 1,
                dist = "normal"
            ).fit(disp="off")
            m = res.params[0]
            o = res.params[1]
            a = res.params[2]
            b = res.params[3]

        mean.append(m)
        alpha.append(a)
        beta.append(b)
        omega.append(o)

    var = [np.nan]*(window - 1)
    var.append(temp["returnRate"].iloc[0:59].std()**2)
    for i in range(window, len(temp)):
        vart = omega[i] + alpha[i]*(temp["returnRate"].iloc[i - 1] - mean[i])**2 + beta[i]*var[-1]
        var.append(vart)
    std = pd.Series(np.sqrt(var)*np.sqrt(252), index = temp.index)/100
    return std