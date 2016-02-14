import pytest
import json
import sys
import os
import mock

if sys.version_info.major == 2:
    import __builtin__ as builtins
else:
    import builtins

cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, cwd + "/../")
import focli
# from unittest.mock import Mock


class TestFocli:
    def setup(self):
        print("setup class")

    def test_main_add_bookmark(self, monkeypatch):
        monkeypatch.setattr('sys.argv',
                            ['focli', '-a', '157'])

        def mock_return(a):
            return True

        monkeypatch.setattr('focli.focli.add_bookmark',
                            mock_return)
        assert focli.focli.main() is True

    def test_main_del_bookmark(self, monkeypatch):
        monkeypatch.setattr('sys.argv',
                            ['focli', '-d', '157'])

        def mock_return(a):
            return True

        monkeypatch.setattr('focli.focli.del_bookmark',
                            mock_return)
        assert focli.focli.main() is True

    def test_main_list_bookmarks(self, monkeypatch):
        monkeypatch.setattr('sys.argv',
                            ['focli', '-l'])

        def mock_return():
            return True

        monkeypatch.setattr('focli.focli.list_bookmarks',
                            mock_return)
        assert focli.focli.main() is True

    def test_main_show_stops(self, monkeypatch):
        monkeypatch.setattr('sys.argv',
                            ['focli', '157', '123', '420'])

        def mock_return(a):
            return True

        monkeypatch.setattr('focli.focli.show_stops',
                            mock_return)
        assert focli.focli.main() is True

    def test_read_config(self, monkeypatch):
        fcontent = '{"123":"abc"}'
        with mock.patch.object(builtins, 'open',
                               mock.mock_open(read_data=fcontent)):
            assert focli.focli.read_config() == json.loads(fcontent)

    def test_write_config(self, monkeypatch):
        fcontent = json.loads('{"123":"abc"}')
        mo = mock.mock_open()
        with mock.patch.object(builtins, 'open', mo):
            focli.focli.write_config(fcontent)
        mo.assert_called_once_with(
            os.path.expanduser(focli.focli.CONFIG_PATH), 'w')
