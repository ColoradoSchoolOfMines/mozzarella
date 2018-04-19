# -*- coding: utf-8 -*-
"""Defines the Banner model.

Banners are the images displayed on the website's fron page with a description.
"""

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode

from depot.fields.sqlalchemy import UploadedFileField
from depot.fields.specialized.image import UploadedImageWithThumb

from acmwebsite.model import DeclarativeBase


class Banner(DeclarativeBase):
    """A model that defines the photos that are dispalyed on the website's main
    page. Includes the photo itself and a short description which is shown just
    below the photo.
    """
    __tablename__ = 'banner'

    id = Column(Integer, autoincrement=True, primary_key=True)
    photo = Column(UploadedFileField(upload_type=UploadedImageWithThumb))
    description = Column(Unicode(2048), unique=True)
