from __future__ import print_function
from abc import ABCMeta, abstractmethod
import numpy as np
from scipy.io import savemat
from tensorflow.keras import models
from tensorflow.keras.utils import plot_model
from sklearn import metrics
from processing.DataProcessors import DataProcessors
from processing.CSVConverters import CSVConverters
import matplotlib.pyplot as plt

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class NeuralNet(metaclass=ABCMeta):
    def __init__(self):
        self.name = self.__class__.__name__
        self._mag = False
        self._inputs = 0
        self._outputs = 0
        self._epochs = 0
        self._batch_size = 0
        self._samples = 0
        self._train_data = []
        self._val_data = []
        self._model = None
        self._history = None

    # ----------------------------------------------- Properties -------------------------------------------------------

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    @property
    def train_data(self):
        return np.copy(self._train_data)

    # ---------------------------------------------- Abstract Methods --------------------------------------------------

    @abstractmethod
    def create_model(self):
        """Creates a keras model based on the Functional API"""
        pass

    @staticmethod
    @abstractmethod
    def pre_process(raw_data, single):
        """Feature extraction"""
        pass

    @staticmethod
    @abstractmethod
    def get_stop_conditions():
        """Feature extraction"""
        pass

    # ----------------------------------------------- Static Methods ---------------------------------------------------
    @staticmethod
    def load_model(filename):
        """Loads and returns a previously created model"""

        try:
            model = models.load_model(filename)
            return model
        except FileNotFoundError as path_error:
            print('Could not find path to .h5 file: {}'.format(filename))
            print(path_error)
            return -1
        except Exception as e:
            print('Failed to load model: {}'.format(filename))
            print(e)
            return -1

    # ----------------------------------------------- Class Methods ----------------------------------------------------

    def load_data(self, roots):
        """Parses all recorded data held within input directories and converts all entries into a normalised np array"""

        for root in roots:  # For each directory
            # Check if loading train or test data
            train = True if 'Training Data' in root else False
            test = True if 'Test Data' in root else False

            all_data = []
            files, labels = CSVConverters.get_data_files(root)  # Get all csv files within the current directory

            if len(files) == 0:
                return False
            else:
                ignored = 0
                for i, file in enumerate(files):
                    data = CSVConverters.csv_to_list(file, remove_mag=(not self._mag))  # Read samples in current file

                    # If simulating short capture, skip last few samples of recording
                    if len(data) > self._samples:
                        data = data[:self._samples]

                    # Normalise and flatten the data samples then prefix the label
                    features = self.pre_process(data)
                    if features is not None:
                        all_data.append(np.concatenate([[labels[i]], features]))
                    else:
                        print('Out of range value detected in:', file)
                        ignored += 1

                print('\nIgnored %d files that had out-of-range values; a ~%.2f%% occurrence rate\n'
                      % (ignored, (ignored/len(all_data) * 100.0)))

            if len(all_data) == 0:
                return False  # No data read in
            else:

                if test:
                    return np.copy(all_data)  # Only need a copy of the data if parsing test directories
                elif train:
                    self._train_data = np.copy(all_data)
                else:
                    self._val_data = np.copy(all_data)

        return True

    def train(self, shuffle=True, save_model=False, save_data=False, plot=True):
        """Trains the model currently held in the model instance attribute"""

        print('Training net\n')
        self._history = None
        val_given = len(self._val_data) != 0  # Check if validation data has been specified

        # Early stopping criteria to stop overfitting
        callback_list = self.get_stop_conditions()

        # Separate labels and train data, shuffling if necessary since they are initially read-in in time order
        train_data, train_targets = DataProcessors.parse_train_data(self._train_data, self._outputs, shuffle)

        if len(self.model.input_shape) == 3:
            train_data = np.expand_dims(train_data, axis=2)

        # Fit model and validate either using given validation data or by splitting the training data
        if val_given:
            val_data, val_targets = DataProcessors.parse_train_data(self._val_data, self._outputs, shuffle)

            if len(self.model.input_shape) == 3:
                val_data = np.expand_dims(val_data, axis=2)

            self._history = self._model.fit(train_data, train_targets, validation_data=(val_data, val_targets),
                                            epochs=self._epochs, batch_size=self._batch_size,
                                            verbose=2, callbacks=callback_list)
        else:
            self._history = self._model.fit(train_data, train_targets, epochs=self._epochs, batch_size=self._batch_size,
                                            validation_split=0.15, verbose=2, callbacks=callback_list)

        if save_data:
            self.save_train_data('Test')

        if save_model:
            self.save_model()

        if plot:
            self.plot()

        return self._history is not None

    def save_model(self):
        """Saves the model held in the _model instance attribute as HDF5 file"""
        # TODO: Better to use checkpoints during training, save only best (lowest)

        filename = '%f - %d inputs_%s.h5' % ((self._history.history['loss'][-1]), self._inputs, self.name)  # Add loss to filename
        filename = 'Saved Models\\Loss - ' + filename
        try:
            self._model.save(filename, overwrite=True)
            return filename
        except Exception as e:
            print('Failed to save ' + filename)
            print(e)
            return False

    def save_train_data(self, filename):
        """Saves the labelled training data held in the _train_data instance attribute as a .csv and .mat file"""

        if len(self._train_data) != 0:
            full_filename = '{0}_{1}.csv'.format(filename, len(self._train_data))
            print('Saving training data in: ' + filename)
            try:
                # np.save(full_filename, self._train_data, delimiter=',')
                cols = {'labels': self._train_data[:, 0], 'data': self._train_data[:, 1:]}
                savemat(full_filename.rstrip('.csv') + '.mat', cols)

            except Exception as e:
                print('Failed to save as .csv and .mat')
                print(e)

    def plot(self):
        """Creates subplots of per-epoch train/validation loss/accuracy history"""

        if self._history is None:
            return False
        else:
            fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex='all')
            fig.tight_layout(pad=3.0)

            # Loss plot
            ax1.plot(self._history.history['loss'], label='Training')
            ax1.plot(self._history.history['val_loss'], label='Validation')
            ax1.legend()
            ax1.set_title('Loss')
            ax1.set_ylabel('Loss')

            # Accuracy plot
            ax2.plot(self._history.history['accuracy'], label='Training')
            ax2.plot(self._history.history['val_accuracy'], label='Validation')
            ax2.legend()
            ax2.set_title('Accuracy')
            ax2.set_xlabel('Epoch')
            ax2.set_ylabel('Accuracy')

            plt.show()

            # plot_model(self.model, to_file='model.png')
            return True

    def predict_directory(self, root, shuffle=True):
        """Gets all files in the given test directory and predicts the class of data in each line"""

        test_data = self.load_data([root])
        score = 0.0
        size = len(test_data)

        if size != 0:
            data = np.zeros((size, len(test_data[0]) - 1), dtype=np.float32)
            labels = np.zeros(size, dtype=np.int32)

            if shuffle:
                print('Shuffling test data\n')
                np.random.shuffle(test_data)

            for i, sample in enumerate(test_data):
                data[i] = sample[1:]  # Remove label from data
                labels[i] = int(sample[0])

            try:
                if len(self.model.input_shape) == 3:
                    data = np.expand_dims(data, axis=2)
            except AttributeError:
                pass

            print('Predicting...\n')
            predictions = self._model.predict(data)
            guesses = np.zeros(len(predictions))

            test_matrix = np.zeros(shape=(self._outputs, self._outputs))
            for i, sample in enumerate(predictions):
                # print(predictions[i])

                if np.ndim(predictions) > 1:
                    guess = np.argmax(predictions[i])  # Best guess is highest probability* score in prediction
                else:
                    guess = int(predictions[i])  # KNN predict is one dimensional

                guesses[i] = guess
                if labels[i] == guess:
                    test_matrix[int(guess)][int(guess)] += 1
                    score += 1
                else:
                    test_matrix[int(labels[i])][int(guess)] += 1
                    # pred = predictions[i]
                    # true = labels[i]
                    # print(true, guess, pred)

            score = (score / size) * 100.0
            print('Net performance: %.2f%%\n' % score)
            for row in test_matrix:
                print(row)

            names = ['Standing', 'Walking', 'Lying F', 'Lying L', 'Lying R', 'Fall F', 'Fall L', 'Fall R']
            print('\n')
            print(metrics.classification_report(labels, guesses, target_names=names, digits=4))
            return score
        else:
            return -1


class Tests:
    def __init__(self, params):
        self._params = params

    def train_net(self, net, shuffle=True, plot=True, save_model=False, save_data=False, predict=True, test_save=False):
        baseline = -1

        loaded = net.load_data(roots=[self._params['train_root'], self._params['val_root']])
        if loaded:
            assert net.train(shuffle=shuffle, save_model=save_model, save_data=save_data, plot=plot)

        if predict:
            baseline = net.predict_directory(root=self._params['test_root'])
            assert baseline != -1

        if predict and test_save and not save_model:
            saved_filename = net.save_model()
            assert saved_filename is not False

            score = self.save_model(net, filename=saved_filename)
            min_score = 0.8 * baseline
            assert min_score <= score

    def save_model(self, net, filename):
        net.model = None
        full_path = os.path.join(os.getcwd(), filename)
        model = NeuralNet.load_model(full_path)
        assert model is not None

        net.model = model
        score = net.predict_directory(root=self._params['test_root'])

        return score
