import numpy as np
import random
import time
from numba import njit, uint32, uint64

import numbarng


N    = 100000000 # number of iterations
high = 100       # will sample an integer from [0,high)


@njit
def test_random():
	r = 0
	i = uint32(0)
	while i < N:
		r += random.randint(0, high)
		i += 1
	return r

@njit
def test_np_random():
	r = 0
	i = uint32(0)
	while i < N:
		r += np.random.randint(high)
		i += 1
	return r


def make_randint_test(cl):
	@njit(fastmath=True)
	def g():
		rng = cl()
		r   = 0
		i   = uint64(0)
		while i < N:
			r += rng.randint(high)
			i += 1
		return r

	g()   # to compile it

	return g

def make_randint_array_test(cl):
	@njit(fastmath=True)
	def g():
		rng = cl()
		z   = rng.randint_array(high, N)
		return z

	g()   # to compile it

	return g


to_run = []
for cl in numbarng.RNG_CLASSES:
	to_run.append( (make_randint_test(cl),  f'numbarng.{cl.__name__}().randint'))
to_run.append( (test_np_random, 'np.random.randint') )
to_run.append( (test_random,    'random.randint') )

print(f"Adding {N} random numbers in range [0,{high}) in numba")
for f, lbl in to_run:
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


to_run2 = []
for cl in numbarng.RNG_CLASSES:
	to_run2.append( (make_randint_array_test(cl),  f'numbarng.{cl.__name__}().randint_array'))
rng_np = np.random.default_rng()
to_run2.append( (lambda: rng_np.integers(high,size=N)      , '[numpy rng].integers') )
to_run2.append( (lambda: np.random.randint(high, size=(N,)), 'np.random.randint') )
to_run2.append( (lambda: test_random_list(high, N)         , 'numba + random.random') )


print(f"Making array of {N} random numbers in range [0,{high})")
for f, lbl in to_run2:
	start_time = time.time()
	f()
	print(f'{lbl:35s} took {time.time() - start_time:3.5f} seconds')
