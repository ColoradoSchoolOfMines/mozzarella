from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, String, Unicode

from acmwebsite.lib.surveytypes import types
from acmwebsite.model import DeclarativeBase, metadata

survey_field_table = Table(
    'survey_field', metadata,
    Column('survey_id', Integer, ForeignKey('survey.id'), primary_key=True),
    Column('field_id', Integer, ForeignKey('field.id'), primary_key=True))


class Survey(DeclarativeBase):
    __tablename__ = 'survey'

    id = Column(Integer, autoincrement=True, primary_key=True)
    meeting = relation('Meeting', back_populates='survey', uselist=False)
    fields = relation(
        'SurveyField',
        secondary=survey_field_table,
        backref='surveys',
        order_by='SurveyField.priority')
    title = Column(Unicode)
    opens = Column(DateTime)
    closes = Column(DateTime)

    @property
    def active(self):
        now = datetime.now()
        return self.opens and self.opens < now and (not self.closes or self.closes > now)

    def field_metadata(self):
        return [{'name': f.name, 'type': f.type} for f in self.fields]


class SurveyField(DeclarativeBase):
    __tablename__ = 'field'

    id = Column(Integer, autoincrement=True, primary_key=True)
    type = Column(String(255), nullable=False)
    priority = Column(Float, default=0)
    name = Column(String(255), unique=True, nullable=False)
    label = Column(Unicode)
    required = Column(Boolean, default=False)
    first_time = Column(Boolean, default=False)
    placeholder = Column(Unicode)
    value = Column(Unicode)
    options = Column(Unicode)
    min = Column(Float)
    max = Column(Float)
    step = Column(Float)

    def type_object(self):
        return types[self.type](
            name=self.name,
            label=self.label,
            required=self.required,
            first_time=self.first_time,
            placeholder=self.placeholder,
            value=self.value,
            options=self.options,
            min=self.min,
            max=self.max,
            step=self.step,
        )


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
        return (self.user and self.user.display_name) or self.provided_name

    @property
    def email(self):
        return self.user and self.user.email_address


class SurveyData(DeclarativeBase):
    __tablename__ = 'response_data'

    response_id = Column(Integer, ForeignKey('response.id'), primary_key=True, nullable=False)
    response = relation('SurveyResponse', backref='data')
    field_id = Column(Integer, ForeignKey('field.id'), primary_key=True, nullable=False)
    field = relation('SurveyField', backref='responses')
    contents = Column(Unicode, nullable=False)
