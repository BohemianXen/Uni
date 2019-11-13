import numpy as np
from scipy.ndimage.filters import gaussian_filter1d

class Filters:

    @staticmethod
    def threshold(series, threshold_limit):
        length = len(series)
        new_series = np.copy(series)
        for sample in range(0,  length):
            if series[sample] <= threshold_limit:
                new_series[sample] = 0
            else:
                new_series[sample] -= threshold_limit

        return new_series

    @staticmethod
    def gaussian(series, std_dev):
        return gaussian_filter1d(series, sigma=std_dev)

    @staticmethod
    def fft(series):
        test = np.fft.fft(series)
        return np.fft.rfft(series)
