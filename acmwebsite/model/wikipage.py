import datetime
from os import urandom
from sqlalchemy import Column, ForeignKey, Table, func
from sqlalchemy.orm import mapper, relation
from sqlalchemy.types import DateTime, Integer, Text, Unicode

from acmwebsite.model import DBSession, DeclarativeBase, metadata

class WikiPage(DeclarativeBase):
    __tablename__ = 'wikipages'

    id = Column(Unicode(32), primary_key=True)
    slug = Column(Unicode(60), nullable=False)
    revision = Column(DateTime, nullable=False, default=datetime.datetime.now)
    comment = Column(Unicode(250), nullable=True)
    title = Column(Unicode(100), nullable=False, default="")
    content = Column(Unicode, nullable=False, default="")

    edit_permission_id = Column(Integer, ForeignKey('tg_permission.permission_id'), nullable=True)
    edit_permission = relation("Permission", back_populates="pages")

    author_id = Column(Integer, ForeignKey('tg_user.user_id'), nullable=False)
    author = relation("User", back_populates="page_revisions")

def latest_revision(slug):
    return (DBSession.query(WikiPage, func.max(WikiPage.revision))
                     .filter(WikiPage.slug == slug)
                     .scalar())
