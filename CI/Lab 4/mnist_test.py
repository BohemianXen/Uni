# Import numpy for arrays and matplotlib for drawing the numbers
import numpy
import matplotlib.pyplot as plt
from neural_network import NeuralNetwork as nn


def mnist_train(training_data, n, reps):
    # train the neural network on each training sample

    while reps > 0:
        for record in training_data:
            all_values = record.split(',')

            # scale and shift the inputs from 0..255 to 0.01..1
            inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            # create the target output values (all 0.01, except the desired label which is 0.99)
            targets = numpy.zeros(n.o_nodes) + 0.01
            targets[int(all_values[0])] = 0.99

            n.train(inputs, targets)
            reps -= 1


def mnist_test(test_data, n):
    scorecard = []

    for record in test_data:
        all_values = record.split(',')
        correct_label = int(all_values[0])
        inputs = (numpy.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
        outputs = n.query(inputs)
        label = numpy.argmax(outputs)
        print('Target: {}\tNetwork: {}'.format(correct_label, label))

        if label == correct_label:
            scorecard.append(1)
        else:
            scorecard.append(0)

        scorecard_array = numpy.asarray(scorecard)
        print('Performance = {}%\n'.format((scorecard_array.sum() / scorecard_array.size) * 100))

    return scorecard


def plot(test_data, results):
    for i in range(len(results)):
        if results[i] == 0:
            all_values = test_data[i].split(',')
            image_array = numpy.asfarray(all_values[1:]).reshape((28, 28))
            plt.imshow(image_array, cmap='Greys', interpolation='None')
            plt.show()  # TODO: subplot


if __name__ == '__main__':

    params = {
        'inputs': 784,
        'hiddens': 100,
        'outputs': 10,
        'lr': 0.3,
        'reps': 100,
        'training file': 'MNIST\mnist_train_100.csv',
        'test file': 'MNIST\mnist_test.csv'
    }

    net = nn(params['inputs'], params['hiddens'], params['outputs'], params['lr'])

    # open, parse, then close the test and training files
    training_file = open(params['training file'], 'r')
    test_file = open(params['test file'], 'r')
    training_list = training_file.readlines()
    test_list = test_file.readlines()
    training_file.close()
    test_file.close()

    # train then test the neural net and plot any incorrect guesses
    mnist_train(training_list, net,  params['reps'])
    results = mnist_test(test_list, net)
    print('Overall performance: {}'.format(results.count(1)/len(results) * 100.0))
    #plot(test_list, results)
