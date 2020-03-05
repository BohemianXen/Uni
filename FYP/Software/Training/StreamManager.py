import asyncio
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot
from Logger import Logger


class StreamManagerSignals(QObject):
    deviceFound = pyqtSignal(bool)
    dataReady = pyqtSignal(list)
    connected = pyqtSignal(bool)

    def __init__(self):
        super(StreamManagerSignals, self).__init__()


class StreamManager(QRunnable):
    def __init__(self, params, connection_manager):
        super(StreamManager, self).__init__()
        self.name = self.__class__.__name__
        self._logger = Logger(self.name)
        self.signals = StreamManagerSignals()
        self._params = params
        self._connection_manager = connection_manager

    def run(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
        loop.run_until_complete(self._connection_manager.discover_devices())
        found = self._connection_manager.find_detector()

        if found != -1:
            print('\nConnecting to %s (with address %s)' % (
            self._connection_manager.target_name, self._connection_manager.target_address))
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._connection_manager.connect(loop))

        else:
            self._connection_manager.signals.connected.emit(False)
            print('Could not find a fall detector device')

        loop.stop()
