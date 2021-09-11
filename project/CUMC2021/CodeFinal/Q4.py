import numpy as np
import xlrd
import xlwt

def Select(arr , x):
    tmp = list()
    for i in range(arr.size):
        if arr[i] <= x:
            tmp.append(arr[i])
            pass
        pass
    tmp = np.array(tmp)
    return tmp.max()
    pass

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
        self.theta_sigma = np.zeros(24)
        s = s.reshape(10 , 24)
        self.theta_max = s.max(axis = 0)
        self.theta_ave = s.mean(axis = 0)
        std = np.sqrt(s.var(axis = 0))
        line = self.theta_ave + std*2
        for i in range(24):
            self.theta_sigma[i] = min(self.theta_max[i] , line[i])
            self.theta_max[i] = max(self.theta_max[i] , line[i])
            pass
        pass
    pass

file = xlrd.open_workbook("42.xls")
sheet = file.sheet_by_index(0)
M = sheet.nrows-1
N = 240

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
def GetBound(List , weeknum):
    bound = list()
    n = len(List)
    for i in range(n):
        tmp = (0. , List[i].theta_max[weeknum])
        bound.append(tmp)
        pass
    bound = tuple(bound)
    return bound
    pass

#C = GetC(ListSupplier)
Aub = GetAub(ListSupplier)
C = Aub.flatten()
Aub = [list(np.zeros(42)+1.)]
Listbound = list()
for i in range(24):
    Listbound.append( GetBound(ListSupplier , i) )
    pass
#bub = np.array([-2.82e4])
bub = np.array([4.8e4])

Max = np.zeros([42 , 24])
Sigma = np.zeros([42 , 24])
Ave = np.zeros([42 , 24])
for j in range(42):
    Max[j] = ListSupplier[j].theta_max
    Sigma[j] = ListSupplier[j].theta_sigma
    Ave = ListSupplier[j].theta_ave
    pass

print("start linprog")

Solution = list()
for i in range(24):
    res = op.linprog(C , Aub , bub , bounds = Listbound[i] , method = "highs-ipm")
    Solution.append(res)
    pass

matX2 = np.zeros([24 , 42])
for i in range(24):
    xx = Solution[i].x
    matX2[i] = xx
    pass
matX2 = np.round(matX2.T)

theta_sigma = np.zeros([42 , 24])
theta_max = np.zeros([42 , 24])
for j in range(42):
    for i in range(24):
        theta_sigma[j][i] = ListSupplier[j].theta_sigma[i]
        theta_max[j][i] = ListSupplier[j].theta_max[i]
        pass
    pass

Sum = np.zeros(24)
for j in range(24):
    tmp = 0.
    for i in range(42):
        tmp += ListSupplier[i].lam * matX2[i][j]
        pass
    Sum[j] = tmp
    pass
Sum

write = xlwt.Workbook()
sheet1 = write.add_sheet("24周供货表")
sheet2 = write.add_sheet("theta_floor取值")
sheet3 = write.add_sheet("theta_ceiling取值")
sheet4 = write.add_sheet("现在换算后的的产能量")
for j in range(42):
    for i in range(24):
        sheet1.write(j , i , matX2[j][i])
        sheet2.write(j , i , theta_sigma[j][i])
        sheet3.write(j , i , theta_max[j][i])
        pass
    pass
for i in range(24):
    sheet4.write(i , 0 , Sum[i])
write.save("Answer to Q4 improve2.xls")