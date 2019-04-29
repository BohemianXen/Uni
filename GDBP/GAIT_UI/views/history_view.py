from PyQt5.QtWidgets import QWidget
import pyqtgraph as pg
from views.ui_files.history_view_ui import Ui_HistoryView
from application.Logger import Logger
import numpy as np

class HistoryView(QWidget):
    def __init__(self, controller):
        super().__init__()

        pg.setConfigOption('background', (29, 29, 49))
        pg.setConfigOption('foreground', 'w')

        self._controller = controller
        self._ui = Ui_HistoryView()
        self._ui.setupUi(self)

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        self._ui.expandPushButton.clicked.connect(lambda: self._controller.expand_button_clicked())
        x = np.random.normal(size=1000)
        y = np.random.normal(size=1000)
        self._ui.graphicsView.plot(x, y, pen=None, symbol='o')

    def toggle_calendar_view(self):
        if self._ui.calendarWidget.isVisible():
            self._ui.calendarWidget.hide()
        else:
            self._ui.calendarWidget.show()
