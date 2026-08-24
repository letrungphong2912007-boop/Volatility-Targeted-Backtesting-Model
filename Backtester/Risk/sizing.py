import pandas as pd
import numpy as np

def sizingWeight(return_table, order_table, std_table, target_vol, start, cap = 1.5, window = 63, refit = 21):

    assert order_table.columns.equals(std_table.columns), "column mismatch"
    assert order_table.index.equals(std_table.index),     "index mismatch"
    assert order_table.columns.equals(return_table.columns), "column mismatch"
    assert order_table.index.equals(return_table.index),     "index mismatch"

    #normalised raw weight
    raw = order_table/std_table
    temp = np.abs(raw)
    rowsum = temp.sum(axis = 1)
    raw = raw.div(rowsum.where(rowsum > 0), axis = 0).fillna(0.0)

    #correlation weight
    sigma_pos_list = [np.nan]*start
    cM = object
    r = start%refit
    for i in range(start, len(return_table)):
        if((i - r)%refit == 0):
            cM = return_table.iloc[i - window: i].corr() #correlation matrix
        diag = np.diag(std_table.iloc[i]) #std diagonal matrix
        v = raw.iloc[[i]].values #raw weight vector
        sigma_pos = np.sqrt(v @ (diag @ cM @ diag) @ v.T).values[0][0]
        
        sigma_pos_list.append(sigma_pos)

    sigma_pos_list = pd.Series(sigma_pos_list, index = return_table.index)

    #final weight
    leverage = target_vol/sigma_pos_list
    leverage = leverage.clip(-cap, cap)
    final_weight = raw.mul(leverage, axis = 0)



    return final_weight