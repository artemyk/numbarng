import numbapcg
import numpy as np
import unittest

class TestObj(unittest.TestCase):

        def test_randint(self):
            rng = numbapcg.PCG32()
            rng.randint(100)

        def test_randint_array(self):
            rng = numbapcg.PCG32()
            rng.randint_array(100,100)

        def test_randint_bounds(self):
            rng = numbapcg.PCG32()
            N = 100
            for _ in range(10000):
                assert(rng.randint(N) < N)

        def test_randint_array_bounds(self):
            rng = numbapcg.PCG32()
            N = 100
            for _ in range(10000):
                assert(np.all(rng.randint_array(N, 100) < N))



if __name__ == '__main__': 
    unittest.main() 

