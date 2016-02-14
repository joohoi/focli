=====
focli
=====

CLI client to timetables for a city of Turku (Föli) bus stop(s), including time differences to prescheduled times for lines that provide realtime data.

.. image:: https://cloud.githubusercontent.com/assets/5235109/13033364/dbae4d6a-d31c-11e5-8829-09c7fbc8086e.gif




Installation
============

Install focli by running::

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



Features
========

* Displays realtime data if available for the stop
* Shows the schedule for the current hour (see TODO section for more)
* Color coding for delayed lines
* Displays as many stop schedules side by side as the active terminal can fit
* Add / delete / list bookmarks

TODO
====

* Configurable the time range to search for




