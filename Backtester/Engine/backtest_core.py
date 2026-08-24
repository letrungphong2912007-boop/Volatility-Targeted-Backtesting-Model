import numpy as np
import pandas as pd

def backtestCore(return_table, weight, start, band = 0.01, commission = 0.001, start_balance = 1000):
    assert weight.index.equals(return_table.index)
    assert weight.columns.equals(return_table.columns)

    port_bal = [np.nan]*start
    cost_list = [np.nan]*(start + 1)
    strategies  = len(return_table.columns)
    port_bal.append(start_balance)
    held_s = [np.nan]*(start)
    held_t = [np.nan]*(start+1)
    remains = [np.nan]*(start+1)
    vpw = [0.0]*strategies  #vector previous weight(at i - 1)

    for i in range(start, len(return_table) - 1):
        balance = port_bal[-1] #balance at i
        vr = return_table.iloc[i + 1] #vector return at i + 1
        vw = weight.iloc[i] #vector weight at i

        #adjust position with band
        exit_now = (vw == np.array([0.0]*strategies )) & (vpw != np.array([0.0]*strategies ))
        flip = vw*vpw < np.array([0.0]*strategies )
        dif = np.abs(vw - vpw) 
        adjust = (dif > np.array([band]*strategies )) | exit_now | flip
        vw = vw*adjust + ([1]*strategies  - adjust)*vpw
        leverage = vw.sum()

        #balance at i+1
        remain = balance*(1 - leverage)
        vsh = (vr + [1]*strategies )*balance*vw #strategies held vector
        total_held = vsh.sum()
        cost = (adjust*dif).sum()*commission*balance
        balance = remain + total_held - cost

        cost_list.append(cost)
        port_bal.append(balance)
        held_t.append(total_held)
        held_s.append(np.array(vsh))
        remains.append(remain)
        vpw = vw
        

    held_s = held_s[start:]
    held_s = pd.DataFrame(held_s, index = return_table.index[start+1:])
    held_s.columns = return_table.columns
    port_bal = pd.DataFrame({
        "Balance": port_bal,
        "Transaction": cost_list,
        "Held": held_t,
        "Cash": remains
        })
    port_bal.index = return_table.index
    
    return port_bal, held_s