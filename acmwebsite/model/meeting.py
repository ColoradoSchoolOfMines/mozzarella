import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import DateTime, Integer, Text, Unicode

from tg import config

from acmwebsite.model import DeclarativeBase


class Meeting(DeclarativeBase):
    __tablename__ = 'meeting'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=True)
    location = Column(Text)
    title = Column(Unicode, nullable=False)
    description = Column(Unicode)
    survey_id = Column(Integer, ForeignKey('survey.id'), nullable=True, unique=True)
    survey = relation("Survey", back_populates="meeting")

    def get_duration(self):
        return datetime.timedelta(seconds=self.duration or
                                  int(config.get('meetings.default_duration')))
