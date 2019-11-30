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

            # [fft_freq, fft_voltages] = Filters.fft(index)
            # plot_fft(fft_freq, fft_voltages)
            # plt.show()


def correlation_method(recording, test=True):
    indices = []
    window = np.hanning(40) * 4  #  recording.slice(recording.index[1])[1]
    step = 35
    thresh = 60
    length = len(recording.d)
    for i in range(0, length, step):
        correlation = np.correlate(recording.d[i:i+step], window)
        if max(correlation) > thresh:  # replace with nn
            indices.append(i)

    print('\nTotal Indices Found', len(indices))
    if test:
        test_indices(recording, indices)

    return np.array(indices)


def test_indices(recording, generated_indices):
    thresh = 50
    indices = list(generated_indices)
    total_indices = len(indices)
    expected_total_indices = len(recording.index)
    sorted_index = sorted(recording.index)
    correct = []
    missed = []
    # indices = list(recording.index)

    while len(indices) != 0:
        for i in range(0, len(sorted_index)):
            if (sorted_index[i] - thresh) <= indices[0] <= (sorted_index[i] + thresh):
                correct.append(indices[0])
                sorted_index.pop(i)
                indices.pop(0)
                break
            if i == len(sorted_index) - 1:
                missed.append(indices[0])
                indices.pop(0)

    total_correct = len(correct)
    total_missed = len(missed)
    false_positives = max(0, (total_indices - expected_total_indices))
    score = max(0, (total_correct - total_missed - false_positives))
    print('\nTotal Correct', total_correct)
    print('Total Missed', total_missed)
    print('False Positives', false_positives)
    print('Index performance = %.2f' % (100.0*score/expected_total_indices))


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


def test_net(recording, n, correct, test=True):
    scorecard = []
    incorrect = []
    guessed = []
    incorrect_guessed = []
    for i in range(len(recording.index)):
        series = recording.slice(recording.index[i], copy=True)[1]
        [fft_freq, fft_voltages] = Filters.fft(series, recording.window)
        outputs = n.query(fft_voltages)
        guess = np.argmax(outputs) + 1
        guessed.append(guess)

        if test:
            correct_class = correct.classes[i]

            if guess == correct_class:
                scorecard.append(1)
            else:
                scorecard.append(0)
                incorrect.append(correct_class)
                incorrect_guessed.append(guess)

    if not test:
        print(guessed.count(1), guessed.count(4),
          guessed.count(3), guessed.count(4))

    if test:
        print('\nClass Net performance: %.2f' % (scorecard.count(1)/len(scorecard) * 100.0))
        print(np.count_nonzero(recording.classes == 1), np.count_nonzero(recording.classes == 2), np.count_nonzero(recording.classes == 3), np.count_nonzero(recording.classes == 4))
        print(incorrect.count(1), incorrect.count(2), incorrect.count(3), incorrect.count(4))
        print(incorrect_guessed.count(1), incorrect_guessed.count(2), incorrect_guessed.count(3), incorrect_guessed.count(4))
    else:
        print(len(guessed), len(recording.index))
    return np.array(guessed)


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
    # TODO: Use gradient to find indices; integrate, differentiate, do shit my niggard
    class_net = NeuralNetwork(params['inputs'], params['hiddens'], params['outputs'], params['lr'], params['bias'])

    sorted_training_set = training_set.__copy__()
    sorted_training_set.sort_indices_in_place()

    correlation_recording = sorted_training_set.__copy__()
    correlation_indices = correlation_method(correlation_recording)
    correlation_recording.index = correlation_indices

    train_classes(training_set, class_net, params['reps'])
    #test_net(training_set, class_net, training_set)
    test_net(sorted_training_set, class_net, sorted_training_set)

    #correlation_classes = test_net(correlation_recording, class_net, sorted_training_set)
    #correlation_recording.classes = correlation_classes

    submission_set = Recording(filename='submission')
    submission_set.index = correlation_method(submission_set, test=False)
    submission_set.classes = test_net(submission_set, class_net, training_set, test=False)
    test_class = 4
    #class_test(correlation_recording, test_class)
    class_test(training_set, test_class)
