# numbapcg

Implementation of the  [PCG](https://en.wikipedia.org/wiki/Permuted_congruential_generator) random number generator in numba for Python. PCG (Permuted congruential generator) is a fast generator for random 32-bit integers.

* O'Neill, Melissa E.  PCG: A Family of Simple Fast Space-Efficient Statistically Good Algorithms for Random Number Generation [(PDF)](https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf) (Technical report). Harvey Mudd College. HMC-CS-2014-0905.

Our case is based on an adaptation of code by Daniel Lemire from the (fastrand)[https://github.com/lemire/fastrand/] repository (see (file)[https://github.com/lemire/fastrand/blob/master/fastrandmodule.c])

## Installation

You can install this by running
```
python -m pip install https://github.com/artemyk/numbapcg/archive/refs/heads/main.zip
```


## Examples
```python
import numbapcg
rng = numbapcg.PCG32()     # Initialize the random number generator
rng.randint(100)           # Get a single random integer in the range [0,100)
rng.randint_array(100, 10) # Get an array of 10 random integers, each in the range [0,100)
```

Importantly, it can be called from numba:
```python
import numbapcg
from numba import njit

@njit
def f():
  rng = numbapcg.PCG32()
  return rng.randint(100)

f()
```

## Benchmarks

Benchmarks on i5 2GHz MacBook Pro:
```
% python benchmark.py
Adding 100000000 random numbers in range [0,100) in numba
[numbapcg rng].randint              took 0.30527 seconds
np.random.randint                   took 1.07643 seconds
random.randint                      took 0.73764 seconds
Making array of 100000000 random numbers in range [0,100)
[numbapcg rng].randint_array        took 0.57106 seconds
[numpy    rng].integers             took 0.81355 seconds
np.random.randint                   took 1.63645 seconds
numba + random.random               took 2.17628 seconds
```
