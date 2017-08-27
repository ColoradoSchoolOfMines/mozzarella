# -*- coding: utf-8 -*-
"""Profile controller module"""

import tg
from tg import expose, redirect, validate, flash, url, lurl, abort, require, request

from acmwebsite.lib.base import BaseController
from acmwebsite.lib.helpers import log
from acmwebsite.model import DBSession, Survey, Meeting, SurveyResponse, SurveyData, User

from sqlalchemy import func

__all__ = ['SurveyController']

def survey_fields(survey):
    return [{'name': f.name, 'type': f.type} for f in survey.fields]

def response_to_dict(response):
    out = {'name': response.name, 'email': response.email}
    for item in response.data:
        out[item.field.name] = item.field.field_object().parse(item.contents)
    return out

class MeetingController(BaseController):
    def __init__(self, meeting):
        self.meeting = meeting

    @expose()
    def _default(self):
        return "Hello, world!"

    @expose('json')
    @require(tg.predicates.has_permission('admin'))
    def results(self, number=None):
        survey = self.meeting.survey
        if not survey:
            abort(404, "No survey for meeting")
        responses = survey.responses if survey.responses else []
        responses = [response_to_dict(r) for r in responses]
        return {
            'count': len(responses),
            'responses': responses, 
            'fields': survey_fields(survey),
            'meeting': self.meeting.title,
            'date': self.meeting.date
        }

    @expose('acmwebsite.templates.survey')
    @require(tg.predicates.not_anonymous())
    def attend(self):
        survey = self.meeting.survey
        if not survey:
            abort(404, "No survey for meeting")

        user = User.by_user_name(request.identity['repoze.who.userid'])

        form = request.POST
        if form:
            response = SurveyResponse(user=user, survey=survey)
            DBSession.add(response)

            for f in survey.fields:
                fo = f.field_object()
                v = fo.value(form)
                if v:
                    DBSession.add(SurveyData(response=response, field=f, contents=v))
            flash('Response submitted successfully')
            redirect(base_url='/')
        else:
            return {'meeting': self.meeting, 'fields': survey.fields }

class MeetingsController(BaseController):
    @expose()
    def _lookup(self, mid, *args):
        meeting = DBSession.query(Meeting).filter(Meeting.id==mid).first()
        if not meeting:
            abort(404, "No such meeting")
        return MeetingController(meeting), args

