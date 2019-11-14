from Recording import Recording
from Filters import Filters
import numpy as np
import matplotlib.pyplot as plt
# import PyQt5


def plot(recording, center=200, time=False, all=False):
    plt.figure(1)
    [x_axis, voltages] = recording.slice(center, all)

    if not all or len(x_axis) < 1000:
        [indexes, colours] = classify_series(recording, x_axis)

    if time:
        x_axis *= recording.period
        indexes *= recording.period

    plt.plot(x_axis, voltages, color=recording.colourmap[0])

    if len(indexes) > 0:
        for i in range(len(indexes)):
            plt.scatter(indexes[i], 0, color=colours[i])


def plot_fft(freq, amplitude):
    plt.figure(2)
    #plt.ylim(top=np.max(amplitude))
    plt.bar(freq, amplitude, width=10)


def classify_series(recording, x):
    indexes_in_x = list(filter(lambda y: y in recording.index, x))
    classes_in_x = [recording.classes[np.where(recording.index == y)] for y in indexes_in_x]
    class_colours = [recording.colourmap[int(y)] for y in classes_in_x]
    return [np.array(indexes_in_x), class_colours]


def class_test(recording, target):
    for i in range(len(recording.classes)):
        if recording.classes[i] == target:
            test_index = recording.index[i]
            plot(recording, center=test_index)

            filtered = recording.__copy__()
            filtered.colourmap = 'pink'
            index = filtered.slice(test_index, copy=False)[1]
            Filters.hanning(index)
            plot(filtered, center=test_index)
            plt.show()

            [fft_freq, fft_voltages] = Filters.fft(index)
            plot_fft(fft_freq, fft_voltages)
            plt.show()
            
            
if __name__ == '__main__':
    training_set = Recording(filename='training')
    #test_index = training_set.index[210]
    test_class = 1
    class_test(training_set, test_class)
