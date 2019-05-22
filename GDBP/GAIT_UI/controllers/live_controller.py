from PyQt5.QtCore import QObject, pyqtSlot, QThreadPool, QTimer, QElapsedTimer
from application.Logger import Logger
from data_processors.Converters import Converters
from controllers.live_manager.SerialPortTest import SerialPortTest
from controllers.live_manager.DummyLiveMotion import DummyLiveMotion
import serial.tools.list_ports

from statistics import mean
import cProfile


class LiveController(QObject):
    def __init__(self, model):
        super().__init__()

        self._model = model
        self._view = None

        self.name = __class__.__name__
        self._logger = Logger(self.name)

        self.pool = QThreadPool.globalInstance()

        self.live_types = {
            'test': None,
            'dummy motion': None,
            'live motion': None
        }
        self.streaming = False
        self.dummy_motion = None
        self.port_test = None


        self.port = 3
        #self.port_test = SerialPortTest(port_no=self.port, msg=None)
        """self.uuid = 0x1200
        self.timer = QTimer()
        self.timer.timeout.connect(self.plot)
        self.elap = QElapsedTimer()
        self.old = 0
        self.times = []

        self.profiler = cProfile.Profile()
        self.profiler.dump_stats('stats.txt')"""

    def link_view(self, view):
        self._view = view
        self.start_stream('test')

    # update view following connect event
    def unlock_view(self):
        self._view.unlock_view()

    def button_toggled(self, view_type):
        if self.streaming:
            self.stop_streaming(view_type)

        self._view.change_stacked_widget(view_type)

    # Port Test
    @pyqtSlot()
    def start_test(self):
        if len(serial.tools.list_ports) > 0:
            port_test = SerialPortTest(port_no=self.port, msg=None)
            #port_test.autoDelete(False)
            port_test.signals.dataReady.connect(self.update_test_console)
            self.pool.start(port_test)


    @pyqtSlot(bytes)
    def update_test_console(self, message):
        try:
            message = message.rstrip()
            self._view.update_test_console(message.decode('utf-8'))
        except Exception as e:
            print(str(e))
            pass

    @pyqtSlot(str)
    def start_stream(self, data_type):
        self.streaming = True

        if data_type == 'test' and len(serial.tools.list_ports.comports()) > 0:
            self._logger.log('Starting port test', Logger.DEBUG)
            port_test = SerialPortTest(port_no=self.port, msg=None)
            port_test.signals.dataReady.connect(self.update_test_console)
            port_test.signals.done.connect(self.stop_streaming)

            self.pool.start(port_test)
            self.live_types[data_type] = port_test
        elif data_type == 'dummy motion':
            self._logger.log('Starting dummy motion plot', Logger.DEBUG)
            dummy_motion = DummyLiveMotion()
            dummy_motion.signals.dataReady.connect(self.update_plot)
            dummy_motion.signals.dataFinished.connect(self.stop_streaming)

            self.pool.start(dummy_motion)
            self.live_types[data_type] = dummy_motion
        else:
            None

    @pyqtSlot(str, list)
    def update_plot(self, data_type, data):
        if data_type == 'dummy motion':
            self._model.add_motion_data(data)

            if len(self._model.motion_data) % 2 == 0:
                self._view.update_motion_plot(self._model.motion_data)
            #if not self.timer.isActive():
            #   self.timer.start(20)
            #self.times.append(self.elap.restart())

    @pyqtSlot()
    def plot(self):
        self._view.update_motion_plot(self._model.motion_data)

    @pyqtSlot(str)
    def stop_streaming(self, caller):
        self._logger.log('Stopping stream for {}'.format(caller), Logger.DEBUG)
        self._model.reset_data()
        self.streaming = False

        #self.timer.stop()
        #self.profiler.print_stats(sort='time')
        #print('Plotted at {} Hz '.format(1000/mean(self.times)))
        #self.times = []

        for live_type, value in self.live_types.items():
            if value is not None and live_type == caller:
                value.streaming = self.streaming
                self.live_types[live_type] = None
