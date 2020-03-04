import csv
from datetime import datetime
from os import path, listdir
import numpy as np


class CSVConverters:
    def __init__(self):
       None

    @staticmethod
    def write_data(data, root='General'):
        written = 0
        with open('Training Data\\{0}\\{1}.csv'.format(root, datetime.now().strftime("%Y-%m-%d %H_%M_%S")), 'w', newline='') as f:
            col_headers = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']  #  'mx', 'my', 'mz']
            if len(data[0]) == 9:
                col_headers.extend(['mx', 'my', 'mz'])
            try:
                f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                f_writer.writerow(col_headers)
                for line in data:
                    f_writer.writerow(line)
                    written += 1
            except Exception as e:
                print(str(e))
                return -1
        return written

    @staticmethod
    def csv_to_list(filename, remove_mag=True):
        data = []
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                if row[0] != 'ax':
                    if remove_mag and len(row) == 9:
                        data.append([float(val) for val in row[:-3]])
                    else:
                        data.append([float(val) for val in row])
        return data




class Tests:
    def __init__(self):
        None

    @staticmethod
    def test_directories():
        None

if __name__ == '__main__':
    test = r'C:\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data'