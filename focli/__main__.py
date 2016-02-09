#!/usr/bin/env python
"""Command entry point"""
import sys

from focli import FoliPrint


def main():
    lines_s = sys.argv[1:]
    lines = []
    for l in lines_s:
        try:
            lines.append(int(l))
        except ValueError:
            print("Error: {} is not a valid stop number".format(l))
            return 1
    f_print = FoliPrint(lines)
    f_print.print_lines()
    return 0

if __name__ == '__main__':
    sys.exit(main())
