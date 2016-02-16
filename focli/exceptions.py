""" focli exceptions """


class FoliException(Exception):
    """ Base exception """
    def __init__(self, message):
        self.message = message


class FoliStopNameException(FoliException):
    """ Stop name error """


class FoliServerException(FoliException):
    """ Stop name error """

class FoliParseDataError(FoliException):
    """ Error parsing data """
