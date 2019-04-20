# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'history_view.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HistoryView(object):
    def setupUi(self, HistoryView):
        HistoryView.setObjectName("HistoryView")
        HistoryView.resize(1600, 775)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(HistoryView.sizePolicy().hasHeightForWidth())
        HistoryView.setSizePolicy(sizePolicy)
        HistoryView.setMinimumSize(QtCore.QSize(1600, 775))
        HistoryView.setMaximumSize(QtCore.QSize(1600, 775))
        font = QtGui.QFont()
        font.setFamily("Tw Cen MT")
        HistoryView.setFont(font)
        self.layoutWidget = QtWidgets.QWidget(HistoryView)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1601, 771))
        self.layoutWidget.setObjectName("layoutWidget")
        self.historyGridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.historyGridLayout.setContentsMargins(0, 0, 0, 0)
        self.historyGridLayout.setObjectName("historyGridLayout")

        self.retranslateUi(HistoryView)
        QtCore.QMetaObject.connectSlotsByName(HistoryView)

    def retranslateUi(self, HistoryView):
        _translate = QtCore.QCoreApplication.translate
        HistoryView.setWindowTitle(_translate("HistoryView", "Form"))

