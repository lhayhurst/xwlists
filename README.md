Installing
==========

Using a [Virtualenv](https://virtualenv.pypa.io/en/latest/) is recommended.

This assumes MySQL as a backend, so you'll need `mysql_config` installed.
Consult your OS documentation for how to do that.  If you're using a
different SQL backend, modify `requirements.txt` to use the appropriate
Python bindings.

    virtualenv ~/venv/xwlists
    . ~/venv/xwlists/bin/activate
    pip install -r requirements.txt

Initializing the Database
=========================

    mysql < dbs/prod.sql

Running the App
===============

In development mode, so you can see meaningful error messages:

    LOCAL_DB_URL='mysql://localhost/sozin$lists' python xwlists.py dev
