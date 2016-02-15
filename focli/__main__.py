#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

"""Command entry point"""

import sys

from focli import focli


def main():
    return focli.main()

if __name__ == '__main__':
    sys.exit(main())
