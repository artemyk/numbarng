from numba import uint64, uint32 
from numba.experimental import jitclass
import numpy as np

multiplier = uint64(6364136223846793005)

@jitclass([('rng_state', uint64),('rng_inc', uint64)])
class PCG32(object):
    """
    numba class that implements the PCG random number generator
    Code adapted from https://github.com/lemire/fastrand/blob/master/fastrandmodule.c

    The seed is initially set as np.random.randint(2**63-1). 
    A different seed can be set by calling set_state.
    """

    def __init__(self):
        # self.rng_state = 0x853c49e6748fea9b 
        self.rng_state = uint64(np.random.randint(2**63-1))
        self.rng_inc   = uint64(0xda3e39cb94b95bdb)


    def set_state(self, rng_state):
        """
        Set state of the generator. Useful for setting a new seed.

        Parameter
        ---------
        rng_state : uint64
            new state
        """
        self.rng_state = rng_state

        
    def set_inc(self, rng_inc):
        """
        Set increment of the generator.

        Parameter
        ---------
        rng_inc : uint64
            new increment
        """
        self.rng_inc = rng_inc


    def pcg32_random(self):
        """
        Core of the PCG32 generator.
        """
        oldstate = self.rng_state
        self.rng_state = oldstate * multiplier + self.rng_inc
        xorshifted = uint32(((oldstate >> 18) ^ oldstate) >> 27)
        rot = uint32(oldstate >> 59)
        return uint32( (xorshifted >> rot) | (xorshifted << ((-rot) & 31)) )


    def randint(self, high):
        """
        Return a random integer.

        Parameters
        ----------
        high : int
            Random number will fall in the range [0, high)
        """

        random32bit    = uint64( self.pcg32_random() )


        multiresult    = uint64(random32bit * high)
        leftover       = uint32(multiresult)
        if (leftover < high):
            threshold = uint32(-high % high)
            while (leftover < threshold):
                random32bit    = uint64( self.pcg32_random() )

                multiresult    = uint64(random32bit * high)
                leftover       = uint32(multiresult)
        return uint32(multiresult >> 32)


    def randint_array(self, high, N):
        """
        Return a numpy array of random integers.

        Parameters
        ----------
        high : int
            Random numbers will fall in the range [0, high)
        N : int
            How many numbers to generate
        """
        z = np.empty(N, dtype='uint32')
        for i in range(N):
            z[i] = self.randint(high)
        return z



# Try to trigger a pre-compilation
_rng = PCG32()
_rng.randint(1)
_rng.set_state(1)
_rng.set_inc(1)
_rng.randint_array(1,2)
del _rng

