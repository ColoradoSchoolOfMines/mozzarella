# -*- coding: utf-8 -*-
"""Profile controller module"""

from tg import expose, redirect, validate, flash, url, lurl, abort

from acmwebsite.lib.base import BaseController
from acmwebsite.lib.helpers import log
from acmwebsite.model import DBSession, User

__all__ = ['TodayController']

class TodayController(BaseController):

    @expose('acmwebsite.templates.today')
    def _default(self):
        return dict(page='today')
