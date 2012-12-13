Setup with virtualenv under Debian
==================================

The following procedure has been tested with a clean '''64bit Debian Wheezy''' server: it should work ''as is'' under Squeeze (or perhaps even Lenny) and with 32bit architectures. The same procedue should apply as is with recent Ubuntu servers, and with minimal changes for other Linux distributions (mainly, the names and the procedure to install the server environment).

Setup the server environment
----------------------------

The following is the minimal set of packages needed on the server (with older Debian releases you can use the system PostgreSQL, there are no critical dependencies from 9.1):

    # apt-get install postgresql-9.1 python-all-dev python-setuptools \
                postgresql-server-dev-all libxslt1-dev \
                libxml2-dev make gcc g++ subversion python-virtualenv

Then as user ''postgres'' create the database, a user and setup a password (in the following we assume that the database and th user are called '''dashboard''', and we setup a silly ''''mypassword'''').

    # su - postgres 
    $ createuser --no-createdb --no-createrole --no-superuser --pwprompt dashboard
    Enter password for new role: mypassword
    Enter it again: mypassword
    $ createdb --owner=dashboard dashboard

See also:

* [http://www.postgresql.org/](http://www.postgresql.org/)
* [http://wiki.debian.org/PostgreSql](http://wiki.debian.org/PostgreSql)
* [https://help.ubuntu.com/community/PostgreSQL](https://help.ubuntu.com/community/PostgreSQL)

Setup the application environment
---------------------------------

First of all checkout the code, setup the virtual environment and activate it:

    $ git clone https://github.com/getpenelope/getpenelope.buildout.git
    $ virtualenv --python=python2.6 --no-site-package getpenelope.buildout
    $ cd getpenelope.buildout 
    $ . ./bin/activate
    $ python bootstrap.py -v 1.5.2 -c development.cfg

Modify or extends development.cfg with

    [dashboard] 
    db_string = postgresql://dashboard:mypassword@localhost:5432/dashboard

somewhere in that file and then run.

    $ bin/buildout -c development.cfg 

Running Penelope
----------------

You can first populate the system with some dummy data. The first option is to use ''populate_with_dummies'':

    $ ./bin/populate_with_dummies etc/development.ini

that will create a lot of dummy data (users, projects, customers, time entries, etcetera), while ''populate_penelope'':

    $ ./bin/populate_penelope etc/development.ini

with create only minimal data (use just one of them, if you really want).

Last you can go straightforwardly to the server login page running:

    $ ./bin/dashboard serve etc/development.ini

and logging in with:

    john@example.com/john@example.com  (Administrator)
    customer@example.com/customer@example.com (Customer)

or:

    admin@example.com/admin@example.com (Administrator)

Enjoy.

[![githalytics.com alpha](https://cruel-carlota.pagodabox.com/ce6556d8087af23a69cd0a7c990355c7 "githalytics.com")](http://githalytics.com/getpenelope/getpenelope.buildout)
