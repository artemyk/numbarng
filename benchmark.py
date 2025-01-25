import numpy as np
import random
import time
from numba import njit

import numbapcg


N    = 100000000 # number of iterations
high = 100       # will sample an integer from [0,high)




@njit
def test_random():
	r = 0
	for _ in range(N):
		r += random.randint(0, high)
	return r

@njit
def test_np_random():
	r = 0
	for _ in range(N):
		r += np.random.randint(high)
	return r

@njit
def test_numbapcg():
	rng = numbapcg.PCG32()
	r = 0
	for _ in range(N):
		r += rng.randint(high)
	return r


print(f"Adding {N} random numbers in range [0,{high}) in numba")
for f,lbl in [(test_numbapcg,  '[numbapcg rng].randint'),
		      (test_np_random, 'np.random.randint'),
		      (test_random,    'random.randint'),
		      ]:
	f() # make sure its compiled
	start_time = time.time()
	f()
	print(f'{lbl:35s} took {time.time() - start_time:3.5f} seconds')


@njit
def test_random_list(high, N):
	z   = np.zeros(N, dtype='uint32')
	for i in range(N):
		z[i] = random.randint(0,high)
	return z

@njit
def random_list(high, N):
	return [random.randint(0,high) for _ in range(N)]

rng    = numbapcg.PCG32()
rng_np = np.random.default_rng()
print(f"Making array of {N} random numbers in range [0,{high})")
for f,lbl in [(lambda: rng.randint_array(high,N)         , '[numbapcg rng].randint_array'),
		      (lambda: rng_np.integers(high,size=N)      , '[numpy    rng].integers'),
		      (lambda: np.random.randint(high, size=(N,)), 'np.random.randint'),
		      (lambda: test_random_list(high, N)         , 'numba + random.random'),
		      ]:
	f() # make sure its compiled
	start_time = time.time()
	f()
	print(f'{lbl:35s} took {time.time() - start_time:3.5f} seconds')
