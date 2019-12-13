import time as t
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from Recording import Recording
from PreProcessing import PreProcessing
from IndexIdentifiers import IndexIdentifiers
from NeuralNetwork import NeuralNetwork


# --------------------------------------------------- Plotting ---------------------------------------------------------
def plot(recording, center=200, time=False, all=False):
    """Prepares a plot of either the recording data centered around a sample no. or the entire plot if requested.
    Args:
        recording (Recording): The neural recording to be sampled.
        center (int): The central sample no. from which to sample. Defaults to 200 for test purposes.
        time (bool, optional): Whether to plot the x-axis in terms of time (us), rarely necessary. Defaults to False.
        all (bool, optional): Whether to just plot all samples in recording, rarely necessary. Defaults to False.
    """

    plt.figure(1)  # Allows for successive calls before a plt.show() outside of this function
    [x_axis, voltages] = recording.slice(center, all, x_needed=True)  # Get the required x and y-axis windows.

    # Arrays to hold the Index markers and their neural type - only plotted if <l000 present in window
    indices, colours = [], []
    if not all or len(x_axis) < 1000:
        [indices, colours] = classify_series(recording, x_axis)

    if time:
        x_axis *= int(recording.period/1e-6)
        indices *= int(recording.period/1e-6)

    plt.plot(x_axis, voltages, color=recording.colourmap[0])  # Each Recording can be set to a unique colour internally
    plt.xlabel('Sample No.')
    if time:
        plt.xlabel('Time (us)')
    plt.ylabel('Voltage [V}')

    if len(indices) > 0:
        for i in range(len(indices)):
            plt.scatter(indices[i], 0, color=colours[i])


def plot_fft(freq, amplitude):
    """Plots the frequencies and amplitudes resultant from a FFT.
    Args:
        freq (ndarray): Frequencies in window - determined by sample rate (consistent) and window size.
        amplitude (ndarray): Amplitudes of corresponding frequencies.
   """
    plt.figure(2)
    plt.bar(freq, amplitude, width=10)


def classify_series(recording, x):
    """Finds all known Indices and their respective Classes present within the window.
    Args:
        recording (Recording): The neural recording to be sampled.
        x (ndarray): Sample no.s in window.
    Returns:
        (list): Indices in sample range paired with their colour representation.
    """
    indices_in_x = list(filter(lambda y: y in recording.index, x))
    classes_in_x = [recording.classes[np.where(recording.index == y)] for y in indices_in_x]
    class_colours = [recording.colourmap[int(y)+1] for y in classes_in_x]
    return [np.array(indices_in_x), class_colours]


def class_test(recording, target, fft=False):
    """Plots all Indices of a given type.
    Args:
        recording (Recording): The neural recording to be sampled.
        target (int): The Class type to be found and plotted.
        fft (bool, optional): Whether to also plot the FFT of each window in a second figure. Defaults to False.
    """

    # Loop through all classes in the recording, plotting only those that match the target
    for i in range(len(recording.classes)):
        if recording.classes[i] == target:
            test_index = recording.index[i]
            plot(recording, center=test_index)  # Prepare the plot of the unfiltered data

            # Process the data in a similar manner to that which is done when training then plot this too for context.
            filtered = recording.__copy__()  #
            filtered.colourmap = 'red'
            [x, series] = filtered.slice(test_index, x_needed=True)
            series = PreProcessing.smooth(series, averaging_length=2)   # Running average and median removal to smooth data
            filtered.d[x[0]:x[-1]+1] = series
            plot(filtered, center=test_index)
            plt.show()

            if fft:
                [fft_freq, fft_voltages] = PreProcessing.fft(series)
                plot_fft(fft_freq, fft_voltages)
                plt.show()


# -------------------------------------------------- Class Training ----------------------------------------------------
def train_net(recording, n, reps=4):
    """Train the neural network using each training index and matching class.
     Args:
         recording (Recording): The training neural recording.
         n (NeuralNetwork): The neural network to be trained.
         reps (int, optional): Total number of training cycles. Defaults to 4.
     """
    # Duplicate test recording and use this for processing (for sanity)
    filtered = recording.__copy__()
    while reps > 0:
        for i in range(len(recording.index)):
            series = filtered.slice(recording.index[i])  # Get window of values about Index
            [fft_freq, fft_voltages] = PreProcessing.fft(series, recording.window)  # Take FFT of window

            # Set all output nodes to zero except for the correct target Class
            targets = np.zeros(n.o_nodes) + 0.01
            targets[recording.classes[i] - 1] = 0.99
            n.train(fft_voltages, targets)  # Train using voltages only as frequency range is constant with window size
        reps -= 1


