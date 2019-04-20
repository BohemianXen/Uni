# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'upload_view.ui'
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
        self.uploadStackedWidget = QtWidgets.QStackedWidget(UploadView)
        self.uploadStackedWidget.setGeometry(QtCore.QRect(0, 0, 1601, 771))
        self.uploadStackedWidget.setObjectName("uploadStackedWidget")
        self.defaultView = QtWidgets.QWidget()
        self.defaultView.setObjectName("defaultView")
        self.gridLayoutWidget = QtWidgets.QWidget(self.defaultView)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1601, 771))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.defaultLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.defaultLabel.setFont(font)
        self.defaultLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.defaultLabel.setObjectName("defaultLabel")
        self.gridLayout.addWidget(self.defaultLabel, 0, 0, 1, 1)
        self.uploadStackedWidget.addWidget(self.defaultView)
        self.connectedView = QtWidgets.QWidget()
        self.connectedView.setObjectName("connectedView")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.connectedView)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(0, 0, 1618, 771))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.uploadStackedWidget.addWidget(self.connectedView)

        self.retranslateUi(UploadView)
        QtCore.QMetaObject.connectSlotsByName(UploadView)

    def retranslateUi(self, UploadView):
        _translate = QtCore.QCoreApplication.translate
        UploadView.setWindowTitle(_translate("UploadView", "Form"))
        self.defaultLabel.setText(_translate("UploadView", "Please connect to a GAIT device to upload data"))

