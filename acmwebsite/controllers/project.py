"""Project controller module."""

from tg import expose, abort

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, Project


class ProjectController(BaseController):
    def __init__(self, project):
        self.project = project

    @expose('acmwebsite.templates.project')
    def index(self):
        return dict(page='project', project=self.project)


class ProjectsController(BaseController):
    """Root controller for listing all projects"""
    def __init__(self):
        self.projects = DBSession.query(Project)

    @expose()
    def _lookup(self, id, *args):
        project = DBSession.query(Project).filter(Project.id == id).first()
        if not project:
            abort(404, "No such project")
        return ProjectController(project), args

    @expose('acmwebsite.templates.projects')
    def index(self):
        return dict(page='projects', projects=self.projects)
