from sqlalchemy import *
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, String, Unicode

from acmwebsite.model import DeclarativeBase, metadata, DBSession
from acmwebsite.lib.surveytypes import types

from ast import literal_eval

survey_field_table = Table('survey_field', metadata,
    Column('survey_id', Integer, ForeignKey('survey.id'), primary_key=True),
    Column('field_id', Integer, ForeignKey('field.id'), primary_key=True)
)

class Survey(DeclarativeBase):
    __tablename__ = 'survey'

    id = Column(Integer, autoincrement=True, primary_key=True)
    meeting = relation('Meeting', back_populates='survey', uselist=False)
    fields = relation('SurveyField', secondary=survey_field_table, backref='surveys', order_by='SurveyField.priority')
    opens = Column(DateTime)
    closes = Column(DateTime)

class SurveyField(DeclarativeBase):
    __tablename__ = 'field'

    id = Column(Integer, autoincrement=True, primary_key=True)

    # Name might be the same (eg. for radios, or surveys which share the same field names)
    # ...or they might be NULL entirely (for component groups maybe)
    name = Column(String(255), unique=False, nullable=True)

    label = Column(Unicode)
    type = Column(String, nullable=False)
    params = Column(String, default='{}')
    priority = Column(Float, default=0)
    first_time = Column(Boolean, default=False)

    def field_object(self):
        return types[self.type](name=self.name, on_first_time=self.first_time, **literal_eval(self.params))

class SurveyResponse(DeclarativeBase):
    __tablename__ = 'response'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('tg_user.user_id'))
    user = relation('User')
    provided_name = Column(Unicode(255))
    survey_id = Column(Integer, ForeignKey('survey.id'), nullable=False)
    survey = relation('Survey', backref='responses')

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


class SurveyData(DeclarativeBase):
    __tablename__ = 'response_data'

    response_id = Column(Integer, ForeignKey('response.id'), primary_key=True, nullable=False)
    response = relation('SurveyResponse', backref='data')
    field_id = Column(Integer, ForeignKey('field.id'), primary_key=True, nullable=False)
    field = relation('SurveyField', backref='responses')
    contents = Column(Unicode, nullable=False)