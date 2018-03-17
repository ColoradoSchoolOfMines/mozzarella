# -*- coding: utf-8 -*-
"""Profile controller module"""

from itertools import chain

from tg import expose, redirect, abort

from depot.manager import DepotManager

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, User

def card_about_me(user):
    if user.bio:
        yield ("About Me", user.bio)

card_types = [card_about_me]

__all__ = ['ProfileController']
class UserController(BaseController):
    def __init__(self, user):
        self.user = user

    @expose('acmwebsite.templates.profile')
    def _default(self):
        """Handle the user's profile page."""

        cards = chain(*(card_gen(self.user) for card_gen in card_types))
        return dict(page='profile', u=self.user, cards=cards)

    @expose()
    def picture(self):
        redirect(DepotManager.url_for(self.user.profile_pic.path))

    @expose('acmwebsite.templates.profile_edit')
    def edit(self):
        return dict(page='profile_edit', u=self.user)

class UsersController(BaseController):
    @expose()
    def _lookup(self, uname, *args):
        user = DBSession.query(User) \
                        .filter(User.user_name == uname) \
                        .one_or_none()
        if not user:
            abort(404, "No such user")

        return UserController(user), args
