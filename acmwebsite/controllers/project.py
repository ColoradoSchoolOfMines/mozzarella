"""Project controller module."""

from tg import expose

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, Project


class ProjectsController(BaseController):
    """Controller for listing all projects"""

    @expose('acmwebsite.templates.projects')
    def index(self):
        return dict(page='projects', projects=DBSession.query(Project))
