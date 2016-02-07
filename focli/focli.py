import datetime
import json

import requests


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
