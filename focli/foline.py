import datetime
import json
import math

import requests
from six.moves import range
from folitable import FoliTable
from blessings import Terminal


class FoliPrint:
    def __init__(self, flines=[], named_stops=dict()):
        self.stops = []
        if flines:
            for l in flines:
                new_stop = FoliStop(l)
                new_stop.run()
                self.stops.append(new_stop)
        elif named_stops:
            for l in named_stops.keys():
                new_stop = FoliStop(int(l))
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
        return math.floor(term.width/29)

    def get_tables(self):
        tables = []
        for s in self.stops:
            t = FoliTable(s.stop_name)
            journeys = self.filter_list(s.journeys)
            for jo in journeys:
                f_timediff = datetime.timedelta(minutes=int(jo.timediff))
                line_time = jo.time + f_timediff
                f_time = "{0:02d}:{1:02d}".format(line_time.hour,
                                                  line_time.minute)
                t.add_row(f_time, jo.name, jo.timediff)
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
                 cancelled=False, ontime=True, timediff=0):
        self.name = name.split(" ")[-1]
        self.time = ltime
        self.realtime = realtime
        self.cancelled = cancelled
        self.ontime = ontime
        self.timediff = timediff


class FoliStop:
    def __init__(self, stopnr=157):
        self.stop_name = ""
        self.stopnr = stopnr
        self.url_base = "http://reittiopas.foli.fi/bin/stboard.exe/3finny?"
        self.attrs = {'dateBegin': self.get_datestring(),
                      'dateEnd': self.get_datestring(),
                      'input': self.format_stopnr(stopnr),
                      'selectDate': 'period',
                      'start': '1',
                      'timeSlots': '1',
                      'boardType': 'dep',
                      'tpl': 'stationboardResult2json'}
        self.url = self.get_url()

    def run(self):
        today = datetime.date.today()
        data = json.loads(self.get_data())
        if not self.stop_name:
            self.stop_name = data['query']['station']['name']
        self.journeys = []
        for jo in data['journeys']:
            try:
                jo_time = jo['time'].split(":")
                line_time = datetime.datetime(today.year, today.month,
                                              today.day, int(jo_time[0]),
                                              int(jo_time[1]))

                new_line = FoliLine(jo['line']['name'], line_time,
                                    realtime=jo['realTime']['hasRealTime'],
                                    cancelled=jo['realTime']['isCanceled'])
                if 'isOnTime' in jo['realTime'].keys():
                    new_line.ontime = jo['realTime']['isOnTime']
                    new_line.timediff = jo['realTime']['delay']
                self.journeys.append(new_line)

            except KeyError:
                print("Error while parsing line")

    def get_querystring(self, qa):
        ql = []
        for i in qa.keys():
            ql.append("{}={}".format(i, qa[i]))
        return "&".join(ql)

    def format_stopnr(self, nr):
        return "0009{0:05d}".format(nr)

    def get_datestring(self):
        today = datetime.date.today()
        return "{0:02d}.{1:02d}.{2:04d}".format(today.day,
                                                today.month,
                                                today.year)

    def get_url(self):
        return self.url_base+self.get_querystring(self.attrs)

    def get_data(self):
        req = requests.get(self.url)
        if req.status_code == 200:
            return req.text
        return None
