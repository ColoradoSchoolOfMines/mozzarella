# -*- coding: utf-8 -*-
from acmwebsite.model import DeclarativeBase
from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode
from depot.fields.sqlalchemy import UploadedFileField
from depot.fields.specialized.image import UploadedImageWithThumb


class Banner(DeclarativeBase):
    __tablename__ = 'banner'

    id = Column(Integer, autoincrement=True, primary_key=True)
    photo = Column(UploadedFileField(upload_type=UploadedImageWithThumb))
    description = Column(Unicode(2048), unique=True)
