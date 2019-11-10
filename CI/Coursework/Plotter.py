import matplotlib.pyplot as plt
from numpy import linspace


class Plotter:

    def __init__(self, recording):
        self._recording = recording
        self._period = recording.period
        self._range = recording.range

    def plot_all(self, time=False):
        total_samples = len(self._recording.d)
        series = linspace(0, total_samples - 1, total_samples)
        if time:
            series *= self._period
        plt.plot(series, self._recording.d)
        plt.show()

    def plot(self, index, time=False):
        total_samples = (self._range * 2) + 1
        start = index - self._range
        stop = index + self._range
        series = linspace(start, stop, total_samples)
        if time:
            series *= self._period

        plt.plot(series, self._recording.d[start:stop + 1])
        plt.show()
