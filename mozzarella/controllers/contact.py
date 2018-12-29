"""Contact controller module"""

from tg import expose
from mozzarella.model import DBSession
from mozzarella.model.auth import User

from mozzarella.lib.base import BaseController


class ContactController(BaseController):
    @expose('mozzarella.templates.contact')
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
