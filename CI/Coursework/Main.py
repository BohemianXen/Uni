from Recording import Recording
from Plotter import Plotter
from Filters import Filters
import numpy as np
# import PyQt5


if __name__ == '__main__':
    training_set = Recording(filename='training')
    training_set_plotter = Plotter(training_set)

    filter1 = Filters()
    filtered_training_set = training_set.__copy__()
    filtered_training_set.d = filter1.threshold(filtered_training_set.d)
    filtered_training_set_plotter = Plotter(filtered_training_set)

    training_set_plotter.plot(center=training_set.index[210], time=True)
    filtered_training_set_plotter.plot(filtered_training_set.index[210])

    print(training_set.d[210])
