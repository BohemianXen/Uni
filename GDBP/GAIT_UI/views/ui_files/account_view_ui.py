# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'account_view.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AccountView(object):
    def setupUi(self, AccountView):
        AccountView.setObjectName("AccountView")
        AccountView.resize(1600, 775)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AccountView.sizePolicy().hasHeightForWidth())
        AccountView.setSizePolicy(sizePolicy)
        AccountView.setMinimumSize(QtCore.QSize(1600, 775))
        AccountView.setMaximumSize(QtCore.QSize(1600, 775))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        AccountView.setFont(font)
        AccountView.setStyleSheet("QListWidget { \n"
"    background-color: rgb(69, 69, 82); \n"
"    alternate-background-color: rgb(39, 39, 52);\n"
"    selection-background-color: rgb(90, 90, 121); \n"
"    border: 0px;\n"
"    border-right: 0px;\n"
"    padding-right: 0px;\n"
"    margin-right: 0px;\n"
"}\n"
"\n"
"QListWidget::item { \n"
"    padding-top: 8px;\n"
"    padding-bottom: 8px;\n"
"    padding-left: 24px;\n"
"    color: white; \n"
"    border-bottom: 2px solid rgb(188, 188, 188);\n"
"}\n"
"\n"
"QListWidget::item:hover { background-color: rgb(90, 90, 121); }\n"
"\n"
"QListWidget::item:selected { background-color: rgb(90, 90, 121); }\n"
"\n"
"QStackedWidget { margin-left: 0px; padding-left: 0px }")
        self.layoutWidget = QtWidgets.QWidget(AccountView)
        self.layoutWidget.setGeometry(QtCore.QRect(-10, 0, 1611, 771))
        self.layoutWidget.setObjectName("layoutWidget")
        self.accountGridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.accountGridLayout.setContentsMargins(0, 0, 0, 0)
        self.accountGridLayout.setObjectName("accountGridLayout")
        self.navigationListWidget = QtWidgets.QListWidget(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navigationListWidget.sizePolicy().hasHeightForWidth())
        self.navigationListWidget.setSizePolicy(sizePolicy)
        self.navigationListWidget.setMinimumSize(QtCore.QSize(305, 0))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(14)
        self.navigationListWidget.setFont(font)
        self.navigationListWidget.setProperty("showDropIndicator", True)
        self.navigationListWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.navigationListWidget.setObjectName("navigationListWidget")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        item.setFont(font)
        self.navigationListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setBackground(brush)
        self.navigationListWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        item.setFont(font)
        self.navigationListWidget.addItem(item)
        self.accountGridLayout.addWidget(self.navigationListWidget, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.accountGridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.stackedWidget = QtWidgets.QStackedWidget(self.layoutWidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.detailsWidget = QtWidgets.QWidget()
        self.detailsWidget.setObjectName("detailsWidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.detailsWidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1291, 751))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.detailsWidget)
        self.calibrationWidget = QtWidgets.QWidget()
        self.calibrationWidget.setObjectName("calibrationWidget")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.calibrationWidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1291, 741))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.stackedWidget.addWidget(self.calibrationWidget)
        self.routeWidget = QtWidgets.QWidget()
        self.routeWidget.setObjectName("routeWidget")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.routeWidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 1291, 731))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.stackedWidget.addWidget(self.routeWidget)
        self.accountGridLayout.addWidget(self.stackedWidget, 0, 1, 1, 1)

        self.retranslateUi(AccountView)
        QtCore.QMetaObject.connectSlotsByName(AccountView)

    def retranslateUi(self, AccountView):
        _translate = QtCore.QCoreApplication.translate
        AccountView.setWindowTitle(_translate("AccountView", "Form"))
        __sortingEnabled = self.navigationListWidget.isSortingEnabled()
        self.navigationListWidget.setSortingEnabled(False)
        item = self.navigationListWidget.item(0)
        item.setText(_translate("AccountView", "My Details"))
        item = self.navigationListWidget.item(1)
        item.setText(_translate("AccountView", "My Goals"))
        item = self.navigationListWidget.item(2)
        item.setText(_translate("AccountView", "Sign Out"))
        self.navigationListWidget.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("AccountView", "Page Under Construction"))

