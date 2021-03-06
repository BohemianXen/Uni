# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\main_view.ui'
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
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 1601, 781))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.gridLayoutWidget_3)
        self.tabWidget.setStyleSheet("QTabBar::tab { color: white; padding: 8px; border-right: 1px solid gray; \n"
"min-width: 120px;} \n"
"\n"
"QTabBar::tab:!selected { background-color: rgb(112, 112, 112); margin-top: 2px}\n"
"\n"
"QTabBar::tab:selected,  QTabBar::tab:hover { background-color: rgb(90, 90, 121); }\n"
"\n"
"QTabWidget::pane { border: 0px}")
        self.tabWidget.setObjectName("tabWidget")
        self.liveTab = QtWidgets.QWidget()
        self.liveTab.setStyleSheet("QGroupBox {color: rgb(188, 188, 188); }\n"
"\n"
"QTextEdit {background-color: rgb(39, 39, 52); color: white}")
        self.liveTab.setObjectName("liveTab")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.liveTab)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1551, 749))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.liveGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.liveGridLayout.setContentsMargins(0, 0, 0, 0)
        self.liveGridLayout.setObjectName("liveGridLayout")
        self.liveGroupBox = QtWidgets.QGroupBox(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.liveGroupBox.sizePolicy().hasHeightForWidth())
        self.liveGroupBox.setSizePolicy(sizePolicy)
        self.liveGroupBox.setMinimumSize(QtCore.QSize(420, 420))
        self.liveGroupBox.setMaximumSize(QtCore.QSize(420, 420))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.liveGroupBox.setFont(font)
        self.liveGroupBox.setObjectName("liveGroupBox")
        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.liveGroupBox)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(0, 50, 411, 381))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.liveGroupGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.liveGroupGridLayout.setContentsMargins(0, 0, 0, 0)
        self.liveGroupGridLayout.setObjectName("liveGroupGridLayout")
        self.modelLabel = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.modelLabel.setMinimumSize(QtCore.QSize(280, 50))
        self.modelLabel.setMaximumSize(QtCore.QSize(280, 16777215))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.modelLabel.setFont(font)
        self.modelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.modelLabel.setObjectName("modelLabel")
        self.liveGroupGridLayout.addWidget(self.modelLabel, 1, 0, 1, 1)
        self.modelPushButton = QtWidgets.QPushButton(self.gridLayoutWidget_4)
        self.modelPushButton.setEnabled(True)
        self.modelPushButton.setMinimumSize(QtCore.QSize(280, 50))
        self.modelPushButton.setMaximumSize(QtCore.QSize(280, 100))
        self.modelPushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.modelPushButton.setObjectName("modelPushButton")
        self.liveGroupGridLayout.addWidget(self.modelPushButton, 0, 0, 1, 1)
        self.actionLabel = QtWidgets.QLabel(self.gridLayoutWidget_4)
        self.actionLabel.setMinimumSize(QtCore.QSize(280, 50))
        self.actionLabel.setMaximumSize(QtCore.QSize(280, 16777215))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.actionLabel.setFont(font)
        self.actionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.actionLabel.setObjectName("actionLabel")
        self.liveGroupGridLayout.addWidget(self.actionLabel, 2, 0, 1, 1)
        self.liveGridLayout.addWidget(self.liveGroupBox, 8, 1, 1, 3)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.liveGridLayout.addItem(spacerItem, 10, 0, 1, 7)
        self.progressBar = QtWidgets.QProgressBar(self.gridLayoutWidget_2)
        self.progressBar.setEnabled(True)
        self.progressBar.setMaximumSize(QtCore.QSize(300, 16777215))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName("progressBar")
        self.liveGridLayout.addWidget(self.progressBar, 6, 2, 1, 1)
        self.connectPushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.connectPushButton.setEnabled(True)
        self.connectPushButton.setMinimumSize(QtCore.QSize(300, 100))
        self.connectPushButton.setMaximumSize(QtCore.QSize(300, 100))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.connectPushButton.setFont(font)
        self.connectPushButton.setObjectName("connectPushButton")
        self.liveGridLayout.addWidget(self.connectPushButton, 3, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.liveGridLayout.addItem(spacerItem1, 4, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.liveGridLayout.addItem(spacerItem2, 3, 1, 4, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.liveGridLayout.addItem(spacerItem3, 3, 3, 4, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.liveGridLayout.addItem(spacerItem4, 0, 0, 1, 7)
        self.recordPushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.recordPushButton.setEnabled(False)
        self.recordPushButton.setMinimumSize(QtCore.QSize(300, 100))
        self.recordPushButton.setMaximumSize(QtCore.QSize(300, 100))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.recordPushButton.setFont(font)
        self.recordPushButton.setObjectName("recordPushButton")
        self.liveGridLayout.addWidget(self.recordPushButton, 5, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.liveGridLayout.addItem(spacerItem5, 3, 0, 7, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.liveGridLayout.addItem(spacerItem6, 7, 1, 1, 3)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.liveGridLayout.addItem(spacerItem7, 3, 4, 7, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.liveGridLayout.addItem(spacerItem8, 1, 0, 2, 5)
        self.consoleTextEdit = QtWidgets.QTextEdit(self.gridLayoutWidget_2)
        self.consoleTextEdit.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.consoleTextEdit.setReadOnly(True)
        self.consoleTextEdit.setObjectName("consoleTextEdit")
        self.liveGridLayout.addWidget(self.consoleTextEdit, 1, 5, 9, 1)
        spacerItem9 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.liveGridLayout.addItem(spacerItem9, 1, 6, 9, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.liveGridLayout.addItem(spacerItem10, 9, 1, 1, 3)
        self.tabWidget.addTab(self.liveTab, "")
        self.plotTab = QtWidgets.QWidget()
        self.plotTab.setObjectName("plotTab")
        self.gridLayoutWidget = QtWidgets.QWidget(self.plotTab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1616, 751))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.plotGridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.plotGridLayout.setContentsMargins(0, 0, 0, 0)
        self.plotGridLayout.setObjectName("plotGridLayout")
        spacerItem11 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.plotGridLayout.addItem(spacerItem11, 1, 0, 3, 1)
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
        spacerItem12 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.plotGridLayout.addItem(spacerItem12, 1, 4, 3, 2)
        spacerItem13 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.plotGridLayout.addItem(spacerItem13, 4, 0, 1, 6)
        spacerItem14 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.plotGridLayout.addItem(spacerItem14, 0, 0, 1, 6)
        self.plotPushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.plotPushButton.setEnabled(False)
        self.plotPushButton.setMinimumSize(QtCore.QSize(280, 50))
        self.plotPushButton.setMaximumSize(QtCore.QSize(280, 100))
        self.plotPushButton.setObjectName("plotPushButton")
        self.plotGridLayout.addWidget(self.plotPushButton, 3, 1, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.plotGridLayout.addItem(spacerItem15, 1, 2, 3, 1)
        self.fileLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.fileLabel.setMinimumSize(QtCore.QSize(280, 50))
        self.fileLabel.setMaximumSize(QtCore.QSize(280, 16777215))
        self.fileLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fileLabel.setObjectName("fileLabel")
        self.plotGridLayout.addWidget(self.fileLabel, 2, 1, 1, 1)
        self.gyroPlot = PlotWidget(self.gridLayoutWidget)
        self.gyroPlot.setMinimumSize(QtCore.QSize(1200, 229))
        self.gyroPlot.setMaximumSize(QtCore.QSize(1200, 229))
        self.gyroPlot.setObjectName("gyroPlot")
        self.plotGridLayout.addWidget(self.gyroPlot, 2, 3, 1, 1)
        self.magPlot = PlotWidget(self.gridLayoutWidget)
        self.magPlot.setMinimumSize(QtCore.QSize(1200, 229))
        self.magPlot.setMaximumSize(QtCore.QSize(1200, 229))
        self.magPlot.setObjectName("magPlot")
        self.plotGridLayout.addWidget(self.magPlot, 3, 3, 1, 1)
        self.tabWidget.addTab(self.plotTab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FallDetector Config"))
        self.liveGroupBox.setTitle(_translate("MainWindow", "Deep Learning"))
        self.modelLabel.setText(_translate("MainWindow", "No Model Selected"))
        self.modelPushButton.setText(_translate("MainWindow", "Select Model"))
        self.actionLabel.setText(_translate("MainWindow", "STANDING"))
        self.connectPushButton.setText(_translate("MainWindow", "Connect"))
        self.recordPushButton.setText(_translate("MainWindow", "Record"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.liveTab), _translate("MainWindow", "Live"))
        self.filePushButton.setText(_translate("MainWindow", "Select File"))
        self.plotPushButton.setText(_translate("MainWindow", "Plot"))
        self.fileLabel.setText(_translate("MainWindow", "No File Selected"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.plotTab), _translate("MainWindow", "Plot"))
from pyqtgraph import PlotWidget
import resources_rc
