# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_view.ui'
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
        MainWindow.setStyleSheet("QMainWindow { background-color: qlineargradient(x1: 0, y1: 0, x2: 0.9, y2: 0.8,\n"
"                                stop: 0 rgb(39, 39, 52), stop: 1 rgb(90, 90, 121)); }\n"
"\n"
"QStatusBar { background-color: rgb(29, 29, 42); }\n"
"")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.mainStackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.mainStackedWidget.setGeometry(QtCore.QRect(0, 0, 1601, 771))
        self.mainStackedWidget.setStyleSheet("QStackedWidget > QWidget { \n"
"    background-color: qlineargradient(x1: 0, y1: 0, x2: 0.9, y2: 0.8,\n"
"                                stop: 0 rgb(39, 39, 52), stop: 1 rgb(90, 90, 121));\n"
"}\n"
"\n"
"QPushButton { color: white; background-color: rgb(90, 90, 121) }\n"
"\n"
"QLabel { color: rgb(188, 188, 188); }\n"
"\n"
"QComboBox {background-color: rgb(49, 49, 62); color: rgb(188, 188, 188)}")
        self.mainStackedWidget.setObjectName("mainStackedWidget")
        self.splashPage = QtWidgets.QWidget()
        self.splashPage.setObjectName("splashPage")
        self.mainStackedWidget.addWidget(self.splashPage)
        self.loggedInView = QtWidgets.QWidget()
        self.loggedInView.setObjectName("loggedInView")
        self.viewsTabWidget = QtWidgets.QTabWidget(self.loggedInView)
        self.viewsTabWidget.setEnabled(True)
        self.viewsTabWidget.setGeometry(QtCore.QRect(0, 0, 1610, 775))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewsTabWidget.sizePolicy().hasHeightForWidth())
        self.viewsTabWidget.setSizePolicy(sizePolicy)
        self.viewsTabWidget.setMinimumSize(QtCore.QSize(1610, 775))
        self.viewsTabWidget.setMaximumSize(QtCore.QSize(1610, 775))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.viewsTabWidget.setFont(font)
        self.viewsTabWidget.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.viewsTabWidget.setAutoFillBackground(False)
        self.viewsTabWidget.setStyleSheet("QTabBar::tab { color: white; padding: 12px; border-right: 1px solid gray; \n"
"min-width: 120px;} \n"
"\n"
"QTabBar::tab:!selected { background-color: rgb(112, 112, 112); margin-top: 2px}\n"
"\n"
"QTabBar::tab:selected,  QTabBar::tab:hover { background-color: rgb(90, 90, 121); }\n"
"\n"
"QTabWidget::pane { border: 0px}")
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
        self.liveTab.setEnabled(True)
        self.liveTab.setObjectName("liveTab")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.liveTab)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 1611, 751))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.liveGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.liveGridLayout.setContentsMargins(0, 0, 0, 0)
        self.liveGridLayout.setObjectName("liveGridLayout")
        self.viewsTabWidget.addTab(self.liveTab, "")
        self.uploadTab = QtWidgets.QWidget()
        self.uploadTab.setEnabled(True)
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
        self.gridLayoutWidget_6.setGeometry(QtCore.QRect(-20, 0, 1631, 751))
        self.gridLayoutWidget_6.setObjectName("gridLayoutWidget_6")
        self.deviceGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_6)
        self.deviceGridLayout.setContentsMargins(0, 0, 0, 0)
        self.deviceGridLayout.setObjectName("deviceGridLayout")
        self.viewsTabWidget.addTab(self.deviceTab, "")
        self.accountTab = QtWidgets.QWidget()
        self.accountTab.setObjectName("accountTab")
        self.gridLayoutWidget_7 = QtWidgets.QWidget(self.accountTab)
        self.gridLayoutWidget_7.setGeometry(QtCore.QRect(-20, 0, 1631, 751))
        self.gridLayoutWidget_7.setObjectName("gridLayoutWidget_7")
        self.accountGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_7)
        self.accountGridLayout.setContentsMargins(0, 0, 0, 0)
        self.accountGridLayout.setObjectName("accountGridLayout")
        self.viewsTabWidget.addTab(self.accountTab, "")
        self.mainStackedWidget.addWidget(self.loggedInView)
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
