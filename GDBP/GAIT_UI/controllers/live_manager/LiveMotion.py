from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable, QObject, QThreadPool
from application.Logger import Logger
import serial
import serial.tools.list_ports
import time
import traceback


class LiveMotionSignals(QObject):
    writeComplete = pyqtSignal(bool)
    dataReady = pyqtSignal(list)
    done = pyqtSignal(str)

    def __init__(self):
        super(LiveMotionSignals, self).__init__()


class LiveMotion(QRunnable):
    """Reads/writes to serial port."""

    def __init__(self, port_no, rate, msg):
        super(LiveMotion, self).__init__()
        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = LiveMotionSignals()
        self._streaming = False
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
            time.sleep(1)

    @property
    def streaming(self):
        return self._streaming

    @streaming.setter
    def streaming(self, value):
        self._streaming = value

    def run(self):
        """Overrides the QRunnable implementation to start a live motion thread."""
        device = self.get_device()
        self._logger.log('Starting new thread; live motion with {}'.format(device), Logger.DEBUG)
        write_successful = False

        self._streaming = True if self.port is not None else False
        if self.streaming and not self.port.is_open:
            self.port.flush()
            self.port.open()

        while self.streaming:
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
                    if line == bytes(b'0\r\n'):
                        data.append(line)
                        while data[-1] != bytes(b'\r\n'): # len(data) != 19:
                            data.append(self.port.readline())
                        #raw = self.port.read(2)  # TODO: how many bytes need reading
                        #temp = [float(val.rstrip().decode('utf-8')) for val in data]
                        self.signals.dataReady.emit(data[:-1])

                        #print(self.port.in_waiting)
                except Exception as e:
                    self._logger.log(str(e), Logger.DEBUG)
                    break

        self.signals.done.emit('test')
        self._logger.log('Deleting live motion thread', Logger.DEBUG)
        self.close_port()

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


class DummyConnector(QObject):
    def __init__(self):
        pool = QThreadPool.globalInstance()
        test = LiveMotion(port_no=4, rate=115200, msg=None)
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