def pca_fit(recording, knn, train_for_noise=False):
    """Train the KNN classifier using slightly smoothed windows about each training Index.
    Args:
        recording (Recording): The training neural recording.
        knn (KNeighborsClassifier): The KNN classifier to be configured.
        train_for_noise (bool, optional): Whether also adding random noise training to input data. Defaults to False.
   """
    averaging_length = 2  # Size of moving average window - v. low to not remove too many unique features
    step = 3000  # Number of samples to skip through when finding noise - the lower the more noise samples trained
    window = 150  # Distance from an Index required to be considered 'noise'

    # Put all windows around each known Index into one 2x1 list holding each window and correct Class label respectively
    paired = [[PreProcessing.smooth(recording.slice(i), averaging_length), recording.classes[np.nonzero(recording.index == i)][0]] for i in recording.index]

    if train_for_noise:
        for i in range(0, len(recording.d), step):
            # Sanitise observation window indices
            start = max(0, i - window)
            end = min(len(recording.d), i + window)
            observation_window = np.arange(start, end)

            # Find all points where current window contains an identified Index, do not use as noise if mathches found
            common = np.intersect1d(observation_window, recording.index, assume_unique=True)
            if len(common) is not 0:
                # Randomly Insert noise window into training data along with a label as type '0' Class
                paired.insert(np.random.randint(0, len(paired) - 1),
                              [PreProcessing.smooth(recording.slice(i), averaging_length), 0])

    # Extract then normalise the principle components from the training data
    train_ext = recording.pca.fit_transform([pair[0] for pair in paired])
    min_max_scaler = MinMaxScaler()
    train_norm = min_max_scaler.fit_transform(train_ext)

    knn.fit(train_norm, [pair[1] for pair in paired])  # Configure classifier using normalised data


def test_classifying_performance(recording, n, correct, test=True, knn=False):
    """Test the neural network/KNN classifier using each generated index and class vector and a test set.
    Args:
        recording (Recording): The training neural recording.
        n (NeuralNetwork): The trained neural network.
        correct (Recording): The testing neural recording.
        test (bool, optional): Whether running on training set or submission set; latter only prints guess counts. Defaults to True.
        knn (bool, optional): Whether the test is being done on a KNN classifier.
    Returns:
        (float): The test score.
   """
    scorecard = []
    guessed = []
    checked = []  # Holds all Indices that have been confirmed using the +/- 50 sample threshold if not exact.

    for i in range(len(recording.index)):
        if not knn:
            # Testing neural net so get series about Index, pre-process it, and query a best guess at which Class
            series = recording.slice(recording.index[i])
            [fft_freq, fft_voltages] = PreProcessing.fft(series, recording.window)
            outputs = n.query(fft_voltages)
            guess = np.argmax(outputs) + 1
        else:  # Testing KNN classifier so recording already has all predictions done.
            guess = recording.classes[i]
        guessed.append(guess)

        if test:
            done = False
            correct_class_index = 0  # An offset just in case indices are missing after Index prediction so true score can be observed
            for correct_i in correct.index:
                # Check all indices within a +/- window given threshold to be applied when marking
                if correct_i - 50 <= recording.index[i] <= correct_i + 50:
                    if correct_i not in checked:
                        correct_class = correct.classes[correct_class_index]
                        if guess == correct_class:
                            scorecard.append(1)
                            done = True  # Signal that a matching index and class was found so do not append 0 score
                        checked.append(correct_i)
                        break
                correct_class_index += 1
            if not done:
                scorecard.append(0)  # Could not find a matching Index in the test set so append a 0 score anyway.

    score = 0.0
    if test:
        score = float(scorecard.count(1)/len(scorecard))
        if not knn:
            print('\nNeural net performance: %.2f' % (score * 100.0))
        else:
            print('\nKNN performance: %.2f' % (score * 100.0))

    print('Guess counts by class:', guessed.count(0), guessed.count(1), guessed.count(2), guessed.count(3), guessed.count(4))
    if test:
        print('Expected counts by class:', np.count_nonzero(correct.classes == 0), np.count_nonzero(correct.classes == 1), np.count_nonzero(correct.classes == 2),
              np.count_nonzero(correct.classes == 3), np.count_nonzero(correct.classes == 4))

    return score


