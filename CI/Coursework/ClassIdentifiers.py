from Recording import Recording
from Filters import Filters
from NeuralNetwork import NeuralNetwork
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


def train_classes(recording, n, reps):
    # train the neural network on each training sample
    filtered = recording.__copy__()
    while reps > 0:
        for i in range(len(recording.index)):
            series = filtered.slice(recording.index[i], copy=True)[1]
            [fft_freq, fft_voltages] = Filters.fft(series, recording.window)
            targets = np.zeros(n.o_nodes) + 0.01
            targets[recording.classes[i]-1] = 0.99
            n.train(fft_voltages, targets)
            reps -= 1


def test_net(recording, n):
    scorecard = []
    incorrect = []
    guessed = []
    for i in range(len(recording.index)):
        series = recording.slice(recording.index[i], copy=True)[1]
        [fft_freq, fft_voltages] = Filters.fft(series, recording.window)
        outputs = n.query(fft_voltages)
        guess = np.argmax(outputs) + 1
        correct_class = recording.classes[i]

        if guess == correct_class:
            scorecard.append(1)
        else:
            scorecard.append(0)
            incorrect.append(correct_class)
            guessed.append(guess)

    print('Net performance: %.2f' % (scorecard.count(1)/len(scorecard) * 100.0))
    print(np.count_nonzero(recording.classes == 1), np.count_nonzero(recording.classes == 2), np.count_nonzero(recording.classes == 3), np.count_nonzero(recording.classes == 4))
    print(incorrect.count(1), incorrect.count(2), incorrect.count(3), incorrect.count(4))
    print(guessed.count(1), guessed.count(2), guessed.count(3), guessed.count(4))


if __name__ == '__main__':
    training_set = Recording(filename='training')
    params = {
        'inputs': training_set.range,
        'hiddens': int(training_set.range/3),
        'outputs': 4,
        'lr': 0.65,
        'bias': np.array([[0.0], [0.02], [-0.27], [-0.1]]),  # [[0.0], [0.0], [0.0], [0.0]]
        'reps': 10000
    }
    # TODO: Use gradient to find indices; integrate, differentiate, do shit my nigga
    class_net = NeuralNetwork(params['inputs'], params['hiddens'], params['outputs'], params['lr'], params['bias'])

    find_indices(training_set)
    #test_index = training_set.index[210]
    #test_class = 3
    #class_test(training_set, test_class)

    #train_classes(training_set, class_net, params['reps'])
    #test_net(training_set, class_net)
