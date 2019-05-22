from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from views.ui_files.live_view_ui import Ui_LiveView
from application.Logger import Logger
import pyqtgraph as pg
import numpy as np


class LiveView(QWidget):
    """ View class. Instantiates all UI QWidgets associated with this view and links signals to controller slots.

    Args:
        controller (QWidget): The view's corresponding controller; that which manipulates this view.

    Parameters:
        newPlotReady (pyqtSignal): Signal indicating a live plot can commence.
        _controller (QWidget): A reference to the passed controller.
        _ui (Ui_LiveView): Holds all the generated UI elements for an added layer of abstraction.
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
        _plot (PlotItem): reference to the main pyqtgraph PlotItem (to reduce line char count when plotting).
    """

    newPlotReady = pyqtSignal(str)

    def __init__(self, controller):
        super().__init__()

        pg.setConfigOption('background', (29, 29, 49))
        pg.setConfigOption('foreground', 'w')

        self._controller = controller
        self._ui = Ui_LiveView()
        self._ui.setupUi(self)

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        self._plot = self._ui.graphicsView.getPlotItem()
        self._plot.setContentsMargins(10, 10, 10, 10)
        self._plot.plot().getViewBox().disableAutoRange()
        self._ui.graphicsView.setYRange(-128, 128, padding=0)

        self._ui.liveStackedWidget.setCurrentWidget(self._ui.connectedView)  # debug only

        # listeners
        self.newPlotReady.connect(self._controller.start_stream)
        self._ui.testRadioButton.toggled.connect(lambda: self._controller.button_toggled('test'))
        self._ui.dummyMotionRadioButton.toggled.connect(lambda: self._controller.button_toggled('dummy motion'))
        self._ui.liveMotionRadioButton.toggled.connect(lambda: self._controller.button_toggled('live motion'))
        self._ui.uvRadioButton.toggled.connect(lambda: self._controller.button_toggled('uv'))

    def change_stacked_widget(self, view_type):  # Need checked check?
        """Updates the stacked widget to match the chosen data view mode.

        Args:
            view_type (str): The name of the live view type required.
        """
        self.clear_graph()
        self._ui.consoleTextEdit.clear()

        if self._ui.testRadioButton.isChecked() and view_type == 'test':
            self._ui.stackedWidget.setCurrentWidget(self._ui.consoleWidget)
            self.newPlotReady.emit(view_type)
        else:
            if self._ui.liveMotionRadioButton.isChecked() and view_type == 'live motion':
                self._plot.setTitle('Live Motion Data')
                self.newPlotReady.emit(view_type)
            elif self._ui.dummyMotionRadioButton.isChecked() and view_type == 'dummy motion':
                self._plot.setTitle('Dummy Motion Data')
                self.newPlotReady.emit(view_type)
            elif self._ui.uvRadioButton.isChecked() and view_type == 'uv':
                self._plot.setTitle('UV Data')
                self.newPlotReady.emit(view_type)
            else:
                None

            self._plot.setLabels(left='Value', bottom='Sample No.')
            # self._plot.addLegend(size=[100, 300])
            self._ui.stackedWidget.setCurrentWidget(self._ui.graphicsWidget)


    def unlock_view(self):
        """Moves to connected view since device connection complete."""
        self._logger.log('Unlocking {}'.format(self.name), self._logger.INFO)
        self._ui.liveStackedWidget.setCurrentWidget(self._ui.connectedView)

    def update_test_console(self, message):
        """Writes a line to the console text widget during a port test.

        Args:
            message (str): The message to be written to the in-app console.
        """
        self._ui.consoleTextEdit.append(message)
        self._ui.consoleTextEdit.ensureCursorVisible()

    def clear_graph(self):
        """Clears the plot ahead of updates."""
        #self._plot.plot().clear()
        self._plot.clear()

    def update_motion_plot(self, data):
        """Updates the motion graph with new data."""
        sensor_names = ['Gyro X', 'Gyro Y', 'Gyro Z', 'Acc X', 'Acc Y', 'Acc Z']
        self._ui.graphicsView.setXRange(0, len(data), padding=0.02)

        for sensor in range(6):
            series = [packet[sensor] for packet in data]
            self._plot.plot().setData(y=series, pen=(sensor, 6), name=sensor_names[sensor])
