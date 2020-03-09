import numpy as np


class DataProcessors:
    def __init__(self):
        None

    @staticmethod
    def parse_train_data(train_data, outputs, shuffle):
        size = len(train_data)
        if size != 0:
            if shuffle:
                np.random.shuffle(train_data)
            data = np.zeros((size, len(train_data[0]) - 1), dtype=np.float32)
            labels = np.zeros(size)
            targets = np.zeros((size, outputs)) + 0.01
            for i, sample in enumerate(train_data):
                data[i] = sample[1:]
                labels[i] = sample[0]
                targets[i][int(labels[i])] = 0.99
            return [data, targets]

    @staticmethod
    def bytearray_to_int(array): #, total_bytes, total_samples):
        total_bytes = len(array[0])
        total_samples = int(total_bytes / 4)
        converted_array = []
        for packet in array:

            parsed = [int.from_bytes(packet[i:i + 3], byteorder='little', signed=True) / 1000.0 for i in range(0, total_bytes, 4)]
            parsed_split = [parsed[i:i + 6] for i in range(0, total_samples, 6)]
            converted_array.extend(parsed_split)
        return converted_array