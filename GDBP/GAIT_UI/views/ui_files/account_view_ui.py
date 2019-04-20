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
        self.layoutWidget = QtWidgets.QWidget(AccountView)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1601, 771))
        self.layoutWidget.setObjectName("layoutWidget")
        self.accountGridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.accountGridLayout.setContentsMargins(0, 0, 0, 0)
        self.accountGridLayout.setObjectName("accountGridLayout")

        self.retranslateUi(AccountView)
        QtCore.QMetaObject.connectSlotsByName(AccountView)

    def retranslateUi(self, AccountView):
        _translate = QtCore.QCoreApplication.translate
        AccountView.setWindowTitle(_translate("AccountView", "Form"))

