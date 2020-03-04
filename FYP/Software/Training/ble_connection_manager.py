from PyQt5.QtCore import QElapsedTimer, QObject, pyqtSignal
from Logger import Logger
import asyncio
from processing.CSVConverters import CSVConverters

UUIDs = {
    'data_ready': ('a34984b9-7b89-4553-aced-242a0b289bbc', '4174c433-4064-4349-bfa2-009a432a24a4'),
    'imu': ('f9dd156e-f108-4139-925c-dd1f157cffa0', '41277a1b-b4f8-4ddc-871a-db0dd23a3a31'),
    'data_send': ('ab36b3d9-12e4-4922-ac94-8873e8252045', '976aca21-135a-4dfa-b548-68308f7acceb')
}

params = {
    # 'address': 57:0F:6E:FA:4E:C9',
    'name': 'FallDetector',
    'total samples': 480,
    'sample length': 6,
    'packet length': 4
}


class ConnectionManagerSignals(QObject):
    dataReady = pyqtSignal(list)
    connected = pyqtSignal(bool)
    progressUpdated = pyqtSignal(int)

    def __init__(self):
        super(ConnectionManagerSignals, self).__init__()


class ConnectionManagerBLE(QObject):
    def __init__(self, caller=None, target_name='FallDetector', total_samples=480, sample_length=6, packet_length=4):
        super().__init__()
        self.name = self.__class__.__name__
        self._logger = Logger(self.name)

        self.caller = caller
        self.target_name = target_name
        self.total_samples = total_samples
        self.sample_length = sample_length
        self.packet_length = packet_length
        self.total_packets = int(self.total_samples/self.packet_length)

        self.devices_found = {}
        self.target_address = None
        self.connected = False
        self.data = []  # zeros((total_samples, sample_length))
        self.current_packet = 0
        self._start_stream = False

        self.short_delay = 0.1
        self.long_delay = 0.025 * self.total_samples

        if self.caller is not None:
            self.signals = ConnectionManagerSignals()
            self.signals.connected.connect(self.caller.device_connected)
            self.signals.dataReady.connect(self.caller.data_ready)
            self.signals.progressUpdated.connect(self.caller.update_progress)

    @property
    def start_stream(self):
        return self._start_stream

    @start_stream.setter
    def start_stream(self, value):
        self._start_stream = value

    async def discover_devices(self):
        from bleak import discover
        self.discovered_devices = await discover()
        for d in self.discovered_devices:
            print(d)

    def find_detector(self):
        try:
            # places discovered devices into a dictionary in address: name format
            for device in self.discovered_devices:
                self.devices_found[device.address] = device.name
                if self.target_name in device.name:
                    self.target_address = device.address
        except Exception as error:
            print(str(error))
            return -1

        if self.target_address is not None:
            return len(self.discovered_devices)
        else:
            return -1

    def list_found_devices(self):
        if len(self.devices_found) != 0:
            for address in self.devices_found.keys():
                print('%s: %s' % (self.devices_found[address], address))

    # TODO: Add attempt counter
    async def connect(self, loop):
        from bleak import BleakClient

        async with BleakClient(self.target_address, loop=loop) as client:
            self._client = client
            self.connected = await client.is_connected()
            print("Connected: {0}".format(self.connected))
            if self.connected:
                if self.caller is not None:
                    self.signals.connected.emit(True)

                print('Starting data transfer notification')
                await client.start_notify(UUIDs['imu'][1], self.imu_notification_handler)

                self.current_packet = 0
                print('Waiting for readings...')
                while self.connected:
                    delay = self.short_delay
                    if self.current_packet == self.total_packets: # self.total_samples: # len(self.data) == self.total_samples:
                        if self.caller is not None:
                            self.signals.dataReady.emit(self.data)
                            print('Done transferring data, saving to csv')
                            self.current_packet = 0
                            self.start_stream = False
                        else:
                            #loop.stop()
                            await client.stop_notify(UUIDs['imu'][1])
                            return self.data

                    if self.start_stream:
                        print('Starting recording through UI')
                        await client.write_gatt_char(UUIDs['data_send'][1], bytearray([0x01]), response=True)

                    self.connected = await client.is_connected()
                    await asyncio.sleep(delay, loop=loop)

                print('Stopping data transfer notification')
                await client.stop_notify(UUIDs['imu'][1])
                #return self.data
            else:
                print('Disconnected')
                if self.caller is not None:
                    self.signals.connected.emit(False)

    def imu_notification_handler(self, sender, data):
        """Simple notification handler which prints the data received."""
        parsed_data = bytearray_to_int(data, len(data), int(len(data)/4))
        for entry in parsed_data:
            self.data.append(entry)

        self.current_packet += 1
        #print("Packet no. {0}: {1}".format(self.current_packet, parsed_data))

        if self.caller is not None:
            self.signals.progressUpdated.emit(self.current_packet)
        self.start_stream = False


def bytearray_to_int(array, total_bytes, total_samples):
    parsed = [int.from_bytes(array[i:i+3], byteorder='little', signed=True)/1000.0 for i in range(0, total_bytes, 4)]
    parsed_split = [parsed[i:i + 6] for i in range(0, total_samples, 6)]
    return parsed_split


if __name__ == '__main__':

    connection_manager = ConnectionManagerBLE(target_name=params['name'], total_samples=params['total samples'],
                                              sample_length=params['sample length'],  packet_length=params['packet length'])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(connection_manager.discover_devices())
    found = connection_manager.find_detector()

    if found != -1:
        print('\nConnecting to %s (with address %s)' % (connection_manager.target_name, connection_manager.target_address))
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(connection_manager.connect(loop))
        #loop.stop()
        success = CSVConverters.write_data(data)

        if success != -1:
            print('Successfully wrote %d entries' % success)
        else:
            print('Failed to save data')
    exit(0)
