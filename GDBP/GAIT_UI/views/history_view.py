from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QFont
import pyqtgraph as pg
from views.ui_files.history_view_ui import Ui_HistoryView
from application.Logger import Logger


class HistoryView(QWidget):
    """ View class. Instantiates all UI QWidgets associated with this view and links signals to controller slots.

    Args:
        controller (QWidget): The view's corresponding controller; that which manipulates this view.

    Parameters:
        _controller (QWidget): A reference to the passed controller.
        _ui (Ui_LiveView): Holds all the generated UI elements for an added layer of abstraction.
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
        _today (QDate): Holds today's date as per system clock.
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

        self._today = self._ui.calendarWidget.selectedDate()

        self._plot = self._ui.graphicsView.getPlotItem()
        self._plot.setContentsMargins(10, 10, 10, 10)

        # connect listeners
        self._ui.calendarWidget.selectionChanged.connect(lambda: self._controller.date_changed(
            self._ui.calendarWidget.selectedDate()))

    def get_today(self):
        """Gets the current day.

        Returns:
            QDate: Today's date.
        """
        return self._today

    def update_stats(self, stats):
        """Updates the stats GroupBox.

        Args:
             stats (dict): A dictionary containing stat name and value pairs.
        """
        self.clear_stats()
        self._ui.formLayout.addRow(QLabel(), QLabel())  # padding

        for stat, value in stats.items():
            # style stat label
            stat_label = QLabel(stat)
            stat_font = QFont(stat_label.font())
            stat_font.setBold(True)
            stat_font.setPointSize(20)
            stat_label.setFont(stat_font)

            # style value label
            value_label = QLabel(value)
            value_font = QFont(stat_font)
            value_font.setBold(False)
            value_font.setPointSize(25)
            value_label.setFont(value_font)

            # add labels
            self._ui.formLayout.addRow(stat_label, value_label)
            self._ui.formLayout.addRow(QLabel(), QLabel())

    def clear_stats(self):
        """Removes all stats from GroupBox."""
        count = self._ui.formLayout.rowCount()
        if count != 0:
            for i in range(count):
                self._ui.formLayout.removeRow(0)

    def plot_steps(self, data, dates):
        """Updates the steps plot with new data.

        Args:
            data (list): A list of the step values.
            dates (dict): An enumerated dictionary of the days as tuple keys.
        """
        x = list(dates.keys())
        brushes = [[(10, 100, 200)]*len(dates)]
        brushes[0][len(dates)-1] = (130, 100, 170)
        bar = pg.BarGraphItem(x=x, height=data, width=0.6, brushes=brushes[0])

        self._plot.addItem(bar)
        self._plot.getAxis('bottom').setTicks([dates.items()])
        self._ui.graphicsView.setLimits(yMin=0)

    def plot_random(self, x, y):
        """Plots random values. Template only."""
        self._plot.plot(x, y, pen=None, symbol='o')
