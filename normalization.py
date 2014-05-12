def normalize(value, pos_max_value, neg_max_value):
    percent = 0
    x = 0
    if value >= 0:
        percent = (value * 100)/pos_max_value
        x = (percent * 7)/100
    else:
        percent = (value * 100)/neg_max_value
        x = (percent * (-7))/100
    return round(x,3)