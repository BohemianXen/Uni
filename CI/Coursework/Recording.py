import scipy.io as spio
import numpy as np
import matplotlib.pyplot as plt


class Recording:
    def __init__(self, d=None, index=None, classes=None, filename=None, colour='black'):
        self._period = 1 / 25e3
        self._range = 50
        self._colourmap = [colour, 'red', 'green', 'blue', 'orange']

        if filename is None:
            self._d = d
            self._index = index
            self._classes = classes
        else:
            try:

                if '.mat' not in filename:
                    filename += '.mat'
                mat = spio.loadmat(filename, squeeze_me=True)
                self._d = mat['d']
                self._index = mat['Index']
                self._classes = mat['Class']
            except Exception as e:
                print('Error generating .mat file:\n', e)
                exit(-1)

    def __copy__(self):
        return Recording(self.d, self.index, self.classes)

# ----------------------------------------------------- Properties -----------------------------------------------------
    @property
    def period(self):
        return self._period

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, range_in):
        self._range = self.range_in

    @property
    def colourmap(self):
        return self._colourmap

    @colourmap.setter
    def colourmap(self, colour):
        self._colourmap[0] = colour

    @property
    def d(self):
        return self._d

    @d.setter
    def d(self, d):
        self._d = d

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    @property
    def classes(self):
        return self._classes

    @classes.setter
    def classes(self, classes):
        self._classes = classes

# ----------------------------------------------------- Methods -- -----------------------------------------------------
    def slice(self, center, all=False):
        total_samples = len(self.d) if all else (self._range * 2) + 1
        start = 0 if all else center - self._range
        stop = total_samples - 1 if all else center + self._range
        series = np.linspace(start, stop, total_samples)

        if start < 0:
            start = 0

        if stop > len(self.d):
            stop = len(self.d) - 1

        return [series, np.copy(self.d[start:stop + 1])]

    def generate_mat(self, filename):
        #if '.mat' not in filename:
         #   filename += '.mat'

        mat = {
            'd': self.d,
            'Index': self.index,
            'Class': self.classes
        }

        try:
            spio.savemat(filename, mat)
        except Exception as e:
            print('Error generating .mat file:\n', e)
            return False

        return True
