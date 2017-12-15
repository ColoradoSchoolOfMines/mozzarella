from tg import abort, expose, flash, redirect, request, require
from tg.predicates import has_permission

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, Survey, SurveyData, SurveyResponse


class SurveyController(BaseController):
    def __init__(self, survey):
        self.survey = survey

    @expose('acmwebsite.templates.survey_results')
    @require(has_permission('admin'))
    def results(self, number=None, order_by=None, reverse=False):
        if type(reverse) is str:
            reverse = reverse == 'True'

        responses = self._survey_responses()
        if order_by:
            responses.sort(key=lambda x: x.get(order_by), reverse=reverse)

        survey_title = (self.survey.title or
                        (self.survey.meeting and self.survey.meeting.title) or
                        'Survey')
        return {
            'survey': self.survey,
            'title': survey_title,
            'count': len(responses),
            'responses': responses,
            'fields': self.survey.field_metadata(),
            'order_by': order_by,
            'reverse': reverse,
        }

    @expose('json')
    @require(has_permission('admin'))
    def results_json(self, number=None):
        responses = self._survey_responses()
        return {
            'count': len(responses),
            'responses': responses,
            'fields': self.survey.field_metadata(),
        }

    def _response_dict(self, response):
        out = {'name': response.name, 'email': response.email}

        # Populate with the default value for the fields. This is necessary for
        # sorting if some respondents didn't fill out an optional field.
        for field in self.survey.fields:
            out[field.name] = field.type_object().default()

        # Override with the actual response data for the fields that exist.
        out.update({
            item.field.name:
            item.field.type_object().from_contents(item.contents)
            for item in response.data
        })

        return out

    def _survey_responses(self):
        responses = self.survey.responses or []
        return [self._response_dict(r) for r in responses]

    @expose('acmwebsite.templates.survey')
    def respond(self):
        if not self.survey:
            abort(404, 'No survey for meeting')

        if not self.survey.active:
            if not has_permission('admin'):
                abort(403, 'Survey not avalible')
                return
            flash('This page is currently disabled. You can see it because you are an admin.',
                  'warn')

        form = request.POST
        if form:
            user = request.identity and request.identity.get('user')
            response = SurveyResponse(
                user=user,
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
                    DBSession.add(
                        SurveyData(response=response, field=f, contents=v))
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
