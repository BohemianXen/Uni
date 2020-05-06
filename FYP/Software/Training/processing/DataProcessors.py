import numpy as np
from Plotter import Plotter


class DataProcessors:
    def __init__(self):
        pass

    @staticmethod
    def bytearray_to_float(array):
        """Converts bytearrays into signed float arrays"""
        total_bytes = len(array[0])
        total_samples = int(total_bytes / 4)
        converted_array = []

        for packet in array:
            # Convert bytes from little endian 4-byte chunks and scale down from long to float
            parsed = [int.from_bytes(packet[i:i + 3], byteorder='little', signed=True) / 1000.0 for i in range(0, total_bytes, 4)]

            # Split each sample into its constituent acc x, y, z and gyro x,y, z values
            parsed_split = [parsed[i:i + 6] for i in range(0, total_samples, 6)]
            converted_array.extend(parsed_split)

        return converted_array

    @staticmethod
    def raw_normalise(data, transpose=True):
        """Normalises data using raw sensor limits then flatten series' to 1D (if not already)"""
        normalised = DataProcessors.normalise(data)

        if normalised is None:
            return None
        else:
            if transpose:
                normalised = normalised.T

            if len(data) != 1:
                normalised = normalised.flatten()

            return normalised

    @staticmethod
    def normalise(data):
        if len(data[0]) == 9:
            limits = np.array([4, 4, 4, 2000, 2000, 2000, 400, 400, 400])
        else:
            limits = np.array([4, 4, 4, 2000, 2000, 2000])

        normalised = np.array(data) / limits[:, ]
        if -1.0 <= np.min(normalised) and np.max(normalised) <= 1.0:
            return normalised
        else:
            return None


        return  # TODO: MinMaxScaler but only after splitting data!

    @staticmethod
    def smv(raw_data, smooth=False, plot=False, no_smv=False):
        data = DataProcessors.normalise(raw_data)  # np.array(raw_data)

        if data is None:
            return None

        acc_raw = data[:, :3].T
        gyro_raw = data[:, 3:].T
        acc_smoothed = acc_raw
        gyro_smoothed = gyro_raw

        if smooth:
            acc_smoothed = DataProcessors.smooth(acc_raw)
            gyro_smoothed = DataProcessors.smooth(gyro_raw)

        ax_std = np.std(acc_smoothed[0])
        ay_std = np.std(acc_smoothed[1])
        az_std = np.std(acc_smoothed[2])

        gx_std = np.std(gyro_smoothed[0])
        gy_std = np.std(gyro_smoothed[1])
        gz_std = np.std(gyro_smoothed[2])

        ax_mean = np.mean(acc_smoothed[0])
        ay_mean = np.mean(acc_smoothed[1])
        az_mean = np.mean(acc_smoothed[2])

        gx_mean = np.mean(gyro_smoothed[0])
        gy_mean = np.mean(gyro_smoothed[1])
        gz_mean = np.mean(gyro_smoothed[2])

        stds = np.array([ax_std, ay_std, az_std, gx_std, gy_std, gz_std])
        means = np.array([ax_mean, ay_mean, az_mean, gx_mean, gy_mean, gz_mean])  # TODO: Minimisation

        # Both for testing only; remember to adjust no. of inputs in SMVNeuralNet if used
        if plot:
            Plotter.pyplot_plot(acc_raw, acc_smoothed, gyro_raw, gyro_smoothed)
        if no_smv:
            acc_smoothed = acc_smoothed.T.flatten()
            gyro_smoothed = gyro_smoothed.T.flatten()
            return np.concatenate([acc_smoothed, gyro_smoothed])

        acc = np.sqrt(np.sum([ax_mean**2, ay_mean**2, az_mean**2]))
        gyro = np.sqrt(np.sum([gx_mean**2, gy_mean**2, gz_mean**2]))

        # acc_sum = np.sum(np.sqrt(np.sum(np.square(acc_smoothed.T), axis=1)))
        # gyro_sum = np.sum(np.sqrt(np.sum(np.square(gyro_smoothed.T), axis=1)))
        # acc_mags = np.sqrt(np.sum(np.square(acc_smoothed.T), axis=1))
        # gyro_mags = np.sqrt(np.sum(np.square(gyro_smoothed.T), axis=1))

        features = np.concatenate([stds, means, [acc], [gyro]])
        # print(features)

        return features

    @staticmethod
    def smooth(series, averaging_length=3, just_average=True):
        """Moving averages the series, optionallu removes the median from all values, and optionally applies window.
        Parameters:
            series(ndarray): The noisy input series.
            averaging_length(int, optional): The length of the moving average. Defaults to 4.
            just_average(bool, optional): Whether to just do the moving average stage only. Defaults to False.
        Returns:
            (ndarray): Smoothed input data.
        """

        smoothed = np.zeros_like(series)
        # Calculate moving average over valid indices
        for i in range(3):
            summed = np.cumsum(series[i, :])
            valid_range = summed[averaging_length:] - summed[:-averaging_length]
            summed[averaging_length:] = valid_range
            averaged = summed[averaging_length - 1:] / averaging_length
            smoothed[i] = np.concatenate([[averaged[0]]*(averaging_length-1), averaged])

        return smoothed

    @staticmethod
    def parse_train_data(train_data, outputs, shuffle):
        """Split data, labels, and targets into separate numpy arrays as necessary"""

        size = len(train_data)

        if size != 0:
            if shuffle:
                np.random.shuffle(train_data)  # Reduce data pool bias by shuffling

            data = np.zeros((size, len(train_data[0]) - 1), dtype=np.float32)
            labels = np.zeros(size)
            targets = np.zeros((size, outputs))  # + 0.01  # Initialise all targets to zero

            for i, sample in enumerate(train_data):
                data[i] = sample[1:]  # Remove label from data
                labels[i] = sample[0]
                targets[i][int(labels[i])] = 1  # 0.99  # Set ideal target index to 0.99

            return [data, targets]

    @staticmethod
    def mirror(data, mask=(1, 1, 1, 1, 1, 1)):
        mask = np.array(mask)
        return np.array(data) * mask[:, ]



    # @staticmethod
    # def raw_normalise(data, smooth=True, single=False):
    #     """Normalises data using raw sensor limits then flatten series' to 1D (if not already)"""
    #     normalised = DataProcessors.normalise(data)
    #     acc_raw = normalised[:, :3].T
    #     gyro_raw = normalised[:, 3:].T
    #
    #     if smooth:
    #         acc_raw = DataProcessors.smooth(acc_raw)
    #         gyro_raw = DataProcessors.smooth(gyro_raw)
    #
    #     smoothed = np.concatenate([acc_raw.T, gyro_raw.T])
    #
    #     if len(data) != 1:
    #         smoothed = smoothed.flatten()
    #     if single:
    #         smoothed = np.expand_dims(normalised, axis=0)  # For only querying one packet at a time
    #     return smoothed
