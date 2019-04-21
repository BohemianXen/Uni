# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'live_view.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LiveView(object):
    def setupUi(self, LiveView):
        LiveView.setObjectName("LiveView")
        LiveView.resize(1600, 775)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LiveView.sizePolicy().hasHeightForWidth())
        LiveView.setSizePolicy(sizePolicy)
        LiveView.setMinimumSize(QtCore.QSize(1600, 775))
        LiveView.setMaximumSize(QtCore.QSize(1600, 775))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        LiveView.setFont(font)
        self.liveStackedWidget = QtWidgets.QStackedWidget(LiveView)
        self.liveStackedWidget.setGeometry(QtCore.QRect(0, 0, 1601, 771))
        self.liveStackedWidget.setObjectName("liveStackedWidget")
        self.defaultView = QtWidgets.QWidget()
        self.defaultView.setObjectName("defaultView")
        self.gridLayoutWidget = QtWidgets.QWidget(self.defaultView)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1601, 771))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.defaultLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.defaultLabel.setFont(font)
        self.defaultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.defaultLabel.setObjectName("defaultLabel")
        self.gridLayout.addWidget(self.defaultLabel, 0, 0, 1, 1)
        self.liveStackedWidget.addWidget(self.defaultView)
        self.connectedView = QtWidgets.QWidget()
        self.connectedView.setObjectName("connectedView")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.connectedView)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1618, 771))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.connectGridLayout = QtWidgets.QGridLayout()
        self.connectGridLayout.setObjectName("connectGridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.pushButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(150, 75))
        self.pushButton.setMaximumSize(QtCore.QSize(150, 75))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.connectGridLayout.addWidget(self.pushButton, 6, 2, 1, 1, QtCore.Qt.AlignHCenter)
        spacerItem1 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem2, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem3, 1, 3, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem4, 5, 2, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem5, 6, 3, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.connectGridLayout.addItem(spacerItem6, 4, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(400, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.connectGridLayout.addItem(spacerItem7, 4, 3, 2, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem8, 1, 0, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem9, 3, 3, 1, 1)
        self.searchButton = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMinimumSize(QtCore.QSize(150, 75))
        self.searchButton.setMaximumSize(QtCore.QSize(150, 75))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.searchButton.setFont(font)
        self.searchButton.setObjectName("searchButton")
        self.connectGridLayout.addWidget(self.searchButton, 1, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.devicesListWidget = QtWidgets.QListWidget(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.devicesListWidget.sizePolicy().hasHeightForWidth())
        self.devicesListWidget.setSizePolicy(sizePolicy)
        self.devicesListWidget.setMinimumSize(QtCore.QSize(800, 300))
        self.devicesListWidget.setMaximumSize(QtCore.QSize(800, 400))
        self.devicesListWidget.setStyleSheet("QListWidget { \n"
"    background-color: rgb(39, 39, 52); \n"
"    alternate-background-color: rgb(29, 29, 42);\n"
"    selection-background-color: rgb(90, 90, 121); \n"
"    border: 2px solid rgb(188, 188, 188);\n"
"}\n"
"\n"
"QListWidget::item { \n"
"    qproperty-alignment: AlignHCenter; \n"
"    color: white; \n"
"}\n"
"\n"
"QListWidget::item::hover {background-color: rgb(90, 90, 121); }")
        self.devicesListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.devicesListWidget.setTabKeyNavigation(True)
        self.devicesListWidget.setAlternatingRowColors(True)
        self.devicesListWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.devicesListWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.devicesListWidget.setObjectName("devicesListWidget")
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.devicesListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.devicesListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.devicesListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.devicesListWidget.addItem(item)
        self.connectGridLayout.addWidget(self.devicesListWidget, 4, 2, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem10, 3, 0, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem11, 3, 2, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem12, 5, 0, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem13, 6, 0, 1, 1)
        spacerItem14 = QtWidgets.QSpacerItem(400, 120, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem14, 7, 2, 1, 1)
        spacerItem15 = QtWidgets.QSpacerItem(400, 120, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem15, 7, 0, 1, 1)
        spacerItem16 = QtWidgets.QSpacerItem(400, 120, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem16, 7, 3, 1, 1)
        self.gridLayout_2.addLayout(self.connectGridLayout, 0, 0, 1, 1)
        self.liveStackedWidget.addWidget(self.connectedView)

        self.retranslateUi(LiveView)
        QtCore.QMetaObject.connectSlotsByName(LiveView)

    def retranslateUi(self, LiveView):
        _translate = QtCore.QCoreApplication.translate
        LiveView.setWindowTitle(_translate("LiveView", "Form"))
        self.defaultLabel.setText(_translate("LiveView", "Please connect to a GAIT device to view live data"))
        self.pushButton.setText(_translate("LiveView", "Connect"))
        self.searchButton.setText(_translate("LiveView", "Search"))
        __sortingEnabled = self.devicesListWidget.isSortingEnabled()
        self.devicesListWidget.setSortingEnabled(False)
        item = self.devicesListWidget.item(0)
        item.setText(_translate("LiveView", "device1"))
        item = self.devicesListWidget.item(1)
        item.setText(_translate("LiveView", "device2"))
        item = self.devicesListWidget.item(2)
        item.setText(_translate("LiveView", "device3"))
        item = self.devicesListWidget.item(3)
        item.setText(_translate("LiveView", "device4"))
        self.devicesListWidget.setSortingEnabled(__sortingEnabled)
