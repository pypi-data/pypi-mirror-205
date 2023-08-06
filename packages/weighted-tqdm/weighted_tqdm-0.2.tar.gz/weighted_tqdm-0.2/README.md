# weighted_tqdm

Install via 
`pip install weighted_tqdm`

Import via
`from weighted_tqdm import *`

## Description
**weighted_tqdm** works equivalently to tqdm, accepting all the same arguments, but also accepts a `weights` argument. This argument specifies the weights of each item in the iterable and can be given as a function of the iterable or be any iterable (list, array, tuple...). The progress bar will then take into account the weights of each item in it's prediciton of the time, and it's progress bar will be weighted accordingly. To the left of the progress bar an iteration counter is shown.
**qudit_tqdm** is a special version of tqdm, that predicts the remaining time for calculations in quantum mechanics, with the added arguments `dit` specifying whether its a calculation of qubits(default, `dit = 0.2, = 3` for qutrits), and the argument `exp` specifying the scaling of computational time with the dimension of a hilbert space. 


### Examples:
```
from weighted_tqdm import *

how_many_qubits = [1,2,3,4,5]
qubits weights = lambda x: (2**x)**3
for i in weighted_tqdm(how_many_qubits, weights=weights):
    # do something
```
or equivalently 
```
from weighted_tqdm import *
how_many_qubits = [1,2,3,4,5]
for i in qudit_tqdm(how_many_qubits, dim=2, exp=3):
    # do something
```


## Authors: 
By Michael Schilling