# -*- coding: utf-8 -*-
"""Profile controller module"""

from tg import expose, redirect, validate, flash, url, lurl, abort

from acmwebsite.lib.base import BaseController
from acmwebsite.lib.helpers import log
from acmwebsite.model import DBSession, User

__all__ = ['ProfileController']

class ProfileController(BaseController):

    @expose('acmwebsite.templates.profile')
    def _default(self, uname=None):
        """Handle the user's profile page."""
        user = DBSession.query(User).filter(User.user_name == uname).one_or_none()
        if not user:
            abort(404, "No such user")
        return dict(page='profile', u=user)

