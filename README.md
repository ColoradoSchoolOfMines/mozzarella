# Mines ACM Student Chapter Website

[acm.mines.edu](https://acm.mines.edu/)

This is the website for the Colorado School of Mines' local chapter for the
[Association for Computing Machinery](http://www.acm.org/).

It is written in Python and uses the powerful web framework
[TurboGears](http://turbogears.com/).

## Setting up your Development Environment

Clone the repo:

    $ git clone https://github.com/ColoradoSchoolOfMines/acm-website.git

### To install in user's personal path (~/.local)

Install the application and its dependencies:

    $ pip install -e . --user

If you do not have `gearbox` installed:

    $ pip install --user tg.devtools

Setup the application:

    $ cp development.ini.sample development.ini
    $ gearbox setup-app

Finally, serve the application:

    $ gearbox serve --reload --debug

### To use a virtual environment

Use a virtual environment if you do not want to install the needed Python
packages into ~/.local

If you're unfamiliar with Python virtual environments:

* [https://virtualenv.pypa.io/en/stable/](https://virtualenv.pypa.io/en/stable/)
* [https://virtualenvwrapper.readthedocs.io/en/latest/](https://virtualenvwrapper.readthedocs.io/en/latest/)

Make sure you have `virtualenvwrapper` installed

On Arch Linux:

    $ sudo pacman -S python-virtualenvwrapper

Make a virtual environment:

    $ mkvirtualenv acm-website

Activate the virtual environment:

    $ workon acm-website

Install the application and its dependencies:

    $ pip install -e .

If you do not have `gearbox` installed:

    $ pip install tg.devtools

Setup the application:

    $ cp development.ini.sample development.ini
    $ gearbox setup-app

Finally, serve the application:

    $ gearbox serve --reload --debug

When you're finished working on the project and want to exit the virtual
environment:

    $ deactivate
