import serial
import serial.tools.list_ports
import csv


class SerialToCSV:
    def __init__(self, port_no=5, rate=115200, timeout=1,  samples=10):
        self.samples = samples
        self.data = []
        self.port = serial.Serial('COM{}'.format(port_no), rate, timeout=timeout)

        if self.port.is_open:
            self.port.flush()
        else:
            self.port.open()

    def stream(self):
        self.streaming = True
        with open('test.csv', 'w', newline='') as f:
            col_headers = ['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz']
            f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            f_writer.writerow(col_headers)

            while self.streaming and self.samples is not 0:
                try:
                    line = self.port.readline()
                    str_line = line.decode('utf-8').rstrip(',\r\n')
                    self.data.append(str_line)
                    print(str_line)
                    self.samples -= 1
                except Exception as e:
                    self.streaming = False
                    print(e)

    def write_data(self):
        with open('test.csv', 'w', newline='') as f:
            col_headers = ['ax', 'ay', 'az', 'gx', 'gy', 'gz', 'mx', 'my', 'mz']
            f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            f_writer.writerow(col_headers)
            for line in self.data:
                f_writer.writerow(line.split(','))


if __name__ == '__main__':
    params = {
        'port_no': 5,
        'rate': 115200,
        'timeout': 1,
        'samples': 10
    }
    serial_to_csv = SerialToCSV(params['port_no'] , params['rate'], params['timeout'])
    serial_to_csv.stream()
    serial_to_csv.write_data()
