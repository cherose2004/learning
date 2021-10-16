# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FEM_v1.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_BasicWindow(object):
    def setupUi(self, BasicWindow):
        if not BasicWindow.objectName():
            BasicWindow.setObjectName(u"BasicWindow")
        BasicWindow.resize(1341, 976)
        self.AddNode = QPushButton(BasicWindow)
        self.AddNode.setObjectName(u"AddNode")
        self.AddNode.setGeometry(QRect(1160, 170, 171, 71))
        self.InputX = QLineEdit(BasicWindow)
        self.InputX.setObjectName(u"InputX")
        self.InputX.setGeometry(QRect(1070, 10, 71, 31))
        self.InputX.setDragEnabled(False)
        self.InputX.setReadOnly(False)
        self.InputX.setClearButtonEnabled(True)
        self.InputY = QLineEdit(BasicWindow)
        self.InputY.setObjectName(u"InputY")
        self.InputY.setGeometry(QRect(1260, 10, 71, 31))
        self.InputY.setClearButtonEnabled(True)
        self.InputPx = QLineEdit(BasicWindow)
        self.InputPx.setObjectName(u"InputPx")
        self.InputPx.setGeometry(QRect(1070, 70, 71, 31))
        self.InputPx.setClearButtonEnabled(True)
        self.InputPy = QLineEdit(BasicWindow)
        self.InputPy.setObjectName(u"InputPy")
        self.InputPy.setGeometry(QRect(1260, 70, 71, 31))
        self.InputPy.setClearButtonEnabled(True)
        self.InputU = QLineEdit(BasicWindow)
        self.InputU.setObjectName(u"InputU")
        self.InputU.setGeometry(QRect(1070, 130, 71, 31))
        self.InputU.setClearButtonEnabled(True)
        self.InputV = QLineEdit(BasicWindow)
        self.InputV.setObjectName(u"InputV")
        self.InputV.setGeometry(QRect(1260, 130, 71, 31))
        self.InputV.setClearButtonEnabled(True)
        self.XLabel = QLabel(BasicWindow)
        self.XLabel.setObjectName(u"XLabel")
        self.XLabel.setGeometry(QRect(970, 10, 91, 31))
        self.YLabel = QLabel(BasicWindow)
        self.YLabel.setObjectName(u"YLabel")
        self.YLabel.setGeometry(QRect(1160, 10, 91, 31))
        self.PxLabel = QLabel(BasicWindow)
        self.PxLabel.setObjectName(u"PxLabel")
        self.PxLabel.setGeometry(QRect(970, 70, 91, 31))
        self.PyLabel = QLabel(BasicWindow)
        self.PyLabel.setObjectName(u"PyLabel")
        self.PyLabel.setGeometry(QRect(1160, 70, 101, 31))
        self.ULabel = QLabel(BasicWindow)
        self.ULabel.setObjectName(u"ULabel")
        self.ULabel.setGeometry(QRect(970, 130, 91, 31))
        self.VLabel = QLabel(BasicWindow)
        self.VLabel.setObjectName(u"VLabel")
        self.VLabel.setGeometry(QRect(1160, 130, 91, 31))
        self.NodeTable = QTableView(BasicWindow)
        self.NodeTable.setObjectName(u"NodeTable")
        self.NodeTable.setGeometry(QRect(10, 10, 921, 301))
        self.DelNode = QPushButton(BasicWindow)
        self.DelNode.setObjectName(u"DelNode")
        self.DelNode.setGeometry(QRect(960, 170, 131, 71))
        self.DelID = QLineEdit(BasicWindow)
        self.DelID.setObjectName(u"DelID")
        self.DelID.setGeometry(QRect(1100, 170, 41, 71))
        self.GenerateSystem = QPushButton(BasicWindow)
        self.GenerateSystem.setObjectName(u"GenerateSystem")
        self.GenerateSystem.setGeometry(QRect(962, 257, 371, 41))
        self.PicBox = QGroupBox(BasicWindow)
        self.PicBox.setObjectName(u"PicBox")
        self.PicBox.setGeometry(QRect(10, 320, 921, 651))
        self.AddConnection = QPushButton(BasicWindow)
        self.AddConnection.setObjectName(u"AddConnection")
        self.AddConnection.setGeometry(QRect(960, 320, 121, 91))
        self.ConnectJLabel = QLabel(BasicWindow)
        self.ConnectJLabel.setObjectName(u"ConnectJLabel")
        self.ConnectJLabel.setGeometry(QRect(1090, 320, 72, 20))
        self.ConnectILabel = QLabel(BasicWindow)
        self.ConnectILabel.setObjectName(u"ConnectILabel")
        self.ConnectILabel.setGeometry(QRect(1220, 320, 72, 20))
        self.ConnectELabel = QLabel(BasicWindow)
        self.ConnectELabel.setObjectName(u"ConnectELabel")
        self.ConnectELabel.setGeometry(QRect(1100, 370, 31, 41))
        self.ConnectALabel = QLabel(BasicWindow)
        self.ConnectALabel.setObjectName(u"ConnectALabel")
        self.ConnectALabel.setGeometry(QRect(1220, 370, 31, 41))
        self.ConnectJ = QLineEdit(BasicWindow)
        self.ConnectJ.setObjectName(u"ConnectJ")
        self.ConnectJ.setGeometry(QRect(1150, 310, 61, 41))
        self.ConnectJ.setDragEnabled(False)
        self.ConnectJ.setReadOnly(False)
        self.ConnectJ.setClearButtonEnabled(True)
        self.ConnectI = QLineEdit(BasicWindow)
        self.ConnectI.setObjectName(u"ConnectI")
        self.ConnectI.setGeometry(QRect(1260, 310, 71, 41))
        self.ConnectI.setDragEnabled(False)
        self.ConnectI.setReadOnly(False)
        self.ConnectI.setClearButtonEnabled(True)
        self.ConnectE = QLineEdit(BasicWindow)
        self.ConnectE.setObjectName(u"ConnectE")
        self.ConnectE.setGeometry(QRect(1130, 370, 81, 41))
        self.ConnectE.setDragEnabled(False)
        self.ConnectE.setReadOnly(False)
        self.ConnectE.setClearButtonEnabled(True)
        self.ConnectA = QLineEdit(BasicWindow)
        self.ConnectA.setObjectName(u"ConnectA")
        self.ConnectA.setGeometry(QRect(1250, 370, 81, 41))
        self.ConnectA.setDragEnabled(False)
        self.ConnectA.setReadOnly(False)
        self.ConnectA.setClearButtonEnabled(True)
        self.AddSheet = QPushButton(BasicWindow)
        self.AddSheet.setObjectName(u"AddSheet")
        self.AddSheet.setGeometry(QRect(960, 440, 121, 151))
        self.SheetI = QLineEdit(BasicWindow)
        self.SheetI.setObjectName(u"SheetI")
        self.SheetI.setGeometry(QRect(1150, 470, 61, 31))
        self.SheetI.setDragEnabled(False)
        self.SheetI.setReadOnly(False)
        self.SheetI.setClearButtonEnabled(True)
        self.SheetJ = QLineEdit(BasicWindow)
        self.SheetJ.setObjectName(u"SheetJ")
        self.SheetJ.setGeometry(QRect(1270, 470, 61, 31))
        self.SheetJ.setDragEnabled(False)
        self.SheetJ.setReadOnly(False)
        self.SheetJ.setClearButtonEnabled(True)
        self.SheetL = QLineEdit(BasicWindow)
        self.SheetL.setObjectName(u"SheetL")
        self.SheetL.setGeometry(QRect(1150, 510, 61, 31))
        self.SheetL.setDragEnabled(False)
        self.SheetL.setReadOnly(False)
        self.SheetL.setClearButtonEnabled(True)
        self.SheetM = QLineEdit(BasicWindow)
        self.SheetM.setObjectName(u"SheetM")
        self.SheetM.setGeometry(QRect(1270, 510, 61, 31))
        self.SheetM.setDragEnabled(False)
        self.SheetM.setReadOnly(False)
        self.SheetM.setClearButtonEnabled(True)
        self.SheetILabel = QLabel(BasicWindow)
        self.SheetILabel.setObjectName(u"SheetILabel")
        self.SheetILabel.setGeometry(QRect(1120, 460, 31, 41))
        self.SheetJLabel = QLabel(BasicWindow)
        self.SheetJLabel.setObjectName(u"SheetJLabel")
        self.SheetJLabel.setGeometry(QRect(1240, 460, 31, 41))
        self.SheetLLabel = QLabel(BasicWindow)
        self.SheetLLabel.setObjectName(u"SheetLLabel")
        self.SheetLLabel.setGeometry(QRect(1120, 500, 31, 41))
        self.SheetMLabel = QLabel(BasicWindow)
        self.SheetMLabel.setObjectName(u"SheetMLabel")
        self.SheetMLabel.setGeometry(QRect(1240, 500, 31, 41))
        self.SheetLabel = QLabel(BasicWindow)
        self.SheetLabel.setObjectName(u"SheetLabel")
        self.SheetLabel.setGeometry(QRect(1101, 424, 231, 51))
        self.SheetGLabel = QLabel(BasicWindow)
        self.SheetGLabel.setObjectName(u"SheetGLabel")
        self.SheetGLabel.setGeometry(QRect(1100, 550, 31, 41))
        self.SheetG = QLineEdit(BasicWindow)
        self.SheetG.setObjectName(u"SheetG")
        self.SheetG.setGeometry(QRect(1130, 550, 81, 41))
        self.SheetG.setDragEnabled(False)
        self.SheetG.setReadOnly(False)
        self.SheetG.setClearButtonEnabled(True)
        self.SheetTLabel = QLabel(BasicWindow)
        self.SheetTLabel.setObjectName(u"SheetTLabel")
        self.SheetTLabel.setGeometry(QRect(1220, 550, 31, 41))
        self.SheetT = QLineEdit(BasicWindow)
        self.SheetT.setObjectName(u"SheetT")
        self.SheetT.setGeometry(QRect(1250, 550, 81, 41))
        self.SheetT.setDragEnabled(False)
        self.SheetT.setReadOnly(False)
        self.SheetT.setClearButtonEnabled(True)
        self.AddSpring = QPushButton(BasicWindow)
        self.AddSpring.setObjectName(u"AddSpring")
        self.AddSpring.setGeometry(QRect(960, 620, 121, 71))
        self.SpringIDLabel = QLabel(BasicWindow)
        self.SpringIDLabel.setObjectName(u"SpringIDLabel")
        self.SpringIDLabel.setGeometry(QRect(1100, 610, 31, 41))
        self.SpringID = QLineEdit(BasicWindow)
        self.SpringID.setObjectName(u"SpringID")
        self.SpringID.setGeometry(QRect(1140, 610, 71, 41))
        self.SpringID.setDragEnabled(False)
        self.SpringID.setReadOnly(False)
        self.SpringID.setClearButtonEnabled(True)
        self.SpringKLabel = QLabel(BasicWindow)
        self.SpringKLabel.setObjectName(u"SpringKLabel")
        self.SpringKLabel.setGeometry(QRect(1220, 610, 31, 41))
        self.SpringK = QLineEdit(BasicWindow)
        self.SpringK.setObjectName(u"SpringK")
        self.SpringK.setGeometry(QRect(1260, 610, 71, 41))
        self.SpringK.setDragEnabled(False)
        self.SpringK.setReadOnly(False)
        self.SpringK.setClearButtonEnabled(True)
        self.SpringDire = QComboBox(BasicWindow)
        self.SpringDire.addItem("")
        self.SpringDire.addItem("")
        self.SpringDire.setObjectName(u"SpringDire")
        self.SpringDire.setGeometry(QRect(1200, 660, 131, 22))
        self.SpringIDLabel_2 = QLabel(BasicWindow)
        self.SpringIDLabel_2.setObjectName(u"SpringIDLabel_2")
        self.SpringIDLabel_2.setGeometry(QRect(1100, 650, 81, 41))
        self.Solve = QPushButton(BasicWindow)
        self.Solve.setObjectName(u"Solve")
        self.Solve.setGeometry(QRect(960, 700, 371, 51))
        self.ExportReport = QPushButton(BasicWindow)
        self.ExportReport.setObjectName(u"ExportReport")
        self.ExportReport.setGeometry(QRect(960, 760, 141, 51))
        self.ReportPathLabel = QLabel(BasicWindow)
        self.ReportPathLabel.setObjectName(u"ReportPathLabel")
        self.ReportPathLabel.setGeometry(QRect(1110, 770, 91, 31))
        self.ReportName = QLineEdit(BasicWindow)
        self.ReportName.setObjectName(u"ReportName")
        self.ReportName.setGeometry(QRect(1200, 770, 131, 31))
        self.ReportName.setClearButtonEnabled(True)
        self.ExportExcel = QPushButton(BasicWindow)
        self.ExportExcel.setObjectName(u"ExportExcel")
        self.ExportExcel.setGeometry(QRect(960, 820, 141, 51))
        self.ExcelPathLabel = QLabel(BasicWindow)
        self.ExcelPathLabel.setObjectName(u"ExcelPathLabel")
        self.ExcelPathLabel.setGeometry(QRect(1110, 830, 91, 31))
        self.ExcelName = QLineEdit(BasicWindow)
        self.ExcelName.setObjectName(u"ExcelName")
        self.ExcelName.setGeometry(QRect(1200, 830, 131, 31))
        self.ExcelName.setClearButtonEnabled(True)
        self.ExportPic = QPushButton(BasicWindow)
        self.ExportPic.setObjectName(u"ExportPic")
        self.ExportPic.setGeometry(QRect(960, 880, 141, 51))
        self.PicPathLabel = QLabel(BasicWindow)
        self.PicPathLabel.setObjectName(u"PicPathLabel")
        self.PicPathLabel.setGeometry(QRect(1110, 890, 91, 31))
        self.PicName = QLineEdit(BasicWindow)
        self.PicName.setObjectName(u"PicName")
        self.PicName.setGeometry(QRect(1200, 890, 131, 31))
        self.PicName.setClearButtonEnabled(True)
        self.SetPrecision = QPushButton(BasicWindow)
        self.SetPrecision.setObjectName(u"SetPrecision")
        self.SetPrecision.setGeometry(QRect(960, 940, 201, 31))
        self.Precision = QComboBox(BasicWindow)
        self.Precision.addItem("")
        self.Precision.addItem("")
        self.Precision.addItem("")
        self.Precision.addItem("")
        self.Precision.addItem("")
        self.Precision.addItem("")
        self.Precision.addItem("")
        self.Precision.addItem("")
        self.Precision.addItem("")
        self.Precision.addItem("")
        self.Precision.setObjectName(u"Precision")
        self.Precision.setGeometry(QRect(1190, 940, 141, 31))

        self.retranslateUi(BasicWindow)

        QMetaObject.connectSlotsByName(BasicWindow)
    # setupUi

    def retranslateUi(self, BasicWindow):
        BasicWindow.setWindowTitle(QCoreApplication.translate("BasicWindow", u"Form", None))
        self.AddNode.setText(QCoreApplication.translate("BasicWindow", u"Add Node", None))
        self.InputX.setText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.InputX.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.InputY.setText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.InputY.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.InputPx.setText(QCoreApplication.translate("BasicWindow", u"NaN", None))
        self.InputPx.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"NaN", None))
        self.InputPy.setText(QCoreApplication.translate("BasicWindow", u"NaN", None))
        self.InputPy.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"NaN", None))
        self.InputU.setText(QCoreApplication.translate("BasicWindow", u"NaN", None))
        self.InputU.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"NaN", None))
        self.InputV.setText(QCoreApplication.translate("BasicWindow", u"NaN", None))
        self.InputV.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"NaN", None))
        self.XLabel.setText(QCoreApplication.translate("BasicWindow", u"X  (meter):", None))
        self.YLabel.setText(QCoreApplication.translate("BasicWindow", u"Y  (meter):", None))
        self.PxLabel.setText(QCoreApplication.translate("BasicWindow", u"Px(Newton):", None))
        self.PyLabel.setText(QCoreApplication.translate("BasicWindow", u"Py (Newton):", None))
        self.ULabel.setText(QCoreApplication.translate("BasicWindow", u"u  (meter):", None))
        self.VLabel.setText(QCoreApplication.translate("BasicWindow", u"v  (meter):", None))
        self.DelNode.setText(QCoreApplication.translate("BasicWindow", u"Delete Node", None))
        self.DelID.setText(QCoreApplication.translate("BasicWindow", u"1", None))
        self.DelID.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"1", None))
        self.GenerateSystem.setText(QCoreApplication.translate("BasicWindow", u"Generate System", None))
        self.PicBox.setTitle(QCoreApplication.translate("BasicWindow", u"Draft", None))
        self.AddConnection.setText(QCoreApplication.translate("BasicWindow", u"Add Connection", None))
        self.ConnectJLabel.setText(QCoreApplication.translate("BasicWindow", u"Begin:", None))
        self.ConnectILabel.setText(QCoreApplication.translate("BasicWindow", u"End:", None))
        self.ConnectELabel.setText(QCoreApplication.translate("BasicWindow", u"E:", None))
        self.ConnectALabel.setText(QCoreApplication.translate("BasicWindow", u"A:", None))
        self.ConnectJ.setText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.ConnectJ.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.ConnectI.setText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.ConnectI.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.ConnectE.setText(QCoreApplication.translate("BasicWindow", u"200e9", None))
        self.ConnectE.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.ConnectA.setText(QCoreApplication.translate("BasicWindow", u"0.01", None))
        self.ConnectA.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"0.01", None))
        self.AddSheet.setText(QCoreApplication.translate("BasicWindow", u"Add Sheet", None))
        self.SheetI.setText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.SheetI.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.SheetJ.setText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.SheetJ.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.SheetL.setText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.SheetL.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.SheetM.setText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.SheetM.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"0", None))
        self.SheetILabel.setText(QCoreApplication.translate("BasicWindow", u"1:", None))
        self.SheetJLabel.setText(QCoreApplication.translate("BasicWindow", u"2:", None))
        self.SheetLLabel.setText(QCoreApplication.translate("BasicWindow", u"3:", None))
        self.SheetMLabel.setText(QCoreApplication.translate("BasicWindow", u"4:", None))
        self.SheetLabel.setText(QCoreApplication.translate("BasicWindow", u"1-2 should be a parallel line \n"
" order should be a cycle", None))
        self.SheetGLabel.setText(QCoreApplication.translate("BasicWindow", u"G:", None))
        self.SheetG.setText(QCoreApplication.translate("BasicWindow", u"100e9", None))
        self.SheetG.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"100e9", None))
        self.SheetTLabel.setText(QCoreApplication.translate("BasicWindow", u"t:", None))
        self.SheetT.setText(QCoreApplication.translate("BasicWindow", u"0.01", None))
        self.SheetT.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"0.01", None))
        self.AddSpring.setText(QCoreApplication.translate("BasicWindow", u"Add Spring", None))
        self.SpringIDLabel.setText(QCoreApplication.translate("BasicWindow", u"ID:", None))
        self.SpringID.setText(QCoreApplication.translate("BasicWindow", u"1", None))
        self.SpringID.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"1", None))
        self.SpringKLabel.setText(QCoreApplication.translate("BasicWindow", u"k:", None))
        self.SpringK.setText(QCoreApplication.translate("BasicWindow", u"1e5", None))
        self.SpringK.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"1e5", None))
        self.SpringDire.setItemText(0, QCoreApplication.translate("BasicWindow", u"x", None))
        self.SpringDire.setItemText(1, QCoreApplication.translate("BasicWindow", u"y", None))

        self.SpringIDLabel_2.setText(QCoreApplication.translate("BasicWindow", u"direction:", None))
        self.Solve.setText(QCoreApplication.translate("BasicWindow", u"Solve Truss System !", None))
        self.ExportReport.setText(QCoreApplication.translate("BasicWindow", u"Export Report", None))
        self.ReportPathLabel.setText(QCoreApplication.translate("BasicWindow", u"Path(.txt):", None))
        self.ReportName.setText(QCoreApplication.translate("BasicWindow", u"Report.txt", None))
        self.ReportName.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"Report.txt", None))
        self.ExportExcel.setText(QCoreApplication.translate("BasicWindow", u"Export Excel", None))
        self.ExcelPathLabel.setText(QCoreApplication.translate("BasicWindow", u"Path(.xls):", None))
        self.ExcelName.setText(QCoreApplication.translate("BasicWindow", u"Excel.xls", None))
        self.ExcelName.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"Excel.xls", None))
        self.ExportPic.setText(QCoreApplication.translate("BasicWindow", u"Export Picture", None))
        self.PicPathLabel.setText(QCoreApplication.translate("BasicWindow", u"Path(.png):", None))
        self.PicName.setText(QCoreApplication.translate("BasicWindow", u"PicName.png", None))
        self.PicName.setPlaceholderText(QCoreApplication.translate("BasicWindow", u"PicName.png", None))
        self.SetPrecision.setText(QCoreApplication.translate("BasicWindow", u"Set Precision", None))
        self.Precision.setItemText(0, QCoreApplication.translate("BasicWindow", u"1", None))
        self.Precision.setItemText(1, QCoreApplication.translate("BasicWindow", u"2", None))
        self.Precision.setItemText(2, QCoreApplication.translate("BasicWindow", u"3", None))
        self.Precision.setItemText(3, QCoreApplication.translate("BasicWindow", u"4", None))
        self.Precision.setItemText(4, QCoreApplication.translate("BasicWindow", u"5", None))
        self.Precision.setItemText(5, QCoreApplication.translate("BasicWindow", u"6", None))
        self.Precision.setItemText(6, QCoreApplication.translate("BasicWindow", u"7", None))
        self.Precision.setItemText(7, QCoreApplication.translate("BasicWindow", u"8", None))
        self.Precision.setItemText(8, QCoreApplication.translate("BasicWindow", u"9", None))
        self.Precision.setItemText(9, QCoreApplication.translate("BasicWindow", u"10", None))

    # retranslateUi

