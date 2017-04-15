API
===
[ListJuggler has a RESTFUL API](https://docs.google.com/document/d/1WkS3qfwVDd_OqK3egC9EUZjFcmgjdUyH9ByAgiqrIvo/edit?usp=sharing) for getting data list and tournament data, and also for creating new tournaments and lists. For example:

- http://lists.starwarsclubhouse.com/api/v1/tournaments
- http://lists.starwarsclubhouse.com/api/v1/tournament/1

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

Initializing and Browsing the Database
=========================

    To familiarize yourself with the database model, please have a look at dbs/database_model.png 

    To create the database, from shell run
        mysql < dbs/prod.sql

    The file dbs/prod.sql is updated hourly into github from the pythonanywhere server.

    This program uses SQL-Alchemy object bindings and expression building for all its sql management. The schema itself is managed manually (it should be using Flask-Migrate).
    

Running the App
===============

In development mode, so you can see meaningful error messages:

    python xwlists.py dev
        
Here are the two environment variables the program expects and some sample values:

    DYLD_LIBRARY_PATH /usr/local/mysql/lib
    LOCAL_DB_URL mysql://root...

The url string for your MySQL database will looking something like mysql://$USER_NAME:$PASSPORT@localhost/sozin$lists

Here are the optional environment variables.

    DO_MAIL set to 1 if you want email
    MAIL_USERNAME if doing mail, your google mail username
    MAIL_PASSWORD and your google mail password
    ADMIN_EMAIL an email address where you'd like to receive your emails
    CHALLONGE_API_KEY if you are using the challonge import functions for vassal league, contact me
    
Note, if you get the following error on application startup:

  ImportError: dlopen(/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/_mysql.so, 2): Library not loaded: libmysqlclient.18.dylib
  Referenced from: /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/_mysql.so
  Reason: image not found

You'll need to set this env variable:

    DYLD_LIBRARY_PATH=/usr/local/mysql/lib/
