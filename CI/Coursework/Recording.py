import scipy.io as spio
import numpy as np
import matplotlib.pyplot as plt


class Recording:
    def __init__(self, filename):
        self._period = 1 / 25e3

        if '.mat' not in filename:
            filename += '.mat'

        try:
            mat = spio.loadmat(filename, squeeze_me=True)
            self._d = mat['d']
            self._index = mat['Index']
            self._morphology = mat['Class']
        except Exception as e:
            print('Error generating .mat file:\n', e)
            return None

    @property
    def d(self):
        return self._d

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    @property
    def morphology(self):
        return self._morphology

    @morphology.setter
    def morphology(self, morphology):
        self._morphology = morphology

    def plot(self):
        total_samples = len(self.d)
        time = np.linspace(0, total_samples-1, total_samples) * self.period
        plt.plot(time, self.d)
        plt.show()

    def generate_mat(self, filename):
        if '.mat' not in filename:
            filename += '.mat'

        mat = {
            'd': self.d,
            'Index': self.index,
            'Class': self.morphology
        }

        try:
            spio.savemat(filename, mat)
        except Exception as e:
            print('Error generating .mat file:\n', e)
            return False

        return True
