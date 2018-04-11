# -*- coding: utf-8 -*-
"""Profile controller module"""

from tg import expose, redirect, abort

from depot.manager import DepotManager

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, User
from acmwebsite.lib.card import Card, CardTypes

cards = CardTypes()

def card_about_me(user):
    if user.bio:
        yield Card("About Me", dict(text=user.bio))

cards.register(card_about_me, body_template="bio_body")

__all__ = ['UsersController']
class UserController(BaseController):
    def __init__(self, user):
        self.user = user

    @expose('acmwebsite.templates.profile')
    def _default(self):
        """Handle the user's profile page."""

        return dict(page='profile', u=self.user, cardlist=cards.gen(self.user))

    @expose()
    def picture(self):
        redirect(DepotManager.url_for(self.user.profile_pic.path))

    @expose('acmwebsite.templates.profile_edit')
    def edit(self):
        return dict(page='profile_edit', u=self.user)

class UsersController(BaseController):
    @expose()
    def _lookup(self, uname=None, *args):
        user = None
        if uname:
            user = DBSession.query(User) \
                            .filter(User.user_name == uname) \
                            .one_or_none()
        if not user:
            abort(404, "No such user")

        return UserController(user), args
