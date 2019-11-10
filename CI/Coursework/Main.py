from Recording import Recording
from Plotter import Plotter
import numpy as np
# import PyQt5


if __name__ == '__main__':
    training_set = Recording('training')
    training_set_plotter = Plotter(training_set)
    training_set_plotter.plot(training_set.index[210], time=True)
    print(training_set.d[210])
