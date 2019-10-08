from Perceptron import Perceptron
import matplotlib.pyplot as plt
import numpy as np
# Our main code starts here


def test0():
    print('Test 0:\n')

    inputs = [1.0, 0.0]
    weights = [1.0, 1.0]
    bias = -1

    perceptron = Perceptron(inputs, weights, bias)
    perceptron.compute()

    print('Inputs: ', inputs)
    print('Weights: ', weights)
    print('Bias: ', bias)
    perceptron.print_results()


def test1():
    print('Test 1 (NAND):\n')

    weights = [-1.0, -1.0]
    bias = 2

    perceptron = Perceptron([0, 0], weights, bias)
    for x1 in range(2):
        for x2 in range(2):
            perceptron.inputs = [x1, x2]
            perceptron.compute()

    perceptron.print_results()


def test2(name):
    print('Test 2:\n')
    GATES = {
        'AND': {'weights': [1, 1], 'bias': -1},
        'OR': {'weights': [1, 1], 'bias': 0},
        'NAND': {'weights': [-1, -1], 'bias': 2},
        'NOR': {'weights': [-1, -1], 'bias': 1},
    }

    perceptron = Perceptron([0, 0], GATES[name]['weights'], GATES[name]['bias'])

    inputs = []
    for x1 in range(2):
        for x2 in range(2):
            inputs.append([x1, x2])
            perceptron.inputs = inputs[-1]
            perceptron.compute()

    plot(inputs, GATES[name]['weights'], GATES[name]['bias'], perceptron.results, name)


def plot(inputs, weights, bias, outputs, title):
    fig = plt.xkcd()
    colors = ['red', 'green']

    index = 0
    for input in inputs:
        plt.scatter(input[0], input[1], s=50, color=colors[outputs[index]])
       
        index += 1

    x = np.linspace(-0.5, 1.5)
    y = -((x * weights[0]) + bias)/weights[1]
    plt.plot(x, y)

    plt.xlim(-0.5, 1.5)
    plt.ylim(-0.5, 1.5)
    plt.ylabel('Input 2')
    plt.title('State Space of Input Vector - {} Gate'.format(title))
    plt.grid(True, linewidth=1, linestyle=':')
    plt.tight_layout()
    
    plt.show()


if __name__ == '__main__':
    #test0()
    #test1()
    test2('NAND')
