import unittest
from . import test_interpreter
from . import test_translator

suite = unittest.TestSuite()
suite.addTests(test_interpreter.tests)
suite.addTests(test_translator.tests)
