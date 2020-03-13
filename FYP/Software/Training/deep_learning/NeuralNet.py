from __future__ import print_function
import numpy as np
import tensorflow as tf

from tensorflow.keras import optimizers, losses, layers, callbacks, models
from processing.DataProcessors import DataProcessors
from processing.CSVConverters import CSVConverters
import matplotlib.pyplot as plt

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class NeuralNet:
    def __init__(self, mag=False, cutoff=1, max_samples=480, hiddens=480,  outputs=3, activation='relu', epochs=10, batch_size=32, lr=0.3):
        self._mag = mag
        self._total_samples = max_samples
        self._hiddens = hiddens
        self._outputs = outputs
        self._activation = activation
        self._epochs = epochs
        self._batch_size = batch_size
        self._lr = lr

        self._samples = int(self._total_samples * cutoff)
        self._inputs = (self._samples * 9) if self._mag else (self._samples * 6)

        self._train_data = []
        self._val_data = []
        self._history = None

        if self._mag:
            self._limits = np.array([4, 4, 4, 2000, 2000, 2000, 400, 400, 400])
        else:
            self._limits = np.array([4, 4, 4, 2000, 2000, 2000])

        self._model = self.create_model(self._inputs, self._hiddens, self._outputs, self._batch_size)
    # ------------------------------------------------- Properties -----------------------------------------------------

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    # -------------------------------------------------- Static Methods ------------------------------------------------

    @staticmethod
    def create_model(inputs, hiddens, outputs, batch_size):
        """Creates a keras model based on the Functional API"""

        # Instantiate layers
        input_layer = tf.keras.Input(shape=(inputs,))  # , batch_input_shape=(batch_size, inputs))
        x = layers.Dense(hiddens, activation='relu')(input_layer)
        x = layers.Dense(hiddens, activation='relu')(x)
        output_layer = layers.Dense(outputs, activation='softmax')(x)

        # Choose loss and optimisation functions/algorithms
        model_loss = losses.mean_squared_error  # losses.categorical_crossentropy
        model_optimiser = optimizers.Adam()

        # Instantiate and compile model
        model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
        model.compile(loss=model_loss, optimizer=model_optimiser, metrics=['accuracy'])
        return model

    @staticmethod
    def load_model(filename, single=False):
        """Loads and returns a previously created model"""

        model = models.load_model(filename)  # TODO: try/catch

        if single:
            # FROM https://datascience.stackexchange.com/questions/13461/how-can-i-get-prediction-for-only-one-instance-in-keras
            weights = model.get_weights()
            single_item_model = NeuralNet.create_model()
            single_item_model.set_weights(weights)
            return single_item_model
        else:
            return model

    # -------------------------------------------------- Methods -------------------------------------------------------

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
                for i, file in enumerate(files):
                    data = CSVConverters.csv_to_list(file, remove_mag=(not self._mag))  # Read samples in current file

                    # If simulating short capture, skip last few samples of recording
                    if len(data) > self._samples:
                        data = data[:self._samples]

                    # Normalise and flatten the data samples then0 prefix the label
                    normalised = DataProcessors.normalise(data, limits=self._limits)
                    all_data.append(np.concatenate([[labels[i]], normalised]))

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

    def train(self, save=False, shuffle=True, plot=True):
        """Trains the model currently held in the model instance attribute"""

        print('Training net\n')
        self._history = None
        val_given = len(self._val_data) != 0  # Check if validation data has been specified

        # Early stopping criteria to stop overfitting
        callback_list = []
        #callback_list.append(callbacks.EarlyStopping(monitor='val_accuracy', patience=15, mode='auto'))
        callback_list.append(callbacks.EarlyStopping(monitor='loss', patience=5, mode='auto'))

        # Separate labels and train data, shuffling if necessary since they are initially read-in in time order
        train_data, train_targets = DataProcessors.parse_train_data(self._train_data, self._outputs, shuffle)

        # Fit model, validating either using given validation data or by splitting the training data
        if val_given:
            val_data, val_targets = DataProcessors.parse_train_data(self._val_data, self._outputs, shuffle)
            self._history = self._model.fit(train_data, train_targets, validation_data=(val_data, val_targets),
                                           epochs=self._epochs, batch_size=self._batch_size,
                                           verbose=2, callbacks=callback_list)
        else:
            self._history = self._model.fit(train_data, train_targets, epochs=self._epochs, batch_size=self._batch_size,
                                           validation_split=0.15, verbose=2, callbacks=callback_list)

        if save:
            self.save_model()

        if plot:
            self.plot()

        return self._history is not None

    def save_model(self):
        """Saves the model held in the _model instance attribute as HDF5 file"""
        # TODO: Better to use checkpoints during training, save only best (lowest)

        filename = '%f - %d inputs.h5' % ((self._history.history['loss'][-1]), self._inputs)  # Add loss to filename
        filename = 'Saved Models\\Loss - ' + filename
        try:
            self._model.save(filename, overwrite=True)
            return filename
        except Exception as e:
            print('Failed to save ' + filename)
            print(e)
            return False

    def save_train_data(self, filename):
        """ UNUSED: Saves the labelled training data held in the _train_data instance attribute as a .csv file"""

        if len(self._train_data) != 0:
            full_filename = '{0}_{1}.csv'.format(filename, len(self._train_data))
            print('Saving training data in: ' + filename)
            np.save(full_filename, self._train_data, delimiter=',')

    def plot(self):
        """Creates subplots of per-epoch train/validation loss/accuracy history"""

        if self._history is None:
            return False
        else:
            fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
            fig.tight_layout(pad=3.0)

            # Loss plot
            ax1.plot(self._history.history['loss'], label='Training')
            ax1.plot(self._history.history['val_loss'], label='Validation')
            ax1.legend()
            ax1.set_title('Loss')
            ax1.set_xlabel('Epoch')
            ax1.set_ylabel('Loss')

            # Accuracy plot
            ax2.plot(self._history.history['accuracy'], label='Training')
            ax2.plot(self._history.history['val_accuracy'], label='Validation')
            ax2.legend()
            ax2.set_title('Accuracy')
            ax2.set_ylabel('Accuracy')

            plt.show()
            return True

    def predict_directory(self, root, shuffle=True):
        """Gets all files in the given test directory and predicts the class of data in each line"""

        test_data = self.load_data([root])
        score = 0.0
        size = len(test_data)

        if size != 0:
            data = np.zeros((size, len(test_data[0]) - 1), dtype=np.float32)
            labels = np.zeros(size)

            if shuffle:
                print('Shuffling test data\n')
                np.random.shuffle(test_data)

            for i, sample in enumerate(test_data):
                data[i] = sample[1:]  # Remove label from data
                labels[i] = sample[0]

            print('Predicting...\n')
            predictions = self._model.predict(data)

            for i, sample in enumerate(predictions):
                print(predictions[i])

                guess = np.argmax(predictions[i])  # Best guess is highest probability* score in prediction
                if labels[i] == guess:
                    score += 1

            score = (score / size) * 100.0
            print('Net performance: %.2f\n' % score)
            return score
        else:
            return -1


