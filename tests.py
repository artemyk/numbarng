import numbarng
import numpy as np
import unittest
from numba import njit 


@njit
def run_numba_tests(rng):                
    rng.randint_array(100,100)
    rng.random32bit()
    N = 100
    for _ in range(10000):
        assert(rng.randint(N) < N)

    for _ in range(1000):
        assert(np.all(rng.randint_array(N, 100) < N))


class TestObj(unittest.TestCase):
        def test_methods(self):
            for cl in numbarng.RNG_CLASSES:
                rng = cl()
                rng.randint_array(100,100)
                rng.random32bit()
                N = 100
                for _ in range(10000):
                    assert(rng.randint(N) < N)

                for _ in range(10000):
                    assert(np.all(rng.randint_array(N, 100) < N))


        def test_methods_numba(self):
            for cl in numbarng.RNG_CLASSES:
                run_numba_tests(cl())

        def test_randint(self):
            for cl in numbarng.RNG_CLASSES:
                rng = cl()
                N = 1000000
                high = 100
                v = rng.randint_array(high,N)
                #counts = np.zeros(high)
                for i in range(high):
                    count = np.sum(v==i)/N
                    if not ( np.abs(count - 1/high) < 5e-3 ):
                        print(i, count)
                        raise Exception(f'Statistical failure for PRNG {cl.__name__}: frequency of outcome {i} is {count}, not 0.01')
                



if __name__ == '__main__': 
    unittest.main() 

