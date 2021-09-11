import numpy as np
import xlrd
import xlwt

file = xlrd.open_workbook("附件2 近5年8家转运商的相关数据.xls")
sheet = file.sheet_by_index(0)
Number = 8
Week = 240
mat = np.zeros([Number , Week])
for j in range(Number):
    for i in range(Week):
        mat[j][i] = sheet.cell_value(rowx = j+1 , colx = i+1)
        pass
    pass

data = np.zeros([Number , 3])
for i in range(Number):
    data[i][0] = np.mean(mat[i])
    data[i][1] = np.std(mat[i])
    data[i][2] = data[i][0] + 2*data[i][1]
    pass
print(data)

dat = np.zeros(Number)
for j in range(Number):
    tmp = list()
    for i in range(Week):
        if mat[j][i] < data[j][2]:
            tmp.append(mat[j][i])
            pass
        pass
    tmp = np.array(tmp)
    dat[j] = np.mean(tmp)
    pass
dat