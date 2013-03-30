PyBF
====

A Python package that provides a Brainfuck_ interpreter and code generator modules.
It also provides command line utility.

Interpreting a Brainfuck_ code file is as easy as::

    $ pybf -i code.bf

Or from standard input::

    $ echo "+++++++++++." | pybf -i -

To generate Brainfuck_ code that will reproduce any content you supply::

    $ echo "hello world" | pybf -g -

Installation
------------

To install it using pip_ all you have to do is::

    $ pip install pybf

To install it using the provided ``setup.py`` file, you'll need to install distutils_ first
and then issue the following command::

    $ python setup.py install

Usage details
-------------

The interpreter by default will reserve 30000 1-byte cells but you can change that
by supplying the ``-s`` with the desired value.

The Brainfuck_ code generator by default reserves 16 cells, memory size here is a trade-off
between optimizing (for size) between big and small input as with more reserved
cells the bigger Brainfuck_ (loop) initialization code will be and less Brainfuck_ instructions
to reproduce 1 byte. The opposite goes for increasing the number of reserved cells as
the initialization code will be smaller but there will be more instructions to
reproduce 1 byte.

.. _Brainfuck: http://en.wikipedia.org/wiki/Brainfuck
.. _pip: http://pypi.python.org/pypi/pip
.. _distutils: http://docs.python.org/2/library/distutils.html
