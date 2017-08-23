# -*- coding: utf-8 -*-
"""Profile controller module"""

from tg import expose, redirect, validate, flash, url, lurl, abort

from acmwebsite.lib.base import BaseController
from acmwebsite.lib.helpers import log
from acmwebsite.model import DBSession, Survey, Meeting

from sqlalchemy import func

__all__ = ['SurveyController']

def survey_feilds(survey):
    return [{'name': f.name, 'type': f.ty} for f in survey.fields]

def response_to_dict(response):
    out = {'name': response.name, 'email': response.email}
    for item in response.data:
        out[item.field.name] = item.contents
    return out

class MeetingController(BaseController):
    def __init__(self, meeting):
        self.meeting = meeting

    @expose()
    def _default(self):
        return "Hello, world!"

    @expose('json')
    def survey(self, number=None):
        survey = self.meeting.survey
        if not survey:
            abort(404, "No survey for meeting")
        responses = survey.responses if survey.responses else []
        responses = [response_to_dict(r) for r in responses]
        return {
            'count': len(responses),
            'responses': responses, 
            'fields': survey_feilds(survey),
            'meeting': self.meeting.title,
            'date': self.meeting.date
        }

class MeetingsController(BaseController):
    @expose()
    def _lookup(self, date, *args):
        meeting = DBSession.query(Meeting).filter(func.date(Meeting.date) == date).first()
        if not meeting:
            abort(404, "No such meeting")
        return MeetingController(meeting), args

