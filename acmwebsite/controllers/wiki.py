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

    @expose('acmwebsite.templates.wiki')
    def index(self, pagename="FrontPage"):
        repo = Repository(tg.config.get('wiki.repo'))
        tb = repo.TreeBuilder(repo.head.peel().tree)
        if tb.get(''.join((pagename, '.rst'))) is None:
            pass #redirect to edit page
        blob = repo.get(repo.index[pagename].id)
        return dict(page=pagename, content=blob.data)

    def save(self, pagename):
        pass
