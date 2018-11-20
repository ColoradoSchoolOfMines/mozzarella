"""Defines the Presentation model.

Presentations are slides, files, or other presentables that the club shares
among its cohorts, usually during Meetings.
"""

import tarfile
import datetime

import magic
import yaml
import bleach
from sqlalchemy import Column, orm, Table, ForeignKey
from sqlalchemy.types import Integer
from sqlalchemy.orm import relation
from depot.fields.sqlalchemy import UploadedFileField

from acmwebsite.model import DeclarativeBase, Group, metadata
from acmwebsite.model.auth import User
from acmwebsite.lib.helpers import rst


presentation_user_xref = Table('author_users', metadata,
                               Column('presentation_id',
                                      Integer,
                                      ForeignKey('presentation.id'),
                                      primary_key=True),
                               Column('user_id',
                                      Integer,
                                      ForeignKey('tg_user.user_id'),
                                      primary_key=True)
)


class Presentation(DeclarativeBase):
    """A model that defines a club presentation.

    Presentations are slides, files, or other presentables that the club shares
    among its cohorts, usually during Meetings. They are displayed on the
    Presentation page.
    """
    __tablename__ = 'presentation'

    id = Column(Integer, primary_key=True)
    tarball = Column(UploadedFileField)
    authors = relation('User', secondary=presentation_user_xref,
                       backref='presentations')

    @orm.reconstructor
    def init_on_load(self):
        # currently only supports tarfiles with .gz, .bz2, and .xz compression
        tarf = tarfile.open(self.tarball.file) # will automatically decompress

        self._meta = yaml.safe_load(tarf.extractfile('metadata.yaml'))

        # ensure every dict key is lowercase
        for k in self._meta:
            if isinstance(k, str) and k.lower() != k:
                self._meta[k.lower()] = self._meta.pop(k)

        # if magic.detect_from_fobj(self.tarball.file).mime_type == ''
        tarball_type = magic.detect_from_fobj(self.tarball.file).mime_type
        if tarball_type in decompression_funcs:
            archive = decompression_funcs[tarball_type](self.tarball.file)
        # now assuming it is a .tar file
        tocf = archive.extractfile('metadata.yaml')
        metadata = yaml.safe_load(tocf.read())

    @property
    def title(self):
        return bleach.clean(self._meta['title'] if 'title' in self._meta
                            else 'No title')

    @property
    def title_rst(self):
        return rst(self.title)

    @property
    def description(self):
        return bleach.clean(self._meta['description'] if 'description' in
                            self._meta else 'No description')

    @property
    def description_rst(self):
        return rst(self.description)

    @property
    def date(self):
        if not isinstance(datetime.date, self._meta['date']):
            raise TypeError('Invalid date format')
        return self._meta['date']

    @property
    def user(self):
        return User.by_id(self.user_id)
