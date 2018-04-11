"""Project controller module."""

from tg import expose

from acmwebsite.controllers import user
from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, Project

from kajiki import XMLTemplate

import acmwebsite.controllers.user
from acmwebsite.lib.card import Card, CardTypes

def project_card_gen(user):
    for proj in user.projects:
        args = dict(project=proj)
        yield Card(args, args)

acmwebsite.controllers.user.cards.register(
    project_card_gen,
    title_template="project_title",
    body_template="project_body",
)

class ProjectsController(BaseController):
    """Controller for listing all projects"""

    @expose('acmwebsite.templates.projects')
    def index(self):
        return dict(page='projects', projects=DBSession.query(Project).all())
