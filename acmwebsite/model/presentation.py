"""Defines the Presentation model.

Presentations are slides, files, or other presentables that the club shares
among its cohorts, usually during Meetings.
"""

import tarfile

import yaml
from sqlalchemy import Column, orm
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
    tarball = Column(UploadedFileField)

    @orm.reconstructor
    def init_on_load(self):
        # currently only supports tarfiles with .gz, .bz2, and .xz compression
        tarf = tarfile.open(self.tarball.file) # will automatically decompress

        self._meta = yaml.safe_load(tarf.extractfile('metadata.yaml'))

        # ensure every dict key is lowercase
        for k in self._meta:
            if isinstance(k, str) and k.lower() != k:
                self._meta[k.lower()] = self._meta.pop(k)
