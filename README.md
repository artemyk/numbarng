# numbarng

Implementation of fast pseudo-random number generators in numba for Python.  

Right now it implements:

* Permuted congruential generator [(PCG)](https://en.wikipedia.org/wiki/Permuted_congruential_generator) random number generator [1]. Based on code by Daniel Lemire from the [fastrand](https://github.com/lemire/fastrand/) repository ([fastrandmodule.c](https://github.com/lemire/fastrand/blob/master/fastrandmodule.c]))

* SplitMix32 random number generator [2]. Based on code by [Kaito Udagawa](https://github.com/umireon/my-random-stuff/blob/master/xorshift/splitmix32.c)

* [Wyhash] algorithm. Based on code by [Wangyi Fudan](https://github.com/wangyi-fudan/wyhash/blob/master/wyhash32.h]).



*References*

[1] ME O'Neill.  PCG: A Family of Simple Fast Space-Efficient Statistically Good Algorithms for Random Number Generation [(PDF)](https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf) (Technical report). Harvey Mudd College. HMC-CS-2014-0905.

[2] GL Steele Jr., D Lea, and CH Flood. 2014. Fast splittable pseudorandom number generators. OOPSLA, 2014.


## Installation

You can install this by running
```
python -m pip install https://github.com/artemyk/numbarng/archive/refs/heads/main.zip
```


## Examples
```python
import numbarng
rng = numbarng.PCG()       # Initialize the random number generator
rng.randint(100)           # Get a single random integer in the range [0,100)
rng.randint_array(100, 10) # Get an array of 10 random integers, each in the range [0,100)
```

Importantly, it can be called from numba:
```python
import numbarng
from numba import njit

@njit
def f():
  rng = numbarng.PCG()
  return rng.randint(100)

f()
```

## Benchmarks

Benchmarks on Apple M2:
``` % python benchmark.py
Adding 100000000 random numbers in range [0,100) in numba
numbarng.PCG().randint              took 0.13278 seconds
numbarng.Wyhash().randint           took 0.09141 seconds
numbarng.SplitMix().randint         took 0.08995 seconds
np.random.randint                   took 0.46833 seconds
random.randint                      took 0.40727 seconds
Making array of 100000000 random numbers in range [0,100)
numbarng.PCG().randint_array        took 0.27915 seconds
numbarng.Wyhash().randint_array     took 0.10958 seconds
numbarng.SplitMix().randint_array   took 0.10672 seconds
[numpy    rng].integers             took 0.26561 seconds
np.random.randint                   took 0.57670 seconds
numba + random.random               took 0.81265 seconds
```
