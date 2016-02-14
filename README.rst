=====
focli
=====

Bookmarkable CLI client to timetables for a city of Turku (Föli) bus stop(s), including time differences to prescheduled times for lines that provide realtime data.

Bookmark once, quickly check all the stop schedules relevant to you any time you need them with only one command. 

.. image:: https://cloud.githubusercontent.com/assets/5235109/13033364/dbae4d6a-d31c-11e5-8829-09c7fbc8086e.gif




Installation
============

Install via pip for current user (needs ~/.local/bin on $PATH)::

    pip install --user focli
    
Globally via pip::

    sudo pip install focli

Or::

    git clone https://github.com/joohoi/focli.git
    cd focli
    python setup.py install


Usage
=====

Client parameters::

    usage: focli [-h] [-a] [-d] [-l] [-n STOPNAME] [stopnumber [stopnumber ...]]
    
    positional arguments:
      stopnumber   Stop number to show / add / delete
    
    optional arguments:
      -h, --help   show this help message and exit
      -a           Add line to bookmarks
      -d           Remove line from bookmarks
      -l           List saved bookmarks
      -n STOPNAME  Custom name for the stop to bookmark


Eg: add two bus stops to list, the one you use to get to work from home, and other the other way around::

    focli -n "Home" -a 157
    focli -n "Work" -a T34
    
after bookmarking, you can get the schedules for both of the stops simultanously every time you run::

    focli
    
without arguments.


Features
========

* Displays realtime data if available for the stop
* Shows the schedule for the current hour (see TODO section for more)
* Color coding for delayed lines
* Displays as many stop schedules side by side as the active terminal can fit
* Add / delete / list bookmarks

TODO
====

* Configurable time range to search for
