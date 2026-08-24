def maximumDrawdown(data):
    temp = data.copy()

    peak = temp.cummax()
    dd = temp - peak
    dd_ratio = dd/peak

    peak_check = peak > temp
    dd_duration = peak_check.groupby((~peak_check).cumsum()).cumsum()

    md = dd_ratio.min()
    mddd = dd_duration.max()
    return md, mddd
