""" focli exceptions """


class FoliStopNameException(Exception):
    """ Stop name error """
    def __init__(self, message):
        self.message = message


class FoliServerException(Exception):
    """ Stop name error """
    def __init__(self, message):
        self.message = message
