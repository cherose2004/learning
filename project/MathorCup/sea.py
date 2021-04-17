def Tsea(deep):
    """
    基准海平面水温20°C
    输入基准海平面以下的深度deep(m)
    输出此处海水的温度(°C)
    """
    if deep<=1000:
        T = 20-(20-4)*deep/1000
    elif deep<=2000:
        T = 4-(4-2)*deep/1000
    elif deep<=3000:
        T = 2-(2-1)*deep/1000
    elif deep<=4000:
        T = 1-(1+1)*deep/1000
    else:
        T = -1
    return T