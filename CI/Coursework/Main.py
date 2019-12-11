from Recording import Recording
from Filters import Filters
from IndexIdentifiers import IndexIdentifiers
from NeuralNetwork import NeuralNetwork
import numpy as np
import matplotlib.pyplot as plt
# import PyQt5


def plot(recording, center=200, time=False, all=False):
    plt.figure(1)
    [x_axis, voltages] = recording.slice(center, all)

    if not all or len(x_axis) < 1000:
        [indices, colours] = classify_series(recording, x_axis)

    if time:
        x_axis *= recording.period
        indices *= recording.period

    plt.plot(x_axis, voltages, color=recording.colourmap[0])

    if len(indices) > 0:
        for i in range(len(indices)):
            plt.scatter(indices[i], 0, color=colours[i])


def plot_fft(freq, amplitude):
    plt.figure(2)
    #plt.ylim(top=np.max(amplitude))
    plt.bar(freq, amplitude, width=10)


def classify_series(recording, x):
    indices_in_x = list(filter(lambda y: y in recording.index, x))
    classes_in_x = [recording.classes[np.where(recording.index == y)] for y in indices_in_x]
    class_colours = [recording.colourmap[int(y)] for y in classes_in_x]
    return [np.array(indices_in_x), class_colours]


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


def train_classes(recording, n, reps=4):
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
    guessed = []
    #incorrect = []
    #incorrect_guessed = []
    checked = []

    for i in range(len(recording.index)):
        series = recording.slice(recording.index[i], copy=True)[1]
        [fft_freq, fft_voltages] = Filters.fft(series, recording.window)
        outputs = n.query(fft_voltages)
        guess = np.argmax(outputs) + 1
        guessed.append(guess)

        if test:
            done = False
            correct_class_index = 0
            for correct_i in correct.index:
                if correct_i - 50 <= recording.index[i] <= correct_i + 50:
                    if correct_i not in checked:
                        correct_class = correct.classes[correct_class_index]
                        if guess == correct_class:
                            scorecard.append(1)
                            done = True
                        checked.append(correct_i)
                        break
                correct_class_index += 1
            if not done:
                scorecard.append(0)
                #incorrect.append(correct_class)
                #incorrect_guessed.append(guess)

    if test:
        print('\nClass Net performance: %.2f' % (scorecard.count(1)/len(scorecard) * 100.0))
        #print(np.count_nonzero(recording.classes == 1), np.count_nonzero(recording.classes == 2), np.count_nonzero(recording.classes == 3), np.count_nonzero(recording.classes == 4))
        #print(incorrect.count(1), incorrect.count(2), incorrect.count(3), incorrect.count(4))
        #print(incorrect_guessed.count(1), incorrect_guessed.count(2), incorrect_guessed.count(3), incorrect_guessed.count(4))
    #else:
    #    print(len(guessed), len(recording.index))
    print('Guess counts by class:', guessed.count(1), guessed.count(2), guessed.count(3), guessed.count(4))
    print('Correct counts by class:', np.count_nonzero(correct.classes == 1), np.count_nonzero(correct.classes == 2),
          np.count_nonzero(correct.classes == 3), np.count_nonzero(correct.classes == 4))

    return np.array(guessed)


if __name__ == '__main__':
    training_set = Recording(filename='training')
    sorted_training_set = training_set.__copy__()
    sorted_training_set.sort_indices_in_place()

    params = {
        'inputs': training_set.range,
        'hiddens': int(training_set.range / 3),
        'outputs': 4,
        'lr': 0.65,
        'bias': np.array([[0.0], [0.02], [-0.27], [-0.2]]),  # [[0.0], [0.0], [0.0], [0.0]]
        'reps': 4
    }
    # TODO: Each neuron can only fire once at a time so perhaps do a rolling classification that prevents duplicates only if they are of the same class

    # Train and test classes net using training set and sorted training set, respectively
    class_net = NeuralNetwork(params['inputs'], params['hiddens'], params['outputs'], params['lr'], params['bias'])
    train_classes(training_set, class_net, params['reps'])
    test_net(sorted_training_set, class_net, sorted_training_set)

    # Test index finding accuracy of correlation method
    correlation_test = training_set.__copy__()
    correlation_test.sort_indices_in_place()
    index_finder_test = IndexIdentifiers(correlation_test)
    index_finder_test.correlation_method(class_net)

    # Test class identification net on generated index set (using closest correct index matching)
    #correlation_classes = test_net(correlation_test, class_net, sorted_training_set)
    #correlation_test.classes = correlation_classes

    # Generate index and class vectors for submission set
    submission_set = Recording(filename='submission')
    index_finder = IndexIdentifiers(submission_set, test=False)
    index_finder.correlation_method(class_net)
    test_net(submission_set, class_net, training_set, test=False)
    test_class = 4
    class_test(submission_set, test_class)
    #class_test(training_set, test_class)

    # plot(submission_set, 0)
    # plt.show()
