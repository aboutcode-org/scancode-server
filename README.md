#### This repo is no longer maintained. Visit https://github.com/nexB/scancode.io/ instead

----------------------------------

# scancode-server

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/59da2f264a5947209f05303cfbe8a223)](https://www.codacy.com/app/RajuKoushik/scancode-server?utm_source=github.com&utm_medium=referral&utm_content=nexB/scancode-server&utm_campaign=badger)


This is a server for the ScanCode toolkit(https://github.com/nexB/scancode-toolkit).

This is a work-in-progress...

The goal is to provide a minimal web UI and a comprehensive REST API to:

 - scan code for origin, licensing and dependencies for a remote URL, a
   remote repo or a file upload.
 - store scan results and eventually offer a central storage place for
   ScanCode scans even when done using the ScanCode CLI app.
 - offer some Travis and/or Github integration to scan on commit with
   webhooks.
 - eventually offer extra goodies such as scan based on a received tweet
   of similar IRC or IM integration.


### Installation

Note: these instructions are tested only for now only on Debian and
Debian derivative Linux distros.

The ScanCode server is designed to run on POSIX (Linux, Mac, etc).
Windows is not tested and not supported for now.


1. System requirements

- Get Python 2.7.x installed first and pip (pip is included in the
  Python.org downloads since Python 2.7.9)

- Install PostgreSQL 9.5.x of later. (9.6 preferred) 
  On Debian distros use: `sudo apt-get install postgresql-9.5`

- Install extra utilities if needed: `sudo apt-get install wget build-essential redis-server python-dev`


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
- Fire a browser at http://127.0.0.1:8000/admin/ to access the admin


### Extras

-  If virtualenv is not available use these commands first to install it:
     - `mkdir -p tmp && cd tmp`
     - `wget https://github.com/pypa/virtualenv/archive/15.1.0.tar.gz`
     - `tar -xf 15.1.0.tar.gz`
     - `cd ..`
     - `python2 tmp/virtualenv-15.1.0/virtualenv.py .`
     - `source bin/activate`

