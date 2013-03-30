# Copyright (c) Amr Ali <amr.ali.cc@gmail.com>
# See LICENSE for details.

class EOPError(Exception): pass

class Interpreter(object):
    """
    A BrainFuck interpreter. This could be thought of it as the machine head
    reading the tabe and executing instructions.
    """

    def __init__(self, fd=None, buf='', memory_size=30000):
        from StringIO import StringIO
        super(Interpreter, self).__init__()
        if fd:
            self._fd = fd
        elif buf:
            self._fd = StringIO(buf)
        else:
            raise RuntimeError("either fd or buf has to be specified")

        self._ip = 0
        self._ptr = 0
        self._memory = [0] * memory_size
        self._stack = [[], []]
        self._skip_loop = False

    def read(self, n=1):
        """
        Read n-number of ops into memory. Return false when no more.
        Note that invalid ops are ignored.
        """
        bfc = self._fd.read(n)
        for op in bfc:
            if self._isvalid_op(op): self._push_op(op)
        return not not bfc

    def interpret(self):
        """
        Interpret a single op in memory.
        """
        import sys
        bfc = self._get_op(self._ip)
        if not self._skip_loop:
            if bfc == '>': self._ptr += 1
            elif bfc == '<': self._ptr -= 1
            elif bfc == '+': self._memory[self._ptr] += 1
            elif bfc == '-': self._memory[self._ptr] -= 1
            elif bfc == ',': self._memory[self._ptr] = ord(sys.stdin.read(1))
            elif bfc == '.': sys.stdout.write(chr(self._memory[self._ptr]))
            elif bfc == '[':
                if self._memory[self._ptr] == 0: self._skip_loop = True
                else:
                    self._skip_loop = False
                    self._push_loop_ptr(self._ip)
            elif bfc == ']':
                self._skip_loop = False
                if self._memory[self._ptr]:
                    # Subtract one so that it gets added later at the
                    # end of the function.
                    self._ip = self._pop_loop_ptr() - 1
        self._ip += 1

    def _isvalid_op(self, bfc):
        return bfc in ['>', '<', '+', '-', '.', ',', '[', ']']

    def _push_op(self, bfc):
        self._stack[0].append(bfc)

    def _get_op(self, ip):
        try:
            return self._stack[0][ip]
        except IndexError:
            raise EOPError("the well's dry")

    def _push_loop_ptr(self, ip):
        self._stack[1].append(ip)

    def _pop_loop_ptr(self):
        try:
            return self._stack[1].pop()
        except IndexError:
            raise SyntaxError("unmatched ']'")
