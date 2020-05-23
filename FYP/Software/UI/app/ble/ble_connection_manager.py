import asyncio

UUIDs = {
    'data ready': ('a34984b9-7b89-4553-aced-242a0b289bbc', '4174c433-4064-4349-bfa2-009a432a24a4'),
    'imu': ('f9dd156e-f108-4139-925c-dd1f157cffa0', '41277a1b-b4f8-4ddc-871a-db0dd23a3a31'),
    'data send': ('ab36b3d9-12e4-4922-ac94-8873e8252045', '976aca21-135a-4dfa-b548-68308f7acceb'),
    'starting stream': ("05b7f95e-0d89-43da-973c-3aa5a67b6031", "20b35680-9cf5-4f41-bde9-308abbc3c019"),
    'prediction': ('e77f260c-813a-4f0b-bb63-4e4ee0c3a103', 'f29c6ec0-13ef-4266-9fb7-b32c0feec1b3')
}

params = {
    'name': 'FallDetector',
    'total samples': 480,
    'sample length': 6,
    'packet length': 8
}


class ConnectionManager:
    """ Connection Manager class. Handles the connection to a peripheral device and all subsequent data transfer."""
    def __init__(self, device=None, target_name='FallDetector', timeout=2.0):
        super().__init__()
        self.name = self.__class__.__name__
        self.device = device
        self.timeout = timeout
        self.target_name = target_name
        self.discovered_devices = None
        self.devices_found = {}
        self.target_address = None
        self.connected = False
        self.streaming = False
        self._start_stream = False

        self.action = None
        self.short_delay = 1.0  # 0.2

    @property
    def start_stream(self):
        return self._start_stream

    @start_stream.setter
    def start_stream(self, value):
        self._start_stream = value

    async def discover_devices(self):
        """Finds and prints details of all nearby Bluetooth devices."""
        from bleak import discover

        self.discovered_devices = await discover()
        if len(self.discovered_devices) > 0:
            return self.find_detector()

    def find_detector(self):
        """Specifically finds a 'FallDetector' named device and saves its name and address."""
        self.target_address = None
        try:
            for device in self.discovered_devices:
                self.devices_found[device.address] = device.name
                if self.target_name in device.name:
                    self.target_address = device.address
        except Exception as error:
            print(str(error))

        return [self.target_name, self.target_address]

    def list_found_devices(self):
        """Alternate method for printing all found devices when in the devices_found parameter."""

        if len(self.devices_found) != 0:
            for address in self.devices_found.keys():
                print('%s: %s' % (self.devices_found[address], address))

    # TODO: Add attempt counter
    async def connect(self, loop):
        """Connects to a FallDetector, subscribes to relevant notifications, and manages the active stream."""
        from bleak import BleakClient
        from bleak.exc import BleakDotNetTaskError

        async with BleakClient(self.target_address, loop=loop, timeout=self.timeout) as client:
            self.connected = await client.is_connected()
            print("Connected: {0}".format(self.connected))

            if self.connected:

                print('Starting data transfer notification')

                await client.start_notify(UUIDs['starting stream'][1], self.starting_stream_notification_handler)
                await client.start_notify(UUIDs['prediction'][1], self.data_notification_handler)

                self.streaming = False
                self.action = 1
                print('Waiting for readings...')

                while self.connected:
                    if self.start_stream:
                        print('Starting recording through UI')
                        await client.write_gatt_char(UUIDs['data send'][1], bytearray([0x01]), response=True)
                        self.start_stream = False
                        self.streaming = True
                    self.connected = await client.is_connected()
                    await asyncio.sleep(self.short_delay, loop=loop)

                print('Stopping data transfer notification')
                try:
                    self.streaming = False
                    await client.stop_notify(UUIDs['starting stream'][1])
                    await client.stop_notify(UUIDs['prediction'][1])
                except BleakDotNetTaskError as e:
                    print(e)

            else:
                self.connected = False

    def starting_stream_notification_handler(self, sender, data):
        """Notification handler for when the user toggles the stream using the device pushbutton."""

        if int.from_bytes(data, byteorder='little', signed=False):
            self.streaming = True
        else:
            self.streaming = False

    def data_notification_handler(self, sender, packet):
        """Notfication handler for new predictions."""

        self.action = int.from_bytes(packet, byteorder='little', signed=False) + 1
        self.streaming = True
        print(self.action)

        self.start_stream = False
