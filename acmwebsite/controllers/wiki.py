from tg import expose

from acmwebsite.lib.base import BaseController

from pygit2 import Repository,init_repository
from pygit2 import Tree
from pygit2 import Signature
from pygit2 import GitError
from pygit2 import GIT_FILEMODE_BLOB

import os
import tg

__all__ = ['WikiController']

class WikiController(BaseController):
    """
    Controls the wiki
    OC code donut steel
    """
    def _before(self, *args, **kw):
        try:
            repo_path = tg.config.get('wiki.repo')
            if not repo_path:
                tg.abort(400, "Wiki not enabled")
            self.repo = Repository(repo_path)
        except GitError:
            self._init_wiki_repo()

    def _init_wiki_repo(self):
        self.repo = init_repository(tg.config.get('wiki.repo'), True)
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
        newfile = open(os.path.join(self.repo.path, filename), 'w')
        newfile.write(data)
        newfile.close()

        blobid = self.repo.create_blob(data)
        tb = self.repo.TreeBuilder(self.repo.head.peel(Tree))
        tb.insert(filename, blobid, GIT_FILEMODE_BLOB)
        tree = tb.write()

        self.repo.create_commit(
            'HEAD',
            signature,
            signature,
            "Initial Commit",
            tree,
            [self.repo.head.target]
        )
        
    @expose('acmwebsite.templates.wiki_view')
    def _default(self, pagename):
        """Display a specific page"""
        from docutils.core import publish_parts
        tb = self.repo.TreeBuilder(self.repo.head.peel(Tree))
        if tb.get(pagename + '.rst') is None:
            tg.abort(404, "Page not found")
        blob = self.repo.get(self.repo.head.peel(Tree)[pagename + '.rst'].id)
        #return dict(page=pagename, content=publish_parts(writer_name='html5', source="Monkey\nD\nLuffy")['body']) #TODO: probably could just open(file) and return raw data
        return dict(page=pagename, content=publish_parts(writer_name='html5', source=blob.data)['body']) #TODO: probably could just open(file) and return raw data
    

    # @expose('acmwebsite.templates.wiki_frontpage')
    # def index(self):
    #     """Display the wiki frontpage"""
    #     pass
