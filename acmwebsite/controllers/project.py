"""Project controller module."""

from tg import expose

from acmwebsite.controllers import user
from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, Project

from kajiki import XMLTemplate

import acmwebsite.controllers.user

# TODO: Make title link
card_title_template = XMLTemplate("""
<ul class="list-inline dot-separated-list">
  <li>Project</li>
  <li>
    ${project.name}
  </li>
</ul>
""")
card_body_template = XMLTemplate("""<html>
<div class="col-md-4">
  <img py:if="project.image" src="${project.image.url}" class="card-image" />
</div>
<div class="col-md-8">
  ${project.description}
</div>
</html>""")

def project_card_gen(user):
    for proj in user.projects:
        args = dict(project=proj)
        yield (
            card_title_template(args).render(),
            card_body_template(args).render(),
        )

acmwebsite.controllers.user.card_types.append(project_card_gen)

class ProjectsController(BaseController):
    """Root controller for listing all projects"""

    @expose('acmwebsite.templates.projects')
    def index(self):
        return dict(page='projects', projects=DBSession.query(Project).all())
