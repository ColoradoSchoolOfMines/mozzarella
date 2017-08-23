# -*- coding: utf-8 -*-
"""Profile controller module"""

from tg import expose, redirect, abort

from depot.manager import DepotManager

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, User

__all__ = ['ProfileController']

class ProfileController(BaseController):

    @expose('acmwebsite.templates.profile')
    def _default(self, uname=None):
        """Handle the user's profile page."""
        user = DBSession.query(User) \
                        .filter(User.user_name == uname) \
                        .one_or_none()
        if not user:
            abort(404, "No such user")
        return dict(page='profile', u=user)

    @expose()
    def profile_pic(self, user_name):
        user = DBSession.query(User) \
                        .filter(User.user_name == user_name) \
                        .one_or_none()
        redirect(DepotManager.url_for(user.profile_pic.path))
