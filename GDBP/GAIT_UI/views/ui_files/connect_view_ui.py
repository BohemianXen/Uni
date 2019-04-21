# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connect_view.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConnectView(object):
    def setupUi(self, ConnectView):
        ConnectView.setObjectName("ConnectView")
        ConnectView.resize(1600, 775)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ConnectView.sizePolicy().hasHeightForWidth())
        ConnectView.setSizePolicy(sizePolicy)
        ConnectView.setMinimumSize(QtCore.QSize(1600, 775))
        ConnectView.setMaximumSize(QtCore.QSize(1600, 775))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        ConnectView.setFont(font)
        self.layoutWidget = QtWidgets.QWidget(ConnectView)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1616, 771))
        self.layoutWidget.setObjectName("layoutWidget")
        self.connectGridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.connectGridLayout.setContentsMargins(0, 0, 0, 0)
        self.connectGridLayout.setObjectName("connectGridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.connectGridLayout.addItem(spacerItem, 6, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(400, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(400, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem2, 1, 4, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 75, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.connectGridLayout.addItem(spacerItem3, 6, 0, 1, 1)
        self.searchButton = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchButton.sizePolicy().hasHeightForWidth())
        self.searchButton.setSizePolicy(sizePolicy)
        self.searchButton.setMinimumSize(QtCore.QSize(250, 100))
        self.searchButton.setMaximumSize(QtCore.QSize(250, 100))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.searchButton.setFont(font)
        self.searchButton.setObjectName("searchButton")
        self.connectGridLayout.addWidget(self.searchButton, 6, 1, 1, 1, QtCore.Qt.AlignRight)
        self.connectButton = QtWidgets.QPushButton(self.layoutWidget)
        self.connectButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.connectButton.sizePolicy().hasHeightForWidth())
        self.connectButton.setSizePolicy(sizePolicy)
        self.connectButton.setMinimumSize(QtCore.QSize(250, 100))
        self.connectButton.setMaximumSize(QtCore.QSize(250, 100))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.connectButton.setFont(font)
        self.connectButton.setObjectName("connectButton")
        self.connectGridLayout.addWidget(self.connectButton, 6, 3, 1, 1, QtCore.Qt.AlignLeft)
        self.instructionsLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.instructionsLabel.setFont(font)
        self.instructionsLabel.setObjectName("instructionsLabel")
        self.connectGridLayout.addWidget(self.instructionsLabel, 1, 1, 1, 3, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignBottom)
        spacerItem4 = QtWidgets.QSpacerItem(400, 300, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.connectGridLayout.addItem(spacerItem4, 4, 4, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 75, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.connectGridLayout.addItem(spacerItem5, 6, 2, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(400, 300, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.connectGridLayout.addItem(spacerItem6, 4, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem7, 5, 0, 1, 5)
        spacerItem8 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem8, 3, 0, 1, 5)
        spacerItem9 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.connectGridLayout.addItem(spacerItem9, 0, 0, 1, 5)
        spacerItem10 = QtWidgets.QSpacerItem(400, 120, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.connectGridLayout.addItem(spacerItem10, 7, 0, 1, 5)
        self.devicesListWidget = QtWidgets.QListWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.devicesListWidget.sizePolicy().hasHeightForWidth())
        self.devicesListWidget.setSizePolicy(sizePolicy)
        self.devicesListWidget.setMinimumSize(QtCore.QSize(800, 300))
        self.devicesListWidget.setMaximumSize(QtCore.QSize(800, 300))
        self.devicesListWidget.setStyleSheet("QListWidget { \n"
"    background-color: rgb(69, 69, 82); \n"
"    alternate-background-color: rgb(39, 39, 52);\n"
"    selection-background-color: rgb(90, 90, 121); \n"
"    border: 2px double rgb(188, 188, 188);\n"
"    border-radius: 8px;\n"
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
        item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.devicesListWidget.addItem(item)
        self.connectGridLayout.addWidget(self.devicesListWidget, 4, 1, 1, 3)

        self.retranslateUi(ConnectView)
        QtCore.QMetaObject.connectSlotsByName(ConnectView)
        ConnectView.setTabOrder(self.searchButton, self.devicesListWidget)
        ConnectView.setTabOrder(self.devicesListWidget, self.connectButton)

    def retranslateUi(self, ConnectView):
        _translate = QtCore.QCoreApplication.translate
        ConnectView.setWindowTitle(_translate("ConnectView", "Form"))
        self.searchButton.setText(_translate("ConnectView", "Search"))
        self.connectButton.setText(_translate("ConnectView", "Connect"))
        self.instructionsLabel.setText(_translate("ConnectView", "Search for a GAIT device, select it in the list below and click Connect "))
        __sortingEnabled = self.devicesListWidget.isSortingEnabled()
        self.devicesListWidget.setSortingEnabled(False)
        item = self.devicesListWidget.item(0)
        item.setText(_translate("ConnectView", "No devices found"))
        self.devicesListWidget.setSortingEnabled(__sortingEnabled)

