# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\upload_view.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UploadView(object):
    def setupUi(self, UploadView):
        UploadView.setObjectName("UploadView")
        UploadView.resize(1600, 775)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(UploadView.sizePolicy().hasHeightForWidth())
        UploadView.setSizePolicy(sizePolicy)
        UploadView.setMinimumSize(QtCore.QSize(1600, 775))
        UploadView.setMaximumSize(QtCore.QSize(1600, 775))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        UploadView.setFont(font)
        self.gridLayoutWidget = QtWidgets.QWidget(UploadView)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 20, 1601, 751))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)

        self.retranslateUi(UploadView)
        QtCore.QMetaObject.connectSlotsByName(UploadView)

    def retranslateUi(self, UploadView):
        _translate = QtCore.QCoreApplication.translate
        UploadView.setWindowTitle(_translate("UploadView", "Form"))
        self.label.setText(_translate("UploadView", "Upload"))

