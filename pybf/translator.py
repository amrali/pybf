# Copyright (c) Amr Ali <amr.ali.cc@gmail.com>
# See LICENSE for details.

class Translator(object):
    """
    A Brainfuck translator that takes any content and translate it
    into Brainfuck code that when ran will reproduce the supplied content.
    """

    def __init__(self, fd=None, buf='', memory_size=16):
        from io import StringIO
        super().__init__()
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
        # Counter value (ctr=8) determines partition size: 256 / (2*ctr*memory_size)
        # With default memory_size=16: 256 / (2*8*16) = 1, meaning each partition
        # covers approximately 256/16 = 16 byte values. This is the trade-off
        # mentioned in README: more cells = bigger init code but fewer instructions
        # per byte to translate. Using ctr=8 balances initialization size vs runtime.
        ctr = 8

        # Initialize cell 0 (counter) to 8. This cell will be decremented to 0
        # during the loop, running the partition setup exactly 8 times.
        prog = "+" * ctr

        # Start loop: runs while counter cell is non-zero (8 iterations)
        prog += "["

        # Loop mechanics: Each iteration moves right through all cells and adds
        # 2*i to cell i. After 8 iterations, cell i contains 2*i*8 = 16*i.
        # This creates partition boundaries at: 0, 16, 32, 48, 64, 80, 96, 112...
        # Each cell becomes the "anchor" for its partition (e.g., cell 2 = 32,
        # which is optimal for byte values 24-39 since it minimizes +/- operations).
        for i in range(0, self._memory_size):
            prog += ">"  # Move to next cell
            prog += "+" * 2 * i  # Add 2*i (will execute 8 times in loop)
            self._memory[i] = 2 * i * ctr  # Track final value: 2*i*8 = 16*i

        # Move back to counter cell and decrement it. Loop continues until counter=0.
        # Final ">": positions pointer at cell 1 (ready for translation operations).
        prog += "<" * self._memory_size + "-]>"
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
        # Goal: Find the cell with value closest to the target byte to minimize
        # the number of +/- operations needed. For example, to output 'A' (65),
        # it's more efficient to start from cell 2 (value 32) requiring 33 increments
        # than to start from cell 0 (value 0) requiring 65 increments.
        cell_ptr_min = 0
        delta_min = 256

        # Linear search strategy: Check every cell to find the one with minimum delta.
        # This exhaustive search guarantees we find the optimal cell for each byte.
        for ptr in range(0, self._memory_size):
            cell = self._memory[ptr]

            # Delta represents the absolute distance between the cell's current value
            # and the target byte. This delta directly translates to the number of
            # +/- BF operations needed to reach the target value from this cell.
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

