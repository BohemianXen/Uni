from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable, QObject, QThreadPool
from application.Logger import Logger
import serial
import serial.tools.list_ports
import time
import traceback


class StreamManagerSignals(QObject):
    writeComplete = pyqtSignal(bool)
    dataReady = pyqtSignal(list)
    testDataReady = pyqtSignal(bytes)
    done = pyqtSignal(str)

    def __init__(self):
        super(StreamManagerSignals, self).__init__()


class StreamManager(QRunnable):
    """Reads/writes to serial port."""

    def __init__(self, port_no, rate, msg, mode):
        super(StreamManager, self).__init__()
        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = StreamManagerSignals()
        self._streaming = False
        self._mode = mode
        self.port = None
        self.rate = rate
        timeout = 1
        self.msg = msg
        self.write_mode = True if self.msg is not None else False

        attempts = 3
        while attempts != 0 and self.port is None:
            try:
                self.port = serial.Serial('COM{}'.format(port_no), self.rate, timeout=timeout)
            except Exception as error:
                self._logger.log('Error ' + str(error), Logger.DEBUG)
                #print(traceback.format_exc())
            attempts -= 1
            time.sleep(3)

    @property
    def streaming(self):
        return self._streaming

    @streaming.setter
    def streaming(self, value):
        self._streaming = value

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        self._mode = value

    def run(self):
        """Overrides the QRunnable implementation to start a live motion thread."""
        device = self.get_device()
        self._logger.log('Starting new thread; live motion with {}'.format(device), Logger.DEBUG)

        self._streaming = True if self.port is not None else False
        if self.streaming:
            if not self.port.is_open:
                self.port.open()

            self.port.flush()
            self.get_data()
        #self.close_port()

    @staticmethod
    def get_device():
        ports = serial.tools.list_ports.comports()
        if len(ports) > 0:
            return ports[0].description
            """for port in ports:
                if port.description is not None:
                   return port.description"""
        return None

    def close_port(self):
        if self.port is not None and self.port.is_open:
            self.port.close()

    def get_data(self):
        while self.streaming:
            write_successful = False
            data = []
            if self.write_mode and self.msg is not None:
                try:
                    self.port.write(bytes([self.msg]))
                    write_successful = True
                    break
                except Exception as e:
                    self._logger.log(str(e), Logger.DEBUG)
                self.signals.testSuccessful.emit(write_successful)
            else:
                try:
                    line = self.port.readline()
                    if self.mode == 'test':
                        if line != bytes(b''):
                            self.signals.testDataReady.emit(line)
                        else:
                            self.signals.testDataReady.emit(bytes(b'sleeping...'))

                    else:
                        if line == bytes(b'0\r\n'):
                            data.append(line)
                            while data[-1] != bytes(b'\r\n'):  # len(data) != 19:
                                data.append(self.port.readline())
                            self.signals.dataReady.emit(data[:-1])
                except Exception as e:
                    self._logger.log(str(e), Logger.DEBUG)
                    break

        #self.signals.done.emit('live motion')


class DummyConnector(QObject):
    def __init__(self):
        pool = QThreadPool.globalInstance()
        test = StreamManager(port_no=4, rate=115200, msg=None)
        #test.signals.dataReady.connect(self.data_ready)
        test.setAutoDelete(False)
        pool.start(test)


    @pyqtSlot(list)
    def data_ready(self, data):
        vals = []
        for line in data:
            vals.append(int.from_bytes(line))
        print(vals)


if __name__ == '__main__':
    dummy_connector = DummyConnector()
    pool = QThreadPool.globalInstance()
    while pool.activeThreadCount() > 0:
        pool.waitForDone(1000)
