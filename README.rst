Mozzarella
==========

This website is a website for clubs and student organizations.

Mozzarella It is written in Python and uses the powerful web framework
TurboGears_.

.. _TurboGears: http://turbogears.com/

Setting up your Development Environment
---------------------------------------

These steps are meant to give you an overview of how to get a development
environment set up for developing this application. Please adapt to your system
as necessary. `This guide`_ gives more in-depth instructions on how to start
working on a TurboGears project.

.. _This guide: https://github.com/ColoradoSchoolOfMines/ACM-Guide-list/blob/master/computer_science/TurboGears.md

Clone the repo::

    $ git clone https://github.com/ColoradoSchoolOfMines/mozzarella.git

Install the application and its dependencies::

    $ pip install -e . --user

If you do not have ``gearbox`` installed::

    $ pip install --user tg.devtools

Setup the application::

    $ cp development.ini.sample development.ini
    $ gearbox setup-app

Serve the application::

    $ gearbox serve --reload --debug

Finaly, go to your web browser and navigate to ``localhost:8080`` to view the
website.
