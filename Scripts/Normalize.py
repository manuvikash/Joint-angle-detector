def getNormalizedValue(param, value):
    if(param[:2] == "CP"):
        return value * 2
    elif(param[:1] == "v"):
        return value * 0.1
    else:
        return value

def calcAvgSim(value, param):
    if(param[:2] == "CP"):
        return value * 0.3
    elif(param[:1] == "v"):
        return value * 1.5
    else:
        return value