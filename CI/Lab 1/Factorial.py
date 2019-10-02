import numpy as np
from functools import reduce
from math import factorial as factorial

num_in = int(input('Enter an integer value: '))  # TODO: sanity check
ans = factorial(num_in + 1)  # reduce((lambda x, y: x*y), np.arange(2, num_in+1))
print('\nThe factorial of {} is {}'.format(num_in, ans))