#!/bin/sh
#python setup.py build_ext --inplace
pip uninstall -y yarp-parser
pip install git+https://github.com/ewimberley/yarp.git@dev