.. scancode server documentation master file, created by
   sphinx-quickstart on Tue Aug 22 13:06:48 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to scancode server's documentation!
===========================================

This is the documentation for the scan code server. A project which uses ScanCode as a library in a web and REST API application that allows you to scan code on demand by entering a URL and then store the scan results.

Copyright and License
===========================================

The project’s idea belongs to AboutCode and Philippe Ombredanne and it has been developed under Google summer of code 2017 by Raju Koushik and Ranvir Singh.

It is distributed under an open-source Apache License. Please find LICENSE in top level directory for details.

Installation
===========================================

Note: these instructions are tested only for now only on Debian and
Debian derivative Linux distros.

The ScanCode server is designed to run on POSIX (Linux, Mac, etc).
Windows is not tested and not supported for now.


1. System requirements

- Get Python 2.7.x installed first and pip (pip is included in the
  Python.org downloads since Python 2.7.9)

- Install PosgreSQL 9.5.x of later. (9.6 preferred)
  On Debian distros use: `sudo apt-get install postgresql-9.5-dev`

- Install extra utilities if needed: `sudo apt-get install wget build-essential redis-server`


2. Configure a local test database

- Create a local test `scancode` database user. Use `scancode` as password when prompted
  (otherwise use any password and update your settings locally).
  `sudo -u postgres createuser --no-createrole --no-superuser --login --inherit --createdb --pwprompt scancode`

- Create a local test`scancode` database.
  `createdb --encoding=utf-8 --owner=scancode  --user=scancode --password --host=localhost --port=5432 scancode`

3. Install and configure the ScanCode server

- Get a clone or archive for the code from https://github.com/nexB/scancode-server

- `cd` to the cloned or extracted archive directory

- Create a local virtual environment with `virtualenv .` and activate this with `source bin/activate`
- Install the required dependencies with `pip install -r requirements.txt`
- Create the db schema `python manage.py migrate`
- Create a local admin user with `python manage.py createsuperuser`
- Run a local test server with `python manage.py runserver`
- Run `redis-server`
- Run a local celery worker in a separate shell with `celery -A scanapp worker -l info`
- Fire a browser at http://127.0.0.1:8000/admin/ to access the adminFire a browser at http://127.0.0.1:8000/admin/ to access the admin


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro
   about
   installation
   plan



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
