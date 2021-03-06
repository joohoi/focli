#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import argparse
import json
import os

from focli.foline import FoliPrint
from focli import exceptions

CONFIG_PATH = "~/.focli"


def main():
    parser = CliParser()
    ns = parser.parse_argv()
    try:
        if ns.add:
            ret = add_bookmark(ns)
        elif ns.delete:
            ret = del_bookmark(ns)
        elif ns.list_bookmarks:
            ret = list_bookmarks()
        else:
            ret = show_stops(ns)
    except exceptions.FoliStopNameException as e:
        print(str(e.message))
        ret = 1
    if ret != 0:
        parser.print_help()
    return ret


def read_config():
    try:
        path = os.path.expanduser(CONFIG_PATH)
        with open(path, 'r') as fh:
            return json.load(fh)
    except IOError:
        return dict()


def write_config(config):
    try:
        path = os.path.expanduser(CONFIG_PATH)
        with open(path, 'w') as fh:
            json.dump(config, fh)
    except TypeError:
        raise


def add_bookmark(ns):
    if len(ns.stopnumber):
        config = read_config()
        config[ns.stopnumber[0]] = ns.stopname
        write_config(config)
        print("Bookmark for stop {0} added.".format(ns.stopnumber[0]))
        return 0
    else:
        print("Please provide stop number to bookmark")
        return 1


def del_bookmark(ns):
    if len(ns.stopnumber):
        config = read_config()
        if str(ns.stopnumber[0]) in config.keys():
            config.pop(str(ns.stopnumber[0]), None)
            write_config(config)
            print("Bookmark for stop {0} deleted.".format(ns.stopnumber[0]))
            return 0
        print("No bookmark for stop {0}.".format(ns.stopnumber[0]))
        return 1
    else:
        print("Please provide stop number to remove.")
        return 1


def list_bookmarks():
    config = read_config()
    if config:
        print("Saved bookmarks:")
        for bm in config.keys():
            print("{0} - {1}".format(bm, config[bm]))
    return 0


def show_stops(ns):
    try:
        if len(ns.stopnumber):
            f_print = FoliPrint(ns.stopnumber, verbose=ns.verbose)
            f_print.print_lines()
            return 0
        else:
            config = read_config()
            if config:
                f_print = FoliPrint(named_stops=config, verbose=ns.verbose)
                f_print.print_lines()
                return 0
            else:
                return 1
    except exceptions.FoliException as e:
        print(e.message)
        return 1


class CliParser:
    def parse_argv(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-a", dest="add", action="store_true",
                                 default=False, help="Add line to bookmarks")
        self.parser.add_argument("-d", dest="delete", action="store_true",
                                 default=False,
                                 help="Remove line from bookmarks")
        self.parser.add_argument("-v", dest="verbose",
                                 action="store_true",
                                 default=False,
                                 help="Verbose output (show destination)")
        self.parser.add_argument("-l", dest="list_bookmarks",
                                 action="store_true",
                                 default=False,
                                 help="List saved bookmarks")
        self.parser.add_argument("-n", dest="stopname", action="store",
                                 help="Custom name for the stop to bookmark")
        self.parser.add_argument("stopnumber", nargs="*",
                                 help="Stop number to show / add / delete")
        return self.parser.parse_args()

    def print_help(self):
        self.parser.print_help()
