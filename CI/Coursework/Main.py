from Recording import Recording
from Filters import Filters
from IndexIdentifiers import IndexIdentifiers
from NeuralNetwork import NeuralNetwork
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier


def plot(recording, center=200, time=False, all=False):
    plt.figure(1)
    [x_axis, voltages] = recording.slice(center, all, x_needed=True)

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
    class_colours = [recording.colourmap[int(y)+1] for y in classes_in_x]
    return [np.array(indices_in_x), class_colours]


def class_test(recording, target, fft=False):
    for i in range(len(recording.classes)):
        if recording.classes[i] == target:
            test_index = recording.index[i]
            plot(recording, center=test_index)

            filtered = recording.__copy__()
            filtered.colourmap = 'pink'
            [x, series] = filtered.slice(test_index, x_needed=True)
            series = Filters.smooth(series, averaging_length=2)
            filtered.d[x[0]:x[-1]+1] = series
            plot(filtered, center=test_index)
            plt.show()

            if fft:
                [fft_freq, fft_voltages] = Filters.fft(series)
                plot_fft(fft_freq, fft_voltages)
                plt.show()


def train_classes(recording, n, reps=4):
    # train the neural network on each training sample
    filtered = recording.__copy__()
    while reps > 0:
        for i in range(len(recording.index)):
            series = filtered.slice(recording.index[i])
            [fft_freq, fft_voltages] = Filters.fft(series, recording.window)
            targets = np.zeros(n.o_nodes) + 0.01
            targets[recording.classes[i] - 1] = 0.99
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
            series = recording.slice(recording.index[i])
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
    print('Guessed counts by class:', guessed.count(0), guessed.count(1), guessed.count(2), guessed.count(3), guessed.count(4))
    if test:
        print('Expected counts by class:', np.count_nonzero(correct.classes == 0), np.count_nonzero(correct.classes == 1), np.count_nonzero(correct.classes == 2),
              np.count_nonzero(correct.classes == 3), np.count_nonzero(correct.classes == 4), '\n')

    return np.array(guessed)


def pca_fit(recording, knn, train_for_noise=False):
    averaging_length = 2
    step = 3000
    window = 150

    paired = [[Filters.smooth(recording.slice(i), averaging_length), recording.classes[np.nonzero(recording.index == i)][0]] for i in recording.index]
    #paired = sorted(paired, key=lambda x: x[0])

    if train_for_noise:
        for i in range(0, len(recording.d), step):
            start = max(0, i - window)
            end = min(len(recording.d), i + window)
            observation_window = np.arange(start, end)
            common = np.intersect1d(observation_window, recording.index, assume_unique=True)
            if len(common) is not 0:
                paired.insert(np.random.randint(0, len(paired)-1), [Filters.smooth(recording.slice(i), averaging_length), 0])

    train_ext = recording.pca.fit_transform([pair[0] for pair in paired])
    min_max_scaler = MinMaxScaler()
    train_norm = min_max_scaler.fit_transform(train_ext)
    knn.fit(train_norm, [pair[1] for pair in paired])


def pca_predict(train, submission, knn):
    test = train.__copy__()
    test.sort_indices_in_place()

    test_indices = []
    submission_indices = []
    averaging_length = 2

    for i in range(len(test.index)):
        series = test.slice(test.index[i])
        series = Filters.smooth(series, averaging_length=averaging_length)
        test_indices.append(series)

    for i in range(len(submission.index)):
        series = submission.slice(submission.index[i])
        series = Filters.smooth(series, averaging_length=averaging_length)
        submission_indices.append(series)

    test_ext = train.pca.transform(test_indices)
    submission_ext = train.pca.transform(submission_indices)

    min_max_scaler = MinMaxScaler()
    test_norm = min_max_scaler.fit_transform(test_ext)
    submission_norm = min_max_scaler.fit_transform(submission_ext)

    test.classes = knn.predict(test_norm)
    submission.classes = knn.predict(submission_norm)
    return test


