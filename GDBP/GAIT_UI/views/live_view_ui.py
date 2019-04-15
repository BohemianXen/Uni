# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\live_view.ui'
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
        self.gridLayoutWidget = QtWidgets.QWidget(LiveView)
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

        self.retranslateUi(LiveView)
        QtCore.QMetaObject.connectSlotsByName(LiveView)

    def retranslateUi(self, LiveView):
        _translate = QtCore.QCoreApplication.translate
        LiveView.setWindowTitle(_translate("LiveView", "Form"))
        self.label.setText(_translate("LiveView", "Live View"))

