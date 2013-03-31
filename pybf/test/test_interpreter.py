# Copyright (c) Amr Ali <amr.ali.cc@gmail.com>
# See LICENSE for details.

import os
import sys
import unittest
from StringIO import StringIO
from pybf import Interpreter

def _get_fd(filename):
    samples_dir = os.path.join(os.path.dirname(__file__), "samples")
    return file(os.path.join(samples_dir, filename))

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        samples = {}
        samples['hello'] = _get_fd('hello_world.b')
        samples['hanoi'] = (_get_fd('hanoi.b'), _get_fd('hanoi.out').read())
        samples['collatz'] = _get_fd('collatz.b')
        samples['400quine'] = (_get_fd('400quine.b'), _get_fd('400quine.out').read())
        samples['numwarp'] = (_get_fd('numwarp.b'), _get_fd('numwarp.out').read())
        samples['utm'] = _get_fd('utm.b')
        self.pybf_samples = samples

    def _init_sample(self, fd, buf_in=''):
        in_buf = StringIO(buf_in)
        out_buf = StringIO()
        itr = Interpreter(fd=fd, fd_in=in_buf, fd_out=out_buf)
        itr.read_all()
        itr.interpret_all()
        out_buf.seek(0)
        return out_buf.read()

    def test_hello_sample(self):
        res = self._init_sample(self.pybf_samples['hello'])
        self.assertEqual(res, "Hello World!\n")

    def test_hanoi_sample(self):
        res = self._init_sample(self.pybf_samples['hanoi'][0], "5\n")
        self.assertEqual(res, self.pybf_samples['hanoi'][1])

    def test_collatz_sample(self):
        res = self._init_sample(self.pybf_samples['collatz'], "34343\n")
        self.assertEqual(res, "173\n")

    def test_400quine_sample(self):
        res = self._init_sample(self.pybf_samples['400quine'][0])
        self.assertEqual(res, self.pybf_samples['400quine'][1])

    def test_numwarp_sample(self):
        res = self._init_sample(self.pybf_samples['numwarp'][0], "4345599\n")
        self.assertEqual(res, self.pybf_samples['numwarp'][1])

    def test_utm_sample(self):
        res = self._init_sample(self.pybf_samples['utm'], "b1b1bbb1c1c11111d\n")
        self.assertEqual(res, "1c11111\n")

tests = unittest.TestSuite()
tests.addTests(unittest.TestLoader().loadTestsFromTestCase(TestInterpreter))
