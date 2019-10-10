from NeuralNetwork import NeuralNetwork

if __name__ == '__main__':
    n = NeuralNetwork(2, 2, 1, 0.6)
    tests = [[0, 0], [0, 1], [1, 0], [1, 1]]
    targets = [0, 0, 0, 1]
    outputs = []

    reps = 10000
    while reps != 0:
        for i in range(len(tests)):
            n.train(tests[i], targets[i])
        reps -= 1

    for test in tests:
        print('Input: {}\nOutput: {}\n'.format(test, n.query(test)))
