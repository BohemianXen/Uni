import sys
from csv import reader as csv_reader
from Logger import Logger
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from ui_files.main_view_ui import Ui_MainWindow
from Plotter import Plotter
from ble_connection_manager import ConnectionManagerBLE
from StreamManager import StreamManager
from csv_writer import SerialToCSV

#import asyncio
from PyQt5.QtCore import QThreadPool
from asyncqt import QEventLoop, asyncSlot, asyncClose


params = {
    # 'address': 57:0F:6E:FA:4E:C9',
    'name': 'FallDetector',
    'samples': 238,
    'length': 9
}


class GUI(QApplication):
    """ Application class. Instantiates all UI models, views, and controllers.

    Args:
        sys_argv (list): Command line arguments for debug purposes.

    Parameters:
        DEBUG_MODE (bool): Class attribute depicting run mode.
        name (str): The name of this class name.
        logger (Logger): Logging instance for this class.
        module_names (list): List of all the modules present in the app.
    """

    DEBUG_MODE = False

    def __init__(self, sys_argv):
        super(GUI, self).__init__(sys_argv)
        self.setStyle('Fusion')
        self.name = self.__class__.__name__
        self.logger = Logger(self.name)
        self.logger.log('App started', Logger.INFO)
        self.main_view = MainView()
        self.main_view.show()


class MainView(QMainWindow):
    """ View class. Instantiates all UI QWidgets associated with this view and links signals to controller slots.

    Args:
        controller (QWidget): The view's corresponding controller; that which manipulates this view.

    Parameters:
        _controller (QWidget): A reference to the passed controller.
        _ui (Ui_LiveView): Holds all the generated UI elements for an added layer of abstraction.
        name (str): The name of this class.
        _logger (Logger): Logging instance for this class.
        _tabs (dict): Maps the tab indexes to their corresponding view objects.
    """

    def __init__(self):
        super().__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        self._plotter = Plotter(self._ui)
        self._connection_manager = ConnectionManagerBLE(caller=self, target_name=params['name'], total_samples=params['samples'], payload_length=params['length'])
        self._stream_manager = StreamManager(params, self._connection_manager)

        self._pool = QThreadPool.globalInstance()

        self._ui.filePushButton.clicked.connect(lambda: self.file_button_clicked())
        self._ui.plotPushButton.clicked.connect(lambda: self.plot_button_clicked())
        self._ui.connectPushButton.clicked.connect(lambda: self.connect_button_clicked())
        self._ui.recordPushButton.clicked.connect(lambda: self.record_button_clicked())

        self._filename = ''
        self._connected = False

    def file_button_clicked(self):
        self._filename = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"CSV Files(*.csv)")[0]
        if self._filename != '':
            msg = 'Selected: ' + self._filename[self._filename.rfind('/')+1:]  # .rstrip('.csv')
            self._logger.log(msg, Logger.INFO)
            self._ui.fileLabel.setText(msg)
            self._ui.plotPushButton.setEnabled(True)
        else:
            self._ui.fileLabel.setText('No File Selected')
            self._ui.plotPushButton.setEnabled(False)

    def plot_button_clicked(self):
        data = []
        with open(self._filename, 'r', newline='') as file:
            reader = csv_reader(file, delimiter=',')
            for row in reader:
                if row[0] != 'ax':
                    data.append([float(val) for val in row])

        if len(data) != 0:
            self._plotter.clear_plots(legend_clear=False)
            self._plotter.add_legends()
            self._plotter.plot(data)

    def connect_button_clicked(self):
        self._pool.start(self._stream_manager)
        self._ui.connectPushButton.setEnabled(False)

    def record_button_clicked(self):
        if self._connected:
            self._ui.connectPushButton.setEnabled(False)
            if not self._connection_manager.start_stream:
                self._connection_manager.start_stream = True
        else:
            self._ui.connectPushButton.setEnabled(True)
            self._ui.recordPushButton.setEnabled(False)


    @pyqtSlot(bool)
    def device_connected(self, connected):
        self._connected = connected
        if connected:
            self._ui.connectPushButton.setEnabled(False)
            self._ui.recordPushButton.setEnabled(True)
        else:
            self._ui.connectPushButton.setEnabled(True)
            self._ui.recordPushButton.setEnabled(False)
        #self.signals.connected.emit(connected)

    @pyqtSlot(list)
    def data_ready(self, data):
        #self.signals.dataReady.emit(data)
        success = SerialToCSV.write_data(data)
        if success != -1:
            print('Successfully wrote %d entries' % success)
        else:
            print('Failed to save data')

    def closeEvent(self, *args, **kwargs):
        self._logger.log('Close button clicked. Shutting down.', Logger.DEBUG)
        #self._controller.on_close()


if __name__ == '__main__':
    gui = GUI(sys.argv)
    if gui.arguments()[1] == '-d':
        gui.DEBUG_MODE = True

        sys.exit(gui.exec_())
