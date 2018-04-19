# -*- coding: utf-8 -*-
"""Project model module."""

from sqlalchemy.orm import relationship
from sqlalchemy import Table, ForeignKey, Column, UniqueConstraint
from sqlalchemy.types import Integer, Unicode

from depot.fields.sqlalchemy import UploadedFileField
from depot.fields.specialized.image import UploadedImageWithThumb

from acmwebsite.model import DeclarativeBase, metadata, User

team_table = Table(
    'team',
    metadata,
    Column('user_id', Integer(),
           ForeignKey('tg_user.user_id'), nullable=False),
    Column('project_id', Integer(), ForeignKey('projects.id'), nullable=False),
    UniqueConstraint('user_id', 'project_id'),
)


class Project(DeclarativeBase):
    """A model that defines a project that the club is working on."""
    __tablename__ = 'projects'

    # Fields
    id = Column(Integer, autoincrement=True, primary_key=True)
    team_members = relationship(User, secondary=team_table,
                                back_populates='projects')
    name = Column(Unicode(1024), unique=True, nullable=False)
    description = Column(Unicode(4096))
    website = Column(Unicode(512))
    repository = Column(Unicode(512))
    video_url = Column(Unicode(512))
    image = Column(UploadedFileField(upload_type=UploadedImageWithThumb))
