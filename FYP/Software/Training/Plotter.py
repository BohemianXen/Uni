from Logger import Logger
from ui_files.main_view_ui import Ui_MainWindow
import pyqtgraph as pg
import numpy as np


class Plotter:
    def __init__(self, ui):
        super().__init__()

        pg.setConfigOption('background', (29, 29, 49))
        pg.setConfigOption('foreground', 'w')

        self._ui = ui

        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        self._acc_plot = self._ui.accPlot.getPlotItem()
        self._acc_plot.setContentsMargins(10, 10, 10, 10)
        #self._acc_plot.plot().getViewBox().disableAutoRange()

        self._gyro_plot = self._ui.gyroPlot.getPlotItem()
        self._gyro_plot.setContentsMargins(10, 10, 10, 10)
        #self._gyro_plot.plot().getViewBox().disableAutoRange()

        self._mag_plot = self._ui.magPlot.getPlotItem()
        self._mag_plot.setContentsMargins(10, 10, 10, 10)
        #self._mag_plot.plot().getViewBox().disableAutoRange()

        self._acc_plot.setTitle('Accelerometer')
        self._acc_plot.setLabels(left='gs', bottom='Sample No.')
        #self._acc_plot.addLegend(size=(100, 100))

        self._gyro_plot.setTitle('Gyroscope')
        self._gyro_plot.setLabels(left='dps', bottom='Sample No.')
        #self._gyro_plot.addLegend(size=(100, 100))

        self._mag_plot.setTitle('Magnetometer')
        self._mag_plot.setLabels(left='uT', bottom='Sample No.')
        #self._mag_plot.addLegend(size=(100, 100))
        #self.clear_plots(legend_clear=True)

        # self._ui.gyroView.setYRange(-500, 500, padding=0)
        # self._ui.accView.setYRange(-, 5, padding=0)
    def add_legends(self):
        self._acc_plot.addLegend(size=(100, 100))
        self._gyro_plot.addLegend(size=(100, 100))
        self._mag_plot.addLegend(size=(100, 100))

    def clear_plots(self, legend_clear=False):
        """Clears the plot ahead of updates."""
        # clear legends
        if legend_clear:
            if self._acc_plot.legend is not None:
                try:
                    if self._acc_plot.legend.scene() is not None:
                        self._acc_plot.legend.scene().removeItem(self._acc_plot.legend)
                except Exception as e:
                    self._logger.log('Error removing dummy plot legend', Logger.DEBUG)
                    self._logger.log(str(e), Logger.ERROR)

            # TODO proper clearing
            if self._gyro_plot.legend is not None:
                try:
                    if self._gyro_plot.legend.scene() is not None:
                        self._gyro_plot.legend.scene().removeItem(self._gyro_plot.legend)
                        self._gyro_plot.legend.scene().removeItem(self._gyro_plot.legend)
                except Exception as e:
                    self._logger.log('Error removing live plot legend', Logger.DEBUG)
                    self._logger.log(str(e), Logger.ERROR)

            if self._mag_plot.legend is not None:
                try:
                    if self._mag_plot.legend.scene() is not None:
                        self._mag_plot.legend.scene().removeItem(self._mag_plot.legend)
                        self._mag_plot.legend.scene().removeItem(self._mag_plot.legend)
                except Exception as e:
                    self._logger.log('Error removing live plot legend', Logger.DEBUG)
                    self._logger.log(str(e), Logger.ERROR)

        self._acc_plot.clear()
        self._gyro_plot.clear()
        self._mag_plot.clear()

    def plot(self, data):
        """Updates the accelerometer graph with new data."""
        sensor_names = ['Acc X', 'Acc Y', 'Acc Z', 'Gyro X', 'Gyro Y', 'Gyro Z', 'Mag X', 'Mag Y', 'Mag Z']
        self._ui.accPlot.setXRange(0, len(data), padding=0.02)
        self._ui.gyroPlot.setXRange(0, len(data), padding=0.02)
        self._ui.magPlot.setXRange(0, len(data), padding=0.02)

        for sensor in range(3):
            acc_series = [packet[sensor] for packet in data]
            gyro_series = [packet[sensor+3] for packet in data]
            mag_series = [packet[sensor+6] for packet in data]
            self._acc_plot.plot().setData(y=acc_series, pen=(sensor, 3), name=sensor_names[sensor])
            self._gyro_plot.plot().setData(y=gyro_series, pen=(sensor+3, 3), name=sensor_names[sensor+3])
            self._mag_plot.plot().setData(y=mag_series, pen=(sensor+6, 3), name=sensor_names[sensor+6])

        if len(self._acc_plot.legend.items) == 0:
            for sensor in range(3):
                self._acc_plot.legend.addItem(self._acc_plot.items[sensor], name=sensor_names[sensor])
                self._gyro_plot.legend.addItem(self._gyro_plot.items[sensor], name=sensor_names[sensor+3])
                self._mag_plot.legend.addItem(self._mag_plot.items[sensor], name=sensor_names[sensor+6])
