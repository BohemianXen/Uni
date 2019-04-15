# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\account_view.ui'
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
        self.gridLayoutWidget = QtWidgets.QWidget(AccountView)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 20, 1601, 751))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)

        self.retranslateUi(AccountView)
        QtCore.QMetaObject.connectSlotsByName(AccountView)

    def retranslateUi(self, AccountView):
        _translate = QtCore.QCoreApplication.translate
        AccountView.setWindowTitle(_translate("AccountView", "Form"))
        self.label.setText(_translate("AccountView", "Account"))

