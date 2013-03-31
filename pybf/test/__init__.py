import unittest
import test_interpreter
import test_translator

suite = unittest.TestSuite()
suite.addTests(test_interpreter.tests)
suite.addTests(test_translator.tests)
