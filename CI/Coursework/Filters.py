import numpy as np


class Filters:
    def __init__(self):
        self._threshold_limit = 0.5

    @property
    def threshold_limit(self):
        return self._threshold_limit

    @threshold_limit.setter
    def threshold_limit(self, new_threshold):
        self._threshold_limit = new_threshold

    def threshold(self, series):
        length = len(series)
        new_series = np.copy(series)
        for sample in range(0,  length):
            if series[sample] < self._threshold_limit:
                new_series[sample] = 0

        return new_series
