from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, String, Unicode

from acmwebsite.model import DeclarativeBase, metadata, DBSession

survey_field_table = Table('survey_field', metadata,
    Column('survey_id', Integer, ForeignKey('survey.id'), primary_key=True),
    Column('field_id', Integer, ForeignKey('field.id'), primary_key=True)
)

class Survey(DeclarativeBase):
    __tablename__ = 'survey'

    id = Column(Integer, autoincrement=True, primary_key=True)
    active = Column(Boolean, default=False)
    avalible = Column(Boolean, default=True)
    meeting = relation("Meeting", back_populates="survey", uselist=False)
    fields = relation("Field", secondary=survey_field_table, backref="surveys")

class Field(DeclarativeBase):
    __tablename__ = 'field'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    ty = Column(String(63), nullable=False)
    vertical = Column(Float, default=0)
    style = Column(String(63), default="basic")
    required = Column(Boolean, default=False)

class Response(DeclarativeBase):
    __tablename__ = 'response'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('tg_user.user_id'))
    user = relation("User")
    provided_name = Column(Unicode(255))
    survey_id = Column(Integer, ForeignKey('survey.id'), nullable=False)
    survey = relation("Survey", backref="responses")

    @property
    def name(self):
        if self.user == None:
            return self.provided_name
        else:
            return self.user.display_name

    @property
    def email(self):
        if self.user == None:
            return None
        else:
            return self.user.email_address


class ResponseData(DeclarativeBase):
    __tablename__ = 'response_data'

    response_id = Column(Integer, ForeignKey('response.id'), primary_key=True, nullable=False)
    response = relation("Response", backref="data")
    field_id = Column(Integer, ForeignKey('field.id'), primary_key=True, nullable=False)
    field = relation("Field", backref="responses")
    contents = Column(Unicode, nullable=False)