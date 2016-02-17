#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

from blessings import Terminal

try:
    from html import unescape  # python 3.4+
except ImportError:
    try:
        from html.parser import HTMLParser  # python 3.x (<3.4)
    except ImportError:
        from HTMLParser import HTMLParser  # python 2.x
    unescape = HTMLParser().unescape


class FoliTable:
    def __init__(self, name, verbose=False):
        self.verbose = verbose
        self.width = 28
        self.width_verbose = 48
        self.rows = []
        self.term = Terminal()
        if verbose:
            name = self.normalize(unescape(name), self.width_verbose)
        else:
            name = self.normalize(unescape(name), self.width)

        self.tpl_head_verbose = [
            "+------------+--------+--------+-------------------+",
            "| {headline} |".format(headline=name),
            "+------------+--------+--------+-------------------+",
            "|    {ti}    |  {li}  |  {di}  | {destination} |".format(
                ti=self.term.bold("Time"),
                li=self.term.bold("Line"),
                di=self.term.bold("Diff"),
                destination=self.term.bold(
                    self.normalize("Destination", 17))),
            "+------------+--------+--------+-------------------+"]
        self.tpl_line_verbose = "| {time} | {line} | {diff} | {dest} |"
        self.tpl_endl_verbose = ("+------------+--------+--------"
                                 "+-------------------+")
        self.tpl_head = [
            "+------------+--------+--------+",
            "| {headline} |".format(headline=name),
            "+------------+--------+--------+",
            "|    {ti}    |  {li}  |  {di}  |".format(
                ti=self.term.bold("Time"),
                li=self.term.bold("Line"),
                di=self.term.bold("Diff")),
            "+------------+--------+--------+"]
        self.tpl_line = "| {time} | {line} | {diff} |"
        self.tpl_endl = "+------------+--------+--------+"

    def add_row(self, ftime, line, diff, timediff, dest=None):
        if timediff <= 0:
            ftime = self.term.green(self.normalize(ftime, 10))
            diff = self.term.green(self.normalize(diff))
        else:
            ftime = self.term.red(self.normalize(ftime, 10))
            diff = self.term.red(self.normalize(diff))
        line = self.term.bold(self.normalize(line))
        if self.verbose:
            dest = self.normalize(dest, 17)
            row = self.tpl_line_verbose.format(
                time=ftime,
                line=line,
                diff=diff,
                dest=dest)
        else:
            row = self.tpl_line.format(
                time=ftime,
                line=line,
                diff=diff)
        self.rows.append(row)

    def get_row(self, rownr):
        if rownr < len(self.tpl_head):
            if self.verbose:
                return self.tpl_head_verbose[rownr]
            else:
                return self.tpl_head[rownr]
        elif rownr < (len(self.tpl_head)+len(self.rows)):
            return self.rows[rownr-len(self.tpl_head)]
        elif rownr == (len(self.tpl_head)+len(self.rows)):
            if self.verbose:
                return self.tpl_endl_verbose
            else:
                return self.tpl_endl
        else:
            if self.verbose:
                return " "*len(self.tpl_endl_verbose)
            else:
                return " "*len(self.tpl_endl)

    def num_lines(self):
        return len(self.tpl_head)+len(self.rows)+1

    def normalize(self, nstr, length=6):
        try:
            nstr = unicode(nstr)
            encode = True
        except NameError:
            if not isinstance(nstr, str):
                nstr = str(nstr)
            encode = False
        if len(nstr) > length:
            nstr = nstr[0:length-1]
        nstr = nstr.center(length, " ")
        if encode:
            return nstr.encode('utf-8')
        return nstr
