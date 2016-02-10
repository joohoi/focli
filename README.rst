=====
focli
=====

CLI interface to quickly see timetables for a Föli bus stop(s), including time differences to "original" schedules for lines that provide realtime data.


Installation
============

Install focli by running::

    git clone https://github.com/joohoi/focli.git
    cd focli
    python setup.py install


Usage
=====

Timetable for single bus stop::

    $ focli 157
    focli 157
    +-------+------+------------+
    |  Time | Line | Difference |
    +-------+------+------------+
    | 19:22 |  30  |     0      |
    | 19:52 |  30  |     0      |
    +-------+------+------------+



Or timetables for multiple stops::

    focli 157 122


Features
========

* Displays realtime data if available for the stop
* Shows the schedule for the current hour (see TODO section for more)

TODO
====

* Configure the time range to search for
* Bus stop bookmark handling
* Add colors to terminal output
* Display multiple stop schedules side by side, if terminal width permits

