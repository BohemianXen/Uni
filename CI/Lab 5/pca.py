import numpy
# Sklearn contains some useful CI tools
# PCA
from sklearn.decomposition import PCA as sk_pca

# Matplotlib for plotting
import matplotlib.pyplot as plt

class PCA:

    def __init__(self, test_filename, train_filename, components):

        # Load the train and test MNIST data
        self.train = numpy.loadtxt(train_filename, delimiter=',')
        self.test = numpy.loadtxt(test_filename, delimiter=',')
        self.components = components

        # Separate labels from training data
        self.train_data = self.train[:, 1:]
        self.train_labels = self.train[:, 0]
        self.test_data = self.test[:, 1:]
        self.test_labels = self.test[:, 0]

        self._pca = sk_pca(n_components=self.components)
        self._pca.fit(self.train_data)

    def refit(self):
        # Select number of components to extract
        self._pca = sk_pca(n_components=self.components)
        # Fit to the training data
        self._pca.fit(self.train_data)

        # Determine amount of variance explained by components
        print('Total Variance Explained: ', numpy.sum(self._pca.explained_variance_ratio_))

    def plot(self):
        # Plot the explained variance
        plt.plot(self._pca.explained_variance_ratio_)
        plt.title('Variance Explained by Extracted Componenents')
        plt.ylabel('Variance')
        plt.xlabel('Principal Components')
        #plt.show()
