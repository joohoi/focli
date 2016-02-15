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
    def __init__(self, name):
        self.width = 24
        self.rows = []
        self.term = Terminal()
        name = self.normalize(unescape(name), self.width)
        self.tpl_head = [
            "+--------+--------+--------+",
            "| {headline} |".format(headline=name),
            "+--------+--------+--------+",
            "|  {ti}  |  {li}  |  {di}  |".format(
                ti=self.term.bold("Time"),
                li=self.term.bold("Line"),
                di=self.term.bold("Diff")),
            "+--------+--------+--------+"]
        self.tpl_line = "| {time} | {line} | {diff} |"
        self.tpl_endl = "+--------+--------+--------+"

    def add_row(self, ftime, line, diff):
        if int(diff) == 0:
            ftime = self.term.green(self.normalize(ftime))
            diff = self.term.green(self.normalize(diff))
        else:
            ftime = self.term.red(self.normalize(ftime))
            diff = self.term.red(self.normalize(diff))
        line = self.term.bold(self.normalize(line))
        row = self.tpl_line.format(
            time=ftime,
            line=line,
            diff=diff)
        self.rows.append(row)

    def get_row(self, rownr):
        if rownr < len(self.tpl_head):
            return self.tpl_head[rownr]
        elif rownr < (len(self.tpl_head)+len(self.rows)):
            return self.rows[rownr-len(self.tpl_head)]
        elif rownr == (len(self.tpl_head)+len(self.rows)):
            return self.tpl_endl
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
