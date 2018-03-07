# -*- coding: utf-8 -*-
"""Profile controller module"""

from tg import expose, redirect, abort

from depot.manager import DepotManager

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, User

__all__ = ['ProfileController']
class UserController(BaseController):
    def __init__(self, user):
        self.user = user

    @expose('acmwebsite.templates.profile')
    def _default(self):
        """Handle the user's profile page."""
        return dict(page='profile', u=self.user)

    @expose()
    def picture(self):
        redirect(DepotManager.url_for(self.user.profile_pic.path))

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
