from PyQt5.QtWidgets import QWidget
from views.ui_files.live_view_ui import Ui_LiveView
from application.Logger import Logger
import pyqtgraph as pg


class LiveView(QWidget):
    """ View class. Instantiates all UI QWidgets associated with this view and links signals to controller slots.

      Args:
          controller (QWidget): The view's corresponding controller; that which manipulates this view

      Parameters:
          _controller (QWidget): A reference to the passed controller
          _ui (Ui_LiveView): Holds all the generated UI elements for an added layer of abstraction
          name (str): The name of this class
          _logger (Logger): Logging instance for this class
    """

    def __init__(self, controller):
        super().__init__()

        pg.setConfigOption('background', (29, 29, 49))
        pg.setConfigOption('foreground', 'w')

        self._controller = controller
        self._ui = Ui_LiveView()
        self._ui.setupUi(self)

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        # self._ui.liveStackedWidget.setCurrentWidget(self._ui.connectedView)  # Debug only

        # radio button listeners
        self._ui.testRadioButton.toggled.connect(lambda: self._controller.button_toggled('console'))
        self._ui.motionRadioButton.toggled.connect(lambda: self._controller.button_toggled('graph'))
        self._ui.uvRadioButton.toggled.connect(lambda: self._controller.button_toggled('graph'))
        self._ui.locationRadioButton.toggled.connect(lambda: self._controller.button_toggled('map'))

    def change_stacked_widget(self, view_type):  # Need checked check?
        """ Updates the stacked widget to match the chosen data view mode.

        Args:
            view_type (str): The name of the view type required; either console, graph, or map
        """
        if view_type == 'console':
            self._ui.stackedWidget.setCurrentWidget(self._ui.consoleWidget)
        elif view_type == 'graph':
            self._ui.stackedWidget.setCurrentWidget(self._ui.graphicsWidget)
        else:
            self._ui.stackedWidget.setCurrentWidget(self._ui.mapWidget)

    def unlock_view(self):
        """ Moves to connected view since device connection complete."""
        self._logger.log('Unlocking {}'.format(self.name), self._logger.INFO)
        self._ui.liveStackedWidget.setCurrentWidget(self._ui.connectedView)

    def update_test_console(self, message):
        """ Writes a line to the console text widget during a port test.

        Args:
            message (str): The message to be written to the in-app console
        """
        self._ui.consoleTextEdit.append(message)
