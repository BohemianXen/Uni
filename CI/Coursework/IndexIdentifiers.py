import numpy as np
import matplotlib.pyplot as plt
from PreProcessing import PreProcessing
from sklearn.preprocessing import MinMaxScaler


class IndexIdentifiers:
    """Class that holds index identification methods (previous failed algorithms removed for clarity).
    Parameters:
        recording (Recording): The Recording instance to be investigated.
        test (bool, optional): Whether the recording data has known Indices already and predictions can be evaluated.
    """
    def __init__(self, recording, test=True):
        self.recording = recording
        self.test = test

    def correlation_method(self, net, knn=None, pca=None, ):
        """Finds points of high rolling difference and correlates a window about this point with a Hanning window to
            determine whether a peak is present. Preliminary neural net and KNN Class vectors are generated here also.
        Arguments:
            recording (Recording): The Recording instance to be investigated.
            test (bool, optional): Whether the recording data has known Indices already and predictions can be evaluated.
        Returns:
            (float): Performance score if test was done.
        """
        # ----------------------------------------------- Param Inits --------------------------------------------------
        indices, classes, knn_series = [], [], []
        step = int(self.recording.range/2)
        diff_thresh, correlation_thresh = 0.28, 36  # Thresholds
        window_size, window_voltage = 48, 3.3
        window = np.hanning(window_size) * window_voltage  # Scaled Hanning window to be used for correlation
        length = len(self.recording.d)
        averaging_length = 3
        duplicate_range = 30
        plot_correlation = False  # For test purposes - plots the correlation result on top of the tested window

        # Loop through data points, skipping in steps
        for i in range(self.recording.range, length-self.recording.range, step):
            end = min(i + step, length - 1)
            # Get noisy series about observation index, slightly smooth this and calculate rolling differences
            series = self.recording.d[i:end]
            diff = np.ediff1d(PreProcessing.smooth(series, averaging_length, just_average=True))

            if max(diff) > diff_thresh:  # If max difference is high enough, go to second stage
                center = i + np.argmax(diff)  # Offset observation index by argument where max rolling diff was found
                [x, vals] = self.recording.slice(center, x_needed=True)  # Get a larger window about this new point
                smoothed = PreProcessing.smooth(vals, averaging_length+2)  # Aggresively smmooth points as small features don't matter as much

                correlation = np.correlate(smoothed, window)  # Calculate cross-correlation at points of full overlap

                if max(abs(correlation[4:-2])) > correlation_thresh: # Ignore fringe correlations to lower false duplicates
                    # Save the current central index and use neural net to guess class
                    indices.append(center)
                    guessed_class = net.query(PreProcessing.fft(vals, self.recording.window)[1])
                    classes.append(np.argmax(guessed_class) + 1)

                    duplicate = False
                    # If two of the same neuron fire simultaneously, consider this a duplicate
                    if len(indices) >= 2 and (center < (indices[-2] + duplicate_range)):
                        if classes[-1] == classes[-2]:
                            # Do not save current values if duplicate detected
                            del classes[-1]
                            del indices[-1]
                            duplicate = True

                    # Test purposes only - plots each found index in the submission set (i.e. NOT self.test)
                    if plot_correlation and not self.test:
                        self.plot_correlation(x, smoothed, correlation, window)

                    if not duplicate:
                        knn_series.append(smoothed)  # Append possible found Index containing window to knn data

        found = len(indices)
        print('\nCorrelation Method Total Found', found, 'Indices')

        if knn is not None and pca is not None:
            # Predict which Classes were present in the found indices (including potential noise) and print results
            test_ext = pca.transform(knn_series)
            min_max_scaler = MinMaxScaler()
            test_norm = min_max_scaler.fit_transform(test_ext)
            knn_classes = knn.predict(test_norm)
            disagreements = [indices[i] for i in range(found) if classes[i] != knn_classes[i]]
            print('Net and KNN Agreed on', found - len(disagreements), 'out of the ', found, 'generated classes')
            if found != 0:
                print('... An agreement percentage: %.2f' % ((found-len(disagreements)) / found * 100.0))

        if self.test:  # Test generated Index performance on training set and updated recording index to reflect this
            score = self.test_indices(indices)
            self.recording.index = np.array(indices)
            return score
        else:
            self.recording.classes = np.array(classes)  # Updated found Classes

        self.recording.index = np.array(indices)  # Update found Indices

    def test_indices(self, generated_indices):
        """Tests Index finding performance on training set.
        Arguments:
            generated_indices (list): A list of the found indices to be tested against the known ones.
        Returns:
          (float): Performance result.
        """
        tolerance = 50
        indices = list(generated_indices)  # Copy generated indices
        total_indices = len(indices)
        expected_total_indices = len(self.recording.index)
        sorted_index = sorted(self.recording.index)
        correct = []
        missed = []
        # indices = list(self.recording.index) # For test purposes only - correct indices tested on self

        # Test the first element found index for matches within the training set and remove both if found - both should be empty if all matches found
        while len(indices) != 0:
            for i in range(0, len(sorted_index)):
                if (sorted_index[i] - tolerance) <= indices[0] <= (sorted_index[i] + tolerance):
                    correct.append(indices[0])
                    sorted_index.pop(i)
                    indices.pop(0)
                    break
                if i == len(sorted_index) - 1:
                    # Reached end of correct indices and no matches were found so mark as missed
                    missed.append(indices[0])
                    indices.pop(0)

        # Calculate, print, and return results
        total_correct = len(correct)
        total_missed = len(missed)
        length_mismatch = max(0, (total_indices - expected_total_indices), (expected_total_indices - total_indices))
        score = float(max(0, (total_correct - total_missed - length_mismatch))/expected_total_indices)
        print('Total Correct', total_correct)
        print('Total Missed', total_missed)
        print('Length Mismatch With Training Set', length_mismatch)
        print('Index performance = %.2f' % (100.0*score))
        return score

    @staticmethod
    def plot_correlation(x, series, correlation, window):
        """For testing only, plots the window and correlation results"""
        series_length, correlation_length, window_length = len(series), len(correlation), len(window)
        figure, v_axis = plt.subplots()
        v_axis.set_title('Finding An Index')

        window_x_offset = int(np.floor((series_length - correlation_length) / 2))
        v_axis.plot(x, series, label='Smoothed Series', color='black')
        v_axis.plot(x[window_x_offset:window_x_offset + window_length], window, label='Correlation Window', color='red')
        v_axis.set_xlabel('Sample No.')
        v_axis.set_ylabel('Voltage [V]')
        v_axis.legend(loc=2, prop={'size': 12})

        correlation_axis = v_axis.twinx()
        corr_x_offset = int(np.floor((series_length - correlation_length) / 2))
        correlation_axis.plot(x[corr_x_offset:corr_x_offset + correlation_length], correlation, label='Result')
        correlation_axis.set_ylabel('Correlation')
        correlation_axis.legend(loc=0, prop={'size': 12})

        figure.tight_layout()
        plt.show()
