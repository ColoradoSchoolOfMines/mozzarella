"""Project controller module."""

from tg import expose

from mozzarella.lib.base import BaseController
from mozzarella.lib.card import Card
from mozzarella.model import DBSession, Project
import mozzarella.controllers.user as user


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

    @expose('mozzarella.templates.projects')
    def index(self):
        return dict(page='projects', projects=DBSession.query(Project).all())
