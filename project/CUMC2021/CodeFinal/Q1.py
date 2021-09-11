import numpy as np
import xlrd
import xlwt
import copy

Number = 402
Week = 240
InitRow = 1
InitColumn = 2

Require = np.zeros([Number , Week])
Supply = np.zeros([Number , Week])
filename = "附件1 近5年402家供应商的相关数据.xls"
file = xlrd.open_workbook(filename)
SheetName = file.sheet_names()
Sheet1 = file.sheet_by_name(sheet_name = SheetName[0])
Sheet2 = file.sheet_by_name(sheet_name = SheetName[1])
for j in range(Number):
    for i in range(Week):
        Require[j][i] = Sheet1.cell_value(rowx = j+InitRow , colx = i+InitColumn)
        Supply[j][i] = Sheet2.cell_value(rowx = j+InitRow , colx = i+InitColumn)
        pass
    pass

class Supplier:

    def __init__(self , r , s):
        self.GetU1(r , s)
        self.GetU2(r , s)
        self.GetU3(r , s)
        self.GetU4(r , s)
        pass

    def GetU1(self , r , s):
        percent = (s.sum() - r.sum()) / r.sum()
        self.u1 = percent
        pass

    def GetU2(self , r , s):
        Sum = s.sum()
        self.u2 = Sum
        pass

    def GetU3(self , r , s):
        a = r.dot(s)
        b = np.sqrt(r.dot(r) * s.dot(s))
        self.u3 = a/b
        pass

    def GetU4(self , r , s):
        vec01 = np.zeros(r.size)
        for i in range(r.size):
            if r[0:i+1].sum() < s[0:i+1].sum():
                vec01[i] = 1
                pass
            pass
        self.u4 = vec01.sum()
        pass
    pass

ListSupplier = list()
for i in range(Number):
    r = Require[i]
    s = Supply[i]
    item = Supplier(r , s)
    ListSupplier.append(item)
    pass

U = np.zeros([Number , 4])
for j in range(Number):
    item = ListSupplier[j]
    U[j][0] = item.u1
    U[j][1] = item.u2
    U[j][2] = item.u3
    U[j][3] = item.u4
    pass

def Normalize(vec):
    return (vec - vec.min()) / (vec.max() - vec.min())
    pass

Un = copy.deepcopy(U.T)
for i in range(4):
    Un[i] = Normalize(Un[i])
    pass

def GetP(X):
    M , N = X.shape
    P = np.zeros([M , N])
    for j in range(M):
        P[j] = X[j] / X[j].sum()
        pass
    return P
    pass
Pn = GetP(Un)

def GetE(P , m):
    k = 1. / np.log(m)
    M , N = P.shape
    E = np.zeros(M)
    for j in range(M):
        SumP = 0.
        for i in range(N):
            p = P[j][i]
            SumP += p * np.log(p)
            pass
        E[j] = -k * SumP
        pass
    return E
    pass

En = GetE(Pn+1e-20 , Number) #修正!!
Dn = 1.-En
Wn = Dn / Dn.sum()
print(Wn)

Fn = np.zeros(Number)
for j in range(Number):
    Fj = 0.
    for i in range(4):
        Fj += Wn[i] * Pn[i][j]
        pass
    Fn[j] = Fj
    pass
Fn

Rank = np.argsort(1-Fn)
Top50 = Rank[0:50] + 1
print(Top50)

Write = xlwt.Workbook()
SheetWrite1 = Write.add_sheet("订单表")
SheetWrite2 = Write.add_sheet("供货表")
for j in range(Rank.size+1):
    if j == 0:
        for i in range(242):
            SheetWrite1.write(j , i , Sheet1.cell_value(rowx = j , colx = i))
            SheetWrite2.write(j , i , Sheet2.cell_value(rowx = j , colx = i))
            pass
        pass
    else:
        k = Rank[j-1]
        line = k + 1
        SheetWrite1.write(j , 0 , Sheet1.cell_value(rowx = line , colx = 0))
        SheetWrite1.write(j , 1 , Sheet1.cell_value(rowx = line , colx = 1))
        SheetWrite2.write(j , 0 , Sheet2.cell_value(rowx = line , colx = 0))
        SheetWrite2.write(j , 1 , Sheet2.cell_value(rowx = line , colx = 1))
        for i in range(2,242):
            SheetWrite1.write(j , i , Sheet1.cell_value(rowx = line , colx = i))
            SheetWrite2.write(j , i , Sheet2.cell_value(rowx = line , colx = i))
            pass
        pass
    pass

SheetU = Write.add_sheet("四个基础指标")
SheetP = Write.add_sheet("比重P")
SheetF = Write.add_sheet("综合指标")
for j in range(Number):
    for i in range(4):
        SheetU.write(j , i , U[j][i])
        SheetP.write(j , i , Pn[i][j])
        pass
    SheetF.write(j , 0 , Fn[j])
    pass

SheetEW = Write.add_sheet("信息熵及权值")
for i in range(4):
    SheetEW.write(0 , i , En[i])
    SheetEW.write(1 , i , Wn[i])
    pass

Write.save("AfterRank.xls")
print("end")