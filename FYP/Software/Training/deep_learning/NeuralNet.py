from __future__ import print_function
import numpy as np
import tensorflow as tf
#from tensorflow import keras
from tensorflow.keras import optimizers, losses
from tensorflow.keras import layers
from processing.CSVConverters import CSVConverters
from os import path, listdir
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from datetime import datetime


class NeuralNet:
    def __init__(self, inputs=238, hiddens=500,  outputs=2, activation='relu', epochs=10, lr=0.3, mag=False):
        self._inputs = (inputs * 9) if mag else (inputs * 6)
        self._hiddens = hiddens
        self._outputs = outputs
        self._activation = activation
        self._epochs = epochs
        self._lr = lr
        self._mag = mag

        self._data = []
        self._limits = np.array([4, 4, 4, 2000, 2000, 2000, 400, 400, 400])

        input_layer = tf.keras.Input(shape=(self._inputs,))
        x = layers.Dense(self._hiddens)(input_layer)
        x = layers.Dense(self._hiddens)(x)
        output_layer = layers.Dense(self._outputs)(x)
        self.model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
        # self.model = tf.keras.Sequential()
        # self.model.add(layers.Dense(self._hiddens, input_shape=(self._inputs,)))
        # self.model.add(layers.Dense(self._hiddens, activation=self._activation))
        # self.model.add(layers.Dense(self._outputs))

    # @property
    # def losses
    def load_data(self, root, save=True):
        print('Parsing data in root directory \'%s\'\n' % root[root.rfind('\\')+1:])
        root = path.normpath(root)
        dirs = [path.join(root, d) for d in listdir(root) if path.isdir(path.join(root, d))]
        data = []

        if dirs != 0:
            for directory in dirs:
                label = int(directory[directory.rfind('_')+1:]) # TODO: Regex practice!
                files = [path.join(directory, f) for f in listdir(directory) if (path.isfile(path.join(directory, f)) and ('.csv' in f))]

                if files != 0:
                    for file in files:
                        all_data = np.array(CSVConverters.csv_to_list(file), dtype=np.float64)
                        normalised = all_data / self._limits[:, ]
                        if not self._mag:
                            all_data = np.array([x[:-3] for x in all_data], dtype=np.float64)
                            normalised = all_data / ((self._limits[:-3])[:, ])

                        flattened = np.concatenate([[label], normalised.flatten()])
                        data.append(flattened)

        if data != 0:
            if save:
                self._data = np.copy(data)
            return np.copy(data)
        else:
            return -1

    def train(self, save=False):
        print('Training net\n')
        model_loss = losses.mean_squared_error
        model_optimiser = optimizers.Adam()
        self.model.compile(loss=model_loss, optimizer=model_optimiser)

        size = len(self._data)
        if size != 0:
            data = np.zeros((size, len(self._data[0]) - 1), dtype=np.float64)
            labels = np.zeros(size)
            targets = np.zeros((size, self._outputs)) + 0.01
            for i, sample in enumerate(self._data):
                data[i] = sample[1:]
                labels[i] = sample[0]
                targets[i][int(labels[i])] = 0.99

            self.model.fit(data, targets, epochs=self._epochs, batch_size=1) # TODO: generate
            #if save(self.model.save('Save - {0}'))

    def predict(self, root='', shuffle=True):
        test_data = self.load_data(root, save=False)
        score = 0.0
        size = len(test_data)

        if size != 0:
            data = np.zeros((size, len(test_data[0]) - 1), dtype=np.float64)
            labels = np.zeros(size)
            if shuffle:
                print('Shuffling test data\n')
                np.random.shuffle(test_data)

            for i, sample in enumerate(test_data):
                data[i] = sample[1:]
                labels[i] = sample[0]

            print('Predicting...\n')
            predictions = self.model.predict(data, batch_size=1)

            for i, sample in enumerate(predictions):
                guess = np.argmax(predictions[i])
                if labels[i] == guess:
                    score += 1
            score = (score / size) * 100.0
            print('Net performance: %.2f\n' % score)
            return score


class Tests:
    def __init__(self):
        None


if __name__ == '__main__':
    params = {
        'samples': 238,
        'hiddens': 500,
        'outputs': 10,
        'lr': 0.3,
        'epochs': 10,
        'train_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data',
        'test_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Test Data'
    }
    test = r'C:\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data\Test_2'
    nn = NeuralNet()
    training_data = nn.load_data(params['train_root'], save=True)
    nn.train()
    score = nn.predict(params['test_root'], shuffle=False)
