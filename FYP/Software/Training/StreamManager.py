import asyncio
from PyQt5.QtCore import QRunnable
from Logger import Logger
from ble_connection_manager import ConnectionManagerBLE
from csv_writer import SerialToCSV


class StreamManager(QRunnable):
    def __init__(self, params, connection_manager):
        super(StreamManager, self).__init__()
        self.name = self.__class__.__name__
        self._logger = Logger(self.name)
        self._params = params
        self._connection_manager = connection_manager


    def run(self) -> None:
        #connection_manager = ConnectionManagerBLE(target_name=self._params['name'], total_samples=self._params['samples'],
        #                                          payload_length=self._params['length'])
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        #time.sleep(2)
        loop = asyncio.get_event_loop()
        loop.set_debug(False)
        loop.run_until_complete(self._connection_manager.discover_devices())
        found = self._connection_manager.find_detector()

        if found != -1:
            print('\nConnecting to %s (with address %s)' % (
            self._connection_manager.target_name, self._connection_manager.target_address))
            #loop = asyncio.get_event_loop()
            data = loop.run_until_complete(self._connection_manager.connect(loop))
            success = SerialToCSV.write_data(data)

            if success != -1:
                print('Successfully wrote %d entries' % success)
            else:
                print('Failed to save data')
            loop.close()

