#!/usr/bin/env python
# Copyright (c) Amr Ali <amr.ali.cc@gmail.com>
# See LICENSE for details.

import os
from unittest import TextTestRunner
from distutils.core import setup, Command
from distutils.command.install import INSTALL_SCHEMES
from pybf.test import suite as pybf_test_suite
from pybf import __version__

# Modify the data install dir to match the source install dir
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

def get_samples():
    rel_dir = os.path.join("pybf", "test", "samples")
    samples_dir = os.path.dirname(__file__)
    samples_dir = os.path.join(samples_dir, "pybf", "test", "samples")
    return (rel_dir, [os.path.join(samples_dir, sample) for sample in os.listdir(samples_dir)])

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """
        Run all test modules.
        """
        t = TextTestRunner(verbosity = 2)
        t.run(pybf_test_suite)

packages = [
    'pybf',
    'pybf.test',
    ]

data_files = [
    get_samples(),
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
        scripts = [os.path.join('bin', 'pybf')],
        packages = packages,
        data_files = data_files,
        license = 'GPLv3+',
        platforms = "Posix; MacOS X; Windows",
        classifiers = classifiers,
        cmdclass = {'test': TestCommand },
     )
