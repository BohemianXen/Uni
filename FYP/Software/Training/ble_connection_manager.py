from PyQt5.QtCore import QElapsedTimer, QObject
import asyncio
#from bleak import discover, BleakClient
from csv_writer import SerialToCSV

UUIDs = {
    'data_ready': ('a34984b9-7b89-4553-aced-242a0b289bbc', '4174c433-4064-4349-bfa2-009a432a24a4'),
    'imu': ('f9dd156e-f108-4139-925c-dd1f157cffa0', '41277a1b-b4f8-4ddc-871a-db0dd23a3a31'),
    'data_send': ('ab36b3d9-12e4-4922-ac94-8873e8252045', '976aca21-135a-4dfa-b548-68308f7acceb')
}

params = {
    # 'address': 57:0F:6E:FA:4E:C9',
    'name': 'FallDetector',
    'samples': 238,
    'length': 9
}


class ConnectionManagerBLE(QObject):

    def __init__(self, target_name='FallDetector', total_samples=238, payload_length=9):
        super().__init__()
        self.target_name = target_name
        self.total_samples = total_samples
        self.payload_length = payload_length
        self.devices_found = {}
        self.target_address = None
        self.connected = False
        self.data = []  # zeros((total_samples, payload_length))
        self.current_sample = 0
        #self.loop = asyncio.get_event_loop()

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
            self.connected = await client.is_connected()
            print("Connected: {0}".format(self.connected))

            if self.connected:
                self.current_sample = 0
                await client.start_notify(UUIDs['imu'][1], self.imu_notification_handler)
                print('Waiting for readings...')
                while self.connected and self.current_sample != self.total_samples:
                    self.connected = await client.is_connected()
                    await asyncio.sleep(0.1, loop=loop)
                await client.stop_notify(UUIDs['imu'][1])
                return self.data

    def imu_notification_handler(self, sender, data):
        """Simple notification handler which prints the data received."""
        parsed_data = bytearray_to_int(data)
        self.data.append(parsed_data)
        print("{0}: {1}".format(sender, parsed_data))
        self.current_sample += 1


def bytearray_to_int(array):
    parsed = [int.from_bytes(array[i:i+3], byteorder='little', signed=True) for i in range(0, 36, 4)]
    return [x/1000.0 for x in parsed]


if __name__ == '__main__':
    #from bleak import discover, BleakClient
    connection_manager = ConnectionManagerBLE(target_name=params['name'], total_samples=params['samples'], payload_length=params['length'])

    loop = asyncio.get_event_loop()
    loop.run_until_complete(connection_manager.discover_devices())
    found = connection_manager.find_detector()

    if found != -1:
        print('\nConnecting to %s (with address %s)' % (connection_manager.target_name, connection_manager.target_address))
        loop = asyncio.get_event_loop()
        data = loop.run_until_complete(connection_manager.connect(loop))
        success = SerialToCSV.write_data(data)

        if success != -1:
            print('Successfully wrote %d entries' % success)
        else:
            print('Failed to save data')
