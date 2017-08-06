# -*- coding: utf-8 -*-
"""MailMessage model module."""
import tg
from sqlalchemy import *
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, DateTime
from sqlalchemy.orm import relationship, backref

from acmwebsite.model import DeclarativeBase, metadata, DBSession

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

__all__ = ['MailMessage']
