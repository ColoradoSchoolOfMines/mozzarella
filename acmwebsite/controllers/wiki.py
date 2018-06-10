from tg import expose

from acmwebsite.lib.base import BaseController

from pygit2 import Repository

import os
import tg

class WikiController(BaseController):
    """
    Controls the wiki
    OC code donut steel
    """

    @expose('acmwebsite.templates.wikiview')
    def index(self, pagename="FrontPage"):
        repo = Repository(tg.config.get('wiki.repo'))
        tb = repo.TreeBuilder(repo.head.peel().tree)
        if tb.get(''.join((pagename, '.rst'))) is None:
            tg.abort(404, "Page not found")
        blob = repo.get(repo.index[''.join((pagename, '.rst'))].id)
        return dict(page=pagename, content=blob.data)

    @expose('acmwebsite.templates.wikiedit')
    def edit(self, pagename):
        pass

    def save(self, pagename):
        pass
