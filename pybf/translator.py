# Copyright (c) Amr Ali <amr.ali.cc@gmail.com>
# See LICENSE for details.

class Translator(object):
    """
    A Brainfuck translator that takes any content and translate it
    into Brainfuck code that when ran will reproduce the supplied content.
    """

    def __init__(self, fd=None, buf='', memory_size=16):
        from StringIO import StringIO
        super(Translator, self).__init__()
        if fd:
            self._fd = fd
        elif buf:
            self._fd = StringIO(buf)
        else:
            raise RuntimeError("either fd or buf has to be specified")

        self._ptr = 0
        self._memory = [0] * memory_size
        self._memory_size = memory_size
        self._init_code = self._init_code()

    def get_init_code(self):
        """
        Return the BF code to initialize memory cells.
        """
        return self._init_code

    def read(self, n=1):
        """
        Return the BF commands that will reproduce each byte read from the buffer.
        """
        prog = ''
        data = self._fd.read(n)
        if not data:
            return None

        for char in data:
            prog += self._translate(ord(char)) + "."
        return prog

    def read_all(self):
        """
        Helper function to read all the translated code in one call.
        """
        prog = ''
        while True:
            bfc = self.read(256)
            if not bfc: break
            prog += bfc
        return prog


    def _init_code(self):
        """
        Partition's the 0-255 range of possible byte values over available
        cells by setting their value to the start of each partition.

        cell_0 = 0 <-> 31
        cell_1 = 32 <-> 63
        cell_2 = 64 <-> 95
        cell_3 = 96 <-> 127
        cell_4 = 128 <-> 159
        ...
        """
        ctr = 8
        prog = "+" * ctr # Initialize counter cell to 8
        prog += "[" # Start loop
        for i in xrange(0, self._memory_size):
            prog += ">"
            prog += "+" * 2 * i
            self._memory[i] = 2 * i * ctr
        prog += "<" * self._memory_size + "-]>" # Decrement counter cell
        return prog

    def _translate(self, byte):
        """
        Translate a byte value to the BF code necessary to reproduce it.
        """
        ptr = self._map(byte)
        prog = self._move_ptr(ptr)
        prog += self._set_cell(byte)
        return prog

    def _map(self, byte):
        """
        Map each byte to the partition/cell that will result in less BF commands.
        """
        cell_ptr_min = 0
        delta_min = 256
        for ptr in xrange(0, self._memory_size):
            cell = self._memory[ptr]
            delta = abs(cell - byte)
            if delta < delta_min:
                delta_min = delta
                cell_ptr_min = ptr
        return cell_ptr_min

    def _move_ptr(self, ptr):
        """
        Set the pointer to the desired cell and return the BF code that does so.
        """
        delta = self._ptr - ptr
        self._ptr = ptr
        if delta < 0:
            return ">" * abs(delta)
        else:
            return "<" * delta

    def _set_cell(self, value):
        """
        Update the currently selected cell with the desired value and return
        the BF code that does so.
        """
        delta = self._memory[self._ptr] - value
        self._memory[self._ptr] = value
        if delta < 0:
            return "+" * abs(delta)
        else:
            return "-" * delta

