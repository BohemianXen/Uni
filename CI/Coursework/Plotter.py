import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    def __init__(self, recording):
        self._colourmap = ('black', 'red', 'green', 'blue', 'orange')
        self._recording = recording
        self._period = recording.period
        self._range = recording.range

    def plot(self, center=200, time=False, all=False):
        total_samples = len(self._recording.d) if all else (self._range * 2) + 1
        start = 0 if all else center - self._range
        stop = total_samples - 1 if all else center + self._range
        series = np.linspace(start, stop, total_samples)

        if not all:
            [indexes, colours] = self.classify_series(series)
            
        if time:
            series *= self._period
            indexes *= self._period

        plt.clf()
        plt.plot(series, self._recording.d[start:stop + 1], color=self._colourmap[0])

        if len(indexes) > 0:
            plt.scatter(indexes, 0, color=colours)

        plt.show()

    def classify_series(self, series):
        indexes_in_series = list(filter(lambda x: x in self._recording.index, series))
        classes_in_series = [self._recording.classes[np.where(self._recording.index == x)] for x in indexes_in_series]
        class_colours = [self._colourmap[int(x)] for x in classes_in_series]
        return [np.array(indexes_in_series), class_colours]
