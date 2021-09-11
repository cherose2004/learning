import numpy as np
import xlrd
import xlwt
import scipy.optimize as op

class supplier:
    def __init__(self , ID , kind , s):
        self.ID = ID
        self.setkind(kind)
        self.settheta(s)
        pass

    def setkind(self , kind):
        self.kind = kind
        if kind == "A":
            self.lam = 1/0.6
            self.k = 1.2
            pass
        elif kind == "B":
            self.lam = 1/0.66
            self.k = 1.1
            pass
        else:
            self.lam = 1/0.72
            self.k = 1.
            pass
        pass

    def settheta(self , s):
        self.theta = s.max()
        ave = np.mean(s)
        stda = np.std(s)
        line = ave + 2*stda
        tmp = list()
        for i in range(s.size):
            if s[i] < line:
                tmp.append(s[i])
                pass
            pass
        tmp = np.array(tmp)
        self.theta_modify = tmp.max()
        pass

file = xlrd.open_workbook("42.xls")
sheet = file.sheet_by_index(0)
M = sheet.nrows-1
N = sheet.ncols-2

ListSupplier = list()
for j in range(M):
    ID = sheet.cell_value(rowx = j+1 , colx = 0)
    kind = sheet.cell_value(rowx = j+1 , colx = 1)
    s = np.zeros(N)
    for i in range(N):
        s[i] = sheet.cell_value(rowx = j+1 , colx = i+2)
        pass
    item = supplier(ID , kind , s)
    ListSupplier.append(item)
    pass

def GetAub(List):
    n = len(List)
    Aub = np.zeros(n)
    for i in range(n):
        Aub[i] = -List[i].lam
        pass
    Aub = np.array([list(Aub)])
    return Aub
    pass
def GetC(List):
    n = len(List)
    C = np.zeros(n)
    for i in range(n):
        C[i] = List[i].k
        pass
    return C
    pass
def GetBound(List):
    bound = list()
    n = len(List)
    for i in range(n):
        tmp = (0. , List[i].theta)
        bound.append(tmp)
        pass
    bound = tuple(bound)
    return bound
    pass

C = GetC(ListSupplier)
Aub = GetAub(ListSupplier)
bound = GetBound(ListSupplier)
bub = np.array([-2.82e4])

print("start linprog")

res = op.linprog(C , Aub , bub , bounds = bound )

np.round(res.x)

res.x[0:14].sum()