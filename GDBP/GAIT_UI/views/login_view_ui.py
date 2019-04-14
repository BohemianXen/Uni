# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_view.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginView(object):
    def setupUi(self, LoginView):
        LoginView.setObjectName("LoginView")
        LoginView.resize(1600, 775)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoginView.sizePolicy().hasHeightForWidth())
        LoginView.setSizePolicy(sizePolicy)
        LoginView.setMinimumSize(QtCore.QSize(1600, 775))
        LoginView.setMaximumSize(QtCore.QSize(1600, 775))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        LoginView.setFont(font)
        self.gridLayoutWidget = QtWidgets.QWidget(LoginView)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1351, 1111))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.page_name = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.page_name.setFont(font)
        self.page_name.setAlignment(QtCore.Qt.AlignCenter)
        self.page_name.setObjectName("page_name")
        self.gridLayout_2.addWidget(self.page_name, 0, 0, 1, 1)

        self.retranslateUi(LoginView)
        QtCore.QMetaObject.connectSlotsByName(LoginView)

    def retranslateUi(self, LoginView):
        _translate = QtCore.QCoreApplication.translate
        LoginView.setWindowTitle(_translate("LoginView", "Form"))
        self.page_name.setText(_translate("LoginView", "Login"))

