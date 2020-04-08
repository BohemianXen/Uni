from __future__ import print_function
import tensorflow as tf
from deep_learning.NeuralNet import NeuralNet, Tests
from tensorflow.keras import optimizers, losses, layers, callbacks
from processing.DataProcessors import DataProcessors
from numpy import expand_dims as expand


class RawNeuralNet(NeuralNet, Tests):
    def __init__(self, mag=False, cutoff=0.25, max_samples=480, hiddens=240,  outputs=8, activation='relu', loss=losses.mean_squared_error, epochs=80, batch_size=64, lr=0.0004):
        super().__init__()
        self.name = self.__class__.__name__
        self._mag = mag
        self._total_samples = max_samples
        self._hiddens = hiddens
        self._outputs = outputs
        self._activation = activation
        self._loss = loss
        self._epochs = epochs
        self._batch_size = batch_size
        self._lr = lr

        self._samples = int(self._total_samples * cutoff)
        self._inputs = (self._samples * 9) if self._mag else (self._samples * 6)

        # self._train_data = []
        # self._val_data = []
        # self._history = None
        #
        # if self._mag:
        #     self._limits = np.array([4, 4, 4, 2000, 2000, 2000, 400, 400, 400])
        # else:
        #     self._limits = np.array([4, 4, 4, 2000, 2000, 2000])

        self.create_model()

    # --------------------------------------------------- Overrides ----------------------------------------------------

    def create_model(self):
        """Creates a keras model based on the Functional API"""

        # Instantiate layers
        input_layer = tf.keras.Input(shape=(self._inputs,))  # , batch_input_shape=(batch_size, inputs))
        x = layers.Dense(self._hiddens, activation=self._activation)(input_layer)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(self._hiddens, activation=self._activation)(x)
        output_layer = layers.Dense(self._outputs, activation='softmax')(x)

        # Choose loss and optimisation functions/algorithms
        model_loss = self._loss
        model_optimiser = optimizers.Adam(learning_rate=self._lr)  # optimizers.SGD(learning_rate=lr)

        # Instantiate and compile model
        self._model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
        self._model.compile(loss=model_loss, optimizer=model_optimiser, metrics=['accuracy'])

    @staticmethod
    def pre_process(raw_data, single=False):
        """Simply flattens and normalises raw data as per sensor max/mins"""
        normalised = DataProcessors.raw_normalise(raw_data)

        if single:
            normalised = expand(normalised, axis=0)

        return normalised

    @staticmethod
    def get_stop_conditions():
        callback_list = []
        # callback_list.append(callbacks.EarlyStopping(monitor='val_accuracy', patience=20, mode='auto'))
        callback_list.append(callbacks.EarlyStopping(monitor='loss', patience=10, mode='auto'))
        return callback_list


if __name__ == '__main__':
    params = {
        'mag': False,
        'cutoff': 0.25,
        'max samples': 480,
        'hiddens': 240,
        'outputs': 8,
        'activation': 'relu',
        'loss': losses.categorical_crossentropy,
        'learning rate': 0.0007,  # 0.0007
        'epochs': 200,
        'batch size': 70,
        'train_root': r'..\Training Data',
        'val_root': r'..\Validation Data',
        'test_root': r'..\Test Data'

    }

    nn = RawNeuralNet(mag=params['mag'], cutoff=params['cutoff'], max_samples=params['max samples'],
                      hiddens=params['hiddens'], outputs=params['outputs'], activation=params['activation'],
                      loss=params['loss'], epochs=params['epochs'], batch_size=params['batch size'],
                      lr=params['learning rate'])

    tests = Tests(params=params)
    tests.train_net(nn, shuffle=True, save_model=False, save_data=False, test_save=False)

