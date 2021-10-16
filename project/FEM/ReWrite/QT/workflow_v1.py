from importlib.resources import path
import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
NaN = np.nan
nan = np.nan
import FEM as fem
from FEM_v1 import *


class MQFigure(FigureCanvas):
    def __init__(self,width=40, height=40):
         # 创建一个Figure,该Figure为matplotlib下的Figure，不是matplotlib.pyplot下面的Figure
        self.fig = plt.figure(figsize=(width, height), facecolor='white')
         # 在父类中激活Figure窗口，此句必不可少，否则不能显示图形
        super(MQFigure, self).__init__(self.fig)
        pass
    pass


class FEMMainWindow(Ui_BasicWindow, QDialog):

    def __init__(self):
        self.nodelist = list()
        self.Pic = MQFigure()
        super(FEMMainWindow, self).__init__()
        self.setupUi(self)
        self.AddNode.clicked.connect(self.AddNodeButton)
        self.DelNode.clicked.connect(self.DelNodeButton)
        self.GenerateSystem.clicked.connect(self.GenerateSystemButton)
        self.AddConnection.clicked.connect(self.AddConnectionButton)
        self.AddSheet.clicked.connect(self.AddSheetButton)
        self.AddSpring.clicked.connect(self.AddSpringButton)
        self.Solve.clicked.connect(self.SolveButton)
        self.ExportReport.clicked.connect(self.ExportReportButton)
        self.ExportExcel.clicked.connect(self.ExportExcelButton)
        self.ExportPic.clicked.connect(self.ExportPicButton)
        self.SetPrecision.clicked.connect(self.SetPrecisionButton)
        self.gridlayout = QGridLayout(self.PicBox)
        self.gridlayout.addWidget(self.Pic)
        self.initTable()
        self.NodeTable.show()
        pass

    def DrawNode(self):
        plt.clf()
        self.Pic.fig.add_subplot(1, 1, 1)
        plt.axis('off')
        for k in range( len(self.nodelist) ):
            node = self.nodelist[k]
            plt.scatter(node.x, node.y, s = 1000, color='r', alpha=0.7)
            plt.text(node.x , node.y , str(k+1) , fontsize = 52 , color = 'gray' , alpha = 0.8)
            pass
        #plt.draw()
        pass

    def initTable(self):
        self.NodeTable.horizontalHeader().setVisible(True)
        self.NodeTable.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        w = 20
        self.NodeTable.setColumnWidth(0, w)
        self.NodeTable.setColumnWidth(1, w)
        self.NodeTable.setColumnWidth(2, w)
        self.NodeTable.setColumnWidth(3, w)
        self.NodeTable.setColumnWidth(4, w)
        self.NodeTable.setColumnWidth(5, w)
        self.NodeTable.setColumnWidth(6, w)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderItem(0, QStandardItem("ID"))
        self.model.setHorizontalHeaderItem(1, QStandardItem("x"))
        self.model.setHorizontalHeaderItem(2, QStandardItem("y"))
        self.model.setHorizontalHeaderItem(3, QStandardItem("Px"))
        self.model.setHorizontalHeaderItem(4, QStandardItem("Py"))
        self.model.setHorizontalHeaderItem(5, QStandardItem("u"))
        self.model.setHorizontalHeaderItem(6, QStandardItem("v"))
        self.NodeTable.setModel(self.model)
        pass

    def AddNodeButton(self):
        x = eval( mainwindow.InputX.text() )
        y = eval( mainwindow.InputY.text() )
        Px = eval( mainwindow.InputPx.text() )
        Py = eval( mainwindow.InputPy.text() )
        u = eval( mainwindow.InputU.text() )
        v = eval( mainwindow.InputV.text() )
        node = fem.Node(x, y, Px, Py, u, v)
        self.nodelist.append(node)
        self.WriteTable()
        self.DelID.setText(QCoreApplication.translate("BasicWindow", str( len(self.nodelist) ), None))
        self.DelID.setPlaceholderText(QCoreApplication.translate("BasicWindow", str( len(self.nodelist) ), None))
        self.DrawNode()
        plt.draw()
        print("Successfully Add A New Node at (" + str(x) + ',' + str(y) + ')')
        pass

    def DelNodeButton(self):
        k = eval( mainwindow.DelID.text() )
        if k <= 0 or k > len(self.nodelist):
            print("Error of ID")
            pass
        else:
            del self.nodelist[k-1]
            self.DelID.setText(QCoreApplication.translate("BasicWindow", str( len(self.nodelist) ), None))
            self.DelID.setPlaceholderText(QCoreApplication.translate("BasicWindow", str( len(self.nodelist) ), None))
            print("Successfully Delete Node"+str(k))
            pass
        self.WriteTable()
        self.DrawNode()
        plt.draw()
        pass

    def GenerateSystemButton(self):
        self.sys = fem.SystemTruss(self.nodelist)
        plt.title("Truss System" , fontsize = 20)
        plt.draw()
        pass

    def AddConnectionButton(self):
        j = eval( mainwindow.ConnectJ.text() )
        i = eval( mainwindow.ConnectI.text() )
        E = eval( mainwindow.ConnectE.text() )
        A = eval( mainwindow.ConnectA.text() )
        self.sys.Connect(j, i, E=E, A=A)
        nodej = self.nodelist[j-1]
        nodei = self.nodelist[i-1]
        plt.plot([nodej.x , nodei.x] , [nodej.y , nodei.y] , linewidth = 13 , alpha = 0.7 , color = 'g')
        plt.draw()
        print("Successfully Connect "+ str(j) + ',' + str(i))
        pass

    def AddSheetButton(self):
        i = eval( mainwindow.SheetI.text() )
        j = eval( mainwindow.SheetJ.text() )
        l = eval( mainwindow.SheetL.text() )
        m = eval( mainwindow.SheetM.text() )
        G = eval( mainwindow.SheetG.text() )
        t = eval( mainwindow.SheetT.text() )
        self.sys.SetSheet(i, j, l, m, G, t)
        nodei = self.nodelist[i-1]
        nodej = self.nodelist[j-1]
        nodel = self.nodelist[l-1]
        nodem = self.nodelist[m-1]
        fillx = np.array([nodei.x , nodej.x , nodel.x , nodem.x])
        filly = np.array([nodei.y , nodej.y , nodel.y , nodem.y])
        plt.fill(fillx , filly , facecolor = 'y' , alpha = 0.3)
        plt.draw()
        print("Successfully Add A Sheet !")
        pass

    def AddSpringButton(self):
        ID = eval( mainwindow.SpringID.text() )
        k = eval( mainwindow.SpringK.text() )
        dire = mainwindow.SpringDire.currentText()
        self.sys.SetSpring(ID, dire, k)
        print("Successfully Add A Spring Bound !")
        pass

    def SolveButton(self):
        self.sys.Generate()
        self.sys.Solve()
        plt.clf()
        self.Pic.fig.add_subplot(1, 1, 1)
        self.__TMPFigure()
        plt.draw()
        pass

    def __TMPFigure(self):
        size = 40
        PointSize = 40*size
        ftsize = size/3
        LineSize = size/3
        for k in range(self.sys.N):
            node = self.sys.NodeList[k]
            x = node.x
            y = node.y
            plt.scatter(x , y , s = PointSize , alpha = 0.7 , color = 'r')
            plt.text(x , y , str(k+1) , fontsize = 3*ftsize , color = 'gray' , alpha = 0.8)
            plt.text(x , y , 'u = '+str(node.u)+'\nv = '+str(node.v) , fontsize = ftsize , color = 'b')
            pass
        '''
        再绘制连接以及
        各端轴力
        '''
        for j in range(self.sys.N):
            for i in range(self.sys.N):
                if self.sys.NodeConnection[j][i] != 1:
                    continue
                else:
                    nodej = self.sys.NodeList[j]
                    nodei = self.sys.NodeList[i]
                    plt.plot([nodej.x , nodei.x] , [nodej.y , nodei.y] , linewidth = LineSize , alpha = 0.7 , color = 'g')
                    x1 = 0.8*nodej.x + 0.2*nodei.x
                    x2 = 0.2*nodej.x + 0.8*nodei.x
                    y1 = 0.8*nodej.y + 0.2*nodei.y
                    y2 = 0.2*nodej.y + 0.8*nodei.y
                    plt.text(x1 , y1 , self.sys.InternalForce[j][i] , fontsize = ftsize , color = 'k')
                    plt.text(x2 , y2 , self.sys.InternalForce[i][j] , fontsize = ftsize , color = 'k')
                    pass
                pass
            pass
        '''
        再绘制薄板约束件
        '''
        for sheet in self.sys.SheetList:
            nodei = self.sys.NodeList[sheet.i]
            nodej = self.sys.NodeList[sheet.j]
            nodel = self.sys.NodeList[sheet.l]
            nodem = self.sys.NodeList[sheet.m]
            fillx = np.array([nodei.x , nodej.x , nodel.x , nodem.x])
            filly = np.array([nodei.y , nodej.y , nodel.y , nodem.y])
            plt.fill(fillx , filly , facecolor = 'y' , alpha = 0.3)
            plt.text(np.mean(fillx) , np.mean(filly) , 'q = ' + str(sheet.q) + '\n' + str(sheet.j+1) + '->' + str(sheet.i+1) , fontsize = ftsize , color = 'k')
            pass
        plt.axis('off')
        plt.title("Truss System" , fontsize = 1.5*ftsize)
        pass

    def WriteTable(self):
        self.model.removeRows(0, self.model.rowCount())
        for k in range(len(self.nodelist)):
            self.model.setItem(k, 0, QStandardItem(str(k+1)))
            self.model.setItem(k, 1, QStandardItem(str( self.nodelist[k].x )))
            self.model.setItem(k, 2, QStandardItem(str( self.nodelist[k].y )))
            self.model.setItem(k, 3, QStandardItem(str( self.nodelist[k].Px )))
            self.model.setItem(k, 4, QStandardItem(str( self.nodelist[k].Py )))
            self.model.setItem(k, 5, QStandardItem(str( self.nodelist[k].u )))
            self.model.setItem(k, 6, QStandardItem(str( self.nodelist[k].v )))
            pass
        pass
    
    def ExportReportButton(self):
        path = mainwindow.ReportName.text()
        self.sys.ExportReport(path)
        pass

    def ExportExcelButton(self):
        path = mainwindow.ExcelName.text()
        self.sys.ExportExcel(path)
        pass

    def ExportPicButton(self):
        path = mainwindow.PicName.text()
        self.sys.ExportFigure(path)
        pass
    
    def SetPrecisionButton(self):
        pre = eval(mainwindow.Precision.currentText())
        pre = int(pre)
        self.sys.SetPrecison(dec = pre)
        plt.clf()
        self.Pic.fig.add_subplot(1, 1, 1)
        self.__TMPFigure()
        plt.draw()
        pass

    pass






if __name__ == "__main__":
    app = QApplication(sys.argv)
    #nodelist = list()
    mainwindow = FEMMainWindow()
    mainwindow.show()
    #app.installEventFilter(main)
    sys.exit(app.exec_())