# -------------------------------------------------- KNN Prediction ----------------------------------------------------
def knn_predict(recording, knn, submission=None):
    """Use the training recording with the PCA tranformation to predict Classes.
    Args:
        recording (Recording): The training or generated submission neural recording.
        knn (KNeighborsClassifier): The KNN classifier to be used for predicion.
        submission (bool, optional): Whether predicting on submission set instead. Defaults to False.
    Returns:
        (Recording): The resultant generated classes if testing on training set.
    """

    test = recording.__copy__()
    test.sort_indices_in_place()
    test_indices = []
    averaging_length = 2  # Again, low averaging length to keep unique features

    # Either use a copy test Recording if testing on training set or use the already generated submission indices
    test_range = range(len(test.index)) if submission is None else range(len(submission.index))
    for i in test_range:
        series = test.slice(test.index[i]) if submission is None else submission.slice(submission.index[i])
        series = PreProcessing.smooth(series, averaging_length)  # Running average and median removal to smooth data
        test_indices.append(series)  # Append series to test data

    # Transform test data using original PCA which used training data then normalise
    test_ext = recording.pca.transform(test_indices)
    min_max_scaler = MinMaxScaler()
    test_norm = min_max_scaler.fit_transform(test_ext)

    # Return the test prediction if not running on submission set, otherwise set the Class vector of the generated submission set in place
    if submission is None:
        test.classes = knn.predict(test_norm)
        return test
    else:
        submission.classes = knn.predict(test_norm)


# ------------------------------------------------- Final Evaluations --------------------------------------------------
def remove_noise(net_recording, knn_recording):
    """Removes all type 0 Classes Indices from both the neural net and KNN versions of the generated submission vectors.
    Args:
        net_recording (Recording): The neural net predicted submission recording.
        knn_recording (Recording): The KNN predicted submission recording.
    Returns:
        (float): A score on how often the two Class predictions matched for each Index.
    """

    # Pair all generated neural net Indices along with their respective Class guesses
    net_pairs = [[net_recording.index[i], net_recording.classes[i]] for i in range(len(net_recording.index))]

    # Extract all non-type zero Classifications in the KNN submission set and store all resultant 'good' Indices
    valid_pairs = [[knn_recording.index[i], knn_recording.classes[i]] for i in range(len(knn_recording.index)) if knn_recording.classes[i] != 0]
    valid_indices = [pair[0] for pair in valid_pairs]

    # Extract only the Classes that match valid Indices and overwrite the original generated submissions for both sets
    valid_classes_net = [pair[1] for pair in net_pairs if pair[0] in valid_indices]
    valid_classes_knn = [pair[1] for pair in valid_pairs]
    net_recording.index = np.array(valid_indices)
    knn_recording.index = np.array(valid_indices)
    net_recording.classes = np.array(valid_classes_net)
    knn_recording.classes = np.array(valid_classes_knn)

    return verify_class_agreements(net_recording, knn_recording)  # Test the ratio of agreements observed


def verify_class_agreements(net_set, knn_set):
    """Tests the agreement rate between the neural net Class and KNN classifier predictions.
    Args:
        net_set (Recording): The neural net predicted submission recording.
        knn_set (Recording): The KNN predicted submission recording.
    Returns:
        (float): A score on how often the two Class predictions matched for each Index.
    """

    # Extract all Indices that show the same predicted Class in both submission sets
    matches = [net_set.index[i] for i in range(len(net_set.index)) if net_set.classes[i] == knn_set.classes[i]]
    score = float(len(matches) / len(knn_set.index))

    # Print results for performance context
    print('Agreed on', len(matches), 'out of', len(knn_set.classes), 'generated classes')
    print('Agreement Percentage: %.2f' % (score * 100.0))
    print('Net guess counts by class:', np.count_nonzero(net_set.classes == 0), np.count_nonzero(net_set.classes == 1),
          np.count_nonzero(net_set.classes == 2),
          np.count_nonzero(net_set.classes == 3), np.count_nonzero(net_set.classes == 4))
    print('KNN guess counts by class:', np.count_nonzero(knn_set.classes == 0), np.count_nonzero(knn_set.classes == 1),
          np.count_nonzero(knn_set.classes == 2),
          np.count_nonzero(knn_set.classes == 3), np.count_nonzero(knn_set.classes == 4), '\n')

    return score


