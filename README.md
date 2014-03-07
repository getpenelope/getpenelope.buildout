[![Build Status](https://travis-ci.org/getpenelope/getpenelope.buildout.png)](https://travis-ci.org/getpenelope/getpenelope.buildout)
[![Selenium Test Status](https://saucelabs.com/browser-matrix/amleczko.svg)](https://saucelabs.com/u/amleczko)

Setup with virtualenv under Debian
==================================

The following procedure has been tested with a clean ''64bit Debian Wheezy'' server: it should work ''as is'' under Squeeze (or perhaps even Lenny) and with 32bit architectures. The same procedue should also apply to recent Ubuntu servers. It should also work with minimal changes for other Linux distributions (namely, the package names and the procedures to install the server environment).

Setup the server environment
----------------------------

The following is the minimal set of packages needed on the server (with older Debian releases you can use the PostgreSQL provided by the system, it is not important to have the 9.1 release):

    # apt-get install postgresql-9.1 python-all-dev python-setuptools \
                postgresql-server-dev-all libxslt1-dev \
                libxml2-dev make gcc g++ subversion python-virtualenv

Next, as user ''postgres'' create the database, a user and setup a password (in the following we assume that the database and the user are called ''dashboard'', and we setup a silly ''mypassword''):

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
    $ python bootstrap.py -v 2.1.0 -c development.cfg

Modify or extend development.cfg adding the following stanza:

    [dashboard] 
    db_string = postgresql://dashboard:mypassword@localhost:5432/dashboard

somewhere in the file, and then run:

    $ bin/buildout -c development.cfg 

Running Penelope
----------------

You can populate the system with some dummy data. The first option is to use ''populate_with_dummies'':

    $ ./bin/populate_with_dummies etc/development.ini

that will create a lot of dummy entries (users, projects, customers, time entries, etcetera), the second option is to use ''populate_penelope'':

    $ ./bin/populate_penelope etc/development.ini

which will create just a minimal dataset (use only one of them, not both, and only if you want to ''pollute'' penelope with mocks).

Now you can run penelope:

    $ ./bin/dashboard serve etc/development.ini

and log in as:

    john@example.com/john@example.com  (Administrator)
    customer@example.com/customer@example.com (Customer)

or (requires `./bin/populate_penelope etc/development.ini` to be run in advance):

    admin@example.com/admin@example.com (Administrator)

Enjoy.


[![githalytics.com alpha](https://cruel-carlota.pagodabox.com/ce6556d8087af23a69cd0a7c990355c7 "githalytics.com")](http://githalytics.com/getpenelope/getpenelope.buildout)
