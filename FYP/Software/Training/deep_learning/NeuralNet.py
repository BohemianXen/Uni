from __future__ import print_function
import numpy as np
import tensorflow as tf
from tensorflow.keras import optimizers, losses, layers, callbacks, models
from processing.DataProcessors import DataProcessors
from processing.CSVConverters import CSVConverters
import matplotlib.pyplot as plt
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from datetime import datetime


class NeuralNet:
    def __init__(self, mag=False, cutoff=1, samples=480, hiddens=480,  outputs=3, activation='relu', epochs=10, batch_size=32, lr=0.3):
        self._mag = mag
        self._total_samples = samples
        self._samples = int(self._total_samples * cutoff)
        self._inputs = (self._samples * 9) if self._mag else (self._samples * 6)


        self._hiddens = hiddens
        self._outputs = outputs
        self._activation = activation
        self._epochs = epochs
        self._batch_size = batch_size
        self._lr = lr
        self._train_data = []
        self._val_data = []
        self._history = None

        if self._mag:
            self._limits = np.array([4, 4, 4, 2000, 2000, 2000, 400, 400, 400])
        else:
            self._limits = np.array([4, 4, 4, 2000, 2000, 2000])

        self.model = self.create_model(self._inputs, self._hiddens, self._outputs, self._batch_size)

    @staticmethod
    def create_model(inputs, hiddens, outputs, batch_size):
        input_layer = tf.keras.Input(shape=(inputs,))  # , batch_input_shape=(batch_size, inputs))
        x = layers.Dense(hiddens, activation='relu')(input_layer)
        x = layers.Dense(hiddens, activation='relu')(x)
        output_layer = layers.Dense(outputs, activation='softmax')(x)

        model_loss = losses.mean_squared_error  # losses.categorical_crossentropy
        model_optimiser = optimizers.Adam()

        model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
        model.compile(loss=model_loss, optimizer=model_optimiser, metrics=['accuracy'])
        return model

    # @property
    # def losses
    def load_data(self, roots, save=True):
        for root in roots:
            train = True if 'Training Data' in root else False
            test = True if 'Test Data' in root else False

            all_data = []
            files, labels = CSVConverters.get_data_files(root)

            if len(files) == 0:
                return -1
            else:
                for i, file in enumerate(files):
                    data = CSVConverters.csv_to_list(file, remove_mag=(not self._mag))


                    # If simulating short capture, skip last few samples of recording
                    if len(data) > self._samples:
                        data = data[:self._samples]

                    normalised = DataProcessors.normalise(data, limits=self._limits)
                    all_data.append(np.concatenate([[labels[i]], normalised]))

            if len(all_data) == 0:
                return -1
            else:
                if test:
                    return np.copy(all_data)
                if train:
                    self._train_data = np.copy(all_data)
                else:
                    self._val_data = np.copy(all_data)


    def train(self, save=False, shuffle=True, plot=True):
        print('Training net\n')
        val_given = len(self._val_data) != 0

        # callback = callbacks.EarlyStopping(monitor='accuracy', min_delta=0.005, patience=10, mode='auto')
        callback = callbacks.EarlyStopping(monitor='loss', patience=8, mode='auto')

        train_data, train_targets = DataProcessors.parse_train_data(self._train_data, self._outputs, shuffle)

        if val_given:
            val_data, val_targets = DataProcessors.parse_train_data(self._val_data, self._outputs, shuffle)
            self._history = self.model.fit(train_data, train_targets, validation_data=(val_data, val_targets),
                                           epochs=self._epochs, batch_size=self._batch_size,
                                           verbose=2, callbacks=[callback])
        else:
            self._history = self.model.fit(train_data, train_targets, epochs=self._epochs, batch_size=self._batch_size,
                                           validation_split=0.15, verbose=2, callbacks=[callback])




        #self.model.evaluate()
        if save:
            self.save_model()
        if plot:
            self.plot()

    def predict_directory(self, root, shuffle=True):
        test_data = self.load_data([root], save=False)
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
            predictions = self.model.predict(data)

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
        filename = '%f - %d inputs.h5' % ((self._history.history['loss'][-1]), self._inputs)
        self.model.save('Saved Models\\Loss - ' + filename, overwrite=False)  # TODO: try/catch

    def save_train_data(self, filename):
        if len(self._train_data) != 0:
            full_filename = '{0}_{1}.csv'.format(filename, len(self._train_data))
            np.save(full_filename, self._train_data, delimiter=',')
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
        #ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Accuracy')

        plt.show()

    # -------------------------------------------------- Static Methods ------------------------------------------------

    @staticmethod
    def load_model(filename, single=False):
        model = models.load_model(filename) # TODO: try/catch

        if single: # fROM https://datascience.stackexchange.com/questions/13461/how-can-i-get-prediction-for-only-one-instance-in-keras
            weights = model.get_weights()
            single_item_model = NeuralNet.create_model()
            single_item_model.set_weights(weights)
            return single_item_model
        else:
            return model



class Tests:
    def __init__(self):
        None


if __name__ == '__main__':
    params = {
        'mag': False,
        'cutoff': 0.5,
        'samples': 480,
        'hiddens': 480,
        'outputs': 3,
        'activation': 'relu',
        'lr': 0.3,
        'epochs': 60,
        'batch size': 32,
        'train_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data',
        'val_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Validation Data',
        'test_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Test Data'

    }

    nn = NeuralNet(mag=params['mag'], cutoff=params['cutoff'], samples=params['samples'], hiddens=params['hiddens'], outputs=params['outputs'],
                   activation=params['activation'], epochs=params['epochs'], batch_size=params['batch size'],
                   )
    training_data = nn.load_data(roots=[params['train_root'], params['val_root']], save=True)
    nn.train(shuffle=True, save=False, plot=True)
    nn.predict_directory(root=params['test_root'])
    nn.save_model()
    model = NeuralNet.load_model(r"C:\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\deep_learning\Saved Models\Loss - 0.002302 - 1440 inputs.h5")
    nn.model = model
    nn.predict_directory(root=params['test_root'])
    print('Done')
    #score = nn.predict(params['test_root'], shuffle=False)
