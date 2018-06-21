Welcome to the wiki!
====================

It looks like this wiki has just been created. A git repository has been created
at the location specified in ``wiki.repo`` in your ``config.ini``.

Contributing
------------

To edit or add pages to the wiki, clone the wiki repository, edit or create your
pages, then commit and push them the remote repository on the website. Pages
must be in `reStructuredText format`_ and have the file extension ``.rst``

.. _reStructuredText format: http://docutils.sourceforge.net/rst.html

The wiki page titles depend on your ReST documents having titles - don't include
any text before the page title.

.. code:: rest

   This is a title
   ===============

This page is in your wiki repository as ``FrontPage.rst``. To replace it (i.e.
set a new index page for your wiki), replace this file with the new front page.
