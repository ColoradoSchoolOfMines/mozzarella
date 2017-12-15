from tg import expose, redirect, flash, abort, require, request
from tg.predicates import has_permission

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, Survey, SurveyResponse, SurveyData


def response_dict(response, fields):
    out = {
        'name': response.name,
        'email': response.email,
    }

    # Populate with the default value for the fields. This is necessary for
    # sorting if some respondents didn't fill out an optional field.
    for field in fields:
        out[field.name] = field.type_object().default()

    # Override with the actual response data for the fields that exist.
    for item in response.data:
        out[item.field.name] = item.field.type_object().from_contents(item.contents)

    return out


class SurveyController(BaseController):
    def __init__(self, survey):
        self.survey = survey

    @expose('acmwebsite.templates.survey_results')
    @require(has_permission('admin'))
    def results(self, number=None, order_by=None, reverse=False):
        if type(reverse) is str:
            reverse = reverse == 'True'

        responses = self.survey.responses or []
        responses = [response_dict(r, self.survey.fields) for r in responses]
        if order_by:
            responses = sorted(responses,
                               key=lambda x: x.get(order_by),
                               reverse=reverse)

        return {
            'survey': self.survey,
            'title': (self.survey.title or
                      (self.survey.meeting and self.survey.meeting.title) or
                      'Survey'),
            'count': len(responses),
            'responses': responses,
            'fields': self.survey.field_metadata(),
            'order_by': order_by,
            'reverse': reverse,
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
            response = SurveyResponse(user=user,
                                      provided_name=form.get('_provided_name'),
                                      survey=self.survey)
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
            return {'survey': self.survey}


class SurveysController(BaseController):
    @expose()
    def _lookup(self, sid, *args):
        survey = DBSession.query(Survey).filter(Survey.id == sid).first()
        if not survey:
            abort(404, "No such survey")
        return SurveyController(survey), args
