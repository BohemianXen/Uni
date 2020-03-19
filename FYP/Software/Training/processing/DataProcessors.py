import numpy as np


class DataProcessors:
    def __init__(self):
        None

    @staticmethod
    def raw_normalise(data, single=False):
        """Normalises data using raw sensor limits then flatten series' to 1D (if not already)"""
        if len(data[0]) == 9:
            limits = np.array([4, 4, 4, 2000, 2000, 2000, 400, 400, 400])
        else:
            limits = np.array([4, 4, 4, 2000, 2000, 2000])

        normalised = np.array(data, dtype=np.float32) / limits[:, ]  # TODO: MinMaxScaler but only after splitting data!
        if len(data) != 1:
            normalised = normalised.flatten()
        if single:
            normalised = np.expand_dims(normalised, axis=0)  # For only querying one packet at a time
        return normalised

    @staticmethod
    def parse_train_data(train_data, outputs, shuffle):
        """Split data, labels, and targets into separate numppy arrays as necessary"""

        size = len(train_data)

        if size != 0:
            if shuffle:
                np.random.shuffle(train_data)  # Reduce data pool bias by shuffling

            data = np.zeros((size, len(train_data[0]) - 1), dtype=np.float32)
            labels = np.zeros(size)
            targets = np.zeros((size, outputs)) + 0.01  # Initialise all targets to zero

            for i, sample in enumerate(train_data):
                data[i] = sample[1:]  # Remove label from data
                labels[i] = sample[0]
                targets[i][int(labels[i])] = 0.99  # Set ideal target index to 0.99

            return [data, targets]

    @staticmethod
    def bytearray_to_float(array):
        """Converts bytearrays into signed float arrays"""
        total_bytes = len(array[0])
        total_samples = int(total_bytes / 4)
        converted_array = []

        for packet in array:
            # Convert bytes in little endian 4-byte chunks and scale from long to float
            parsed = [int.from_bytes(packet[i:i + 3], byteorder='little', signed=True) / 1000.0 for i in range(0, total_bytes, 4)]

            # Split into each separate sensor sample and return
            parsed_split = [parsed[i:i + 6] for i in range(0, total_samples, 6)]
            converted_array.extend(parsed_split)

        return converted_array
