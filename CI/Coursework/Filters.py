import numpy as np
from scipy.ndimage.filters import gaussian_filter1d


class Filters:

    @staticmethod  # use np.clip
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
    def hanning(series):
        window = np.hanning(len(series))
        series *= window

    @staticmethod
    def fft(series, window=''):
        length = len(series)
        if window is 'hanning':
            series *= np.hanning(length)
        elif window is 'hamming':
            series *= np.hamming(length)
        elif window is 'blackman':
            series *= np.blackman(length)
        else:
            pass

        fft = np.fft.fft(series)
        freq = np.fft.fftfreq(length) * 25e3
        voltages = [np.abs(x)/length for x in fft]
        #phase = [np.arctan()]

        return [freq[0:int(length/2)], np.array(voltages[0:int(length/2):])]
