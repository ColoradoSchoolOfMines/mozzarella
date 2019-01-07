"""Defines the Presentation model.

Presentations are slides, files, or other presentables that the club shares
among its cohorts, usually during Meetings.
"""

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, Unicode, String, DateTime

from acmwebsite.model import DeclarativeBase, metadata
from acmwebsite.model.auth import User


presentation_author_table = Table(
    'presentation_author', metadata,
    Column('presentation_id', Integer,
           ForeignKey('presentation.id'), primary_key=True),
    Column('user_id', Integer,
           ForeignKey('tg_user.user_id'), primary_key=True))


class Presentation(DeclarativeBase):
    """A model that defines a club presentation.

    Presentations are slides, files, or other presentables that the club shares
    among its cohorts, usually during Meetings. They are displayed on the
    Presentation page.
    """
    __tablename__ = 'presentation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Unicode)
    description = Column(String(32))
    date = Column(DateTime, nullable=False)
    authors = relation(
        User,
        secondary=presentation_author_table,
        backref='presentations'
    )
