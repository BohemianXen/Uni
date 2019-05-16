from PyQt5.QtWidgets import QWidget
import pyqtgraph as pg
from views.ui_files.history_view_ui import Ui_HistoryView
from application.Logger import Logger
import numpy as np


class HistoryView(QWidget):
    """ View class. Instantiates all UI QWidgets associated with this view and links signals to controller slots.

    Args:
        controller (QWidget): The view's corresponding controller; that which manipulates this view.

    Parameters:
        _controller (QWidget): A reference to the passed controller.
        _ui (Ui_LiveView): Holds all the generated UI elements for an added layer of abstraction.
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
    """

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
        # self._ui.expandPushButton.hide()

        x = np.random.normal(size=1000)
        y = np.random.normal(size=1000)
        self._ui.graphicsView.getPlotItem().plot(x, y, pen=None, symbol='o')

    def toggle_calendar_view(self):
        if self._ui.calendarWidget.isVisible():
            self._ui.calendarWidget.hide()
        else:
            self._ui.calendarWidget.show()
