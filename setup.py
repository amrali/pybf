#!/usr/bin/env python
# Copyright (c) Amr Ali <amr.ali.cc@gmail.com>
# See LICENSE for details.

from distutils.core import setup
from pybf import __version__

packages = [
    'pybf',
    ]

classifiers = [
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Natural Language :: English',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    ]

setup(
        name = 'PyBF',
        version = __version__,
        description = 'Brainfuck interpreter and code generator',
        long_description = file('README.rst').read(),
        author = 'Amr Ali',
        author_email = 'amr.ali.cc@gmail.com',
        maintainer = 'Amr Ali',
        maintainer_email = 'amr.ali.cc@gmail.com',
        url = 'https://github.com/amrali/pybf',
        scripts = ['bin/pybf'],
        packages = packages,
        license = 'GPLv3+',
        platforms = "Posix; MacOS X; Windows",
        classifiers = classifiers,
     )