class Tests:
    def __init__(self):
        None

    @staticmethod
    def train_net(net, shuffle=True, plot=True, save=False, predict=True, test_save=False):
        baseline = -1

        loaded = net.load_data(roots=[params['train_root'], params['val_root']])
        if loaded:
            assert net.train(shuffle=shuffle, save=save, plot=plot)

        if predict:
            baseline = net.predict_directory(root=params['test_root'])
            assert baseline != -1

        if predict and test_save and not save:
            saved_filename = net.save_model()
            assert saved_filename is not False

            score = Tests.save_model(net, filename=saved_filename)
            min_score = 0.8 * baseline
            assert min_score <= score

    @staticmethod
    def save_model(net, filename):
        net.model = None
        full_path = os.path.join(os.getcwd(), filename)
        model = NeuralNet.load_model(full_path)
        assert model is not None

        net.model = model
        score = net.predict_directory(root=params['test_root'])

        return score


if __name__ == '__main__':
    params = {
        'mag': False,
        'cutoff': 0.5,
        'max samples': 480,
        'hiddens': 480,
        'outputs': 3,
        'activation': 'relu',
        'learning rate': 0.3,
        'epochs': 50,
        'batch size': 32,
        'train_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data',
        'val_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Validation Data',
        'test_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Test Data'

    }

    nn = NeuralNet(mag=params['mag'], cutoff=params['cutoff'], max_samples=params['max samples'],
                   hiddens=params['hiddens'], outputs=params['outputs'],activation=params['activation'],
                   epochs=params['epochs'], batch_size=params['batch size'], lr=params['learning rate'])

    Tests.train_net(nn, save=True, test_save=False)
    #score = nn.predict(params['test_root'], shuffle=False)
