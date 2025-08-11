from numba import uint64, uint32, int32, njit
from numba.experimental import jitclass
import numpy as np
from numba.core.types import FunctionType
import numba
MAX_SEED64 = 2**63-1


# The following are used because @jitclass does not support inheritance
@njit(inline='always', fastmath=True, cache=True)
def _randint(rng, high : uint32):
    """
    Use to a 32-bit random number generator to sample a random integer.

    Parameters
    ----------
    rng : object
        Random number generator
    high : int
        Random number will fall in the range [0, high)
    """
    high           = uint32(high)
    random32bit    = uint64(rng())
    multiresult    = uint64(random32bit * high)
    leftover       = uint32(multiresult)
    if (leftover < high):
        threshold = uint32(-high % high)  # Computes 2^32 - high % high, see end of Sec 2. in https://arxiv.org/pdf/2408.06213
        while (leftover < threshold):
            random32bit    = uint64( rng() )

            multiresult    = uint64(random32bit * high)
            leftover       = uint32(multiresult)
    return uint32(multiresult >> 32)


@njit(inline='always', fastmath=True, cache=True)
def _randint_array(rng, high, size):
    """
    Return a numpy array of random integers.

    Parameters
    ----------
    rng : object
        Random number generator
    high : int
        Random numbers will fall in the range [0, high)
    size : int
        How many numbers to generate
    """
    z = np.empty(size, dtype='uint32')
    for i in range(size):
        z[i] = _randint(rng, high)
    return z



@jitclass
class Wyhash:
    """
    Based on wyhash algorithm by Wangyi Fudan. Has 64-bit state.
    https://github.com/wangyi-fudan/wyhash/blob/master/wyhash32.h
    """
    rng_state : uint64

    def __init__(self):
        self.rng_state = uint64(np.random.randint(MAX_SEED64))

    def set_state(self, rng_state):
        self.rng_state = rng_state

    def random32bit(self):
        self.rng_state += uint64(0xa0761d6478bd642f)
        see1  = uint64(self.rng_state^0xe7037ed1a0b428db)
        see1 *= (see1>>32)|(see1<<32)
        x     = (self.rng_state*((self.rng_state>>32)|(self.rng_state<<32)))^((see1>>32)|(see1<<32)) 
        return uint32( x >> 32 )

    def randint(self, high):
        return _randint(self.random32bit, high)
    def randint_array(self, high, size):
        return _randint_array(self.random32bit, high, size)


@jitclass
class SplitMix:
    """
    Based on code by Kaito Udagawa. Has 32-bit state
    https://github.com/umireon/my-random-stuff/blob/master/xorshift/splitmix32.c

    Itself based on MurmurHash3 fmix32 with adding GOLDEN_GAMMA.
    - Guy L. Steele, Jr., Doug Lea, and Christine H. Flood. 2014. Fast splittable pseudorandom number generators. OOPSLA, 2014.
    """
    rng_state : uint32

    def __init__(self):
        self.rng_state = uint32(np.random.randint(2**32-1))

    def set_state(self, rng_state):
        self.rng_state = rng_state

    def random32bit(self):
        self.rng_state += 0x9e3779b9
        z = uint32(self.rng_state)
        z ^= z >> 16
        z *= 0x21f0aaad
        z ^= z >> 15
        z *= 0x735a2d97
        z ^= z >> 15
        return uint32(z)

    def randint(self, high):
        return _randint(self.random32bit, high)
    def randint_array(self, high, size):
        return _randint_array(self.random32bit, high, size)

# @jitclass
# class SplitMix64:
#     """
#     Based on code by Kaito Udagawa. Has 32-bit state
#     https://github.com/umireon/my-random-stuff/blob/master/xorshift/splitmix32.c

#     Itself based on MurmurHash3 fmix32 with adding GOLDEN_GAMMA.
#     - Guy L. Steele, Jr., Doug Lea, and Christine H. Flood. 2014. Fast splittable pseudorandom number generators. OOPSLA, 2014.
#     """
#     rng_state : uint64

#     def __init__(self):
#         self.rng_state = uin64(np.random.randint(MAX_SEED64))

#     def set_state(self, rng_state):
#         self.rng_state = rng_state

#     def random32bit(self):
#         self.rng_state += 0x9e3779b9
#         z = uint32(self.rng_state)
#         z ^= z >> 16
#         z *= 0x21f0aaad
#         z ^= z >> 15
#         z *= 0x735a2d97
#         z ^= z >> 15
#         return uint32(z)

#     def randint(self, high):
#         return _randint(self, high)
#     def randint_array(self, high, size):
#         return _randint_array(self, high, size)

# x ^= x >> 32;
# x *= 0xe9846af9b1a615d;
# x ^= x >> 32;
# x *= 0xe9846af9b1a615d;
# x ^= x >> 28;


@jitclass
class PCG(object):
    """
    PCG random number generator. Has 64-bit state
    Code adapted from https://github.com/lemire/fastrand/blob/master/fastrandmodule.c
    """
    rng_state : uint64
    rng_inc   : uint64
    

    def __init__(self):
        self.rng_state = uint64(np.random.randint(MAX_SEED64))
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


    def random32bit(self):
        MULTIPLIER = uint64(6364136223846793005)
        oldstate = self.rng_state
        self.rng_state = uint64(oldstate * MULTIPLIER + self.rng_inc)
        xorshifted = uint32(((oldstate >> 18) ^ oldstate) >> 27)
        rot = uint32(oldstate >> 59)
        return uint32( (xorshifted >> rot) | (xorshifted << ((-rot) & 31)) )


    def randint(self, high):
        return _randint(self.random32bit, high)
    def randint_array(self, high, size):
        return _randint_array(self.random32bit, high, size)


RNG_CLASSES = [PCG, Wyhash, SplitMix]
