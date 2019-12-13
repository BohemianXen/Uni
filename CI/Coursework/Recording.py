import scipy.io as spio
import numpy as np
from sklearn.decomposition import PCA as sk_pca


class Recording:
    """Recording class. Holds the instance recording data that is to be observed and manipulated.
    Parameters:
        d (ndarray, optional): Recorded data. Defaults to None.
        index (ndarray, optional): Spike positions. Defaults to None.
        classes (ndarray, optional): Spike types. Defaults to None.
        filename (str, optional): Name of the .mat file to read in. Defaults to None to allow shallow copying of recordings.
        colour (str, optional): Default plot colour for the recording. Defaults to 'black'.
    """

    def __init__(self, d=None, index=None, classes=None, filename=None, colour='black', components=20):
        # Common parameters
        self._period = 1 / 25e3
        self._range = 36  # +/- Tbservaion window size about a given Index
        self._offset = 10  # Targinally account for fact indices start at beginning of spikes
        self._window = 'hanning'  # Type of smoothing window to be used
        self._colourmap = [colour, 'red', 'green', 'blue', 'yellow',  'purple']  # Series colour followed by Class types
        self._pca = sk_pca(components)

        if filename is None:  # Shallow copying pre-existing Recording
            self._d = d
            self._index = index
            self._classes = classes
        else:  # Attempt to read in .mat file
            try:
                if '.mat' not in filename:
                    filename += '.mat'
                mat = spio.loadmat(filename, squeeze_me=True)
                self._d = mat['d']
                if 'submission' not in filename:
                    self._index = mat['Index']
                    self._classes = mat['Class']
            except Exception as e:
                print('\nError reading .mat file:\n'.upper(), e)
                exit(-1)

    def __copy__(self):
        """Returns a shallow copy of the Recording."""
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

    @property
    def pca(self):
        return self._pca

# ----------------------------------------------------- Methods --------------------------------------------------------
    def sort_indices_in_place(self):
        """Pairs all indices with their respective classes before sorting in ascending Index order."""
        paired = [[self.index[i], self.classes[i]] for i in range(0, len(self.index))]
        paired = sorted(paired, key=lambda x: x[0])

        # Update Index and Class vectors to reflect sorting
        self.index = np.array([x[0] for x in paired])
        self.classes = np.array([x[1] for x in paired])

    def slice(self, center, all=False, x_needed=False):
        """Gets a window about a given sample no. index using the default Recording +/- range.
        Parameters:
            center(int): Central sample no. to take window about.
            all (bool, optional): Whether to just plot all samples in recording, rarely necessary. Defaults to False.
            x_needed (bool, optional): Whether to also return the corresponding sample no. array. Defaults to False.
        Returns:
             (list, ndarray): The window sample no. values (optionally) and the recording data (always)
       """
        total_samples = len(self.d) if all else (self.range * 2)
        start = 0 if all else center - self.range
        stop = total_samples if all else center + self.range
        start += self.offset
        stop += self.offset

        # Sanitise window sample no. limits
        if start < 0:
            start = 0
            stop = total_samples
        if stop > len(self.d):
            stop = len(self.d)
            if not all:
                start = stop - total_samples - 1

        x_axis = np.arange(start, stop)
        if x_needed:  # Return required window of data as well as the sample no. x axis
            return [x_axis, np.copy(self.d[start:stop])]
        else:  # Return just the required window of data
            return np.copy(self.d[start:stop])

    def generate_mat(self, filename):
        """Generates a .mat file of the Recording instance.
        Parameters:
            filename(str): The intended filename of the written .mat file.
        Returns:
            (bool): Whether or not the writing process was successful.
        """

        # Generate dict of current Recording data, Index, and Class vectors
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
