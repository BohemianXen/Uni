from __future__ import print_function
import numpy as np
import tensorflow as tf
#from tensorflow import keras
from tensorflow.keras import optimizers, losses, layers, callbacks, models
from processing.CSVConverters import CSVConverters
from os import path, listdir
import matplotlib.pyplot as plt
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from datetime import datetime


class NeuralNet:
    def __init__(self, mag=False, samples=480, hiddens=960,  outputs=2, activation='relu', epochs=10, batch_size=32, lr=0.3):
        self._mag = mag
        self._inputs = (samples * 9) if self._mag else (samples * 6)

        self._hiddens = hiddens
        self._outputs = outputs
        self._activation = activation
        self._epochs = epochs
        self._batch_size = batch_size
        self._lr = lr
        self._data = []
        self._history = None

        if self._mag:
            self._limits = np.array([4, 4, 4, 2000, 2000, 2000, 400, 400, 400])
        else:
            self._limits = np.array([4, 4, 4, 2000, 2000, 2000])

        input_layer = tf.keras.Input(shape=(self._inputs,))
        x = layers.Dense(self._hiddens, activation='relu')(input_layer)
        x = layers.Dense(self._hiddens, activation='relu')(x)
        output_layer = layers.Dense(self._outputs, activation='softmax')(x)
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
        dirs = [path.join(root, d) for d in listdir(root) if path.isdir(path.join(root, d)) and 'General' not in d]
        data = []

        if dirs != 0:
            for directory in dirs:
                label = int(directory[directory.rfind('_')+1:]) # TODO: Regex practice!
                files = [path.join(directory, f) for f in listdir(directory) if (path.isfile(path.join(directory, f)) and ('.csv' in f))]

                if files != 0:
                    for file in files:
                        all_data = np.array(CSVConverters.csv_to_list(file, remove_mag=(not self._mag)), dtype=np.float32)
                        normalised = all_data / self._limits[:, ]  # TODO: MinMaxScaler but only after splitting data!
                        flattened =  all_data if len(all_data) == 1 else np.concatenate([[label], normalised.flatten()])
                        data.append(flattened)

        if data != 0:
            if save:
                self._data = np.copy(data)
            return np.copy(data)
        else:
            return -1

    def train(self, save=False, shuffle=True, validation_data=None, plot=True):
        print('Training net\n')
        model_loss = losses.mean_squared_error  # losses.categorical_crossentropy
        model_optimiser = optimizers.Adam()
        self.model.compile(loss=model_loss, optimizer=model_optimiser, metrics=['accuracy'])


        size = len(self._data)
        if size != 0:
            if shuffle:
                np.random.shuffle(self._data)
            data = np.zeros((size, len(self._data[0]) - 1), dtype=np.float32)
            labels = np.zeros(size)
            targets = np.zeros((size, self._outputs)) + 0.01
            for i, sample in enumerate(self._data):
                data[i] = sample[1:]
                labels[i] = sample[0]
                targets[i][int(labels[i])] = 0.99

            #callback = callbacks.EarlyStopping(monitor='accuracy', min_delta=0.005, patience=10, mode='auto')
            callback = callbacks.EarlyStopping(monitor='loss', patience=4, mode='auto')

            self._history = self.model.fit(data, targets, epochs=self._epochs, batch_size=self._batch_size, validation_split=0.15, verbose=2, callbacks=[callback]) # TODO: generate
            #self.model.evaluate()
            if save:
                self.save_model()
            if plot:
                self.plot()

    def predict(self, root='', shuffle=True):
        test_data = self.load_data(root, save=False)
        score = 0.0
        size = len(test_data)

        if size != 0:
            data = np.zeros((size, len(test_data[0]) - 1), dtype=np.float32)
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
                print(predictions[i])
                guess = np.argmax(predictions[i])
                if labels[i] == guess:  # guess == np.random.choice([0, 1, labels[i]]):
                    score += 1
            score = (score / size) * 100.0
            print('Net performance: %.2f\n' % score)
            return score

    def save_model(self):
        # TODO: Better to use checkpoints during training, save only best (lowest) loss
        filename = '%.2f_.h5'%((self._history.history['val_accuracy'][-1])*100)
        self.model.save('Saved Models\\Val Accuracy - ' + filename, overwrite=False) # TODO: try/catch

    @staticmethod
    def load_model(filename):
       return models.load_model(filename) # TODO: try/catch

    def save_data(self, filename):
        if len(self._data) != 0:
            full_filename = '{0}_{1}.csv'.format(filename, len(self._data))
            np.save(full_filename, self._data, delimiter=',')
            print('Saving training data in: ' + filename)

    def plot(self):
        if self._history is None:
            return -1
        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
        fig.tight_layout(pad=3.0)

        ax1.plot(self._history.history['loss'], label='Training')
        ax1.plot(self._history.history['val_loss'], label='Validation')
        ax1.legend()
        ax1.set_title('Loss')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Loss')

        #plt.subplot(2, 1, 2)
        #x = np.arange(0, self._epochs)
        ax2.plot(self._history.history['accuracy'], label='Training')
        ax2.plot(self._history.history['val_accuracy'], label='Validation')
        ax2.legend()
        ax2.set_title('Accuracy')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy')

        plt.show()


class Tests:
    def __init__(self):
        None


if __name__ == '__main__':
    params = {
        'samples': 480,
        'hiddens': 480,
        'outputs': 2,
        'activation': 'relu',
        'lr': 0.3,
        'epochs': 80,
        'batch size': 32,
        'train_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data',
        'test_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Test Data',
        'mag': False
    }
    test = r'C:\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data\Test_2'
    nn = NeuralNet(samples=params['samples'], hiddens=params['hiddens'], outputs=params['outputs'],
                   activation=params['activation'], epochs=params['epochs'], batch_size=params['batch size'],
                   mag=params['mag'])
    training_data = nn.load_data(params['train_root'], save=True)
    nn.train(shuffle=True, save=False, plot=True)
    #nn.predict(root=params['test_root'])

    model = NeuralNet.load_model(r'C:\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\deep_learning\Saved Models\Val Accuracy - 95.83_.h5')
    print('Done')
    #score = nn.predict(params['test_root'], shuffle=False)
