"""Wiki controller module"""
from tg import expose

from acmwebsite.lib.base import BaseController

from pygit2 import Repository,init_repository
from pygit2 import Tree
from pygit2 import Signature
import pygit2 as pg

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
        except pg.GitError:
            self._init_wiki_repo()

    def _init_wiki_repo(self):
        self.repo = init_repository(tg.config.get('wiki.repo'), True)
        signature = Signature("Example McPersonson", "emailuser@emailsite.tld") #TODO: Replace me

        tb = self.repo.TreeBuilder()

        # Create blob from frontpage content and insert into tree
        from pkg_resources import resource_filename
        filename = "FrontPage.rst"
        filepath = resource_filename('acmwebsite', 'wiki-assets/FrontPage.rst')
        blobid = self.repo.create_blob_fromdisk(filepath)
        tb.insert(filename, blobid, pg.GIT_FILEMODE_BLOB)
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
        settings = {'initial_header_level': 2,
                    'file_insertion_enabled': 0,
                    'raw_enabled': 0,
                    'disable_config': 1,
        }

        tb = self.repo.TreeBuilder(self.repo.head.peel(Tree))
        if not tb.get(pagename + '.rst'):
            tg.abort(404, "Page not found")
        blob = self.repo.get(self.repo.head.peel(Tree)[pagename + '.rst'].id)
        document = publish_parts(blob.data, writer_name='html5', settings_overrides=settings)
        return dict(pagename=pagename, parts=document)

    @expose('acmwebsite.templates.wiki_history')
    def history(self, pagename):
        filename = pagename + ".rst"
        revision_list = []
        last_id = None

        #Get a list of commits that include the queried file
        for commit in self.repo.walk(self.repo.head.target, pg.GIT_SORT_TIME):
            if filename in commit.tree:
                entry = commit.tree[filename]
                if entry.id != last_id: #Only add to history if it file chnaged.
                    revision_list.append({"author": commit.author,
                                          "time": commit.commit_time,
                                          "message": commit.message})
                last_id = entry.id

        if not revision_list: #No commits include file - possibly faulty?
            tg.abort(404, "Page not found")
        return dict(page=pagename, revisions=revision_list)

    @expose('acmwebsite.templates.wiki_pagelist')
    def pagelist(self):
        pages = [entry.name[:-4] for entry in self.repo.head.peel(Tree)]
        return dict(pages=pages)


    @expose()
    def index(self):
        """Display the wiki frontpage"""
        tg.redirect('/wiki/FrontPage')
