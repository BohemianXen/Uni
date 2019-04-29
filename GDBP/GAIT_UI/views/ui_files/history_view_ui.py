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
        HistoryView.setStyleSheet("QTableView {  \n"
"    background-color: rgb(39, 39, 52);\n"
"    selection-background-color: rgb(90, 90, 121); \n"
"}\n"
"\n"
"QPushButton {padding-bottom: 7px; }\n"
"\n"
"QGroupBox {color: rgb(188, 188, 188); }\n"
"\n"
"QRadioButton {color: rgb(188, 188, 188); margin-top: 11px; margin-bottom: 2px; margin-left: 120px }\n"
"")
        self.layoutWidget = QtWidgets.QWidget(HistoryView)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1601, 771))
        self.layoutWidget.setObjectName("layoutWidget")
        self.historyGridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.historyGridLayout.setContentsMargins(0, 0, 0, 0)
        self.historyGridLayout.setObjectName("historyGridLayout")
        self.statsComboBox = QtWidgets.QComboBox(self.layoutWidget)
        self.statsComboBox.setMinimumSize(QtCore.QSize(400, 30))
        self.statsComboBox.setMaximumSize(QtCore.QSize(400, 20))
        self.statsComboBox.setObjectName("statsComboBox")
        self.statsComboBox.addItem("")
        self.statsComboBox.addItem("")
        self.statsComboBox.addItem("")
        self.statsComboBox.addItem("")
        self.statsComboBox.addItem("")
        self.statsComboBox.addItem("")
        self.historyGridLayout.addWidget(self.statsComboBox, 0, 2, 1, 1, QtCore.Qt.AlignRight)
        spacerItem = QtWidgets.QSpacerItem(20, 60, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.historyGridLayout.addItem(spacerItem, 7, 0, 1, 4)
        self.expandPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.expandPushButton.setMinimumSize(QtCore.QSize(30, 30))
        self.expandPushButton.setMaximumSize(QtCore.QSize(30, 30))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.expandPushButton.setFont(font)
        self.expandPushButton.setObjectName("expandPushButton")
        self.historyGridLayout.addWidget(self.expandPushButton, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.historyGridLayout.addItem(spacerItem1, 3, 0, 2, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.historyGridLayout.addItem(spacerItem2, 0, 3, 7, 1)
        self.calendarWidget = QtWidgets.QCalendarWidget(self.layoutWidget)
        self.calendarWidget.setMinimumSize(QtCore.QSize(400, 300))
        self.calendarWidget.setMaximumSize(QtCore.QSize(400, 300))
        self.calendarWidget.setStyleSheet("")
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setObjectName("calendarWidget")
        self.historyGridLayout.addWidget(self.calendarWidget, 2, 1, 3, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.historyGridLayout.addItem(spacerItem3, 1, 0, 1, 3)
        spacerItem4 = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.historyGridLayout.addItem(spacerItem4, 0, 0, 1, 2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.historyGridLayout.addItem(spacerItem5, 6, 0, 1, 2)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.historyGridLayout.addItem(spacerItem6, 5, 0, 1, 2)
        self.viewModeGroupBox = QtWidgets.QGroupBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.viewModeGroupBox.setFont(font)
        self.viewModeGroupBox.setObjectName("viewModeGroupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.viewModeGroupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 1131, 41))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.verticalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.dailyRadioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.dailyRadioButton.setChecked(True)
        self.dailyRadioButton.setObjectName("dailyRadioButton")
        self.horizontalLayout.addWidget(self.dailyRadioButton)
        self.weeklyRadioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.weeklyRadioButton.setObjectName("weeklyRadioButton")
        self.horizontalLayout.addWidget(self.weeklyRadioButton)
        self.monthlyRadioButton = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.monthlyRadioButton.setObjectName("monthlyRadioButton")
        self.horizontalLayout.addWidget(self.monthlyRadioButton)
        self.historyGridLayout.addWidget(self.viewModeGroupBox, 6, 2, 1, 1)
        self.graphicsView = PlotWidget(self.layoutWidget)
        self.graphicsView.setObjectName("graphicsView")
        self.historyGridLayout.addWidget(self.graphicsView, 2, 2, 4, 1)

        self.retranslateUi(HistoryView)
        QtCore.QMetaObject.connectSlotsByName(HistoryView)

    def retranslateUi(self, HistoryView):
        _translate = QtCore.QCoreApplication.translate
        HistoryView.setWindowTitle(_translate("HistoryView", "Form"))
        self.statsComboBox.setItemText(0, _translate("HistoryView", "UV Exposure"))
        self.statsComboBox.setItemText(1, _translate("HistoryView", "Location"))
        self.statsComboBox.setItemText(2, _translate("HistoryView", "Heart Rate"))
        self.statsComboBox.setItemText(3, _translate("HistoryView", "Cadence"))
        self.statsComboBox.setItemText(4, _translate("HistoryView", "Strike Power"))
        self.statsComboBox.setItemText(5, _translate("HistoryView", "Pollution Exposure"))
        self.expandPushButton.setText(_translate("HistoryView", "⤡"))
        self.viewModeGroupBox.setTitle(_translate("HistoryView", "View Mode"))
        self.dailyRadioButton.setText(_translate("HistoryView", "Daily"))
        self.weeklyRadioButton.setText(_translate("HistoryView", "Weekly"))
        self.monthlyRadioButton.setText(_translate("HistoryView", "Monthly"))

from pyqtgraph import PlotWidget
