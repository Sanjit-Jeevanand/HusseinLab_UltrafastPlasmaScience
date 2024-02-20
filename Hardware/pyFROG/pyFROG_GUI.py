# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyFROG_GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(912, 843)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_29 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_29.setFont(font)
        self.label_29.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_29.setObjectName("label_29")
        self.gridLayout_3.addWidget(self.label_29, 0, 0, 1, 1)
        self.ControlTab = QtWidgets.QTabWidget(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ControlTab.setFont(font)
        self.ControlTab.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ControlTab.setObjectName("ControlTab")
        self.tab_FROG = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tab_FROG.setFont(font)
        self.tab_FROG.setProperty("current", "")
        self.tab_FROG.setObjectName("tab_FROG")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_FROG)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.plotWidget = GraphicsLayoutWidget(self.tab_FROG)
        self.plotWidget.setBaseSize(QtCore.QSize(10, 60))
        self.plotWidget.setObjectName("plotWidget")
        self.verticalLayout_6.addWidget(self.plotWidget)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_17 = QtWidgets.QLabel(self.tab_FROG)
        self.label_17.setObjectName("label_17")
        self.gridLayout_5.addWidget(self.label_17, 1, 0, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.tab_FROG)
        self.label_18.setObjectName("label_18")
        self.gridLayout_5.addWidget(self.label_18, 1, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.tab_FROG)
        self.label_19.setObjectName("label_19")
        self.gridLayout_5.addWidget(self.label_19, 1, 2, 1, 1)
        self.in_scanstepsize = QtWidgets.QLineEdit(self.tab_FROG)
        self.in_scanstepsize.setObjectName("in_scanstepsize")
        self.gridLayout_5.addWidget(self.in_scanstepsize, 2, 1, 1, 1)
        self.in_scanlen = QtWidgets.QLineEdit(self.tab_FROG)
        self.in_scanlen.setObjectName("in_scanlen")
        self.gridLayout_5.addWidget(self.in_scanlen, 2, 0, 1, 1)
        self.in_scanstepnumbers = QtWidgets.QLineEdit(self.tab_FROG)
        self.in_scanstepnumbers.setObjectName("in_scanstepnumbers")
        self.gridLayout_5.addWidget(self.in_scanstepnumbers, 2, 2, 1, 1)
        self.horizontalLayout_8.addLayout(self.gridLayout_5)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.p_aquirescan = QtWidgets.QPushButton(self.tab_FROG)
        self.p_aquirescan.setObjectName("p_aquirescan")
        self.gridLayout_6.addWidget(self.p_aquirescan, 0, 0, 1, 1)
        self.p_bkgscan = QtWidgets.QPushButton(self.tab_FROG)
        self.p_bkgscan.setObjectName("p_bkgscan")
        self.gridLayout_6.addWidget(self.p_bkgscan, 3, 0, 1, 1)
        self.p_savescan = QtWidgets.QPushButton(self.tab_FROG)
        self.p_savescan.setObjectName("p_savescan")
        self.gridLayout_6.addWidget(self.p_savescan, 2, 0, 1, 1)
        self.c_scanautosave = QtWidgets.QCheckBox(self.tab_FROG)
        self.c_scanautosave.setObjectName("c_scanautosave")
        self.gridLayout_6.addWidget(self.c_scanautosave, 1, 0, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout_6)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_20 = QtWidgets.QLabel(self.tab_FROG)
        self.label_20.setObjectName("label_20")
        self.verticalLayout.addWidget(self.label_20)
        self.in_scansavedir = QtWidgets.QLineEdit(self.tab_FROG)
        self.in_scansavedir.setMinimumSize(QtCore.QSize(200, 20))
        self.in_scansavedir.setObjectName("in_scansavedir")
        self.verticalLayout.addWidget(self.in_scansavedir)
        self.label_21 = QtWidgets.QLabel(self.tab_FROG)
        self.label_21.setObjectName("label_21")
        self.verticalLayout.addWidget(self.label_21)
        self.in_tracebasename = QtWidgets.QLineEdit(self.tab_FROG)
        self.in_tracebasename.setObjectName("in_tracebasename")
        self.verticalLayout.addWidget(self.in_tracebasename)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.ControlTab.addTab(self.tab_FROG, "")
        self.tab_align = QtWidgets.QWidget()
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.tab_align.setFont(font)
        self.tab_align.setObjectName("tab_align")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_align)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.alignmentPlot = MplCanvas(self.tab_align)
        self.alignmentPlot.setObjectName("alignmentPlot")
        self.verticalLayout_8.addWidget(self.alignmentPlot)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.tab_align)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.p_actsmallforward = QtWidgets.QPushButton(self.tab_align)
        self.p_actsmallforward.setObjectName("p_actsmallforward")
        self.gridLayout.addWidget(self.p_actsmallforward, 4, 3, 1, 1)
        self.p_actsmallback = QtWidgets.QPushButton(self.tab_align)
        self.p_actsmallback.setObjectName("p_actsmallback")
        self.gridLayout.addWidget(self.p_actsmallback, 4, 2, 1, 1)
        self.p_actlargeforward = QtWidgets.QPushButton(self.tab_align)
        self.p_actlargeforward.setObjectName("p_actlargeforward")
        self.gridLayout.addWidget(self.p_actlargeforward, 5, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.tab_align)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.in_actabsmove = QtWidgets.QLineEdit(self.tab_align)
        self.in_actabsmove.setObjectName("in_actabsmove")
        self.gridLayout.addWidget(self.in_actabsmove, 2, 1, 1, 1)
        self.p_actabsmove = QtWidgets.QPushButton(self.tab_align)
        self.p_actabsmove.setObjectName("p_actabsmove")
        self.gridLayout.addWidget(self.p_actabsmove, 2, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.tab_align)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 5, 0, 1, 1)
        self.p_actlargeback = QtWidgets.QPushButton(self.tab_align)
        self.p_actlargeback.setObjectName("p_actlargeback")
        self.gridLayout.addWidget(self.p_actlargeback, 5, 2, 1, 1)
        self.in_actsmallrel = QtWidgets.QLineEdit(self.tab_align)
        self.in_actsmallrel.setObjectName("in_actsmallrel")
        self.gridLayout.addWidget(self.in_actsmallrel, 4, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.tab_align)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.tab_align)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 1, 1, 1)
        self.in_actlargerel = QtWidgets.QLineEdit(self.tab_align)
        self.in_actlargerel.setObjectName("in_actlargerel")
        self.gridLayout.addWidget(self.in_actlargerel, 5, 1, 1, 1)
        self.c_actenableabs = QtWidgets.QCheckBox(self.tab_align)
        self.c_actenableabs.setObjectName("c_actenableabs")
        self.gridLayout.addWidget(self.c_actenableabs, 2, 3, 1, 1)
        self.x_pos_lcd_2 = QtWidgets.QLCDNumber(self.tab_align)
        self.x_pos_lcd_2.setProperty("value", 1.234)
        self.x_pos_lcd_2.setObjectName("x_pos_lcd_2")
        self.gridLayout.addWidget(self.x_pos_lcd_2, 1, 3, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.tab_align)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 6, 0, 1, 1)
        self.out_saveposition = QtWidgets.QLineEdit(self.tab_align)
        self.out_saveposition.setObjectName("out_saveposition")
        self.gridLayout.addWidget(self.out_saveposition, 6, 1, 1, 1)
        self.p_actsaveposition = QtWidgets.QPushButton(self.tab_align)
        self.p_actsaveposition.setObjectName("p_actsaveposition")
        self.gridLayout.addWidget(self.p_actsaveposition, 6, 2, 1, 1)
        self.go_home_button_2 = QtWidgets.QPushButton(self.tab_align)
        self.go_home_button_2.setObjectName("go_home_button_2")
        self.gridLayout.addWidget(self.go_home_button_2, 6, 3, 1, 1)
        self.verticalLayout_8.addLayout(self.gridLayout)
        self.ControlTab.addTab(self.tab_align, "")
        self.tab_Setup = QtWidgets.QWidget()
        self.tab_Setup.setObjectName("tab_Setup")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.tab_Setup)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.in_specexposure = QtWidgets.QLineEdit(self.tab_Setup)
        self.in_specexposure.setObjectName("in_specexposure")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.in_specexposure)
        self.label_6 = QtWidgets.QLabel(self.tab_Setup)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.in_boxcar = QtWidgets.QSpinBox(self.tab_Setup)
        self.in_boxcar.setObjectName("in_boxcar")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.in_boxcar)
        self.label_8 = QtWidgets.QLabel(self.tab_Setup)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.in_percentnoise = QtWidgets.QLineEdit(self.tab_Setup)
        self.in_percentnoise.setObjectName("in_percentnoise")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.in_percentnoise)
        self.label_14 = QtWidgets.QLabel(self.tab_Setup)
        self.label_14.setObjectName("label_14")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.in_numberaverage = QtWidgets.QSpinBox(self.tab_Setup)
        self.in_numberaverage.setObjectName("in_numberaverage")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.in_numberaverage)
        self.label_15 = QtWidgets.QLabel(self.tab_Setup)
        self.label_15.setObjectName("label_15")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.in_specsavedir = QtWidgets.QLineEdit(self.tab_Setup)
        self.in_specsavedir.setObjectName("in_specsavedir")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.in_specsavedir)
        self.label_16 = QtWidgets.QLabel(self.tab_Setup)
        self.label_16.setObjectName("label_16")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.in_specbasename = QtWidgets.QLineEdit(self.tab_Setup)
        self.in_specbasename.setObjectName("in_specbasename")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.in_specbasename)
        self.label_5 = QtWidgets.QLabel(self.tab_Setup)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.label_3 = QtWidgets.QLabel(self.tab_Setup)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.gridLayout_7.addLayout(self.formLayout, 0, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.c_subbkg = QtWidgets.QCheckBox(self.tab_Setup)
        self.c_subbkg.setObjectName("c_subbkg")
        self.gridLayout_4.addWidget(self.c_subbkg, 7, 0, 1, 1)
        self.c_darkcounts = QtWidgets.QCheckBox(self.tab_Setup)
        self.c_darkcounts.setObjectName("c_darkcounts")
        self.gridLayout_4.addWidget(self.c_darkcounts, 6, 1, 1, 1)
        self.c_calibration = QtWidgets.QCheckBox(self.tab_Setup)
        self.c_calibration.setObjectName("c_calibration")
        self.gridLayout_4.addWidget(self.c_calibration, 6, 0, 1, 1)
        self.gridLayout_7.addLayout(self.gridLayout_4, 1, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ConnectThorlabs = QtWidgets.QPushButton(self.tab_Setup)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ConnectThorlabs.setFont(font)
        self.ConnectThorlabs.setObjectName("ConnectThorlabs")
        self.verticalLayout_4.addWidget(self.ConnectThorlabs)
        self.p_loadspec = QtWidgets.QPushButton(self.tab_Setup)
        self.p_loadspec.setObjectName("p_loadspec")
        self.verticalLayout_4.addWidget(self.p_loadspec)
        self.p_loadbkg = QtWidgets.QPushButton(self.tab_Setup)
        self.p_loadbkg.setObjectName("p_loadbkg")
        self.verticalLayout_4.addWidget(self.p_loadbkg)
        self.p_savespec = QtWidgets.QPushButton(self.tab_Setup)
        self.p_savespec.setObjectName("p_savespec")
        self.verticalLayout_4.addWidget(self.p_savespec)
        self.p_takebkg = QtWidgets.QPushButton(self.tab_Setup)
        self.p_takebkg.setObjectName("p_takebkg")
        self.verticalLayout_4.addWidget(self.p_takebkg)
        self.gridLayout_7.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
        self.verticalLayout_9.addLayout(self.gridLayout_7)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.in_groupname = QtWidgets.QComboBox(self.tab_Setup)
        self.in_groupname.setObjectName("in_groupname")
        self.in_groupname.addItem("")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.in_groupname)
        self.label_13 = QtWidgets.QLabel(self.tab_Setup)
        self.label_13.setObjectName("label_13")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.in_actip = QtWidgets.QLineEdit(self.tab_Setup)
        self.in_actip.setObjectName("in_actip")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.in_actip)
        self.label_12 = QtWidgets.QLabel(self.tab_Setup)
        self.label_12.setObjectName("label_12")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.in_actstatus = QtWidgets.QLineEdit(self.tab_Setup)
        self.in_actstatus.setText("")
        self.in_actstatus.setObjectName("in_actstatus")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.in_actstatus)
        self.label_10 = QtWidgets.QLabel(self.tab_Setup)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.verticalLayout_5.addLayout(self.formLayout_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_23 = QtWidgets.QLabel(self.tab_Setup)
        self.label_23.setObjectName("label_23")
        self.verticalLayout_2.addWidget(self.label_23)
        self.in_actmaxlim = QtWidgets.QLineEdit(self.tab_Setup)
        self.in_actmaxlim.setObjectName("in_actmaxlim")
        self.verticalLayout_2.addWidget(self.in_actmaxlim)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 5, 3, 1, 1)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_46 = QtWidgets.QLabel(self.tab_Setup)
        self.label_46.setObjectName("label_46")
        self.verticalLayout_7.addWidget(self.label_46)
        self.in_actminlim_2 = QtWidgets.QLineEdit(self.tab_Setup)
        self.in_actminlim_2.setObjectName("in_actminlim_2")
        self.verticalLayout_7.addWidget(self.in_actminlim_2)
        self.gridLayout_2.addLayout(self.verticalLayout_7, 5, 2, 1, 1)
        self.p_actsetlim = QtWidgets.QPushButton(self.tab_Setup)
        self.p_actsetlim.setObjectName("p_actsetlim")
        self.gridLayout_2.addWidget(self.p_actsetlim, 5, 1, 1, 1)
        self.p_actinit = QtWidgets.QPushButton(self.tab_Setup)
        self.p_actinit.setObjectName("p_actinit")
        self.gridLayout_2.addWidget(self.p_actinit, 3, 1, 1, 1)
        self.p_acthome = QtWidgets.QPushButton(self.tab_Setup)
        self.p_acthome.setObjectName("p_acthome")
        self.gridLayout_2.addWidget(self.p_acthome, 3, 2, 1, 1)
        self.p_actenable = QtWidgets.QPushButton(self.tab_Setup)
        self.p_actenable.setObjectName("p_actenable")
        self.gridLayout_2.addWidget(self.p_actenable, 3, 3, 1, 1)
        self.ConnectXPS = QtWidgets.QPushButton(self.tab_Setup)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ConnectXPS.setFont(font)
        self.ConnectXPS.setObjectName("ConnectXPS")
        self.gridLayout_2.addWidget(self.ConnectXPS, 3, 0, 1, 1)
        self.verticalLayout_5.addLayout(self.gridLayout_2)
        self.verticalLayout_9.addLayout(self.verticalLayout_5)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem)
        self.ControlTab.addTab(self.tab_Setup, "")
        self.gridLayout_3.addWidget(self.ControlTab, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 912, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.ControlTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_29.setText(_translate("MainWindow", "Hussein Lab pyFROG"))
        self.label_17.setText(_translate("MainWindow", "Scan Length (fs)"))
        self.label_18.setText(_translate("MainWindow", "Scan Step Size (fs)"))
        self.label_19.setText(_translate("MainWindow", "Number of Steps"))
        self.p_aquirescan.setText(_translate("MainWindow", "Aquire Scan"))
        self.p_bkgscan.setText(_translate("MainWindow", "Background Scan"))
        self.p_savescan.setText(_translate("MainWindow", "Save Scan"))
        self.c_scanautosave.setText(_translate("MainWindow", "Autosave"))
        self.label_20.setText(_translate("MainWindow", "Trace Directory"))
        self.label_21.setText(_translate("MainWindow", "Trace Name"))
        self.ControlTab.setTabText(self.ControlTab.indexOf(self.tab_FROG), _translate("MainWindow", "FROG Main"))
        self.label_2.setText(_translate("MainWindow", "Small\n"
"Relative\n"
"Move"))
        self.p_actsmallforward.setText(_translate("MainWindow", "Small Step\n"
"Forward"))
        self.p_actsmallback.setText(_translate("MainWindow", "Small Step\n"
" Back"))
        self.p_actlargeforward.setText(_translate("MainWindow", "Large Step\n"
"Forward"))
        self.label.setText(_translate("MainWindow", "Absolute\n"
"Move"))
        self.in_actabsmove.setText(_translate("MainWindow", "0.0"))
        self.p_actabsmove.setText(_translate("MainWindow", "Absolute\n"
"Move"))
        self.label_9.setText(_translate("MainWindow", "Large\n"
"Relative\n"
"Move"))
        self.p_actlargeback.setText(_translate("MainWindow", "Large Step\n"
"Back"))
        self.in_actsmallrel.setText(_translate("MainWindow", "0.0"))
        self.label_7.setText(_translate("MainWindow", "Currrent Position:"))
        self.label_4.setText(_translate("MainWindow", "Stage Settings"))
        self.in_actlargerel.setText(_translate("MainWindow", "0.0"))
        self.c_actenableabs.setText(_translate("MainWindow", "Enable Abs.\n"
"Move"))
        self.label_24.setText(_translate("MainWindow", "Last Saved Home"))
        self.p_actsaveposition.setText(_translate("MainWindow", "Save Home"))
        self.go_home_button_2.setText(_translate("MainWindow", "Go Home"))
        self.ControlTab.setTabText(self.ControlTab.indexOf(self.tab_align), _translate("MainWindow", "Alignment Mode"))
        self.in_specexposure.setText(_translate("MainWindow", "100.0"))
        self.label_6.setText(_translate("MainWindow", "Thorlabs Box Car Averaging"))
        self.label_8.setText(_translate("MainWindow", "Percent Noise Cutoff"))
        self.in_percentnoise.setText(_translate("MainWindow", "0.0"))
        self.label_14.setText(_translate("MainWindow", "Spectra Saved"))
        self.label_15.setText(_translate("MainWindow", "Save Directory"))
        self.in_specsavedir.setText(_translate("MainWindow", "C:\\Users\\Sorry\\Documents\\data\\FROG Traces"))
        self.label_16.setText(_translate("MainWindow", "Base Name"))
        self.in_specbasename.setText(_translate("MainWindow", "frog_trace"))
        self.label_5.setText(_translate("MainWindow", "Thorlabs Exposure Time"))
        self.label_3.setText(_translate("MainWindow", "Thorlabs Settings"))
        self.c_subbkg.setText(_translate("MainWindow", "Subtract Bkg"))
        self.c_darkcounts.setText(_translate("MainWindow", "Dark Counts"))
        self.c_calibration.setText(_translate("MainWindow", "Calibration"))
        self.ConnectThorlabs.setText(_translate("MainWindow", "Connect Spec"))
        self.p_loadspec.setText(_translate("MainWindow", "Load Spectrum"))
        self.p_loadbkg.setText(_translate("MainWindow", "Load Background"))
        self.p_savespec.setText(_translate("MainWindow", "Save Spectrum"))
        self.p_takebkg.setText(_translate("MainWindow", "Take Background"))
        self.in_groupname.setItemText(0, _translate("MainWindow", "FROG"))
        self.label_13.setText(_translate("MainWindow", "IP Address"))
        self.in_actip.setText(_translate("MainWindow", "FROG"))
        self.label_12.setText(_translate("MainWindow", "Status"))
        self.label_10.setText(_translate("MainWindow", "Group Name"))
        self.label_23.setText(_translate("MainWindow", "Maximum Travel (mm)"))
        self.in_actmaxlim.setText(_translate("MainWindow", "10"))
        self.label_46.setText(_translate("MainWindow", "Minimum Travel (mm)"))
        self.in_actminlim_2.setText(_translate("MainWindow", "0"))
        self.p_actsetlim.setText(_translate("MainWindow", "Update\n"
" Limits"))
        self.p_actinit.setText(_translate("MainWindow", "Initialize"))
        self.p_acthome.setText(_translate("MainWindow", "Home"))
        self.p_actenable.setText(_translate("MainWindow", "Enable/Disable"))
        self.ConnectXPS.setText(_translate("MainWindow", "Connect XPS"))
        self.ControlTab.setTabText(self.ControlTab.indexOf(self.tab_Setup), _translate("MainWindow", "Hardware Setup"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
from mplcanvas import MplCanvas
from pyqtgraph import GraphicsLayoutWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
