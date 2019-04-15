# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\device_view.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DeviceView(object):
    def setupUi(self, DeviceView):
        DeviceView.setObjectName("DeviceView")
        DeviceView.resize(1600, 775)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DeviceView.sizePolicy().hasHeightForWidth())
        DeviceView.setSizePolicy(sizePolicy)
        DeviceView.setMinimumSize(QtCore.QSize(1600, 775))
        DeviceView.setMaximumSize(QtCore.QSize(1600, 775))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        DeviceView.setFont(font)
        self.gridLayoutWidget = QtWidgets.QWidget(DeviceView)
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

        self.retranslateUi(DeviceView)
        QtCore.QMetaObject.connectSlotsByName(DeviceView)

    def retranslateUi(self, DeviceView):
        _translate = QtCore.QCoreApplication.translate
        DeviceView.setWindowTitle(_translate("DeviceView", "Form"))
        self.label.setText(_translate("DeviceView", "Device"))

