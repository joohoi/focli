#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime
import json
import math

import requests
from six.moves import range
from focli.folitable import FoliTable
from focli import exceptions
from blessings import Terminal


class FoliPrint:
    def __init__(self, flines=[], named_stops=dict(), verbose=False):
        self.verbose = verbose
        self.stops = []
        if flines:
            for l in flines:
                new_stop = FoliStop(l)
                new_stop.run()
                self.stops.append(new_stop)
        elif named_stops:
            for l in named_stops.keys():
                new_stop = FoliStop(l)
                new_stop.stop_name = named_stops[l]
                new_stop.run()
                self.stops.append(new_stop)

    def print_lines(self):
        tables_handled = 0
        timetables = self.get_tables()
        t_per_line = self.fits_line()
        while len(timetables) > tables_handled:
            if (len(timetables)-tables_handled) < t_per_line:
                handle = len(timetables)-tables_handled
            else:
                handle = t_per_line
            p_list = timetables[int(tables_handled):int(tables_handled+handle)]
            height = max(h.num_lines() for h in p_list)
            for i in range(height):
                line = " ".join([t.get_row(i) for t in p_list])
                print(line)
            tables_handled += handle

    def fits_line(self):
        term = Terminal()
        try:
            if self.verbose:
                retwidth = math.floor(term.width/53)
            else:
                retwidth = math.floor(term.width/33)
        except TypeError:
            raise exceptions.FoliTerminalException(
                "Could not determine terminal size")
        return retwidth

    def get_tables(self):
        tables = []
        for s in self.stops:
            t = FoliTable(s.stop_name, self.verbose)
            journeys = self.filter_list(s.journeys)
            for jo in journeys:
                f_timediff = jo.timediff-jo.time
                line_time = jo.time + f_timediff
                f_time = "{0:02d}:{1:02d}:{2:02d}".format(line_time.hour,
                                                          line_time.minute,
                                                          line_time.second)
                if f_timediff.days < 0:
                    t_diff_secs = f_timediff.seconds - 86400
                else:
                    t_diff_secs = f_timediff.seconds
                t.add_row(f_time, jo.name, jo.timediff_min_sec(),
                          t_diff_secs, jo.dest)
            tables.append(t)
        return tables

    def filter_list(self, flist, start_min=-5, end_min=60):
        now = datetime.datetime.now()
        start_delta = datetime.timedelta(minutes=start_min)
        end_delta = datetime.timedelta(minutes=end_min)
        start = now + start_delta
        end = now + end_delta
        return [f for f in flist if f.time > start and f.time < end]


class FoliLine:
    def __init__(self, name, ltime, realtime=False,
                 cancelled=False, ontime=True, timediff=0,
                 dest=None):
        if timediff == 0:
            timediff = ltime
        self.name = name
        self.time = ltime
        self.realtime = realtime
        self.cancelled = cancelled
        self.ontime = ontime
        self.timediff = timediff
        self.dest = dest

    def timediff_min_sec(self):
        """ Get timediff in format 1m48s """
        tdiff = self.timediff - self.time
        if tdiff.days < 0:
            diff_secs = tdiff.seconds - 86400
        else:
            diff_secs = tdiff.seconds
        minutes, seconds = divmod(diff_secs, 60)
        if minutes == 0 and seconds == 0:
            return "-"
        if minutes:
            return "{0}m{1:02d}s".format(minutes, seconds)
        return "{0:02d}s".format(seconds)


class FoliStop:
    def __init__(self, stopnr="157"):
        self.stop_name = ""
        self.stopnr = self.normalize_stopnr(stopnr)
        self.url = ("http://data-western.foli.fi/stops/{0}".format(
            self.stopnr))

    def run(self):
        """ Perform request, and populate journey data table """
        try:
            data = json.loads(self.get_data())
        except ValueError:
            raise exceptions.FoliParseDataException(
                "Got bad data from url: {0}".format(self.url))
        if not self.stop_name:
            self.stop_name = self.stopnr
        self.journeys = []
        try:
            for jo in data['result']:
                jo_time = jo['aimeddeparturetime']
                line_time = datetime.datetime.fromtimestamp(jo_time)
                destination = jo['destinationdisplay']
                new_line = FoliLine(jo['lineref'], line_time,
                                    realtime=True,
                                    dest=destination)
                if 'delay' in jo.keys():
                    new_line.ontime = False
                    new_line.timediff = datetime.datetime.fromtimestamp(
                        jo['expecteddeparturetime'])
                self.journeys.append(new_line)

        except KeyError:
            raise exceptions.FoliParseDataError("Error while parsing data"
                                                " for line {0}".format(
                                                    self.stopnr))

    def normalize_stopnr(self, nr):
        """ Simple validation and normalization of stop nr,
            raise FoliStopNameException if b0rked
        """
        try:
            if nr[0].lower() == "t":
                retnr = "T{0}".format(int(nr[1:]))
            else:
                retnr = "{0}".format(int(nr))
        except ValueError:
            raise exceptions.FoliStopNameException(
                "{0} is not a valid stop id".format(nr))
        return retnr

    def get_data(self):
        req = requests.get(self.url)
        if req.status_code == 200:
            return req.text
        elif req.status_code == 404:
            raise exceptions.FoliServerException(
                "Server response was: 404 - Not Found, '{0}'"
                " doesn't seem like a valid stop id".format(self.stopnr))
        else:
            raise exceptions.FoliServerException(
                "Server responded with status {0}".format(req.status_code))
