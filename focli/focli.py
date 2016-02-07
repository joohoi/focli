class FoliLine:
    def __init__(self, name, ltime, realtime=False,
                 cancelled=False, ontime=True, timediff=0):
        self.name = name.split(" ")[-1]
        self.time = ltime
        self.realtime = realtime
        self.cancelled = cancelled
        self.ontime = ontime
        self.timediff = timediff
