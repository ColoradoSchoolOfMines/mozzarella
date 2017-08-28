from tg import expose, redirect, validate, flash, url, lurl, abort, require, request
from tg.predicates import has_permission, not_anonymous

from acmwebsite.lib.base import BaseController
from acmwebsite.lib.helpers import log
from acmwebsite.model import DBSession, Survey, SurveyResponse, SurveyData, User

def survey_fields(survey):
    return [{'name': f.name, 'type': f.type} for f in survey.fields]

def response_to_dict(response):
    out = {'name': response.name, 'email': response.email}
    for item in response.data:
        out[item.field.name] = item.field.type_object().from_contents(item.contents)
    return out

class SurveyController(BaseController):
    def __init__(self, survey):
        self.survey = survey

    @expose('json')
    @require(has_permission('admin'))
    def results(self, number=None):
        responses = self.survey.responses or []
        responses = [response_to_dict(r) for r in responses]
        return {
            'count': len(responses),
            'responses': responses, 
            'fields': survey_fields(self.survey),
        }

    @expose('acmwebsite.templates.survey')
    def respond(self):
        if not self.survey:
            abort(404, 'No survey for meeting')

        if not self.survey.active:
            if not has_permission('admin'):
                abort(403, 'Survey not avalible')
                return
            flash('This page is currently disabled. You can see it because you are an admin.', 'warn')

        form = request.POST
        if form:
            user = request.identity and request.identity.get('user')
            response = SurveyResponse(user=user, provided_name=form.get('_provided_name'), survey=self.survey)
            DBSession.add(response)

            requires_ft = bool(form.get('first_time'))

            for f in self.survey.fields:
                if f.first_time and not requires_ft:
                    continue
                fo = f.type_object()
                v = fo.from_post(form)
                if v:
                    DBSession.add(SurveyData(response=response, field=f, contents=v))
            flash('Response submitted successfully')
            redirect(base_url='/')
        else:
            return {'survey': self.survey }

class SurveysController(BaseController):
    @expose()
    def _lookup(self, sid, *args):
        survey = DBSession.query(Survey).filter(Survey.id==sid).first()
        if not survey:
            abort(404, "No such survey")
        return SurveyController(survey), args
