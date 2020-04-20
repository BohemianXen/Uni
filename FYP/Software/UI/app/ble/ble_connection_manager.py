from PyQt5.QtCore import QElapsedTimer, QObject, pyqtSignal
import asyncio



UUIDs = {
    'data ready': ('a34984b9-7b89-4553-aced-242a0b289bbc', '4174c433-4064-4349-bfa2-009a432a24a4'),
    'imu': ('f9dd156e-f108-4139-925c-dd1f157cffa0', '41277a1b-b4f8-4ddc-871a-db0dd23a3a31'),
    'data send': ('ab36b3d9-12e4-4922-ac94-8873e8252045', '976aca21-135a-4dfa-b548-68308f7acceb'),
    'starting stream': ("05b7f95e-0d89-43da-973c-3aa5a67b6031", "20b35680-9cf5-4f41-bde9-308abbc3c019"),
    'prediction': ('e77f260c-813a-4f0b-bb63-4e4ee0c3a103', 'f29c6ec0-13ef-4266-9fb7-b32c0feec1b3')
}

params = {
    # 'address': 57:0F:6E:FA:4E:C9',
    'name': 'FallDetector',
    'total samples': 480,
    'sample length': 6,
    'packet length': 8
}


class ConnectionManagerSignals(QObject):
    connected = pyqtSignal(bool)
    startingStream = pyqtSignal(bool)
    progressUpdated = pyqtSignal(int)
    dataReady = pyqtSignal(list)

    def __init__(self):
        super(ConnectionManagerSignals, self).__init__()


class ConnectionManagerBLE(QObject):
    def __init__(self, caller=None, target_name='FallDetector'):
        super().__init__()
        self.name = self.__class__.__name__

        self.discovered_devices = None
        self.devices_found = {}
        self.target_address = None
        self.connected = False
        self.data = []  # zeros((total_samples, sample_length))
        self.current_packet = 0
        self._start_stream = False
        self.new_reading = False
        self.guess = None

        self.short_delay = 1.0  # 0.2

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

        async with BleakClient(self.target_address, loop=loop, timeout=5.0) as client:
            self.connected = await client.is_connected()
            print("Connected: {0}".format(self.connected))
            if self.connected:
                if self.caller is not None:
                    self.signals.connected.emit(True)
                self.force_disconnect = False
                print('Starting data transfer notification')

                await client.start_notify(UUIDs['starting stream'][1], self.starting_stream_notification_handler)

                await client.start_notify(UUIDs['prediction'][1], self.data_notification_handler)
                # await client.start_notify(UUIDs['data ready'][1], self.data_ready_notification_handler)
                # await client.set_disconnected_callback(self.disconnect_handler)

                self.new_reading = False
                print('Waiting for readings...')

                while self.connected:
                    if self.new_reading:  # self._total_samples: # len(self.data) == self._total_samples:

                        self.guess = int.from_bytes(data[0], byteorder='little', signed=False)

                        self.current_packet = False
                        self.data = []

                        self.delay = self.short_delay
                    else:
                        #loop.stop()

                        await client.stop_notify(UUIDs['prediction'][1])
                        return self.data[:]

                    if self.start_stream:
                        print('Starting recording through UI')
                        await client.write_gatt_char(UUIDs['data send'][1], bytearray([0x01]), response=True)  # TODO: Toggle off too
                        self.start_stream = False

                    self.connected = await client.is_connected() and not self.force_disconnect
                    #print('\nLooping ' + str(self.current_packet) + '\n')
                    await asyncio.sleep(self.delay, loop=loop)

                print('Stopping data transfer notification')
                await client.stop_notify(UUIDs['starting stream'][1])
                if not self.onboard_predict:
                    await client.stop_notify(UUIDs['imu'][1])
                else:
                    await client.stop_notify(UUIDs['prediction'][1])
                #await client.stop_notify(UUIDs['data ready'][1])
            else:
                print('Disconnected')
                if self.caller is not None:
                    self.signals.connected.emit(False)

    def starting_stream_notification_handler(self, sender, data):
        if int.from_bytes(data, byteorder='little', signed=False):
            if self.caller is not None:
                self.signals.startingStream.emit(True)
                #self.delay = self.long_delay

    def data_ready_notification_handler(self, sender, data):
        ready = int.from_bytes(data, byteorder='little', signed=False)
        print("Data ready: %d" % ready)
        self.delay = self.long_delay if ready else self.short_delay

    def data_notification_handler(self, sender, packet):
        """Simple notification handler which prints the data received."""

        self.data.append(packet)
        self.new_reading = True

        # print("Packet no. {0}: {1}".format(self.current_packet, self.data[-1]))
        self.start_stream = False


if __name__ == '__main__':
    pass
