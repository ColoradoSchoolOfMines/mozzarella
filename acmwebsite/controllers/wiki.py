from tg import expose

from acmwebsite.lib.base import BaseController

from pygit2 import Repository,init_repository
from pygit2 import Signature
from pygit2 import GitError
from pygit2 import GIT_FILEMODE_BLOB

import os
import tg

class WikiController(BaseController):
    """
    Controls the wiki
    OC code donut steel
    """

    def _before(self, *args, **kw):
        try:
            self.repo = Repository(tg.config.get('wiki.repo'))
        except GitError:
            self.repo = init_repository(tg.config.get('wiki.repo'), False)
            signature = Signature("Brandon Verkamp", "jadelclemens@gmail.com") #TODO: Replace me
            
            tb = self.repo.TreeBuilder()
            tree = tb.write()
            branch_commit = self.repo.create_commit(
                'HEAD',
                signature,
                signature,
                "Create master branch",
                tree,
                []
            )

            filename = "FrontPage.rst"
            data = "In the future, this content will be filled from a standard file!"
            newfile = open(os.path.join(self.repo.workdir, filename), 'w')
            newfile.write(data)
            newfile.close()

            fileid = self.repo.create_blob_fromworkdir(filename)
            tb = self.repo.TreeBuilder(self.repo.head.peel().tree)
            tb.insert(filename, fileid, GIT_FILEMODE_BLOB)
            tree = tb.write()

            self.repo.index.read()
            self.repo.index.add(filename)
            self.repo.index.write()

            self.repo.create_commit(
                'HEAD',
                signature,
                signature,
                "Initial Commit",
                tree,
                [self.repo.head.target]
            )

        

    @expose('acmwebsite.templates.wikiview')
    def index(self, pagename="FrontPage"):
        tb = self.repo.TreeBuilder(self.repo.head.peel().tree)
        if tb.get(''.join((pagename, '.rst'))) is None:
            tg.abort(404, "Page not found")
        blob = self.repo.get(self.repo.index[''.join((pagename, '.rst'))].id)
        return dict(page=pagename, content=blob.data) #TODO: probably could just open(file) and return raw data

    @expose('acmwebsite.templates.wikiedit')
    def edit(self, pagename):
        pass

    def save(self, pagename):
        pass
