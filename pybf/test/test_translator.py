# Copyright (c) Amr Ali <amr.ali.cc@gmail.com>
# See LICENSE for details.

import unittest
from io import StringIO
from pybf import Translator, Interpreter

class TestTranslator(unittest.TestCase):
    def test_generation(self):
        sample = open(__file__)
        tr = Translator(fd=sample)
        prog = tr.get_init_code()
        prog += tr.read_all()
        self.assertNotIn(',', prog)

        fd = StringIO(prog)
        out_buf = StringIO()
        itr = Interpreter(fd=fd, fd_out=out_buf)
        itr.read_all()
        itr.interpret_all()
        out_buf.seek(0)

        orig = open(__file__).read()
        self.assertEqual(orig, out_buf.read())

tests = unittest.TestSuite()
tests.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTranslator))
