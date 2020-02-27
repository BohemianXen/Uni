# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_view.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
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
"\n"
"/*QTabWidget>QWidget { background-color: rgb(90, 90, 121); } */")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        self.centralwidget.setFont(font)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1601, 781))
        self.tabWidget.setStyleSheet("QTabBar::tab { color: white; padding: 8px; border-right: 1px solid gray; \n"
"min-width: 120px;} \n"
"\n"
"QTabBar::tab:!selected { background-color: rgb(112, 112, 112); margin-top: 2px}\n"
"\n"
"QTabBar::tab:selected,  QTabBar::tab:hover { background-color: rgb(90, 90, 121); }\n"
"\n"
"QTabWidget::pane { border: 0px}")
        self.tabWidget.setObjectName("tabWidget")
        self.configTab = QtWidgets.QWidget()
        self.configTab.setObjectName("configTab")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.configTab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1616, 751))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.configGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.configGridLayout.setContentsMargins(0, 0, 0, 0)
        self.configGridLayout.setObjectName("configGridLayout")
        self.tabWidget.addTab(self.configTab, "")
        self.plotTab = QtWidgets.QWidget()
        self.plotTab.setObjectName("plotTab")
        self.gridLayoutWidget = QtWidgets.QWidget(self.plotTab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1616, 751))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.plotGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.plotGridLayout.setContentsMargins(0, 0, 0, 0)
        self.plotGridLayout.setObjectName("plotGridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.plotGridLayout.addItem(spacerItem, 1, 0, 3, 1)
        self.accPlot = PlotWidget(self.gridLayoutWidget)
        self.accPlot.setMinimumSize(QtCore.QSize(1200, 229))
        self.accPlot.setMaximumSize(QtCore.QSize(1200, 229))
        self.accPlot.setObjectName("accPlot")
        self.plotGridLayout.addWidget(self.accPlot, 1, 3, 1, 1)
        self.filePushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.filePushButton.setMinimumSize(QtCore.QSize(280, 50))
        self.filePushButton.setMaximumSize(QtCore.QSize(280, 100))
        self.filePushButton.setObjectName("filePushButton")
        self.plotGridLayout.addWidget(self.filePushButton, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.plotGridLayout.addItem(spacerItem1, 0, 0, 1, 6)
        self.gyroPlot = PlotWidget(self.gridLayoutWidget)
        self.gyroPlot.setMinimumSize(QtCore.QSize(1200, 229))
        self.gyroPlot.setMaximumSize(QtCore.QSize(1200, 229))
        self.gyroPlot.setObjectName("gyroPlot")
        self.plotGridLayout.addWidget(self.gyroPlot, 2, 3, 1, 1)
        self.fileLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.fileLabel.setMinimumSize(QtCore.QSize(280, 50))
        self.fileLabel.setMaximumSize(QtCore.QSize(280, 16777215))
        self.fileLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fileLabel.setObjectName("fileLabel")
        self.plotGridLayout.addWidget(self.fileLabel, 2, 1, 1, 1)
        self.plotPushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.plotPushButton.setEnabled(False)
        self.plotPushButton.setMinimumSize(QtCore.QSize(280, 50))
        self.plotPushButton.setMaximumSize(QtCore.QSize(280, 100))
        self.plotPushButton.setObjectName("plotPushButton")
        self.plotGridLayout.addWidget(self.plotPushButton, 3, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.plotGridLayout.addItem(spacerItem2, 1, 4, 3, 2)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.plotGridLayout.addItem(spacerItem3, 1, 2, 3, 1)
        self.magPlot = PlotWidget(self.gridLayoutWidget)
        self.magPlot.setMinimumSize(QtCore.QSize(1200, 229))
        self.magPlot.setMaximumSize(QtCore.QSize(1200, 229))
        self.magPlot.setObjectName("magPlot")
        self.plotGridLayout.addWidget(self.magPlot, 3, 3, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.plotGridLayout.addItem(spacerItem4, 4, 0, 1, 6)
        self.tabWidget.addTab(self.plotTab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FallDetector Config"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.configTab), _translate("MainWindow", "Configure"))
        self.filePushButton.setText(_translate("MainWindow", "Select File"))
        self.fileLabel.setText(_translate("MainWindow", "No File Selected"))
        self.plotPushButton.setText(_translate("MainWindow", "Plot"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plotTab), _translate("MainWindow", "Plot"))
from pyqtgraph import PlotWidget
import resources_rc
