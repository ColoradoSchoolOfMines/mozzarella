# -*- coding: utf-8 -*-
"""MailMessage model module."""
import tg
import re
from sqlalchemy import *
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, DateTime
from sqlalchemy.orm import relationship, backref

from acmwebsite.model import DeclarativeBase, metadata, DBSession, User

user_p = re.compile(r'<(\w+)@(?:mymail\.)?mines\.edu>')

class MailMessage(DeclarativeBase):
    __tablename__ = 'mailmessages'

    message_id = Column(Unicode, primary_key=True)
    body = Column(Unicode, nullable=True)
    from_ = Column(Unicode, nullable=False)
    date = Column(DateTime, nullable=False)
    subject = Column(Unicode, nullable=True)
    parent_message_id = Column(Unicode, nullable=True)

    @property
    def url(self):
        return tg.url('/mailinglist/message/' + self.message_id + '.html')

    @property
    def parent(self):
        return DBSession.query(MailMessage).filter(MailMessage.message_id == self.parent_message_id).one_or_none()

    @property
    def children(self):
        return DBSession.query(MailMessage).filter(MailMessage.parent_message_id == self.message_id).all()

    @property
    def linkname(self):
        return self.from_ + ': ' + self.subject if self.subject else ''

    @property
    def next_by_date(self):
        return DBSession.query(MailMessage)\
                        .filter(MailMessage.date > self.date)\
                        .order_by(MailMessage.date)\
                        .first()

    @property
    def prev_by_date(self):
        return DBSession.query(MailMessage)\
                        .filter(MailMessage.date < self.date)\
                        .order_by(MailMessage.date.desc())\
                        .first()

    @property
    def mines_username(self):
        m = user_p.search(self.from_)
        return m.group(1) if m else None

    @property
    def user(self):
        return DBSession.query(User)\
                        .filter(User.user_name == self.mines_username)\
                        .one_or_none()

    @property
    def from_display(self):
        u = self.user
        if u:
            return '<a href="{u.profile_url}">{u}</a>'.format(u=u)
        else:
            return self.from_.replace('@', '&nbsp;at&nbsp;').replace('<', '(').replace('>', ')')


__all__ = ['MailMessage']
