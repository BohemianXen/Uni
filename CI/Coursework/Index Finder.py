def correlation_method(self):
    indices = []
    #  self.recording.slice(recording.index[1])[1]
    step = 20
    thresh = 19
    thresh2 = 0.28
    length = len(self.recording.d)
    averaging_length = 4
    index_counter = 0
    for i in range(0, length, step):
        end = min(i + step, length - 1)
        series = self.recording.d[i:end]
        diff = np.ediff1d(self.moving_average(series, averaging_length))

        if self.test and (self.recording.index[0] - 30 < i < self.recording.index[0] + 30):
            g = np.ediff1d(series)

        if max(diff) > thresh2:
            center = i + np.argmax(diff)
            [x, vals] = self.recording.slice(center)
            smoothed = self.moving_average(vals, averaging_length)
            smoothed = np.subtract(smoothed, np.median(vals[0:6]))
            window = np.hanning(50) * 3
            if self.test:
                closest_index = self.recording.index[index_counter]
            if self.test and (self.recording.index[index_counter] - 30 < i < self.recording.index[index_counter] + 30):
                ##plt.plot(x, vals)
                # plt.plot(x[averaging_length-1:], smoothed)
                # plt.show()

                index_counter += 1

            correlation = np.correlate(smoothed, window)
            if abs(max(correlation)) > thresh:
                indices.append(i + self.recording.range)
            else:
                if self.test:
                    print(i, max(correlation))

    print('\nCorrelation Method Total Indices Found', len(indices))
    if self.test:
        self.test_indices(indices)

    self.recording.index = np.array(indices)


@staticmethod
def moving_average(series, length):
    summed = np.cumsum(series)
    valid_range = summed[length:] - summed[:-length]
    summed[length:] = valid_range
    averaged = summed[length - 1:] / length
    return averaged