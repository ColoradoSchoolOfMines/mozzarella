# -*- coding: utf-8 -*-

#  Quickstarted Options:
#
#  sqlalchemy: True
#  auth:       sqlalchemy
#  mako:       False
#
#

# This is just a work-around for a Python2.7 issue causing
# interpreter crash at exit when trying to log an info message.
try:
    import logging
    import multiprocessing
except:
    pass

import sys
py_version = sys.version_info[:2]

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

testpkgs = [
    'coverage',
    'gearbox',
    'nose',
    'WebTest >= 1.2.3',
]

install_requires = [
    "alembic",
    "Beaker >= 1.8.0",
    "filedepot",
    "icalendar",
    "Kajiki >= 0.6.3",
    "docutils",
    "pygit2",
    "pytz",
    "repoze.who",
    "requests",
    "sqlalchemy",
    "tgext.admin >= 0.6.1",
    "tgscheduler",
    "TurboGears2 >= 2.3.11",
    "tw2.forms",
    "WebHelpers2",
    "zope.sqlalchemy >= 0.4",
    "Pillow",
]

if py_version != (3, 2):
    # Babel not available on 3.2
    install_requires.append("Babel")

setup(
    name='acm-website',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    packages=find_packages(exclude=['ez_setup']),
    install_requires=install_requires,
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=testpkgs,
    package_data={'acmwebsite': [
        'i18n/*/LC_MESSAGES/*.mo',
        'templates/*/*',
        'public/*/*'
    ]},
    message_extractors={'acmwebsite': [
        ('**.py', 'python', None),
        ('templates/**.xhtml', 'kajiki', {'strip_text': False, 'extract_python': True}),
        ('public/**', 'ignore', None)
    ]},
    entry_points={
        'paste.app_factory': [
            'main = acmwebsite.config.middleware:make_app'
        ],
        'gearbox.plugins': [
            'turbogears-devtools = tg.devtools'
        ]
    },
    zip_safe=False
)
