from NeuralNetwork import NeuralNetwork

if __name__ == '__main__':
    n = NeuralNetwork(2, 2, 1, 0.2)
    test = [0, 1]
    print('Input: {}\nOutput: {}'.format(test, n.query(test)))
