import numpy as np
import matplotlib.pyplot as plt
from Filters import Filters


class IndexIdentifiers:
    def __init__(self, recording, test=True):
        self.recording = recording
        self.test = test

    def correlation_method(self, net, knn=None):
        net_indices = []
        knn_indices = []
        net_classes = []
        knn_classes = []
        step = 18
        diff_thresh = 0.3
        correlation_thresh = 40
        window_size = 50
        window_voltage = 3
        length = len(self.recording.d)
        averaging_length = 4
        duplicate_range = 20 #14
        index_counter = 0

        for i in range(self.recording.range, length-self.recording.range, step):
            end = min(i + step, length - 1)
            series = self.recording.d[i:end]
            diff = np.ediff1d(Filters.smooth(series, averaging_length, just_average=True))

            if max(diff) > diff_thresh:
                center = i + np.argmax(diff)
                [x, vals] = self.recording.slice(center, x_needed=True)
                smoothed = Filters.smooth(vals, averaging_length=averaging_length, just_average=True)
                smoothed = np.subtract(smoothed, np.median(smoothed))
                window = np.hanning(window_size) * window_voltage

                if self.test and (self.recording.index[index_counter] - 30 < i < self.recording.index[index_counter] + 30):
                    #plt.plot(x, vals)
                    #plt.plot(x[averaging_length-1:], smoothed)
                    #window_x = (self.recording.range*2)-window_size
                    #plt.plot(x[window_x:window_x+window_size], window)
                    #plt.show()
                    if index_counter < len(self.recording.index) - 1:
                        index_counter += 1

                correlation = np.correlate(smoothed, window)
                if max(abs(correlation)) > correlation_thresh:
                    guessed_class = net.query(Filters.fft(vals, self.recording.window)[1])
                    net_classes.append(np.argmax(guessed_class) + 1)
                    net_indices.append(center)
                    #knn_classes.append(knn.predict())
                    duplicate = False
                    if len(net_indices) >= 2 and (center < (net_indices[-2] + duplicate_range)):
                        if net_classes[-1] == net_classes[-2]:
                            del net_classes[-1]
                            del net_indices[-1]
                            duplicate = True

                    if not self.test and not duplicate:
                        #plt.plot(x, vals)
                        #plt.plot(x[averaging_length-1:], smoothed)
                        #plt.show()
                        None
                else:
                    None

        print('Correlation Method Total Indices Found', len(net_indices))

        if self.test:
            self.test_indices(net_indices)
        else:
            self.recording.classes = np.array(net_classes)
            None

        self.recording.index = np.array(net_indices)

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
        score = max(0, (total_correct - total_missed - length_mismatch))
        print('Total Correct', total_correct)
        print('Total Missed', total_missed)
        print('Length Mismatch', length_mismatch)
        print('Index performance = %.2f' % (100.0*score/expected_total_indices))


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
