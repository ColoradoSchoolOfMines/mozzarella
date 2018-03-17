"""Project controller module."""

from tg import expose

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, Project

__all__ = ['ProjectsController']
class ProjectController(BaseController):
    def __init__(self, project):
        self.project = project

    @expose('acmwebsite.templates.project')
    def _default(self):
        """Handle the project's page."""
        return dict(page='project', p=self.project)

    @expose()
    def picture(self):
        redirect(DepotManager.url_for(self.project.image.path))

class ProjectsController(BaseController):
    """Root controller for listing all projects"""

    @expose('acmwebsite.templates.projects')
    def index(self):
        return dict(page='projects', projects=DBSession.query(Project).all())

    @expose()
    def _lookup(self, pid=None, *args):
        # TODO: change to use textual ID instead of project id
        project = None
        if pid:
            project = DBSession.query(Project) \
                            .filter(Project.id == pid) \
                            .one_or_none()
        if not project:
            abort(404, "No such project")
        return ProjectController(project), args