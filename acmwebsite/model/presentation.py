"""Defines the Presentation model.

Presentations are slides, files, or other presentables that the club shares
among its cohorts, usually during Meetings.
"""

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, Unicode, String, Date

from depot.fields.sqlalchemy import UploadedFileField
from depot.fields.specialized.image import UploadedImageWithThumb

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
    title = Column(String(32), nullable=False)
    description = Column(Unicode)
    date = Column(Date, nullable=False)
    thumbnail = Column(UploadedFileField(upload_type=UploadedImageWithThumb))
    authors = relation(
        User,
        secondary=presentation_author_table,
        backref='presentations'
    )
    repo_url = Column(Unicode(512))
    slides_pdf = Column(UploadedFileField)
    latex_source = Column(UploadedFileField)

    @property
    def page_buttons(self):
        return dict(
            repo_url=(self.repo_url,
                      'View repo', 'fa fa-github') if self.repo_url else None,
            slides_pdf=(self.slides_pdf.url,
                        'View Slides PDF', 'fa fa-file-pdf-o') if self.slides_pdf else None,
            latex_source=(self.latex_source.url,
                          'View LaTeX source', 'fa fa-file-code-o') if self.latex_source else None,
        )
