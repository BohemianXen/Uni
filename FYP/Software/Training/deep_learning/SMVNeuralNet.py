from __future__ import print_function
import tensorflow as tf
from deep_learning.NeuralNet import NeuralNet, Tests
from tensorflow.keras import optimizers, losses, layers, callbacks
from processing.DataProcessors import DataProcessors


class SMVNeuralNet(NeuralNet, Tests):
    def __init__(self, mag=False, cutoff=0.25, max_samples=480, hiddens=9,  outputs=8, activation='relu', epochs=100, batch_size=18, lr=0.01):
        super().__init__()
        self._mag = mag
        self._total_samples = max_samples
        self._hiddens = hiddens
        self._outputs = outputs
        self._activation = activation
        self._epochs = epochs
        self._batch_size = batch_size
        self._lr = lr

        self._samples = int(self._total_samples * cutoff)
        #self._inputs = (self._samples * 3) if self._mag else (self._samples * 2)
        self._inputs = 15  # += 6

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
        input_layer = tf.keras.Input(shape=(self._inputs,))  # , batch_input_shape=(batch_size, inputs))
        x = layers.Dense(self._hiddens, activation=self._activation)(input_layer)
        x = layers.Dense(self._hiddens, activation=self._activation)(x)
        output_layer = layers.Dense(self._outputs, activation='softmax')(x)

        # Choose loss and optimisation functions/algorithms
        model_loss = losses.mean_squared_error  # losses.categorical_crossentropy
        model_optimiser = optimizers.Adam(learning_rate=self._lr)  # optimizers.RMSprop(learning_rate=self._lr)   #  optimizers.SGD(learning_rate=self._lr)

        # Instantiate and compile model
        self._model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
        self._model.compile(loss=model_loss, optimizer=model_optimiser, metrics=['accuracy'])

    @staticmethod
    def pre_process(raw_data, single=False):
        """Simply flattens and normalises raw data as per sensor max/mins"""
        return DataProcessors.smv(raw_data, single=single)

    @staticmethod
    def get_stop_conditions():
        callback_list = []
        #callback_list.append(callbacks.EarlyStopping(monitor='val_accuracy', patience=15, mode='auto'))
        callback_list.append(callbacks.EarlyStopping(monitor='loss', patience=12, mode='auto'))
        return callback_list


if __name__ == '__main__':
    params = {
        'mag': False,
        'cutoff': 0.25,
        'max samples': 480,
        'hiddens': 9,
        'outputs': 8,
        'activation': 'tanh',
        'learning rate': 0.004,
        'epochs': 100,
        'batch size': 64,
        'train_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data',
        'val_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Validation Data',
        'test_root': r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Test Data'

    }

    nn = SMVNeuralNet(mag=params['mag'], cutoff=params['cutoff'], max_samples=params['max samples'],
                   hiddens=params['hiddens'], outputs=params['outputs'],activation=params['activation'],
                   epochs=params['epochs'], batch_size=params['batch size'], lr=params['learning rate'])

    tests = Tests(params=params)
    tests.train_net(nn, save=True, test_save=False)
    #score = nn.predict(params['test_root'], shuffle=False)
