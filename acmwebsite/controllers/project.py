"""Project controller module."""

from tg import expose

from acmwebsite.lib.base import BaseController
from acmwebsite.lib.card import Card
from acmwebsite.model import DBSession, Project
import acmwebsite.controllers.user as user


def project_card_gen(user):
    for proj in user.projects:
        args = {'project': proj}
        yield Card(args, args)


user.cards.register(
    project_card_gen,
    title_template="cards/project_title.xhtml",
    body_template="cards/project_body.xhtml",
)


class ProjectsController(BaseController):
    """Controller for listing all projects"""

    @expose('acmwebsite.templates.projects')
    def index(self):
        return dict(page='projects', projects=DBSession.query(Project).all())
