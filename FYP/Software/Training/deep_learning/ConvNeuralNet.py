from __future__ import print_function
import tensorflow as tf
from numpy import expand_dims as expand
from deep_learning.NeuralNet import NeuralNet, Tests
from tensorflow.keras import optimizers, losses, layers, callbacks
from processing.DataProcessors import DataProcessors


class ConvNeuralNet(NeuralNet, Tests):
    def __init__(self, mag=False, cutoff=0.25, max_samples=480, hiddens=240,  outputs=8, activation='tanh',
                 loss=losses.categorical_crossentropy, epochs=25, batch_size=64, lr=0.00045):
        super().__init__()
        self.name = self.__class__.__name__
        self._mag = mag
        self._total_samples = max_samples
        self._samples = int(self._total_samples * cutoff)
        self._inputs = (self._samples * 9) if self._mag else (self._samples * 6)
        self._hiddens = hiddens
        self._outputs = outputs
        self._activation = activation
        self._loss = loss
        self._epochs = epochs
        self._batch_size = batch_size
        self._lr = lr

        self.create_model()
    # ------------------------------------------------- Properties -----------------------------------------------------

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    # --------------------------------------------------- Overrides ----------------------------------------------------

    def create_model(self):
        """Creates a keras model based on the Functional API"""

        # Instantiate layers
        input_layer = tf.keras.Input(shape=(self._inputs, 1))

        x = layers.Conv1D(32, kernel_size=3, activation=self._activation, padding='same', data_format='channels_last')(input_layer)
        x = layers.MaxPool1D()(x)
        x = layers.Conv1D(64, kernel_size=9, activation=self._activation, padding='valid', data_format='channels_last')(x)
        x = layers.MaxPool1D()(x)
        x = layers.Dropout(0.4)(x)

        x = layers.Flatten()(x)
        x = layers.Dense(self._hiddens, activation='relu')(x)
        output_layer = layers.Dense(self._outputs, activation='softmax')(x)

        # Choose loss and optimisation functions/algorithms
        model_loss = self._loss
        model_optimiser = optimizers.Adam(learning_rate=self._lr)  # optimizers.RMSprop(learning_rate=self._lr)   #  optimizers.SGD(learning_rate=self._lr)

        # Instantiate and compile model
        self._model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
        self._model.compile(loss=model_loss, optimizer=model_optimiser, metrics=['accuracy'])

    @staticmethod
    def pre_process(raw_data, single=False):
        """Simply flattens and normalises raw data as per sensor max/mins"""
        normalised = DataProcessors.raw_normalise(raw_data)

        if single:
            normalised = expand(normalised, axis=1)
            normalised = expand(normalised, axis=0)

        return normalised

    @staticmethod
    def get_stop_conditions():
        callback_list = []
        #callback_list.append(callbacks.EarlyStopping(monitor='val_accuracy', patience=15, mode='auto'))
        callback_list.append(callbacks.EarlyStopping(monitor='loss', patience=4, mode='auto'))
        return callback_list


if __name__ == '__main__':
    params = {
        'mag': False,
        'cutoff': 0.25,
        'max samples': 480,
        'hiddens': 240,
        'outputs': 8,
        'activation': 'tanh',
        'loss':  losses.categorical_crossentropy,  # losses.mean_squared_error,
        'learning rate': 0.00042,
        'epochs': 30,
        'batch size': 60,
        'train_root': r'..\Training Data',
        'val_root': r'..\Validation Data',
        'test_root': r'..\Test Data'

    }

    nn = ConvNeuralNet(mag=params['mag'], cutoff=params['cutoff'], max_samples=params['max samples'],
                       hiddens=params['hiddens'], outputs=params['outputs'], activation=params['activation'],
                       loss=params['loss'], epochs=params['epochs'], batch_size=params['batch size'],
                       lr=params['learning rate'])

    tests = Tests(params=params)
    tests.train_net(nn, shuffle=True, save_model=True, save_data=False, test_save=False)
