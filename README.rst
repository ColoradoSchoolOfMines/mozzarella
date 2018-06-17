Mozzarella
==========
A Collaborative Web System for Student Computing Clubs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Mozzarella is a web application made to help student computing clubs better
collaborate and organize their projects, presentations, and even mailing list
messages. Mozzarella is written in `Python 3`_ using the TurboGears_ framework.

.. _Python 3: https://python.org
.. _TurboGears: http://turbogears.org/

Setting up a Development Environment
------------------------------------

1. First, clone the repository:

   .. code:: console

       $ git clone https://github.com/ColoradoSchoolOfMines/mozzarella.git
       $ cd mozzarella

2. Next, install the application in editable form using ``pip``. Passing the
   ``--user`` flag installs for just your local user (typically in ``~/.local``).
   Alternatively, you may wish to use a `virtual enviornment`_.

   .. _virtual enviornment: https://docs.python.org/3/library/venv.html

   .. code:: console

       $ pip install -e . --user

3. Install development tools for TurboGears:

   .. code:: console

       $ pip install --user tg.devtools

4. Next, setup the ``development.ini`` file:

   .. code:: console

       $ cp development.ini.sample development.ini
       $ vim development.ini

5. Seed the development database:

   .. code:: console

       $ gearbox setup-app

6. Finally, serve the application:

   .. code:: console

       $ gearbox serve --reload --debug

   Once up, use your web browser to navigate to http://localhost:8080/.

Deploying Mozzarella
--------------------

Mozzarella is a WSGI application, and can be deployed using any WSGI-capable
web server. In our production environment, we use Apache 2.4 with ``mod_wsgi``,
but any other WSGI environment should work fine (such as Gunicorn, or uWSGI).

First, clone the repository and install the application:

.. code:: console

    $ git clone https://github.com/ColoradoSchoolOfMines/mozzarella.git /path/to/site

Next, install the application:

.. code:: console

    $ pip install .

Next, set up a ``production.ini`` file next to ``app.wsgi``. This file should
look like ``development.ini``, but you should be sure to disable debug mode and
make a new random key for cookies.

Database
~~~~~~~~

Supported databases are PostgreSQL_ and SQLite_. For production purposes, we
recommend PostgreSQL_. MySQL should work, but we have no intents to maintain
compatibility with MySQL in the long term.

.. _PostgreSQL: https://www.postgresql.org/
.. _SQLite: https://www.sqlite.org/index.html

Configure the path to your database in ``production.ini``:

.. code:: ini

    sqlalchemy.url = postgresql://user:pass@hostname/db

Depot Storage
~~~~~~~~~~~~~

Setup a depot storage. You can either use a path on the file system, or MongoDB
GridFS. Configure in your ``production.ini``:

.. code:: ini

    # If you opt for file system storage
    depot.storage_path = /path/to/depot/storage

.. code:: ini

    # If you opt for MongoDB GridFS
    depot.backend = depot.io.gridfs.GridFSStorage
    depot.mongouri = mongodb://localhost/db

See the `Depot documentation`_ for more information.

.. _Depot documentation: https://depot.readthedocs.io/en/latest/userguide.html

Apache
~~~~~~

Here is an example config for Apache with ``mod_wsgi``:

.. code:: apache

    <VirtualHost *:443>
        ServerAdmin jrosenth@mines.edu
        ServerName acm.mines.edu

        # Setup the WSGI process group
        WSGIProcessGroup mozzarella
        WSGIDaemonProcess mozzarella user=mozzarella group=mozzarella home=/path/to/site threads=8
        WSGIScriptAlias / /path/to/site/app.wsgi

        <Directory /path/to/site>
                Require all granted
        </Directory>

        # Make sure to alias the static files so that we don't have to go thru
        # a WSGI application to get these
        Alias /css /path/to/public/css
        Alias /img /path/to/public/img
        Alias /fonts /path/to/public/fonts
        Alias /js /path/to/public/js

        # Optional, where to log errors to
        ErrorLog /var/log/apache2/mozzarella-error.log
        CustomLog /var/log/apache2/mozzarella-access.log combined
        LogLevel warn

        # Make sure to setup anything else you are using, such as SSL certs
    </VirtualHost>

Static Assets
~~~~~~~~~~~~~

The location of site-specific assets for development can be configured in your development config: 

.. code:: ini 

    # Custom Assets Configuration
    custom_assets.dir = /path/to/assets/dir
    custom_assets.css = relative/path/to/css.file
    custom_assets.logo = relative/path/to/logo.file

Wiki
~~~~

Mozzarella includes a wiki that can be enabled by uncommenting the `wiki.repo` option in your configuration.
When visiting the wiki for the first time after enabling it, Mozzarella will generate a bare git repository with a sample
page in it.

.. code:: ini

   # Wiki repository location
   wiki.repo = /path/to/wiki/dir
