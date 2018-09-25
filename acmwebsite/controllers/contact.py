"""Contact controller module"""

from tg import expose
from acmwebsite.model import DBSession
from acmwebsite.model.auth import User

from acmwebsite.lib.base import BaseController


class ContactController(BaseController):
    @expose('acmwebsite.templates.contact')
    def index(self):
        """Handle the 'contact' page."""
        officer_sort = [
            "President",
            "Vice President",
            "Secretary",
            "Treasurer"
        ]
        users = DBSession.query(User)
        officers = []
        general = []
        for user in users:
            if user.officer_title:
                officers.append(user)
        officers.sort(key=lambda u: officer_sort.index(u.officer_title))
        return dict(page='contact', officers=officers, general=general)
