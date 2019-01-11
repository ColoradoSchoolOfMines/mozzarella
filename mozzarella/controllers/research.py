"""Research controller module"""

from tg import expose

from mozzarella.lib.base import BaseController


class ResearchController(BaseController):
    """Controller for research page"""

    @expose('mozzarella.templates.research')
    def index(self):
        return dict(page='research')
