from __future__ import absolute_import

import pytest
import sys
import os

if sys.version_info[0] == 2:
    import __builtin__ as builtins
    import mock
else:
    import builtins
    import unittest.mock as mock

cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, cwd + "/../../")
from focli import foline
from focli import exceptions
from freezegun import freeze_time


@freeze_time("2016-02-16 13:22:01")
@pytest.fixture
def foliprint(monkeypatch):
    def mock_req_get(*args, **kwargs):
        mock_requests_get = mock.Mock()
        mock_requests_get.status_code = 200
        dloc = os.path.dirname(os.path.abspath(__file__)) + "/data/focli.txt"
        with open(dloc, 'r') as fh:
            mock_requests_get.text = fh.read()
        return mock_requests_get
    monkeypatch.setattr('requests.get', mock_req_get)
    monkeypatch.setattr('blessings.Terminal.width', 100)
    return foline.FoliPrint(['T34', '157'])


@pytest.fixture
def foliprint_named(monkeypatch):
    def mock_run(*args, **kwargs):
        return
    monkeypatch.setattr('focli.foline.FoliStop.run', mock_run)
    return foline.FoliPrint(named_stops={
        'T34': 'Some', '157': 'Thing'})


class TestFocli:
    def test_init(self, monkeypatch, foliprint, foliprint_named):
        assert len(foliprint.stops) == 2
        assert len(foliprint_named.stops) == 2

    def test_fits_line(self, monkeypatch, foliprint):
        monkeypatch.setattr('blessings.Terminal.width', 100)
        assert foliprint.fits_line() == 3

    @freeze_time("2016-02-16 13:22:01")
    def test_get_tables(self, monkeypatch, foliprint):
        assert len(foliprint.get_tables()) == 2

    @freeze_time("2016-02-16 13:22:01")
    def test_run(self, monkeypatch, foliprint):
        assert len(foliprint.stops[0].journeys) == 30

    def test_bad_format(self):
        with pytest.raises(exceptions.FoliStopNameException):
            foline.FoliPrint(['nonexistent'])

    def test_breaking_request(self, monkeypatch):
        def mock_req_get(*args, **kwargs):
            mock_requests_get = mock.Mock()
            mock_requests_get.status_code = 404
            return mock_requests_get
        monkeypatch.setattr('requests.get', mock_req_get)
        with pytest.raises(exceptions.FoliServerException):
            foline.FoliPrint(['157'])

    def test_broken_json(self, monkeypatch):
        def mock_req_get(*args, **kwargs):
            mock_requests_get = mock.Mock()
            mock_requests_get.status_code = 200
            dloc = os.path.dirname(
                os.path.abspath(__file__)) + "/data/focli_broken.txt"
            with open(dloc, 'r') as fh:
                mock_requests_get.text = fh.read()
            return mock_requests_get
        monkeypatch.setattr('requests.get', mock_req_get)
        with pytest.raises(exceptions.FoliParseDataError):
            foline.FoliPrint(['T34'])
