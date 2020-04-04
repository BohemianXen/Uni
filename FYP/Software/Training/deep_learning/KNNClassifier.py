from __future__ import print_function

import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from deep_learning import RawNeuralNet, SMVNeuralNet
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors, datasets


class KNNClassifier:

    def __init__(self, neighbours=4, distance=3, train_root='', val_root=''):
        super().__init__()
        self.name = self.__class__.__name__
        self._neighbours = neighbours
        self._distance = distance
        self._train_root = train_root
        self._val_root = val_root
        self._model = None
        self._train_data = None
        self._helper = SMVNeuralNet()

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
        """Creates a keras model based on the Functional API"""

        #train_ext = pca.fit_transform([pair[0] for pair in paired])
        #min_max_scaler = MinMaxScaler()
        #train_norm = min_max_scaler.fit_transform(train_ext)
        self._model = KNeighborsClassifier(n_neighbors=self._neighbours, p=self._distance)
        self._model.fit(self._train_data[:, 1:], self._train_data[:, 0])

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
        self._helper.predict_directory(root=root, shuffle=shuffle)

    # def plot(self):
    #     h = .02  # step size in the mesh
    #
    #     # Create color maps
    #     cmap_light = ListedColormap(['orange', 'cyan', 'cornflowerblue'])
    #     cmap_bold = ListedColormap(['darkorange', 'c', 'darkblue'])
    #
    #     for weights in ['uniform', 'distance']:
    #         # we create an instance of Neighbours Classifier and fit the data.
    #         clf = neighbors.KNeighborsClassifier(n_neighbors, weights=weights)
    #         clf.fit(X, y)
    #
    #         # Plot the decision boundary. For that, we will assign a color to each
    #         # point in the mesh [x_min, x_max]x[y_min, y_max].
    #         x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    #         y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    #         xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
    #                              np.arange(y_min, y_max, h))
    #         Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    #
    #         # Put the result into a color plot
    #         Z = Z.reshape(xx.shape)
    #         plt.figure()
    #         plt.pcolormesh(xx, yy, Z, cmap=cmap_light)
    #
    #         # Plot also the training points
    #         plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
    #                     edgecolor='k', s=20)
    #         plt.xlim(xx.min(), xx.max())
    #         plt.ylim(yy.min(), yy.max())
    #         plt.title("3-Class classification (k = %i, weights = '%s')"
    #                   % (n_neighbors, weights))
    #
    #         plt.show()


class Tests:
    def __init__(self, params):
        self._params = params

    def fit_knn(self, knn):
        knn.load_data()


if __name__ == '__main__':
    params = {
        'neighbours': 5,
        'distance': 2,
        'train_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data',
        'val_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Validation Data',
        'test_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Test Data',
        'save': False

    }

    knn = KNNClassifier(neighbours=params['neighbours'], distance=params['distance'], train_root=params['train_root'],
                        val_root=params['val_root'])

    knn.predict_directory(params['test_root'])

    if params['save']:
        knn.save_model()

    # model = knn.load_model(r"C:\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\deep_learning\Saved Models\5 Neighbours - 3 Norm - 8 classes_KNNClassifier")
    #print(type(model))
