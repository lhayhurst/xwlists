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

Note, if you get the following error on application startup:

  ImportError: dlopen(/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/_mysql.so, 2): Library not loaded: libmysqlclient.18.dylib
  Referenced from: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/_mysql.so
  Reason: image not found

You'll need to set this env variable:

    DYLD_LIBRARY_PATH=/usr/local/mysql/lib/