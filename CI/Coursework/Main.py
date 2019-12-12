from Recording import Recording
from Filters import Filters
from IndexIdentifiers import IndexIdentifiers
from NeuralNetwork import NeuralNetwork
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
# k Nearest Neighbour
from sklearn.neighbors import KNeighborsClassifier
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
            [x, series] = filtered.slice(test_index, copy=True)
            series = Filters.smooth(series)
            filtered.d[x[0]:x[-1]+1] = series
            plot(filtered, center=test_index)
            plt.show()

            [fft_freq, fft_voltages] = Filters.fft(series)
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


def test_net(recording, n, correct, test=True, knn=False):
    scorecard = []
    guessed = []
    #incorrect = []
    #incorrect_guessed = []
    checked = []

    for i in range(len(recording.index)):
        if not knn:
            series = recording.slice(recording.index[i], copy=True)[1]
            [fft_freq, fft_voltages] = Filters.fft(series, recording.window)
            outputs = n.query(fft_voltages)
            guess = np.argmax(outputs) + 1
        else:
            guess = recording.classes[i]
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
        if not knn:
            print('\nClass Net performance: %.2f' % (scorecard.count(1)/len(scorecard) * 100.0))
        else:
            print('\nKNN performance: %.2f' % (scorecard.count(1) / len(scorecard) * 100.0))
        #print(np.count_nonzero(recording.classes == 1), np.count_nonzero(recording.classes == 2), np.count_nonzero(recording.classes == 3), np.count_nonzero(recording.classes == 4))
        #print(incorrect.count(1), incorrect.count(2), incorrect.count(3), incorrect.count(4))
        #print(incorrect_guessed.count(1), incorrect_guessed.count(2), incorrect_guessed.count(3), incorrect_guessed.count(4))
    #else:
    #    print(len(guessed), len(recording.index))
    print('Guessed counts by class:', guessed.count(1), guessed.count(2), guessed.count(3), guessed.count(4))
    if test:
        print('Expected counts by class:', np.count_nonzero(correct.classes == 1), np.count_nonzero(correct.classes == 2),
              np.count_nonzero(correct.classes == 3), np.count_nonzero(correct.classes == 4))

    return np.array(guessed)


def pca_train(train, submission, knn):
    test = train.__copy__()
    test.sort_indices_in_place()
    train_indices = []
    test_indices = []
    submission_indices = []

    for i in range(len(train.index)):
        series = train.slice(train.index[i], copy=True)[1]
        series *= np.hanning(len(series))
        train_indices.append(series)

    for i in range(len(test.index)):
        series = test.slice(test.index[i], copy=True)[1]
        series *= np.hanning(len(series))
        test_indices.append(series)

    for i in range(len(submission.index)):
        series = submission.slice(submission.index[i], copy=True)[1]
        series *= np.hanning(len(series))
        submission_indices.append(series)

    train_ext = train.pca.fit_transform(train_indices)
    test_ext = train.pca.transform(test_indices)
    submission_ext = train.pca.transform(submission_indices)

    min_max_scaler = MinMaxScaler()
    train_norm = min_max_scaler.fit_transform(train_ext)
    test_norm = min_max_scaler.fit_transform(test_ext)
    submission_norm = min_max_scaler.fit_transform(submission_ext)

    knn.fit(train_norm, train.classes)
    test.classes = knn.predict(test_norm)
    submission.classes = knn.predict(submission_norm)
    return test


if __name__ == '__main__':
    training_set = Recording(filename='training')

    params = {
        'inputs': training_set.range,
        'hiddens': int(training_set.range / 3),
        'outputs': 4,
        'lr': 0.65,
        'bias': np.array([[0.0], [0.0], [-0.28], [-0.17]]),  # [[0.0], [0.0], [0.0], [0.0]]
        'reps': 4,
        'components': 10,
        'neighbours': 8,
        'distance': 2
    }

    training_set.components = params['components']  # TODO: getters and setters for new knn params
    sorted_training_set = training_set.__copy__()
    sorted_training_set.sort_indices_in_place()

    # Train and test classes net using training set and sorted training set, respectively

    knn = KNeighborsClassifier(n_neighbors=params['neighbours'], p=params['distance'])
    class_net = NeuralNetwork(params['inputs'], params['hiddens'], params['outputs'], params['lr'], params['bias'])
    train_classes(training_set, class_net, params['reps'])

    # Test index finding accuracy of correlation method
    correlation_test = training_set.__copy__()
    correlation_test.sort_indices_in_place()
    index_finder_test = IndexIdentifiers(correlation_test)
    index_finder_test.correlation_method(class_net)

    # Generate index and class vectors for submission set
    net_submission_set = Recording(filename='submission')
    index_finder = IndexIdentifiers(net_submission_set, test=False)
    index_finder.correlation_method(class_net)
    test_net(net_submission_set, class_net, training_set, test=False)

    test_net(sorted_training_set, class_net, sorted_training_set)

    knn_submission_set = net_submission_set.__copy__()
    pca_set = pca_train(training_set, knn_submission_set, knn)
    test_net(pca_set, class_net, sorted_training_set, knn=True)

    # None
    test_class = 4
    # class_test(training_set, test_class)
    # class_test(training_set, test_class)
    # class_test(submission_set, test_class)
    class_test(knn_submission_set, test_class)

    # plot(submission_set, 0)
    # plt.show()
