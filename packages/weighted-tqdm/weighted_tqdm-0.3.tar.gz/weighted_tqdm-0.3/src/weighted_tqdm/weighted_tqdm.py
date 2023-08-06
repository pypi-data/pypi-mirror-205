# -*- coding: utf-8 -*-
# A function that modifies tqdm progress bars to estimate the remaining time, by allowing the user to specify how much time a step takes with respect to the others
# adds input weights=[1,2,4,8,16] for a progress bar that takes into account that iteration 2 takes twice as long as iteration 1, and iteration 3 takes 4 times as long as iteration 1, etc.
import time
from tqdm import tqdm
def weighted_tqdm(iterable, weights=None, **kwargs):
    # calulcate the total number of iterations
    if hasattr(iterable, '__len__'):
        total = len(iterable)
    # check if total is an argument in kwargs
    elif 'total' in kwargs:
        total = kwargs['total']
    elif isinstance(weights, (list, tuple, np.ndarray)):
        total = len(weights)
    else:
        raise ValueError('tqdm_factor requires a total number of iterations to be specified, either by using an iterator with __len__, by specifying total directly or by providing a weights list')
    # determine the sum of the weights if weights is specified otherwise assume weights are all 1
    if weights is not None:
        if hasattr(weights, '__iter__'): #isinstance(weights, (list, tuple, np.ndarray)):
            min_weight = min(weights)
            weights = [int(i/min_weight) for i in weights]
            weight_sum = sum(weights)
        else:
            weight_vals = [weights(i) for i in iterable]
            min_weight = min(weight_vals)
            weights = [int(i/min_weight) for i in weight_vals]
            weight_sum = sum(weights)
    else:
        weight_sum = total
        weights = [1]*total
    # create a new tqdm object, then with every iteration yield the next weight in weight_vals
    pbar = tqdm(total=weight_sum, **kwargs)
    i = 1
    pbar.set_description('(' +str(i) + '/' + str(total) + ')')
    # with every iteration 
    iterator = iter(iterable)
    yield next(iterator)
    for weight in weights[:-1]:
        i += 1
        pbar.set_description('(' +str(i) + '/' + str(total) + ')')
        pbar.update(weight)
        yield next(iterator)
    pbar.set_description('(Done)')
    pbar.update(weights[-1])
    pbar.close()

def qudit_tqdm(iterable, dit=2, exp=3, **kwargs):
    #  calculates the increase in compute for qudit calculations (by default for qubits and considereng O(n**3) operations)
    return weighted_tqdm(iterable, weights=lambda i: (dit**i)**exp, **kwargs)
        
# test it out
#weights = lambda i: (2**i)**3
#iterable = [1,2,3]
#for i, j in enumerate(weighted_tqdm(iterable, weights=weights)):
#    time.sleep(weights(i)/8)