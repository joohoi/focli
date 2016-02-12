from blessings import Terminal


class FoliTable:
    def __init__(self, name):
        self.rows = []
        self.term = Terminal()
        name = self.normalize(name, 24)
        self.tpl_head = [
            "+--------+--------+--------+",
            "| {normalized_header_line} |".format({'normalized_header_line':
                                                   name}),
            "+--------+--------+--------+",
            "|  {ti}  |  {li}  |  {di}  |".format({'ti':
                                                   self.term.bold("Time"),
                                                   'li':
                                                   self.term.bold("Line"),
                                                   'di':
                                                   self.term.bold("Diff")}),
            "+--------+--------+--------+"]
        self.tpl_line = "| {time} | {line} | {diff} |"
        self.tpl_endl = "+--------+--------+--------+"

    def add_row(self, ftime, line, diff):
        if diff == 0:
            ftime = self.term.green(self.normalize(ftime))
            diff = self.term.green(self.normalize(diff))
        else:
            ftime = self.term.red(self.normalize(ftime))
            diff = self.term.red(self.normalize(diff))
        line = self.term.bold(self.normalize(line))
        row = self.tpl_line.format({
            'time': ftime,
            'line': line,
            'diff': diff})
        self.rows.append(row)

    def normalize(self, nstr, length=6):
        if len(nstr) > length:
            nstr = nstr[0:length-1]
        return nstr.center(length, " ")
