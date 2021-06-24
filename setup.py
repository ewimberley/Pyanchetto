#!/usr/bin/env python

from distutils.core import setup
from setuptools import setup
from Cython.Build import cythonize

setup(name='pyanchetto',
      version='0.1',
      description='A python chess engine.',
      author='Eric Wimberley',
      packages=['pyanchetto'],
      #ext_modules=cythonize(["pyanchetto/chess.pyx"])
      )