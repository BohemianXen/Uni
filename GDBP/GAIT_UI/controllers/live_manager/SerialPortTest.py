from PyQt5.QtCore import pyqtSignal, pyqtSlot, QRunnable, QObject, QThreadPool
from application.Logger import Logger
import serial
import serial.tools.list_ports
import time
import traceback


class SerialPortTestSignals(QObject):
    writeComplete = pyqtSignal(bool)
    dataReady = pyqtSignal(bytes)
    done = pyqtSignal(str)

    def __init__(self):
        super(SerialPortTestSignals, self).__init__()


class SerialPortTest(QRunnable):
    """Reads/writes to serial port."""

    def __init__(self, port_no, rate, msg):
        super(SerialPortTest, self).__init__()
        self.name = __class__.__name__
        self._logger = Logger(self.name)
        self.signals = SerialPortTestSignals()
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
                # print(traceback.format_exc())
            attempts -= 1
            time.sleep(timeout)

    @property
    def streaming(self):
        return self._streaming

    @streaming.setter
    def streaming(self, value):
        self._streaming = value

    def run(self):
        """Overrides the QRunnable implementation to start a serial port connection thread."""
        device = self.get_device()
        self._logger.log('Starting new thread; port test with {}'.format(device), Logger.DEBUG)
        write_successful = False

        self._streaming = True if self.port is not None else False
        if self.streaming and not self.port.is_open:
            self.port.flush()
            self.port.open()

        while self.streaming:
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
                    data = self.port.readline()
                    #raw = self.port.read(2)  # TODO: how many bytes need reading
                    self.signals.dataReady.emit(data)
                    #print(self.port.in_waiting)
                except Exception as e:
                    self._logger.log(str(e), Logger.DEBUG)
                    break

        self.signals.done.emit('test')
        self._logger.log('Deleting port test thread', Logger.DEBUG)
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
        test = SerialPortTest(port_no=3, msg=None)
        test.signals.dataReady.connect(self.data_ready)
        test.setAutoDelete(False)
        pool.start(test)

    #@pyqtSlot(bytes)
    def data_ready(self, data):
        val = int.from_bytes(data)
        print(val)


if __name__ == '__main__':
    dummy_connector = DummyConnector()
    pool = QThreadPool.globalInstance()
    while pool.activeThreadCount() > 0:
        pool.waitForDone(1000)
        #print(pool.activeThreadCount())
