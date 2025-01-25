from setuptools import setup

setup(
   name='numbapcg',
   version='0.1',
   description='PCG 32-bit random number generator for numba',
   author='Artemy Kolchinsky',
   author_email='artemyk@gmail.com',
   packages=['numbapcg'],
   install_requires=['numpy', 'numba',],
)

