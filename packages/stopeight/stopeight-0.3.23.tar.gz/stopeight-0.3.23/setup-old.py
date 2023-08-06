#!/usr/bin/env python

import os
_include_dirs=[
    os.path.join('stopeight-clibs','cmake-git-version-tracking','better-example'),
]
_qt5_include_dirs=_include_dirs

from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup, find_namespace_packages

setup( use_scm_version=True,
       packages=find_namespace_packages(include=['stopeight.*']),
       ext_modules = [
           Pybind11Extension(
               'stopeight.grapher',
               [os.path.join('stopeight-clibs','grapher','python','IFPyGrapher.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join('stopeight-clibs','include'),
                   os.path.join('stopeight-clibs','grapher')
               ],
               libraries=['stopeight-clibs-grapher',
               'stopeight-clibs-matrix'],
               language='c++',
               optional=False
           ),
           Pybind11Extension(
               'stopeight.matrix',
               [os.path.join('stopeight-clibs','matrix','python','IFPyMatrix.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join('stopeight-clibs','include'),
                   os.path.join('stopeight-clibs','matrix')
               ],
               libraries=['stopeight-clibs-matrix'],
               language='c++',
               optional=False
           ),
           Pybind11Extension(
               'stopeight.analyzer',
               [os.path.join('stopeight-clibs','analyzer','python','IFPyAnalyzer.cpp')],
               include_dirs=_include_dirs + [
                   os.path.join('stopeight-clibs','include'),
                   os.path.join('stopeight-clibs','analyzer')
               ],
               libraries=['stopeight-clibs-analyzer'],
               language='c++',
               optional=True
           ),
           Pybind11Extension(
              'stopeight.legacy',
               [os.path.join('stopeight-clibs','legacy','python','interfacepython.cpp'),
               ],
               include_dirs=_qt5_include_dirs + [
                   os.path.join('stopeight-clibs','legacy/include'),
                   os.path.join('stopeight-clibs','legacy','python')
               ],
               libraries=['stopeight-clibs-legacy','Qt5Core'],#Qt5Core needed for old wrapper
               language='c++',
               optional=True
              ),
            Pybind11Extension(
              'stopeight.getters',
               [os.path.join('stopeight-clibs','legacy','python','IFPyGetters.cpp'),
               os.path.join('stopeight-clibs','legacy','python','IFPyShared.cpp')],
               include_dirs=_qt5_include_dirs + [
                   os.path.join('stopeight-clibs','legacy/include'),
                   os.path.join('stopeight-clibs','legacy','python')
               ],
               libraries=['stopeight-clibs-legacy','stopeight-clibs-matrix','Qt5Core'],#Qt5Core needed for old wrapper
               language='c++',
               optional=True
              ),
            Pybind11Extension(
              'stopeight.finders',
               [os.path.join('stopeight-clibs','legacy','python','IFPyFinders.cpp'),
               os.path.join('stopeight-clibs','legacy','python','IFPyShared.cpp')],
               include_dirs=_qt5_include_dirs + [
                   os.path.join('stopeight-clibs','legacy/include'),
                   os.path.join('stopeight-clibs','legacy','python')
               ],
               libraries=['stopeight-clibs-legacy','stopeight-clibs-matrix','Qt5Core'],#Qt5Core needed for old wrapper
               language='c++',
               optional=True
              ),
       ],
       cmdclass={'build_ext': build_ext},
)
