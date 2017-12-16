"""Project controller module."""

from tg import abort, expose, request
from tg.predicates import has_permission, not_anonymous

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
        project = self.projects.filter(Project.id == id).first()
        if not project:
            abort(404, "No such project")
        return ProjectController(project), args

    @expose('acmwebsite.templates.projects')
    def index(self):
        # Only show verified projects or projects that the current user is on.
        if has_permission('admin'):
            projects = self.projects.all()
        elif request.identity:
            user = request.identity['user']
            projects = self.projects.filter(Project.status == 'v'
                                            or user in Project.team_members)
        else:
            projects = self.projects.filter(Project.status == 'v')

        return dict(page='projects', projects=projects)

    @expose('acmwebsite.templates.submit_project')
    def submit(self):
        if request.method == 'POST':
            pass
        else:
            return dict(page='project_submit')
