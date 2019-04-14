# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'home_view.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HomeView(object):
    def setupUi(self, HomeView):
        HomeView.setObjectName("HomeView")
        HomeView.resize(1600, 775)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HomeView.sizePolicy().hasHeightForWidth())
        HomeView.setSizePolicy(sizePolicy)
        HomeView.setMinimumSize(QtCore.QSize(1600, 775))
        HomeView.setMaximumSize(QtCore.QSize(1600, 775))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        HomeView.setFont(font)
        self.gridLayoutWidget = QtWidgets.QWidget(HomeView)
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

        self.retranslateUi(HomeView)
        QtCore.QMetaObject.connectSlotsByName(HomeView)

    def retranslateUi(self, HomeView):
        _translate = QtCore.QCoreApplication.translate
        HomeView.setWindowTitle(_translate("HomeView", "Form"))
        self.page_name.setText(_translate("HomeView", "Home"))

