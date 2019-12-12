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
    def smooth(series, averaging_length=4, window='', just_average=False):
        summed = np.cumsum(series)
        valid_range = summed[averaging_length:] - summed[:-averaging_length]
        summed[averaging_length:] = valid_range
        averaged = summed[averaging_length - 1:] / averaging_length

        if just_average:
            return averaged

        smoothed = np.subtract(averaged, np.median(averaged))
        smoothed = np.pad(smoothed, (0, averaging_length-1), mode='edge')

        if window is 'hanning':
            smoothed *= np.hanning(len(smoothed))
        elif window is 'hamming':
            smoothed *= np.hamming(len(smoothed))
        elif window is 'blackman':
            smoothed *= np.blackman(len(smoothed))
        else:
            pass

        return smoothed

    @staticmethod
    def fft(series, window='hanning'):
        length = len(series)
        series = Filters.smooth(series, window=window, averaging_length=3)
        fft = np.fft.fft(series)
        freq = np.fft.fftfreq(length) * 25e3
        voltages = [np.abs(x)/length for x in fft]
        #phase = [np.arctan()]

        return [freq[0:int(length/2)], np.array(voltages[0:int(length/2):])]
