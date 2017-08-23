# -*- coding: utf-8 -*-
"""Profile controller module"""

from tg import expose, redirect, abort

from depot.manager import DepotManager

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, User

__all__ = ['ProfileController']

class ProfileRootController(BaseController):
    def __init__(self, uname):
        self.uname = uname

    @expose('acmwebsite.templates.profile')
    def _default(self):
        """Handle the user's profile page."""
        user = DBSession.query(User) \
                        .filter(User.user_name == self.uname) \
                        .one_or_none()
        if not user:
            abort(404, "No such user")
        return dict(page='profile', u=user)

    @expose()
    def picture(self):
        user = DBSession.query(User) \
                        .filter(User.user_name == self.uname) \
                        .one_or_none()
        redirect(DepotManager.url_for(user.profile_pic.path))

class ProfilesController(BaseController):
    @expose()
    def _lookup(self, uname, *args):
        return ProfileRootController(uname), args