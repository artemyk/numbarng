from setuptools import setup

setup(
   name='numbarng',
   version='0.2',
   description='Fast random numbers for numba',
   author='Artemy Kolchinsky',
   author_email='artemyk@gmail.com',
   packages=['numbarng'],
   install_requires=['numpy', 'numba',],
)

