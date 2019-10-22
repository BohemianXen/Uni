from NeuralNetwork import NeuralNetwork

GATES = {
    'and': [0, 0, 0, 1],
    'nand': [1, 1, 1, 0],
    'or': [0, 1, 1, 1],
    'nor': [1, 0, 0, 0],
    'xor': [0, 1, 1, 0],
}

if __name__ == '__main__':
    n = NeuralNetwork(2, 4, 1, 0.6)
    tests = [[0, 0], [0, 1], [1, 0], [1, 1]]
    targets = GATES['xor']
    outputs = []

    reps = 10000
    while reps != 0:
        for i in range(len(tests)):
            n.train(tests[i], targets[i])
        reps -= 1

    for test in tests:
        print('Input: {}\nOutput: {}\n'.format(test, n.query(test)))
