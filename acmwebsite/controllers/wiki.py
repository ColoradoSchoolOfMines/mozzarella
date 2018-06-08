from tg import expose

from acmwebsite.lib.base import BaseController

class WikiController(BaseController):
    """
    Controls the wiki
    OC code donut steel
    """

    @expose('acmwebsite.templates.wiki')
    def index(self):
        return dict(page='wiki')

