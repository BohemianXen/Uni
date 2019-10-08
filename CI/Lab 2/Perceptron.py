import numpy as np


class Perceptron:
    def __init__(self, inputs, weights, bias):
        self._inputs = inputs
        self._weights = weights
        self._bias = bias
        self._results = []

    def compute(self):
        summed = np.dot(self.inputs, self.weights)
        summed += self.bias

        # Calculate output
        # N.B this is a ternary operator, neat huh?
        output = 1 if summed > 0 else 0
        self.results.append(output)

    def print_results(self):
        print('Results: ', self.results)

    @property
    def results(self):
        return self._results

    def reset_results(self):
        self.results = []

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        self._inputs = inputs

    @property
    def weights(self):
        return self._weights

    @weights.setter
    def weights(self, weights):
        self._weights = weights

    @property
    def bias(self):
        return self._bias

    @bias.setter
    def bias(self, bias):
        self._bias = bias
