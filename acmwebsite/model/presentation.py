"""Defines the Presentation model.

Presentations are slides, files, or other presentables that the club shares
among its cohorts, usually during Meetings.
"""

from sqlalchemy import Column
from sqlalchemy.types import Integer

from acmwebsite.model import DeclarativeBase


class Presentation(DeclarativeBase):
    """A model that defines a club presentation.

    Presentations are slides, files, or other presentables that the club shares
    among its cohorts, usually during Meetings. They are displayed on the
    Presentation page.
    """
    __tablename__ = 'presentation'

    id = Column(Integer, primary_key=True)
