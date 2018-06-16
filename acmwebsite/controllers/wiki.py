"""Wiki controller module"""
from tg import expose

from acmwebsite.lib.base import BaseController

from pygit2 import Repository,init_repository
from pygit2 import Tree
from pygit2 import Signature
from pygit2 import GitError
from pygit2 import GIT_FILEMODE_BLOB

from docutils.core import publish_parts

import os
import tg

__all__ = ['WikiController']

class WikiController(BaseController):
    """Controls the wiki"""

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
        signature = Signature("Example McPersonson", "emailuser@emailsite.tld") #TODO: Replace me

        tb = self.repo.TreeBuilder()

        # Write initial front page
        filename = "FrontPage.rst"
        data = "In the *future*, this **content** will be filled from a standard file!"

        # Create blob from frontpage content and insert into tree
        blobid = self.repo.create_blob(data)
        tb.insert(filename, blobid, GIT_FILEMODE_BLOB)
        tree = tb.write()
        
        # Commit the change
        branch_commit = self.repo.create_commit(
            'HEAD',
            signature,
            signature,
            "Initial commit",
            tree,
            []
        )

    @expose('acmwebsite.templates.wiki_view')
    def _default(self, pagename):
        """Display a specific page"""
        tb = self.repo.TreeBuilder(self.repo.head.peel(Tree))
        if not tb.get(pagename + '.rst'):
            tg.abort(404, "Page not found")
        blob = self.repo.get(self.repo.head.peel(Tree)[pagename + '.rst'].id)
        settings = {'initial_header_level': 2, 'file_insertion_enabled': 0, 'raw_enabled': 0, 'disable_config': 1,}
        return dict(page=pagename, content=publish_parts(blob.data, writer_name='html5', settings_overrides=settings)['body']) #TODO: probably could just open(file) and return raw data
    

    @expose('acmwebsite.templates.wiki_front')
    def index(self):
        """Display the wiki frontpage"""
        return dict()
