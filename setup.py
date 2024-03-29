#!/usr/bin/env python

from distutils.core import setup
from setuptools import setup
#from Cython.Build import cythonize

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='pyanchetto',
      version='0.3.0',
      description='A python chess engine.',
      author='Eric Wimberley',
      packages=['pyanchetto'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/ewimberley/Pyanchetto",
      project_urls={
          "Bug Tracker": "https://github.com/ewimberley/Pyanchetto/issues",
      },
      python_requires=">=3.6",
      install_requires="yarp-parser>=0.2",
      #ext_modules=cythonize(["pyanchetto/chess.pyx"])
      )