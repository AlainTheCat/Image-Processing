from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize("cython/cythonImage.pyx"),
    include_dirs=[numpy.get_include()]
)    
