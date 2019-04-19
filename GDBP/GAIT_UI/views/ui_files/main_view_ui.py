# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_view.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1600, 800))
        MainWindow.setMaximumSize(QtCore.QSize(1600, 800))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/small logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMainWindow { background-color: rgb(29, 29, 42); }\n"
"\n"
"QMainWindow > QWidget { background-color: rgb(29, 29, 42); }\n"
"")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1612, 781))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.mainGridLayout = QtWidgets.QGridLayout(self.verticalLayoutWidget)
        self.mainGridLayout.setContentsMargins(0, 0, 0, 0)
        self.mainGridLayout.setObjectName("mainGridLayout")
        self.viewsTabWidget = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.viewsTabWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewsTabWidget.sizePolicy().hasHeightForWidth())
        self.viewsTabWidget.setSizePolicy(sizePolicy)
        self.viewsTabWidget.setMinimumSize(QtCore.QSize(1610, 775))
        self.viewsTabWidget.setMaximumSize(QtCore.QSize(1610, 775))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.viewsTabWidget.setFont(font)
        self.viewsTabWidget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.viewsTabWidget.setAutoFillBackground(False)
        self.viewsTabWidget.setStyleSheet("QWidget > QWidget { \n"
"    /*background: qlineargradient(x1: 0, y1: 0, x2: 0.9, y2: 0.8,\n"
"                                stop: 0 rgb(39, 39, 52), stop: 1 rgb(90, 90, 121));*/\n"
"    background-color: rgb(75, 75, 90);\n"
"}\n"
"\n"
"QPushButton { color: white; }\n"
"\n"
"QLabel { color: rgb(188, 188, 188); }\n"
"\n"
"QTabBar::tab { color: white; padding: 12px; border-right: 1px solid gray; \n"
"min-width: 100px;} \n"
"\n"
"QTabBar::tab:!selected { background-color: rgb(112, 112, 112); margin-top: 2px}\n"
"\n"
"QTabBar::tab:selected,  QTabBar::tab:hover { background-color: rgb(90, 90, 121); }\n"
"\n"
"\n"
"QTabWidget::pane { \n"
"    border-top: 3px solid white;\n"
"    border-left: 0px;\n"
"    border-right: 0px;\n"
" }")
        self.viewsTabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.viewsTabWidget.setTabBarAutoHide(True)
        self.viewsTabWidget.setObjectName("viewsTabWidget")
        self.homeTab = QtWidgets.QWidget()
        self.homeTab.setAutoFillBackground(False)
        self.homeTab.setStyleSheet("")
        self.homeTab.setObjectName("homeTab")
        self.gridLayoutWidget = QtWidgets.QWidget(self.homeTab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-40, 0, 1651, 741))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.homeGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.homeGridLayout.setContentsMargins(0, 0, 0, 0)
        self.homeGridLayout.setObjectName("homeGridLayout")
        self.viewsTabWidget.addTab(self.homeTab, "")
        self.connectTab = QtWidgets.QWidget()
        self.connectTab.setObjectName("connectTab")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.connectTab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1611, 751))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.connectGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.connectGridLayout.setContentsMargins(0, 0, 0, 0)
        self.connectGridLayout.setObjectName("connectGridLayout")
        self.viewsTabWidget.addTab(self.connectTab, "")
        self.liveTab = QtWidgets.QWidget()
        self.liveTab.setEnabled(False)
        self.liveTab.setObjectName("liveTab")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.liveTab)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 1611, 751))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.liveGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.liveGridLayout.setContentsMargins(0, 0, 0, 0)
        self.liveGridLayout.setObjectName("liveGridLayout")
        self.viewsTabWidget.addTab(self.liveTab, "")
        self.uploadTab = QtWidgets.QWidget()
        self.uploadTab.setEnabled(False)
        self.uploadTab.setObjectName("uploadTab")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.uploadTab)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 1611, 751))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.uploadGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.uploadGridLayout.setContentsMargins(0, 0, 0, 0)
        self.uploadGridLayout.setObjectName("uploadGridLayout")
        self.viewsTabWidget.addTab(self.uploadTab, "")
        self.historyTab = QtWidgets.QWidget()
        self.historyTab.setObjectName("historyTab")
        self.gridLayoutWidget_5 = QtWidgets.QWidget(self.historyTab)
        self.gridLayoutWidget_5.setGeometry(QtCore.QRect(0, 0, 1611, 751))
        self.gridLayoutWidget_5.setObjectName("gridLayoutWidget_5")
        self.historyGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_5)
        self.historyGridLayout.setContentsMargins(0, 0, 0, 0)
        self.historyGridLayout.setObjectName("historyGridLayout")
        self.viewsTabWidget.addTab(self.historyTab, "")
        self.deviceTab = QtWidgets.QWidget()
        self.deviceTab.setObjectName("deviceTab")
        self.gridLayoutWidget_6 = QtWidgets.QWidget(self.deviceTab)
        self.gridLayoutWidget_6.setGeometry(QtCore.QRect(0, 0, 1611, 751))
        self.gridLayoutWidget_6.setObjectName("gridLayoutWidget_6")
        self.deviceGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_6)
        self.deviceGridLayout.setContentsMargins(0, 0, 0, 0)
        self.deviceGridLayout.setObjectName("deviceGridLayout")
        self.viewsTabWidget.addTab(self.deviceTab, "")
        self.accountTab = QtWidgets.QWidget()
        self.accountTab.setObjectName("accountTab")
        self.gridLayoutWidget_7 = QtWidgets.QWidget(self.accountTab)
        self.gridLayoutWidget_7.setGeometry(QtCore.QRect(0, 0, 1611, 751))
        self.gridLayoutWidget_7.setObjectName("gridLayoutWidget_7")
        self.accountGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_7)
        self.accountGridLayout.setContentsMargins(0, 0, 0, 0)
        self.accountGridLayout.setObjectName("accountGridLayout")
        self.viewsTabWidget.addTab(self.accountTab, "")
        self.mainGridLayout.addWidget(self.viewsTabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.viewsTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GAIT Demo App"))
        self.viewsTabWidget.setTabText(self.viewsTabWidget.indexOf(self.homeTab), _translate("MainWindow", "Home"))
        self.viewsTabWidget.setTabText(self.viewsTabWidget.indexOf(self.connectTab), _translate("MainWindow", "Connect"))
        self.viewsTabWidget.setTabText(self.viewsTabWidget.indexOf(self.liveTab), _translate("MainWindow", "Live View"))
        self.viewsTabWidget.setTabText(self.viewsTabWidget.indexOf(self.uploadTab), _translate("MainWindow", "Upload"))
        self.viewsTabWidget.setTabText(self.viewsTabWidget.indexOf(self.historyTab), _translate("MainWindow", "History"))
        self.viewsTabWidget.setTabText(self.viewsTabWidget.indexOf(self.deviceTab), _translate("MainWindow", "My Device"))
        self.viewsTabWidget.setTabText(self.viewsTabWidget.indexOf(self.accountTab), _translate("MainWindow", "My Account"))

import resources_rc
