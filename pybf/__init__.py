# Copyright (c) Amr Ali <amr.ali.cc@gmail.com>
# See LICENSE for details.

from .interpreter import Interpreter
from .translator import Translator
from .version import __version__

def pybf_main():
    """
    Main program code for running the BF interpreter and code generator.
    """
    import sys, argparse
    _desc = "BrainFuck interpreter and code generator."
    _epilog = "Report bugs on <https://github.com/amrali/pybf/issues>\n" \
            "pybf git repository: <https://github.com/amrali/pybf>"
    parser = argparse.ArgumentParser(description=_desc, epilog=_epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)

    mutex_group = parser.add_mutually_exclusive_group()
    mutex_group.add_argument('-i', '--interpret', action='store_true',
            help="interpret code in a file or from standard input.")
    mutex_group.add_argument('-g', '--generate', action='store_true',
            help="generate BF code for the content in a file or from standard input.")

    parser.add_argument('-s', '--memory-size', type=int, default=0,
            help="memory size or cells available for the program, the default for the " \
                    "interpreter is 30000 and 16 for the code generator. Note that " \
                    "it is preferred to use the default value for the code generator.")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__,
            help="output version information and exit")
    parser.add_argument('input',
            help="the filename to read content from or specify `-` to read from standard input")

    args = parser.parse_args()
    if args.input == '-':
        cont_input = sys.stdin
    else:
        cont_input = file(args.input)

    if args.interpret:
        if args.memory_size:
            itr = Interpreter(fd=cont_input, memory_size=args.memory_size)
        else:
            itr = Interpreter(fd=cont_input)
        itr.read_all()
        itr.interpret_all()
        sys.stdout.flush()
    elif args.generate:
        if args.memory_size:
            tr = Translator(fd=cont_input, memory_size=args.memory_size)
        else:
            tr = Translator(fd=cont_input)
        sys.stdout.write(tr.get_init_code())
        while True:
            bfc = tr.read()
            if not bfc: break
            sys.stdout.write(bfc)
        sys.stdout.write("\n")
        sys.stdout.flush()