def verify_class_agreements(net_set, knn_set):
    matches = [net_set.index[i] for i in range(len(net_set.index)) if net_set.classes[i] == knn_set.classes[i]]
    print('Agreed on', len(matches), 'out of', len(knn_set.classes), 'generated classes')
    print('Agreement Percentage: %.2f' % (len(matches)/len(knn_set.index) * 100.0))
    filtered = list(net_set.index)
    filtered_classes = list(net_set.classes)
    removed = 0
    for i in range(len(net_set.index)-1):
        if net_set.classes[i] == 4:
            if net_set.index[i] + 40 > net_set.index[i+1]:
                filtered[i] = -1
                filtered_classes[i] = -1
    filtered = [i for i in filtered if i != -1]
    filtered_classes = [i for i in filtered_classes if i != -1]
    print(len(net_set.classes) - len(filtered))


def remove_noise(recording):
    invalid = len(recording.classes) - np.count_nonzero(recording.classes)
    print('Removing', invalid, 'indices')
    valid_pairs = [[recording.index[i], recording.classes[i]] for i in range(0, len(recording.index)) if recording.classes[i] != 0]
    valid_indices = [pair[0] for pair in valid_pairs]
    valid_classes = [pair[1] for pair in valid_pairs]
    recording.index = np.array(valid_indices)
    recording.classes = np.array(valid_classes)

if __name__ == '__main__':
    training_set = Recording(filename='training')

    params = {
        'inputs': training_set.range,
        'hiddens': int(training_set.range / 3),
        'outputs': 4, #5,
        'lr': 0.65,
        'bias': np.array([[0.05], [0.05], [-0.33], [-0.18]]),  # [[0.0], [0.0], [0.0], [0.0]]
        'reps': 4,
        'components': 20,
        'neighbours': 6,
        'distance': 2,
        'noise removal': True
    }

    training_set.components = params['components']  # TODO: getters and setters for new knn params
    sorted_training_set = training_set.__copy__()
    sorted_training_set.sort_indices_in_place()

    # Train and test classes net using training set and sorted training set, respectively
    print('Training class identification neural net')
    class_net = NeuralNetwork(params['inputs'], params['hiddens'], params['outputs'], params['lr'], params['bias'])
    train_classes(training_set, class_net, params['reps'])

    print('\nFitting PCA')
    knn = KNeighborsClassifier(n_neighbors=params['neighbours'], p=params['distance'])
    pca_fit(training_set, knn, train_for_noise=True)

    # Test index finding accuracy of correlation method
    print('\nTesting index identification performance')
    correlation_test = training_set.__copy__()
    correlation_test.sort_indices_in_place()
    index_finder_test = IndexIdentifiers(correlation_test)
    index_finder_test.correlation_method(class_net, knn=knn, pca=training_set.pca)

    # Generate index and class vectors for submission set
    print('\nFinding submission indices')
    net_submission_set = Recording(filename='submission')
    index_finder = IndexIdentifiers(net_submission_set, test=False)
    index_finder.correlation_method(class_net)

    print('\nTraining class performance')
    test_net(sorted_training_set, class_net, sorted_training_set)

    knn_submission_set = net_submission_set.__copy__()

    pca_set = pca_predict(training_set, knn_submission_set, knn)
    test_net(pca_set, class_net, sorted_training_set, knn=True)

    print('\nSumming submission generated class counts')
    test_net(net_submission_set, class_net, training_set, test=False)
    test_net(knn_submission_set, class_net, training_set, test=False, knn=True)
    verify_class_agreements(net_submission_set, knn_submission_set)
    if params['noise removal']:
        #class_test(knn_submission_set, 0)
        remove_noise(knn_submission_set)
        print(len(knn_submission_set.index))


    test_class = 4
    # class_test(training_set, test_class)
    # class_test(training_set, test_class)
    #class_test(net_submission_set, test_class)

    plot(net_submission_set, 1000)
    #plt.show()
