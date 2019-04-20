# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'device_view.ui'
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
        self.layoutWidget = QtWidgets.QWidget(DeviceView)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1601, 771))
        self.layoutWidget.setObjectName("layoutWidget")
        self.deviceGridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.deviceGridLayout.setContentsMargins(0, 0, 0, 0)
        self.deviceGridLayout.setObjectName("deviceGridLayout")

        self.retranslateUi(DeviceView)
        QtCore.QMetaObject.connectSlotsByName(DeviceView)

    def retranslateUi(self, DeviceView):
        _translate = QtCore.QCoreApplication.translate
        DeviceView.setWindowTitle(_translate("DeviceView", "Form"))

