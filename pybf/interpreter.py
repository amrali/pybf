# Copyright (c) Amr Ali <amr.ali.cc@gmail.com>
# See LICENSE for details.

import sys

class Interpreter(object):
    """
    A Brainfuck interpreter. This could be thought of it as the machine head
    reading the tape and executing instructions.
    """

    def __init__(self, fd=None, buf='', memory_size=30000, fd_in=sys.stdin, fd_out=sys.stdout):
        from StringIO import StringIO
        super(Interpreter, self).__init__()
        if fd:
            self._fd = fd
        elif buf:
            self._fd = StringIO(buf)
        else:
            raise RuntimeError("either fd or buf has to be specified")

        self._fd_in = fd_in
        self._fd_out = fd_out
        self._memory_size = memory_size
        self.reset()

    def read(self, n=1):
        """
        Read n-number of ops into memory. Return false when no more.
        Note that invalid ops are ignored.
        """
        bfc = self._fd.read(n)
        for op in bfc:
            if self._isvalid_op(op): self._push_op(op)
        return not not bfc

    def read_all(self):
        """
        Helper function to read all instructions into memory in one call.
        """
        while self.read(512): pass

    def reset(self):
        """
        Reset the machine state and clear out all registers.
        """
        self._ip = 0
        self._ptr = 0
        self._memory = [0] * self._memory_size
        self._stack = [[], []]

    def interpret(self):
        """
        Interpret a single op in memory.
        """
        bfc = self._get_op(self._ip)
        if bfc == False:
            return False

        if bfc == '>':
            self._ptr += 1
        elif bfc == '<':
            self._ptr -= 1
        elif bfc == '+':
            self._memory[self._ptr] = (self._memory[self._ptr] + 1) % 256
        elif bfc == '-':
            self._memory[self._ptr] = (self._memory[self._ptr] - 1) % 256
        elif bfc == ',':
            char = self._fd_in.read(1)
            if len(char) == 0:
                return False
            self._memory[self._ptr] = ord(char)
        elif bfc == '.':
            self._fd_out.write(chr(self._memory[self._ptr]))
        elif bfc == '[':
            if self._memory[self._ptr] == 0:
                # Skip all further instructions till a matching ']' is found.
                loop = 1
                while loop > 0:
                    self._ip += 1
                    bfc = self._get_op(self._ip)
                    if bfc == '[':
                        loop += 1
                    elif bfc == ']':
                        loop -= 1
                    elif bfc == False:
                        raise SyntaxError("unmatched '['")
            else:
                # Push loop IP to the stack so later we can jump to it directly.
                self._push_loop_ptr(self._ip)
        elif bfc == ']':
            # Subtract one so that it gets added later at the
            # end of the function.
            self._ip = self._pop_loop_ptr() - 1
        self._ip += 1
        return True

    def interpret_all(self):
        """
        Helper function to interpret all instructions in one call.
        """
        while self.interpret(): pass

    def _isvalid_op(self, bfc):
        return bfc in ['>', '<', '+', '-', '.', ',', '[', ']']

    def _push_op(self, bfc):
        self._stack[0].append(bfc)

    def _get_op(self, ip):
        try:
            return self._stack[0][ip]
        except IndexError:
            return False

    def _push_loop_ptr(self, ip):
        self._stack[1].append(ip)

    def _pop_loop_ptr(self):
        try:
            return self._stack[1].pop()
        except IndexError:
            raise SyntaxError("unmatched ']'")
