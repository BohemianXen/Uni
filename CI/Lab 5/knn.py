# Import numpy for arrays and matplotlib for drawing the numbers
import numpy
from pca import PCA
from sklearn.preprocessing import MinMaxScaler
# k Nearest Neighbour
from sklearn.neighbors import KNeighborsClassifier


if __name__ == '__main__':

    params = {
        'training file': 'MNIST\mnist_train_100.csv',
        'test file': 'MNIST\mnist_test.csv',
        'components': 10
    }

    pca = PCA(params['training file'], params['test file'], params['components'])
    pca.plot()

    # Extract the principle components from the training data
    train_ext =pca._pca.fit_transform(pca.train_data)
    # Transform the test data using the same components
    test_ext = pca._pca.transform(pca.test_data)

    # Normalise the data sets
    min_max_scaler = MinMaxScaler()
    train_norm = min_max_scaler.fit_transform(train_ext)
    test_norm = min_max_scaler.fit_transform(test_ext)

    # Create a KNN classification system with k = 5
    # Uses the p2 (Euclidean) norm
    knn = KNeighborsClassifier(n_neighbors=5, p=2)
    knn.fit(train_norm, pca.train_labels)

    # Feed the test data in the classifier to get the predictions
    pred = knn.predict(test_norm)

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
        print('Performance = ', (scorecard_array.sum() / scorecard_array.size) * 100, ' % ')
