# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates, session
from acmwebsite import model
from acmwebsite.controllers.secure import SecureController
from acmwebsite.model import DBSession
from tgext.admin.tgadminconfig import BootstrapTGAdminConfig as TGAdminConfig
from tgext.admin.controller import AdminController

from acmwebsite.model.meeting import Meeting

from acmwebsite.lib.base import BaseController
from acmwebsite.controllers.error import ErrorController
from acmwebsite.lib.helpers import mmadmin

import datetime

__all__ = ['RootController']

class RootController(BaseController):
    """
    The root controller for the acm-website application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "acmwebsite"

    @expose('acmwebsite.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('acmwebsite.templates.mailinglist')
    def mailinglist(self):
        """Handle the 'mailinglist' page."""
        return dict(page='mailinglist')

    @expose()
    def post_mailinglist(self, came_from=lurl('/mailinglist'), ml_username=None, ml_fullname=None):
        try:
            mmadmin.mymail_subscribe(ml_username, ml_fullname)
            flash("Successfully subscribed to mailing list")
        except Exception as e:
            flash("An error occurred: {}".format(e), 'error')
        return HTTPFound(location=came_from)

    @expose('acmwebsite.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        if failure is not None:
            if failure == 'user-not-found':
                flash(_('User not found'), 'error')
            elif failure == 'invalid-password':
                flash(_('Invalid Password'), 'error')

        login_counter = request.environ.get('repoze.who.logins', 0)
        if failure is None and login_counter > 0:
            flash(_('Wrong credentials'), 'warning')

        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        return HTTPFound(location=came_from)

    @expose()
    def toggle_theme(self):
        if session.get('theme', None) == 'dark':
            session['theme'] = 'light'
        else:
            session['theme'] = 'dark'
        session.save()
        return session.get('theme', None)

    @expose('acmwebsite.templates.schedule')
    def schedule(self):
        """Handle the schedule page."""
        meetings = DBSession.query(Meeting).filter(
                Meeting.date > datetime.datetime.now() - datetime.timedelta(hours=3)
                ).order_by(Meeting.date)
        return dict(page='schedule', meetings=meetings)
