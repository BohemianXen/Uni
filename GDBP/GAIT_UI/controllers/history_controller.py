from PyQt5.QtCore import QObject, pyqtSlot, QDate
from application.Logger import Logger
from os import getcwd
import numpy as np
import statistics


class HistoryController(QObject):
    """ Controller class. Handles the core program logic and data transfer between its view and model counterparts.

    Args:
        model (QWidget): The controller's corresponding model.

    Parameters:
        _model (QWidget): A reference to the passed model.
        _view (QWidget): A reference to this controller's corresponding view.
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
    """

    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None

        self.name = __class__.__name__
        self._logger = Logger(self.name)

    def link_view(self, view):
        self._view = view
        self.plot_dummy_steps(self.get_week(self._view.get_today()))

    def date_changed(self, date):
        """Handler for selected date events.

        Args:
            date (QDate): The new selected date.
        """
        self._logger.log("Date changed to: {}".format(QDate.toString(date)), Logger.DEBUG)

        # for now, just plot the dummy step data
        self.plot_dummy_steps(self.get_week(date))

    @staticmethod
    def get_week(date):
        """ Gets all days in the week leading up to 'date'.

        Args:
            date (QDate): The reference date.
        """
        days = [date.addDays(-i).toString() for i in range(7)]
        days_formatted = []

        for day in days:
            x = day.split(' ')
            days_formatted.insert(0, x[2] + ' ' + x[1])  # stores date in Day Month form

        return dict(enumerate(days_formatted))

    def plot_dummy_steps(self, dates):
        """Plots dummy step data from text file.

        Args:
            dates (dict): Enumerated dict of date range covered.
        """
        dummy_file = getcwd()[:getcwd().rfind('\\') + 1]
        dummy_file += r'resources\dummy_files\steps.txt'

        try:
            f = open(dummy_file, 'r')
            data = f.readlines()
            f.close()
            data_int = [int(val) for val in data]  # would be in model if not dummy
            stats = {
                " Peak:\t    ": str(max(data_int)),
                " Mean:\t    ": str(int(statistics.mean(data_int)))
            }
            self._view.update_stats(stats=stats)
            self._view.plot_steps(data=data_int, dates=dates)
        except Exception as e:
            self._logger.log("Error encountered plotting dummy steps", Logger.ERROR)
            self._logger.log(str(e), Logger.DEBUG)

    @pyqtSlot()
    def plot_random(self):
        """Unused. Plots random data for templates."""
        # make random plot for template view
        x = np.random.normal(size=1000)
        y = np.random.normal(size=1000)
        self._view.plot_random(x, y)

