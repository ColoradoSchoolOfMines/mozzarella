"""Defines the Presentation model.

Presentations are slides, files, or other presentables that the club shares
among its cohorts, usually during Meetings.
"""

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import relation
from sqlalchemy.types import Date, Integer, String, Unicode

from acmwebsite.model import DeclarativeBase, metadata
from acmwebsite.model.auth import User
from depot.fields.specialized.image import UploadedImageWithThumb
from depot.fields.sqlalchemy import UploadedFileField

presentation_author_table = Table(
    'presentation_author', metadata,
    Column(
        'presentation_id',
        Integer,
        ForeignKey('presentation.id'),
        primary_key=True),
    Column(
        'user_id', Integer, ForeignKey('tg_user.user_id'), primary_key=True))


class PresentationFile(DeclarativeBase):
    """A model that defines a file which is associated with a presentation."""
    __tablename__ = 'presentation_file'

    id = Column(Integer, primary_key=True, autoincrement=True)
    presentation_id = Column(Integer, ForeignKey('presentation.id'), nullable=False)
    description = Column(String(32), nullable=False)
    file = Column(UploadedFileField)

    def __init__(self, description, file):
        self.description = description
        self.file = file

    @property
    def icon(self):
        icons = {'application/pdf': 'fa-file-pdf-o'}
        return icons.get(self.file.content_type, 'fa-file-code-o')

    @property
    def url(self):
        return self.file.url


class Presentation(DeclarativeBase):
    """A model that defines a club presentation.

    Presentations are slides, files, or other presentables that the club shares
    among its cohorts, usually during Meetings. They are displayed on the
    Presentation page.
    """
    __tablename__ = 'presentation'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(32), nullable=False)
    description = Column(Unicode)
    date = Column(Date, nullable=False)
    thumbnail = Column(UploadedFileField(upload_type=UploadedImageWithThumb))
    repo_url = Column(Unicode(512))

    authors = relation(
        User, secondary=presentation_author_table, backref='presentations')
    files = relation(PresentationFile)

    @property
    def page_buttons(self):
        buttons = [
            (self.repo_url, 'View repo',
             'fa-code-fork') if self.repo_url else None,
        ]
        for file in self.files:
            buttons.append((file.url, file.description, file.icon))

        return buttons
