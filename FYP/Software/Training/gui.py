import sys
from Logger import Logger
from ui_files.main_view_ui import Ui_MainWindow
from Plotter import Plotter
from ble_connection_manager import ConnectionManagerBLE
from StreamManager import StreamManager
from processing.CSVConverters import CSVConverters
from AudioPlayer import AudioPlayer
from processing.DataProcessors import DataProcessors
from deep_learning import RawNeuralNet, SMVNeuralNet, ConvNeuralNet, KNNClassifier

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QCoreApplication, QThreadPool
from datetime import datetime
import numpy as np
import tensorflow as tf
tf.get_logger().setLevel('DEBUG')  # Reduce logging


params = {
    'live mode': True,
    'quick capture': False,
    'play audio': False,
    'name': 'FallDetector',
    'live packet size': 40,
    'total live samples': 120,
    'total capture samples': 480,
    'sample length': 6,
    'packet length': 8,
    'root': 'General',
    'actions': ('Standing'.upper(), 'Walking'.upper(), 'Lying Forwards'.upper(), 'Lying Left'.upper(),
                'Lying Right'.upper(),  'Forward Fall'.upper(), 'Left Fall'.upper(), 'Right Fall'.upper()),
    'actions colours': ('Green', 'Green', 'Green', 'Green', 'Green', 'Red', 'Red', 'Red'),
    'raw threshold': 0.92,  # TODO: Add these (and many other params) to gui for code cleanup + quicker config changes
    'smv threshold': 0.94,
    'conv threshold': 0.94
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
        self._classifier = None
        self._plotter = Plotter(self._ui)
        self._audio_player = AudioPlayer()

        # Thread pools

        self._pool = QThreadPool.globalInstance()
        self._pool.setMaxThreadCount(4)

        # Instantiate BLE modules
        self._connection_manager = ConnectionManagerBLE(caller=self, target_name=params['name'],
                                                        total_samples=params['total capture samples'],
                                                        sample_length=params['sample length'],
                                                        packet_length=params['packet length'],
                                                        live_mode=params['live mode'])

        self._stream_manager = StreamManager(params, self._connection_manager)

        self._live_mode = params['live mode']
        if self._live_mode:
            self._logger.log('Starting in Live Mode', Logger.DEBUG)
            self._connection_manager.total_samples = params['live packet size']

        else:
            self._logger.log('Starting in Data Capture Mode', Logger.DEBUG)

        # UI callbacks
        self._ui.filePushButton.clicked.connect(lambda: self.file_button_clicked())
        self._ui.plotPushButton.clicked.connect(lambda: self.plot_button_clicked())
        self._ui.connectPushButton.clicked.connect(lambda: self.connect_button_clicked())
        self._ui.recordPushButton.clicked.connect(lambda: self.record_button_clicked())
        self._ui.modelPushButton.clicked.connect(lambda: self.model_button_clicked())

        # Final initialisations
        self._ui.progressBar.setValue(0)
        self._filename = ''
        self._model_filename = ''
        self._connected = False
        self._model = None
        self._live_data = []
        self._prev_guess = None
        self._threshold = min(params['raw threshold'], params['smv threshold'], params['conv threshold'])

    def update_console(self, message):
        """Writes a line to the console text widget during a port test.

        Args:
            message (str): The message to be written to the in-app console.
        """
        full_message = datetime.now().strftime("%H:%M:%S") + ':\t' + message + '\n'
        self._ui.consoleTextEdit.append(full_message)
        self._ui.consoleTextEdit.ensureCursorVisible()
        self._logger.log(message, Logger.DEBUG)

    # ----------------------------------------------------Callbacks ----------------------------------------------------
    def file_button_clicked(self):
        """Opens .csv file dialogue"""

        default_dir = 'Training Data\\' + params['root']
        self._filename = QFileDialog.getOpenFileName(self, 'Open file', default_dir, 'CSV Files(*.csv)')[0]

        if self._filename != '':
            msg = 'Selected: ' + self._filename[self._filename.rfind('/')+1:]  # .rstrip('.csv')
            self.update_console(msg)
            self._ui.fileLabel.setText(msg)
            self._ui.plotPushButton.setEnabled(True)
        else:
            self._ui.fileLabel.setText('No File Selected')
            self._ui.plotPushButton.setEnabled(False)

    def model_button_clicked(self):
        """Opens .h5 file dialogue"""

        default_dir = 'deep_learning\\Saved Models'
        #filters = "H5 Files (*.h5);;Pickle files (*.txt)"
        self._model_filename = QFileDialog.getOpenFileName(self, 'Open file', default_dir)[0]

        if self._model_filename != '':
            msg = 'Selected: ' + self._model_filename[self._model_filename.rfind('/')+1:]
            self.update_console(msg)
            self._ui.modelLabel.setText(msg)

            if self._live_mode:

                if 'Raw' in self._model_filename:
                    self._classifier = RawNeuralNet
                    self._threshold = params['raw threshold']
                elif 'SMV' in self._model_filename:
                    self._classifier = SMVNeuralNet
                    self._threshold = params['smv threshold']
                elif 'Conv' in self._model_filename:
                    self._classifier = ConvNeuralNet
                    self._threshold = params['conv threshold']
                elif 'KNN' in self._model_filename:
                    self._classifier = KNNClassifier
                else:
                    pass

                if self._classifier is not None:
                    self._model = self._classifier.load_model(self._model_filename)

        else:
            self._ui.fileLabel.setText('No Model Selected')

            if self._live_mode:
                self._ui.recordPushButton.setEnabled(True)
                self._model = None

    def plot_button_clicked(self):
        """Plots data within the currently selected .csv file"""
        msg = 'Plot button clicked, reading {} then plotting'.format(self._filename)
        self.update_console(msg)

        data = CSVConverters.csv_to_list(self._filename)

        if len(data) != 0:
            self._plotter.clear_plots(legend_clear=False)
            self._plotter.add_legends()
            mag = True if len(data[0]) == 9 else False
            self._plotter.plot(data, mag=mag)

    def connect_button_clicked(self):
        """Starts a stream manager in a new thread"""
        # TODO: Fix stability on multiple clicks

        msg = 'Connect button clicked; starting new stream manager thread and searching for devices'
        self.update_console(msg)

        self._pool.start(self._stream_manager)
        self._ui.connectPushButton.setEnabled(False)
        self._ui.progressBar.setValue(0)

    def record_button_clicked(self):  # TODO: disable while saving
        """Remotely starts/stops stream if a device is connected"""

        if self._connected:
            msg = 'Starting stream remotely'
            self.update_console(msg)

            self._ui.connectPushButton.setEnabled(False)
            if not self._connection_manager.start_stream:
                self._connection_manager.start_stream = True
        else:
            msg = 'Record button clicked but no device is connected'
            self.update_console(msg)

            self._ui.connectPushButton.setEnabled(True)
            self._ui.recordPushButton.setEnabled(False)
            self._ui.progressBar.setValue(0)

    # -------------------------------------------------- Slots ---------------------------------------------------------

    @pyqtSlot(bool)
    def device_connected(self, connected):
        """Slot triggered when a FallDetector device is connected"""

        self._connected = connected
        msg = 'Device connected status - ' + str(connected)
        self.update_console(msg)

        if connected:
            self._ui.connectPushButton.setEnabled(False)
            self._ui.recordPushButton.setEnabled(True)
            if self._live_mode:
                self._ui.modelPushButton.setEnabled(True)
        else:
            self._ui.connectPushButton.setEnabled(True)
            self._ui.recordPushButton.setEnabled(False)
            if self._live_mode:
                self._ui.modelPushButton.setEnabled(False)

    @pyqtSlot(bool)
    def starting_stream(self, value):
        """Slot triggered when device writes to startingStream characteristic"""

        msg = 'Device wrote \"' + str(value) + '\" to starting stream characteristic'
        self.update_console(msg)

        if value and params['play audio']:
            # Play audio cue to aid timing
            self._logger.log('Playing audio', Logger.DEBUG)
            self._audio_player.play()  # TODO: only works once if separate thread

    @pyqtSlot(int)
    def update_progress(self, value):
        """Updates progress bar packet-wise"""
        if not self._live_mode:
            percentage = int(((value*params['packet length'])/params['total capture samples']) * 100)
            self._ui.progressBar.setValue(percentage)
            self.update_console('Transfer %d%% complete' % percentage)

    @pyqtSlot(list)
    def data_ready(self, data):
        """Slot triggered when a data packet has been received in full"""

        converted_data = DataProcessors.bytearray_to_float(data)  # Convert byte array to signed floats

        if not self._live_mode:
            self.capture_packet_ready(converted_data)
        else:
            self._live_data.extend(converted_data)
            overlap = len(self._live_data) - params['total live samples']
            if overlap >= 0 and (params['quick capture'] or self._model is not None):
                if overlap == 0:
                    self.live_packet_ready(self._live_data, capture=params['quick capture'])
                else:
                    self.live_packet_ready(self._live_data[-params['total live samples']:], capture=params['quick capture'])
                    self._live_data = self._live_data[overlap:]

    # ------------------------------------------- Data Packet Funcs ----------------------------------------------------

    def capture_packet_ready(self, data):
        """Saves the current data packet in csv format."""

        msg = 'Attempting to save %d entries in csv file' % len(data)
        self.update_console(msg)

        success = CSVConverters.write_data(data, root=params['root'])
        if success != -1:
            msg = 'Successfully wrote %d entries' % success
            self.update_console(msg)
        else:
            msg = 'Failed to save data'
            self.update_console(msg)

    def live_packet_ready(self, new_data, capture):
        """Either saves the current live packet or puts it through the trained model for action determination."""

        if capture:
            self.capture_packet_ready(new_data)
        else:
            try:
                features = self._classifier.pre_process(new_data, single=True)
                if features is not None:
                    prediction = self._model.predict(features)

                    if np.ndim(prediction) > 1:
                        most_likely = np.argmax(prediction)
                        if most_likely > 4:
                            guess = most_likely if np.max(prediction) >= self._threshold else self._prev_guess
                        else:
                            guess = most_likely
                    else:
                        guess = int(prediction[0])  # KNN predict is absolute

                    self.update_console(params['actions'][guess])

                    if guess != self._prev_guess:
                        # if guess > 4:
                        #     print(prediction)
                        self._ui.actionLabel.setText(params['actions'][guess])
                        self._ui.actionLabel.setStyleSheet('color: ' + params['actions colours'][guess])
                        self._prev_guess = guess

            except Exception as e:
                print(e)

    # -------------------------------------------------- On Close ------------------------------------------------------

    def closeEvent(self, *args, **kwargs):
        self._logger.log('Close button clicked. Shutting down.', Logger.DEBUG)

        print('{} thread(s) running on termination'.format(self._pool.activeThreadCount()))
        while self._pool.activeThreadCount() > 0:
            self._connection_manager.force_disconnect = True
            self._pool.waitForDone(1000)
            print('Finishing up...')

        QCoreApplication.exit(0)


if __name__ == '__main__':
    gui = GUI(sys.argv)
    if len(gui.arguments()) > 1 and gui.arguments()[1] == '-d':
        gui.DEBUG_MODE = True

    sys.exit(gui.exec_())