if __name__ == '__main__':
    print('\nTrying to load test and submission files...'.upper())
    training_set = Recording(filename='training')
    print('\nSuccessfully loaded test and submission files...'.upper())
    net_submission_set = Recording(filename='submission')

    """For test purposes only - observes the generated classes in the generated set to be handed in."""
    # generated_set_test = Recording(filename='11222')
    # test_class = 2
    # class_test(generated_set_test, test_class)

    # dict of Neural net, KNN, and general parameters for quick adjustments
    params = {
        'inputs': training_set.range,
        'hiddens': int(training_set.range / 3),
        'outputs': 4,
        'lr': 0.65,  # learning rate
        'bias': np.array([[0.1], [0.1], [-0.28], [-0.2]]),  # Output bias adjustments to better tune net performance
        'reps': 4,
        'components': 12,
        'neighbours': 3,
        'distance': 2,
        'noise removal': True
    }

    training_set.components = params['components']
    sorted_training_set = training_set.__copy__()
    sorted_training_set.sort_indices_in_place()

    # ----------------------------------------------- Net Training -----------------------------------------------------
    print('\nTraining class identification neural net...'.upper())
    class_net = NeuralNetwork(params['inputs'], params['hiddens'], params['outputs'], params['lr'], params['bias'])
    start = t.time()
    train_net(training_set, class_net, params['reps'])
    net_train_time = t.time() - start
    print('Neural net trained in %.2fs (%d reps)...' % (net_train_time, params['reps']))

    # ----------------------------------------------- PCA Fitting ------------------------------------------------------
    print('\nFitting PCA...'.upper())
    knn = KNeighborsClassifier(n_neighbors=params['neighbours'], p=params['distance'])
    start = t.time()
    pca_fit(training_set, knn, train_for_noise=params['noise removal'])
    pca_fit_time = t.time() - start
    print('PCA completed in %.2fs  (%d components, %d neighbours, p%d norm)...'
          % (pca_fit_time, params['components'], params['neighbours'], params['distance']))

    # ------------------------------------------ Classification Testing ------------------------------------------------
    print('\nTesting neural net class performance on training set...'.upper())
    net_score = test_classifying_performance(sorted_training_set, class_net, sorted_training_set)

    print('\nTesting KNN class performance on training set...'.upper())
    knn_score = test_classifying_performance(knn_predict(training_set, knn), class_net, sorted_training_set, knn=True)

    # -------------------------------------- Test Index Prediction Performance -----------------------------------------
    print('\nTesting index identification performance...'.upper())
    correlation_test = training_set.__copy__()
    correlation_test.sort_indices_in_place()
    index_finder_test = IndexIdentifiers(correlation_test)
    index_score = index_finder_test.correlation_method(class_net, knn=knn, pca=training_set.pca)

    # ---------------------------------- Submission Set Index and Class Predictions ------------------------------------
    print('\nNeural net predicting submission classes while Finding submission indices...'.upper())
    index_finder = IndexIdentifiers(net_submission_set, test=False)
    start = t.time()
    index_finder.correlation_method(class_net)
    index_time = t.time() - start
    print('Submission indices AND classes simultaneously predicted in %.2fs (neural net)...' % index_time)

    print('\nKNN predicting submission classes...'.upper())
    knn_submission_set = net_submission_set.__copy__()
    start = t.time()
    knn_predict(training_set, knn, knn_submission_set)
    knn_predict_time = t.time() - start
    print('Submission classes predicted in %.2fs (KNN)...' % knn_predict_time)

    print('\nChecking guess counts of submission sets for plausibility...\n'.upper())
    test_classifying_performance(net_submission_set, class_net, training_set, test=False)
    test_classifying_performance(knn_submission_set, class_net, training_set, test=False, knn=True)

    print('\nCalculating neural net and knn submission class prediction agreements...'.upper())
    agreement_score = verify_class_agreements(net_submission_set, knn_submission_set)

    # ---------------------------------------------- Noise Removal -----------------------------------------------------
    if params['noise removal']:
        # class_test(knn_submission_set, 0)  # Test purposes, comment in to plot the generated 'noise' Indices
        print('Removing noise and re-calculating agreements...'.upper())
        agreement_score = remove_noise(net_submission_set, knn_submission_set)

    # --------------------------------------------- Output Generation --------------------------------------------------
    total_indices = len(knn_submission_set.index)
    if knn_score >= net_score:
        total_score = knn_score * index_score
        output_filename = '%.2f - %.2f - %d - KNN' % (total_score * 100.0, agreement_score * 100, total_indices)
        knn_submission_set.generate_mat(output_filename)
    else:
        total_score = net_score * index_score
        output_filename = '%.2f - %.2f - %d - Net' % (total_score * 100.0, agreement_score * 100, total_indices)
        net_submission_set.generate_mat(output_filename)
