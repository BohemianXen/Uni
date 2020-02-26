import bluetooth, traceback
from PyQt5.QtCore import QElapsedTimer


class ConnectionManager:
    def __init__(self, target_name='FallDetector'):
        self.devices_found = {}
        self.target_name = target_name
        self.target_address = None

    def find_detector(self):
        try:
            discovered_devices = bluetooth.discover_devices(lookup_names=True)  # discover nearby/paired devices

            # places discovered devices into a dictionary in address: name format
            for (address, name) in discovered_devices:
                self.devices_found[address] = name
                if self.target_name in name:
                    self.target_address = address
        except bluetooth.BluetoothError as error:
            print(str(error))
            return -1

        if len(discovered_devices) != 0:
            return len(discovered_devices)

    def connect_to_target(self):
        if self.target_address is not None:
            try:
                device_found = bluetooth.lookup_name(self.target_address)
                if device_found is None:
                    print('Could not re-discover target')
                else:
                    print('Re-discovered target, scanning services')

                    timer = QElapsedTimer()
                    timer.start()
                    services = bluetooth.find_service(address=self.target_address)
                    scan_time = timer.elapsed()
                    print('Completed scan in {} ms'.format(scan_time))

                    if len(services) > 0:
                        print("Found {} services on {}".format(len(services), self.target_name))
                        connection_complete = True
                    else:
                        print("No services found")

                    for service in services:
                        print("Service Name: {}".format(service["name"]))
                        print("    Host:        {}".format(service["host"]))
                        print("    Description: {}".format(service["description"]))
                        print("    Provided By: {}".format(service["provider"]))
                        print("    Protocol:    {}".format(service["protocol"]))
                        print("    Channel/PSM: {}".format(service["port"]))
                        print("    Service Classes: {}".format(service["service-classes"]))
                        print("    Profiles:    {}".format(service["profiles"]))
                        print("    Service ID:  {}".format(service["service-id"]))

            except bluetooth.BluetoothError as error:
                print(str(error))

            except OSError:
                print('Exception encountered while searching for devices')
                print(traceback.format_exc())

    def list_found_devices(self):
        if len(self.devices_found) != 0:
            for address in self.devices_found.keys():
                print('%s: %s' % (self.devices_found[address], address))


if __name__ == '__main__':
    connection_manager = ConnectionManager()
    found = connection_manager.find_detector()
    if found != -1:
        print('Found %d devices:' % found)
        connection_manager.list_found_devices()
        connection_manager.connect_to_target()
    else:
        print('Could not find a Fall Detector nearby')
        exit(0)
