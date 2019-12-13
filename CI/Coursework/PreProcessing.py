import numpy as np
from scipy.ndimage.filters import gaussian_filter1d


class PreProcessing:
    """Class of pre-processing algorithms and methods"""

    @staticmethod
    def smooth(series, averaging_length=4, window='', just_average=False):
        """Moving averages the series, optionallu removes the median from all values, and optionally applies window.
        Parameters:
            series(ndarray): The noisy input series.
            averaging_length(int, optional): The length of the moving average. Defaults to 4.
            window(str, optional): The type of window to be applied. Defaults to empty string (i.e. no window).
            just_average(bool, optional): Whether to just do the moving average stage only. Defaults to False.
        Returns:
            (ndarray): Smoothed input data.
        """

        # Calculate moving average over valid indices
        summed = np.cumsum(series)
        valid_range = summed[averaging_length:] - summed[:-averaging_length]
        summed[averaging_length:] = valid_range
        averaged = summed[averaging_length - 1:] / averaging_length  # divide each rolling sum by number of points considered
        if just_average:
            return averaged

        # Remove median to bring DC level down to around zero and pad to account for the lost samples when averaging earlier
        smoothed = np.subtract(averaged, np.median(averaged))
        smoothed = np.pad(smoothed, (0, averaging_length-1), mode='edge')

        # Apply window to series
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
        """Performs Fast Fourier Transform on a windowed series.
        Parameters:
            series(ndarray): The noisy input series.
            window(str, optional): The type of window to be applied. Defaults to hanning window.
        Returns:
            (ndarray): Half of the FFT frequencies and their respective voltages due to mirroring.
        """
        length = len(series)
        series = PreProcessing.smooth(series, window=window, averaging_length=2)  # Smooth the data

        # Apply fft and scale
        fft = np.fft.fft(series)
        freq = np.fft.fftfreq(length) * 25e3
        voltages = [np.abs(x)/length for x in fft]

        return [freq[0:int(length/2)], np.array(voltages[0:int(length/2):])]  # Return only half the spectrum

    @staticmethod
    def threshold(series, threshold_limit):
        """Not used - a hard thresholding method to remove noise above a certain level"""
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
        """Not used - an attempt at 1D gaussian noise filtering"""
        return gaussian_filter1d(series, sigma=std_dev)