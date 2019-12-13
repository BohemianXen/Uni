import numpy as np
import matplotlib.pyplot as plt
from Filters import Filters
from sklearn.preprocessing import MinMaxScaler


class IndexIdentifiers:
    def __init__(self, recording, test=True):
        self.recording = recording
        self.test = test

    def correlation_method(self, net, knn=None, pca=None):
        indices = []
        classes = []
        knn_series = []
        step = 18
        diff_thresh = 0.28
        correlation_thresh = 30
        window_size = 30
        window_voltage = 3
        window = np.hanning(window_size) * window_voltage
        length = len(self.recording.d)
        averaging_length = 3
        duplicate_range = 30 #14
        index_counter = 0

        for i in range(self.recording.range, length-self.recording.range, step):
            end = min(i + step, length - 1)
            series = self.recording.d[i:end]
            diff = np.ediff1d(Filters.smooth(series, averaging_length, just_average=True))

            if max(diff) > diff_thresh:
                center = i + np.argmax(diff)
                [x, vals] = self.recording.slice(center, x_needed=True)
                smoothed = Filters.smooth(vals, averaging_length+1)

                if self.test and (self.recording.index[index_counter] - 30 < i < self.recording.index[index_counter] + 30):
                    #plt.plot(x, vals)
                    #plt.plot(x[averaging_length-1:], smoothed)
                    #window_x = (self.recording.range*2)-window_size
                    #plt.plot(x[window_x:window_x+window_size], window)
                    #plt.show()
                    if index_counter < len(self.recording.index) - 1:
                        index_counter += 1

                correlation = np.correlate(smoothed, window)
                if max(abs(correlation[10:-10])) > correlation_thresh:
                    guessed_class = net.query(Filters.fft(vals, self.recording.window)[1])
                    classes.append(np.argmax(guessed_class) + 1)
                    indices.append(center)
                    duplicate = False
                    if len(indices) >= 2 and (center < (indices[-2] + duplicate_range)):
                        if classes[-1] == classes[-2]:
                            del classes[-1]
                            del indices[-1]
                            duplicate = True

                    if not duplicate:  # and not self.test:
                        knn_series.append(smoothed)
                        #plt.plot(x, vals)
                        #plt.plot(x[averaging_length-1:], smoothed)
                        #plt.show()
                        None
                else:
                    None
        found = len(indices)
        print('\nCorrelation Method Total Found', found, 'Indices')

        if knn is not None and pca is not None:
            test_ext = pca.transform(knn_series)
            min_max_scaler = MinMaxScaler()
            test_norm = min_max_scaler.fit_transform(test_ext)
            knn_classes = knn.predict(test_norm)
            disagreements = [indices[i] for i in range(found) if classes[i] != knn_classes[i]]
            print('Net and KNN Agreed on', found - len(disagreements), 'out of the ', found, 'generated classes')
            print('... An agreement percentage: %.2f' % ((found-len(disagreements)) / found * 100.0))

        if self.test:
            score = self.test_indices(indices)
            self.recording.index = np.array(indices)
            return score
        else:
            self.recording.classes = np.array(classes)

        self.recording.index = np.array(indices)

    def median_method(self):
        indices = []
        window_length = 35 #80
        step = 35
        grad_step = 1
        thresh = 1.5
        max_grad = 0
        length = len(self.recording.d)

        for i in range(0, length, step):
            grads = []
            end = i + window_length #length-1)
            if end >= length:
                end = length - 1
            series = np.copy(self.recording.d[i:end])
            median = np.median(series)
            adjusted_series = np.subtract(series, median)
            adjusted_series *= (np.hanning(len(series)) * 4)
            adjusted_series = np.gradient(adjusted_series)
            zero_crossings = np.where(np.diff(np.sign(adjusted_series)))[0]
            for crossing in zero_crossings:
                diff = adjusted_series[crossing] - adjusted_series[crossing + 1]
                if np.sign(adjusted_series[crossing]) == 1 and diff > thresh:
                    indices.append(i + crossing)

            if max(adjusted_series) > max_grad:
                max_grad = max(adjusted_series)

        print(max_grad)
        print('\nMedian Method Total Indices Found', len(indices))
        if self.test:
            self.test_indices(indices)

        self.recording.index = np.array(indices)

    def test_indices(self, generated_indices):
        thresh = 50
        indices = list(generated_indices)
        total_indices = len(indices)
        expected_total_indices = len(self.recording.index)
        sorted_index = sorted(self.recording.index)
        correct = []
        missed = []
        # indices = list(self.recording.index)

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
        length_mismatch = max(0, (total_indices - expected_total_indices), (expected_total_indices - total_indices))
        score = float(max(0, (total_correct - total_missed - length_mismatch))/expected_total_indices)
        print('Total Correct', total_correct)
        print('Total Missed', total_missed)
        print('Length Mismatch With Training Set', length_mismatch)
        print('Index performance = %.2f' % (100.0*score))
        return score


if __name__ == '__main__':
    from Recording import Recording

    training_set = Recording(filename='training')
    training_set.sort_indices_in_place()

    correlation_set = training_set.__copy__()
    correlation_index_finder = IndexIdentifiers(correlation_set)
    correlation_index_finder.correlation_method()

    #median_set = training_set.__copy__()
    #median_index_finder = IndexIdentifiers(median_set)
    #median_index_finder.median_method()

    submission_set = Recording(filename='submission')
    index_finder = IndexIdentifiers(submission_set, test=False)
    index_finder.correlation_method()
