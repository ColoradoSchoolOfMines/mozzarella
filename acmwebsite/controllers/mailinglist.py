# -*- coding: utf-8 -*-
"""MailingListController controller module"""

from tg import expose, redirect, validate, flash, url, lurl, abort
from tg.exceptions import HTTPFound
from tg.decorators import paginate

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, MailMessage
from acmwebsite.lib.helpers import mmadmin

class MailingListController(BaseController):

    @expose('acmwebsite.templates.mailinglist')
    def index(self):
        """Handle the 'mailinglist' page."""
        recents = DBSession.query(MailMessage).order_by(MailMessage.date.desc()).limit(5)
        return dict(page='mailinglist', recents=recents)

    @expose()
    def subscribe(self, came_from=lurl('/mailinglist'), ml_username=None, ml_fullname=None):
        try:
            mmadmin.mymail_subscribe(ml_username, ml_fullname)
            flash("Successfully subscribed to mailing list")
        except Exception as e:
            flash("An error occurred: {}".format(e), 'error')
        return HTTPFound(location=came_from)

    @expose('acmwebsite.templates.message')
    def message(self, message_id):
        msg = DBSession.query(MailMessage).filter(MailMessage.message_id == message_id).one_or_none()
        if not msg:
            abort(404, "No message with ID {}".format(message_id))
        return dict(page='mailinglist', message=msg)

    @expose('acmwebsite.templates.archives')
    @paginate('messages', items_per_page=30)
    def archives(self):
        messages = DBSession.query(MailMessage).order_by(MailMessage.date.desc())
        return dict(page='mailinglist', messages=messages)
