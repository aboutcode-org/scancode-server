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