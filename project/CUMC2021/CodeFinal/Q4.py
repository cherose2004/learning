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

Max = np.zeros([42 , 24])
Sigma = np.zeros([42 , 24])
Ave = np.zeros([42 , 24])
for j in range(42):
    Max[j] = ListSupplier[j].theta_max
    Sigma[j] = ListSupplier[j].theta_sigma
    Ave = ListSupplier[j].theta_ave
    pass

Sum = np.zeros(24)
for j in range(24):
    tmp = 0.
    for i in range(42):
        tmp += ListSupplier[i].lam * Max[i][j]
        pass
    Sum[j] = tmp
    pass

Write = xlwt.Workbook()
sheet1 = Write.add_sheet("24周供货表")
sheet2 = Write.add_sheet("每周产能")

for i in range(24):
    for j in range(42):
        sheet1.write(j , i , Max[j][i])
        pass
    sheet2.write(i , 0 , Sum[i])
    pass
Write.save("Answer to Q4 improve.xls")