# Import numpy for arrays and matplotlib for drawing the numbers
import numpy
from pca import PCA
from sklearn.preprocessing import MinMaxScaler
# k Nearest Neighbour
from sklearn.neighbors import KNeighborsClassifier
from neural_network import NeuralNetwork as nn


def knn():

    pca = PCA(params['test file'], params['training file'], params['components'])
    pca.plot()

    # Extract the principle components from the training data
    train_ext = pca._pca.fit_transform(pca.train_data)
    # Transform the test data using the same components
    test_ext = pca._pca.transform(pca.test_data)

    # Normalise the data sets
    min_max_scaler = MinMaxScaler()
    train_norm = min_max_scaler.fit_transform(train_ext)
    test_norm = min_max_scaler.fit_transform(test_ext)

    # Create a KNN classification system with k = 5
    # Uses the p2 (Euclidean) norm
    knn = KNeighborsClassifier(n_neighbors=params['neighbours'], p=params['distance'])
    knn.fit(train_norm, pca.train_labels)

    # Feed the test data in the classifier to get the predictions
    pred = knn.predict(test_norm)
    calculate_score(pca, pred)
    return [pca, train_norm, test_norm]


def calculate_score(name, pca, pred):
    # Check how many were correct
    scorecard = []

    for i, sample in enumerate(pca.test_data):
        # Check if the KNN classification was correct
        if round(pred[i]) == pca.test_labels[i]:
            scorecard.append(1)
        else:
            scorecard.append(0)
            pass
        # Calculate the performance score, the fraction of correct answers
        scorecard_array = numpy.asarray(scorecard)

    print('KNN performance: %.2f\n' % ((scorecard_array.sum() / scorecard_array.size) * 100))


def mnist_train(training_data, labels, n, reps):
    # train the neural network on each training sample
    while reps > 0:
        count = 0
        for record in training_data:
            # scale and shift the inputs from 0..255 to 0.01..1
            inputs = (numpy.asfarray(record) / 1.0 * 0.99) + 0.01
            # create the target output values (all 0.01, except the desired label which is 0.99)
            targets = numpy.zeros(n.o_nodes) + 0.01
            targets[int(labels[count])] = 0.99
            n.train(inputs, targets)
            count += 1
        reps -= 1


def mnist_test(test_data, labels, n):
    scorecard = []
    count = 0
    for record in test_data:
        inputs = (numpy.asfarray(record) / 1.0 * 0.99) + 0.01
        outputs = n.query(inputs)
        label = numpy.argmax(outputs)

        correct_label = int(labels[count])
        #print('Target: {}\tNetwork: {}'.format(correct_label, label))

        if label == correct_label:
            scorecard.append(1)
        else:
            scorecard.append(0)
        count += 1

    return scorecard


def neural_net(pca, train_norm, test_norm):
    net = nn(params['components'], params['hiddens'], params['outputs'], params['lr'])
    mnist_train(train_norm, pca.train_labels, net,  params['reps'])
    results = mnist_test(test_norm, pca.test_labels, net)
    print('Net performance: %.2f' % (results.count(1)/len(results) * 100.0))
    #plot(test_list, results)


if __name__ == '__main__':
    params = {
        'training file': 'MNIST\mnist_train_100.csv',
        'test file': 'MNIST\mnist_test.csv',
        'components': 20,
        'neighbours': 6,
        'distance': 2,
        'hiddens': 7,
        'outputs': 10,
        'lr': 0.3,
        'reps': 1000
    }

    [pca, train_norm, test_norm] = knn()
    neural_net(pca, train_norm, test_norm)
