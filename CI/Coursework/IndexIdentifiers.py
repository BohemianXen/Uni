import numpy as np
import matplotlib.pyplot as plt
from Filters import Filters
from sklearn.preprocessing import MinMaxScaler


class IndexIdentifiers:
    def __init__(self, recording, test=True):
        self.recording = recording
        self.test = test

    def correlation_method(self, net, knn=None, pca=None, ):
        indices, classes, knn_series = [], [], []
        step = int(self.recording.range/2)
        diff_thresh, correlation_thresh = 0.28, 30
        window_size, window_voltage = 30, 3
        window = np.hanning(window_size) * window_voltage
        length = len(self.recording.d)
        averaging_length = 3
        duplicate_range = 30
        plot_correlation = False  # For test purposes

        for i in range(self.recording.range, length-self.recording.range, step):
            end = min(i + step, length - 1)
            series = self.recording.d[i:end]
            diff = np.ediff1d(Filters.smooth(series, averaging_length, just_average=True))

            if max(diff) > diff_thresh:
                center = i + np.argmax(diff)
                [x, vals] = self.recording.slice(center, x_needed=True)
                smoothed = Filters.smooth(vals, averaging_length+1)
                correlation = np.correlate(smoothed, window)

                if max(abs(correlation[5:-5])) > correlation_thresh:
                    indices.append(center)
                    guessed_class = net.query(Filters.fft(vals, self.recording.window)[1])
                    classes.append(np.argmax(guessed_class) + 1)
                    duplicate = False
                    if len(indices) >= 2 and (center < (indices[-2] + duplicate_range)):
                        if classes[-1] == classes[-2]:
                            del classes[-1]
                            del indices[-1]
                            duplicate = True

                    if plot_correlation and not self.test:
                        self.plot_correlation(x, smoothed, correlation, window)

                    if not duplicate:
                        knn_series.append(smoothed)

        found = len(indices)
        print('\nCorrelation Method Total Found', found, 'Indices')

        if knn is not None and pca is not None:
            test_ext = pca.transform(knn_series)
            min_max_scaler = MinMaxScaler()
            test_norm = min_max_scaler.fit_transform(test_ext)
            knn_classes = knn.predict(test_norm)
            disagreements = [indices[i] for i in range(found) if classes[i] != knn_classes[i]]
            print('Net and KNN Agreed on', found - len(disagreements), 'out of the ', found, 'generated classes')
            if found != 0:
                print('... An agreement percentage: %.2f' % ((found-len(disagreements)) / found * 100.0))

        if self.test:
            score = self.test_indices(indices)
            self.recording.index = np.array(indices)
            return score
        else:
            self.recording.classes = np.array(classes)

        self.recording.index = np.array(indices)

    @staticmethod
    def plot_correlation(x, series, correlation, window):
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

    def median_method(self):
        indices = []
        window_length = 35  # 80
        step = 35
        grad_step = 1
        thresh = 1.5
        max_grad = 0
        length = len(self.recording.d)

        for i in range(0, length, step):
            grads = []
            end = i + window_length  # length-1)
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
