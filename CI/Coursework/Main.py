from Recording import Recording
from Plotter import Plotter
from Filters import Filters
import numpy as np
import matplotlib.pyplot as plt
# import PyQt5


def plot(recording, center=200, time=False, all=False):
    total_samples = len(recording.d) if all else (recording.range * 2) + 1
    start = 0 if all else center - recording.range
    stop = total_samples - 1 if all else center + recording.range

    if start < 0:
        start = 0

    if stop > len(recording.d):
        stop = len(recording.d) - 1

    x = np.linspace(start, stop, total_samples)
    voltage = recording.d[start:stop + 1]

    if not all or len(x) < 1000:
        [indexes, colours] = classify_series(recording, x)

    if time:
        x *= recording.period
        indexes *= recording.period

    plt.plot(x, voltage, color=recording.colourmap[0])

    if len(indexes) > 0:
        for i in range(len(indexes)):
            plt.scatter(indexes[i], 0, color=colours[i])


def classify_series(recording, x):
    indexes_in_x = list(filter(lambda y: y in recording.index, x))
    classes_in_x = [recording.classes[np.where(recording.index == y)] for y in indexes_in_x]
    class_colours = [recording.colourmap[int(y)] for y in classes_in_x]
    return [np.array(indexes_in_x), class_colours]


if __name__ == '__main__':
    training_set = Recording(filename='training')
    test_index = training_set.index[210]

    training_thresh = training_set.__copy__()
    training_thresh.colourmap = 'pink'
    training_thresh.d = Filters.threshold(training_thresh.d, 0.5)
    training_fft = training_thresh.__copy__()
    training_fft.d = Filters.fft(training_fft.slice(test_index)[1])

    plot(training_set, center=test_index)
    plot(training_thresh, test_index)
    plt.show()
    plot(training_fft, all=True)
    plt.show()

    print(training_set.d[test_index])
