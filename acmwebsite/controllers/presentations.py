"""Presentations controller"""
from tg import expose, request, redirect, url

from acmwebsite.model import DBSession
from acmwebsite.model.presentation import Presentation
from acmwebsite.lib.base import BaseController

__all__ = ['PresentationsController']

class PresentationsController(BaseController):
    @expose('acmwebsite.templates.presentations')
    def index(self):
        """List all presentations"""
        presentations = list(DBSession.query(Presentation))
        presentations.sort(key=lambda p: p.date, reverse=True)

        return dict(page='presentations', presentations=presentations)

    @expose('acmwebsite.templates.presentation_upload')
    def upload(self):
        if request.POST:
            # TODO
            pass
            return '\n'.join(dir(request.POST))

        # GET
        if request.identity:
            return dict(page='presentation_upload')
        else:
            redirect(url('/login',
                         params=dict(came_from='/presentations/upload')))
