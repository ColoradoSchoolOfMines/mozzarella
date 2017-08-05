from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Text, Unicode, DateTime

from acmwebsite.model import DeclarativeBase, metadata, DBSession

class Meeting(DeclarativeBase):
    __tablename__ = 'meeting'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    location = Column(Text)
    title = Column(Unicode, nullable=False)
    description = Column(Unicode)
