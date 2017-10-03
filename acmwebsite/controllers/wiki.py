# -*- coding: utf-8 -*-
"""Wiki Pages Controller"""

from tg import expose, redirect, validate, flash, url, lurl, abort, require, request, predicates

from acmwebsite.lib.base import BaseController
from acmwebsite.lib.helpers import log
from acmwebsite.model import DBSession, WikiPage
from acmwebsite.model.wikipage import latest_revision

class WikiPageController(BaseController):
    def __init__(self, page, new=False):
        self.page = page
        self.new = new

    @expose('acmwebsite.templates.wikiview')
    def index(self):
        """View the page"""
        return dict(page='wiki', wikipage=self.page, new=self.new)

    @expose('acmwebsite.templates.wikiedit')
    @require(predicates.not_anonymous())
    def edit(self):
        user = request.identity.get('user')
        if (self.page # anyone may make a new page
            and self.page.edit_permission # pages without permissions set may be edited by anyone
            and self.page.edit_permission not in user.permissions):
            abort(403, "You do not have permission to edit this page.")
        return dict(page='wiki', wikipage=self.page)

    @expose('acmwebsite.template.wikihistory')
    def history(self):
        revisions = (DBSession.query(WikiPage)
                              .filter(WikiPage.slug == self.page.slug)
                              .order_by(WikiPage.revision.desc())
                              .all())
        return dict(page='wiki', revisions=revisions)

class WikiPagesController(BaseController):
    @expose()
    def _lookup(self, slug, *args):
        if slug == 'history':
            if not args:
                abort(404)
            return self.page_by_id(*args)
        page = latest_revision(slug)
        new = not page
        if new:
            page = WikiPage(slug=slug)
        return WikiPageController(page, new=new), args

    def page_by_id(self, id, *args):
        page = DBSession.query(WikiPage).filter(WikiPage.id == id).one_or_none()
        if not page:
            abort(404)
        return WikiPageController(page), args
