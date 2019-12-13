import scipy.io as spio
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA as sk_pca


class Recording:
    def __init__(self, d=None, index=None, classes=None, filename=None, colour='black', components=20):
        self._period = 1 / 25e3
        self._range = 36
        self._offset = 10
        self._window = 'hanning'
        self._colourmap = [colour, 'red', 'green', 'blue', 'yellow',  'purple']
        self.pca = sk_pca(components)  #TODO: PROTECT

        if filename is None:
            self._d = d
            self._index = index
            self._classes = classes
        else:
            try:
                print(("\n Trying to load %s .mat file..."%filename).upper())
                if '.mat' not in filename:
                    filename += '.mat'
                mat = spio.loadmat(filename, squeeze_me=True)
                self._d = mat['d']
                if 'submission' not in filename:
                    self._index = mat['Index']
                    self._classes = mat['Class']
                print(("\n Successfully to loaded %s .mat file..." % filename).upper())
            except Exception as e:
                print('Error generating .mat file:\n', e)
                exit(-1)
        #self.sort_indices_in_place()

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
        self._range = range_in

    @property
    def offset(self):
        return self._offset

    @property
    def window(self):
        return self._window

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

# ----------------------------------------------------- Methods --------------------------------------------------------
    def sort_indices_in_place(self):
        paired = [[self.index[i], self.classes[i]] for i in range(0, len(self.index))]
        paired = sorted(paired, key=lambda x: x[0])
        self.index = np.array([x[0] for x in paired])
        self.classes = np.array([x[1] for x in paired])

    def slice(self, center, all=False, x_needed=False):
        total_samples = len(self.d) if all else (self.range * 2)
        start = 0 if all else center - self.range
        stop = total_samples if all else center + self.range
        start += self.offset
        stop += self.offset

        if start < 0:
            start = 0
            stop = total_samples

        if stop > len(self.d):
            stop = len(self.d)
            start = stop - total_samples - 1

        x_axis = np.arange(start, stop)
        if x_needed:
            return [x_axis, np.copy(self.d[start:stop])]
        else:
            return  np.copy(self.d[start:stop])

    def generate_mat(self, filename):

        mat = {
            'd': self.d,
            'Index': self.index,
            'Class': self.classes
        }

        try:
            spio.savemat(filename, mat)
            print('Successfully saved: %s' % filename)
        except Exception as e:
            print('Error generating .mat file:\n', e)
            return False

        return True
