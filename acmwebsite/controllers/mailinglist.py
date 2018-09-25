# -*- coding: utf-8 -*-
"""MailingListController controller module"""

import re
from tg import expose, flash, lurl, abort, app_globals
from tg.exceptions import HTTPFound
from tg.decorators import paginate

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, MailMessage

mailtokens = re.compile(r'''
        (?P<header>^[^\n]+\n(?:={3,}|-{3,})\n)
    |   (?P<quote>(?:^On [^\n]+ wrote:\n\n?)?(?:^>[ ][^\n]*\n|^>\n)+)
    |   (?P<signature>^--[ ]\n.*\Z)
    |   (?P<body>^[^\n]*\n)''', re.DOTALL | re.MULTILINE | re.VERBOSE)


class MailingListController(BaseController):
    @expose('acmwebsite.templates.mailinglist')
    def index(self):
        """Handle the 'mailinglist' page."""
        recents = DBSession.query(MailMessage).order_by(MailMessage.date.desc()).limit(5)
        return dict(page='mailinglist', recents=recents)

    @expose()
    def subscribe(self, came_from=lurl('/mailinglist'), ml_username=None, ml_fullname=None):
        try:
            app_globals.mmadmin.mymail_subscribe(ml_username, ml_fullname)
            flash("Successfully subscribed to mailing list")
        except Exception as e:
            flash("An error occurred: {}".format(e), 'error')
        return HTTPFound(location=came_from)

    @expose('acmwebsite.templates.message')
    def message(self, message_id):
        msg = (DBSession.query(MailMessage)
                        .filter(MailMessage.message_id == message_id)
                        .one_or_none())
        if not msg:
            abort(404, "No message with ID {}".format(message_id))

        bodyparts = []
        for m in mailtokens.finditer(msg.body.rstrip('\n') + '\n'):
            for k, v in m.groupdict().items():
                if v is not None:
                    bodyparts.append((k, v))

        return dict(
            page='mailinglist',
            message=msg,
            bodyparts=bodyparts)

    @expose('acmwebsite.templates.archives')
    @paginate('messages', items_per_page=30)
    def archives(self):
        messages = DBSession.query(MailMessage).order_by(MailMessage.date.desc())
        return dict(page='mailinglist', messages=messages)
