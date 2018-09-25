"""Profile controller module"""

from tg import expose, redirect, abort, url
from depot.manager import DepotManager

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, User
from acmwebsite.lib.card import Card, CardTypes

__all__ = ['UsersController']


def card_about_me(user):
    if user.bio:
        yield Card("About Me", dict(text=user.bio))


cards = CardTypes()
cards.register(card_about_me, body_template="cards/bio_body.xhtml")


class UserController(BaseController):
    def __init__(self, user):
        self.user = user

    @expose('acmwebsite.templates.profile')
    def _default(self):
        """Handle the user's profile page."""

        return dict(page='profile', u=self.user,
                    cardlist=cards.generate_cards(self.user))

    @expose()
    def picture(self):
        if self.user.profile_pic:
            redirect(DepotManager.url_for(self.user.profile_pic.path))
        else:
            redirect(url('/img/default_user.png'))

    @expose('acmwebsite.templates.profile_edit')
    def edit(self):
        return dict(page='profile_edit', u=self.user)


class UsersController(BaseController):
    @expose()
    def _lookup(self, uname=None, *args):
        user = None
        if uname:
            user = DBSession.query(User) \
                            .filter(User.user_name == uname) \
                            .one_or_none()
        if not user:
            abort(404, "No such user")

        return UserController(user), args
