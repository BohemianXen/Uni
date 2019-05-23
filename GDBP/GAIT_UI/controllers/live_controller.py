from PyQt5.QtCore import QObject, pyqtSlot, QThreadPool, QTimer, QElapsedTimer
from application.Logger import Logger
from data_processors.Converters import Converters
from controllers.live_manager.SerialPortTest import SerialPortTest
from controllers.live_manager.DummyLiveMotion import DummyLiveMotion
from controllers.live_manager.DummyLiveMotion1 import DummyLiveMotion1
from controllers.live_manager.LiveMotion import LiveMotion
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

        self.dummy_live_mode = True

        self.streaming = False
        self.dummy_motion = None
        self.port_test = None

        self.port = 4
        self.rate = 115200

        # Debug Only
        """self.port_test = SerialPortTest(port_no=self.port, msg=None)
        self.uuid = 0x1200
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

    @pyqtSlot(str)
    def start_stream(self, data_type):
        self.streaming = True

        if data_type == 'test' and len(serial.tools.list_ports.comports()) > 0:
            self._logger.log('Starting port test', Logger.DEBUG)
            port_test = SerialPortTest(port_no=self.port, rate=self.rate, msg=None)
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
        elif data_type == 'live motion':
            self._logger.log('Starting live motion', Logger.DEBUG)

            if not self.dummy_live_mode and len(serial.tools.list_ports.comports()) > 0:
                live_motion = LiveMotion(port_no=self.port, rate=self.rate, msg=None)
            else:
                live_motion = DummyLiveMotion1()
            live_motion.signals.dataReady.connect(self.live_plot)
            live_motion.signals.done.connect(self.stop_streaming)

            self.pool.start(live_motion)
            self.live_types[data_type] = live_motion
        else:
            None

    @pyqtSlot(bytes)
    def update_test_console(self, message):
        try:
            message = message.rstrip()
            self._view.update_test_console(message.decode('utf-8'))
        except Exception as e:
            print(str(e))
            pass

    @pyqtSlot(str, list)
    def update_plot(self, data_type, data):
        if data_type == 'dummy motion':
            self._model.add_motion_data(type=0, new_data=data)

            if len(self._model.motion_data) % 2 == 0:
                self._view.update_dummy_plot(self._model.motion_data)
            #if not self.timer.isActive():
            #   self.timer.start(20)
            #self.times.append(self.elap.restart())

    # Test Only
    @pyqtSlot()
    def plot(self):
        self._view.update_dummy_plot(self._model.motion_data)

    @pyqtSlot(list)
    def live_plot(self, data):
        # TODO: Test port switch fix with device
        # TODO: Invalid packet length
        length = len(data)
        if not self.dummy_live_mode:
            data = [float(val.rstrip().decode('utf-8')) for val in data]
        else:
            data = [float(val.rstrip()) for val in data]
        if length >= 13:
            self._model.add_uv_data(data[13])

        if length >= 25:
            indices = [21, 23, 25, 15, 17, 19]
            self._model.add_motion_data(type=1, new_data=[data[i] for i in indices])

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

        self._model.reset_data()
