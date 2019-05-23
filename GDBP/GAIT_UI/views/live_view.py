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

        self._dummy_plot = self._ui.dummyView.getPlotItem()
        self._dummy_plot.setContentsMargins(10, 10, 10, 10)
        self._dummy_plot.plot().getViewBox().disableAutoRange()

        self._gyro_plot = self._ui.gyroView.getPlotItem()
        self._gyro_plot.setContentsMargins(10, 10, 10, 10)
        self._gyro_plot.plot().getViewBox().disableAutoRange()

        self._acc_plot = self._ui.accView.getPlotItem()
        self._acc_plot.setContentsMargins(10, 10, 10, 10)
        self._acc_plot.plot().getViewBox().disableAutoRange()

        self._uv_plot = self._ui.uvView.getPlotItem()
        self._uv_plot.setContentsMargins(10, 10, 10, 10)
        self._uv_plot.plot().getViewBox().disableAutoRange()

        self._ui.liveStackedWidget.setCurrentWidget(self._ui.connectedView)  # debug only
        #self._ui.stackedWidget.setCurrentWidget(self._ui.consoleWidget)

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
                self._ui.gyroView.setYRange(-500, 500, padding=0)
                self._ui.accView.setYRange(-5, 5, padding=0)

                self._gyro_plot.setTitle('Live Gyro XYZ Data')
                self._gyro_plot.setLabels(left='dps', bottom='Sample No.')
                self._gyro_plot.addLegend(size=(100, 100))

                self._acc_plot.setTitle('Live Accelerometer XYZ Data')
                self._acc_plot.setLabels(left='gs', bottom='Sample No.')
                self._acc_plot.addLegend(size=(100, 100))

                self._ui.stackedWidget.setCurrentWidget(self._ui.liveWidget)
                self.newPlotReady.emit(view_type)

            elif self._ui.dummyMotionRadioButton.isChecked() and view_type == 'dummy motion':
                self._ui.dummyView.setYRange(-128, 128, padding=0)
                self._dummy_plot.setTitle('Dummy Motion Data')
                self._dummy_plot.setLabels(left='Value', bottom='Sample No.')
                self._dummy_plot.addLegend(size=(100, 200))

                self.newPlotReady.emit(view_type)
                self._ui.stackedWidget.setCurrentWidget(self._ui.dummyWidget)

            elif self._ui.uvRadioButton.isChecked() and view_type == 'uv':
                self._ui.uvView.setYRange(-5, 5, padding=0)  # TODO: Find out range of UV data
                self._uv_plot.setTitle('UV Data')
                self._uv_plot.setLabels(left='Value', bottom='Sample No.')
                self.newPlotReady.emit(view_type)
                self._ui.stackedWidget.setCurrentWidget(self._ui.uvWidget)
            else:
                None

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
        # clear legends
        if self._dummy_plot.legend is not None:
            try:
                self._dummy_plot.legend.scene().removeItem(self._dummy_plot.legend)
            except Exception as e:
                self._logger.log('Error removing dummy plot legend', Logger.DEBUG)
                self._logger.log(str(e), Logger.ERROR)

        # TODO proper clearing
        if self._gyro_plot.legend is not None:
            try:
                self._gyro_plot.legend.scene().removeItem(self._gyro_plot.legend)
                self._acc_plot.legend.scene().removeItem(self._acc_plot.legend)
            except Exception as e:
                self._logger.log('Error removing live plot legend', Logger.DEBUG)
                self._logger.log(str(e), Logger.ERROR)

        self._dummy_plot.clear()
        self._gyro_plot.clear()
        self._acc_plot.clear()
        self._uv_plot.clear()


    def uv_on(self):
        if self._ui.uvRadioButton.isChecked():
            return True
        else:
            return False

    def update_steps_label(self, val):
        self._ui.stepsLabel.setText(str(val))

    def update_dummy_plot(self, data):
        """Updates the dummy motion graph with new data."""
        sensor_names = ['Gyro X', 'Gyro Y', 'Gyro Z', 'Acc X', 'Acc Y', 'Acc Z']
        self._ui.dummyView.setXRange(0, len(data), padding=0.02)

        for sensor in range(6):
            series = [packet[sensor] for packet in data]
            self._dummy_plot.plot().setData(y=series, pen=(sensor, 6), name=sensor_names[sensor])

        if len(self._dummy_plot.legend.items) == 0:
            for sensor in range(6):
                self._dummy_plot.legend.addItem(self._dummy_plot.items[sensor], name=sensor_names[sensor])

    def update_motion_plot(self, data):
        """Updates the motion graph with new data."""
        sensor_names = ['Gyro X', 'Gyro Y', 'Gyro Z', 'Acc X', 'Acc Y', 'Acc Z']
        self._ui.gyroView.setXRange(0, len(data), padding=0.02)
        self._ui.accView.setXRange(0, len(data), padding=0.02)

        for sensor in range(3):
            gyro_series = [packet[sensor] for packet in data]
            acc_series = [packet[sensor+3] for packet in data]

            self._gyro_plot.plot().setData(y=gyro_series, pen=(sensor, 3), name=sensor_names[sensor])
            self._acc_plot.plot().setData(y=acc_series, pen=(sensor+3, 3), name=sensor_names[sensor+3])

        if len(self._gyro_plot.legend.items) == 0:
            for sensor in range(3):
                self._gyro_plot.legend.addItem(self._gyro_plot.items[sensor], name=sensor_names[sensor])
                self._acc_plot.legend.addItem(self._acc_plot.items[sensor], name=sensor_names[sensor+3])

    def update_uv_plot(self, data):
        """Updates the uv graph with new data."""

        self._ui.uvView.setXRange(0, len(data), padding=0.02)
        self._uv_plot.plot().setData(y=data, pen=0)
