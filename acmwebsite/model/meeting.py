from sqlalchemy import *
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import mapper, relation
from sqlalchemy.types import DateTime, Integer, Text, Unicode

from acmwebsite.model import DBSession, DeclarativeBase, metadata


class Meeting(DeclarativeBase):
    __tablename__ = 'meeting'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    location = Column(Text)
    title = Column(Unicode, nullable=False)
    description = Column(Unicode)
    survey_id = Column(Integer, ForeignKey('survey.id'), nullable=True, unique=True)
    survey = relation("Survey", back_populates="meeting")
