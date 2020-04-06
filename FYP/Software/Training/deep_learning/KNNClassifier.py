from __future__ import print_function

import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import NeighborhoodComponentsAnalysis as sk_nca
from sklearn.decomposition import PCA as sk_pca
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as sk_lda
from deep_learning import RawNeuralNet, SMVNeuralNet

import matplotlib.pyplot as plt
import matplotlib


class KNNClassifier:

    def __init__(self, neighbours=5, distance=3, weights='uniform', decomposer=None, components=2, train_root='', val_root=''):
        super().__init__()
        self.name = self.__class__.__name__
        self._neighbours = neighbours
        self._distance = distance
        self._weights = weights
        self._train_root = train_root
        self._val_root = val_root
        self._model = None
        self._train_data = None
        self._components = components
        self._decomposer = None if decomposer is None else decomposer(n_components=components)
        self._helper = RawNeuralNet() if self._decomposer else SMVNeuralNet()


        self.load_data()
        self.create_model()
    # ------------------------------------------------- Properties -----------------------------------------------------

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    def create_model(self):
        """Creates and fits a KNN classifier using the scikit-learn lib"""

        self._model = KNeighborsClassifier(n_neighbors=self._neighbours, p=self._distance, weights=self._weights)
        labels = self._train_data[:, 0]

        if self._decomposer is not None:
            # lda = sk_lda(n_components=self._components)
            features = self._decomposer.fit_transform(self._train_data[:, 1:], labels)

        else:
            features = self._train_data[:, 1:]

        self._model.fit(features, labels)

            # import seaborn as sns
            # import pandas as pd
            # data = pd.DataFrame(self._train_data)  # columns=(['label'].extend([('c' + str(i)) for i in range(14)])))
            # data_corr = data.corr()
            # sns.heatmap(data_corr)
            # plt.show()

    @staticmethod
    def pre_process(raw_data, single=False):
        """Simply flattens and normalises raw data as per sensor max/mins"""
        return SMVNeuralNet.pre_process(raw_data, single=single)

    def load_data(self, shuffle=True):
        self._helper.load_data(roots=[self._train_root, self._val_root])
        self._train_data = self._helper.train_data
        if shuffle:
            np.random.shuffle(self._train_data)

    def save_model(self):
        filename = '%d Neighbours - %d Norm - %d classes_%s' % (self._neighbours, self._distance,
                                                                len(self._model.classes_), self.name)
        if self._pca:
            filename = 'Saved Models\\' + '%d PCA - ' % self._components + filename
        else:
            filename = 'Saved Models\\' + filename
        try:
            pickle.dump(self._model, open(filename, 'wb'))
        except Exception as e:
            print('Failed to pickle ', filename)
            print(e)

    @staticmethod
    def load_model(filename):
        """Loads and returns a previously created model"""

        try:
            model = pickle.load(open(filename, 'rb'))
            return model
        except FileNotFoundError as path_error:
            print('Could not find path to pickle file: {}'.format(filename))
            print(path_error)
            return -1
        except Exception as e:
            print('Failed to load model: {}'.format(filename))
            print(e)
            return -1

    def predict_directory(self, root, shuffle=True):
        self._helper.model = self._model
        return self._helper.predict_directory(root=root, shuffle=shuffle, decomposer=self._decomposer)

# ---------------------------------------------------- Plotting --------------------------------------------------------
    from matplotlib.colors import ListedColormap

    def plot(self):
        h = .01  # step size in the mesh

        # Create color maps
        cmap_light = cmap_map(lambda x: x/2 + 0.5, matplotlib.cm.jet)
        cmap_bold = matplotlib.cm.jet

        if self._decomposer is None:
            X = self._train_data[:, [13, 14]]
        else:
            X = self._decomposer.transform(self._train_data[:, 1:])

        y = self._train_data[:, 0]

        clf = KNeighborsClassifier(self._neighbours, weights=self._weights)
        clf.fit(X, y)

        # Plot the decision boundary. For that, we will assign a color to each
        # point in the mesh [x_min, x_max]x[y_min, y_max].
        x_min, x_max = X.min() - 0.5, X.max() + 0.5
        y_min, y_max = X.min() - 0.5, X.max() + 0.5

        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        # Z = self._model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        plt.figure()

        plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

        # Plot also the training points
        plt.scatter(X[:, 0], X[:, 1], c=y, edgecolor='k', s=20, cmap=cmap_bold)
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        # plt.title("3-Class classification (k = %i, weights = '%s')"
        #           % (n_neighbors, weights))
        # plt.legend()
        plt.show()


def cmap_map(function, cmap):  # from https://scipy-cookbook.readthedocs.io/items/Matplotlib_ColormapTransformations.html
    """ Applies function (which should operate on vectors of shape 3: [r, g, b]), on colormap cmap.
    This routine will break any discontinuous points in a colormap.
    """
    cdict = cmap._segmentdata
    step_dict = {}
    # Firt get the list of points where the segments start or end
    for key in ('red', 'green', 'blue'):
        step_dict[key] = list(map(lambda x: x[0], cdict[key]))
    step_list = sum(step_dict.values(), [])
    step_list = np.array(list(set(step_list)))
    # Then compute the LUT, and apply the function to the LUT
    reduced_cmap = lambda step : np.array(cmap(step)[0:3])
    old_LUT = np.array(list(map(reduced_cmap, step_list)))
    new_LUT = np.array(list(map(function, old_LUT)))
    # Now try to make a minimal segment definition of the new LUT
    cdict = {}
    for i, key in enumerate(['red','green','blue']):
        this_cdict = {}
        for j, step in enumerate(step_list):
            if step in step_dict[key]:
                this_cdict[step] = new_LUT[j, i]
            elif new_LUT[j,i] != old_LUT[j, i]:
                this_cdict[step] = new_LUT[j, i]
        colorvector = list(map(lambda x: x + (x[1], ), this_cdict.items()))
        colorvector.sort()
        cdict[key] = colorvector

    return matplotlib.colors.LinearSegmentedColormap('colormap',cdict,1024)


class Tests:
    def __init__(self, params):
        self._params = params

    def fit_knn(self, knn):
        knn.load_data()


if __name__ == '__main__':
    params = {
        'neighbours': 3,   # nca best is 10, 2, 10
        'distance': 2,
        'weights': 'distance',  # 'distance'
        'decomposer': sk_pca,
        'components': 3,
        'train_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data',
        'val_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Validation Data',
        'test_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Test Data',
        'save': False,
        'plot': False

    }

    knn = KNNClassifier(neighbours=params['neighbours'], distance=params['distance'], weights=params['weights'],
                        decomposer=params['decomposer'], components=params['components'], train_root=params['train_root'],
                        val_root=params['val_root'])

    if params['plot']:
        knn.plot()

    knn.predict_directory(params['test_root'])

    if params['save'] and params['decomposer'] is None:
        knn.save_model()
