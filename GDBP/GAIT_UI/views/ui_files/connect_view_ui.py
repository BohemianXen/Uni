# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\connect_view.ui'
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
        self.gridLayoutWidget = QtWidgets.QWidget(ConnectView)
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

        self.retranslateUi(ConnectView)
        QtCore.QMetaObject.connectSlotsByName(ConnectView)

    def retranslateUi(self, ConnectView):
        _translate = QtCore.QCoreApplication.translate
        ConnectView.setWindowTitle(_translate("ConnectView", "Form"))
        self.label.setText(_translate("ConnectView", "Connect"))

