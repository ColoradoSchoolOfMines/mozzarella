from tg import abort, expose, flash, redirect, request, require
from tg.predicates import has_permission

from acmwebsite.lib.base import BaseController
from acmwebsite.model import DBSession, Survey, SurveyData, SurveyResponse


class SurveyController(BaseController):
    def __init__(self, survey):
        self.survey = survey

    @expose('acmwebsite.templates.survey_results')
    @expose("json")
    @require(has_permission('admin'))
    def results(self, number=None, order_by=None, reverse=False):
        """Return results of surveys

        :param number: (optional) does nothing. Defaults to ``None``.
        :param order_by: (optional) which field to sort survey results by. 
            Defaults to ``None``.
        :param reverse: (optional) whether or not the returned results should be
            ascending. Defaults to ``False``.
        :return: Results of surveys, modified by parameters
        :rtype: Dictionary
        """
        if type(reverse) is str:
            reverse = reverse == 'True'

        if order_by:
            # TODO (#46): this doesn't work... If the column is nullable, then
            # the sort can't deal with comparing None types
            # order = '{} {}'.format(order_by, 'asc' if reverse else 'desc')
            # responses = self.survey.responses.order_by(order)
            responses = self.survey.responses
        else:
            responses = self.survey.responses

        # TODO (#46): This sucks. It would be good to have this done for us with
        # SQLAlchemy magic
        responses = [self._response_dict(r) for r in responses or []]

        survey_title = (self.survey.title or
                        (self.survey.meeting and self.survey.meeting.title) or
                        'Survey')
        return {
            'survey_id': self.survey.id,
            'title': survey_title,
            'count': len(responses),
            'responses': responses,
            'fields': self.survey.field_metadata(),
            'order_by': order_by,
            'reverse': reverse,
        }

    def _response_dict(self, response):
        """Creates a dictionary based on a single survey response

        :param response: which specific survey response is desired. This 
            function is called for each response in a survey.
        :return: a single survey response 
        :rtype: Dictionary
        """
        out = {'name': response.name, 'email': response.email}

        # Add the actual response data for the fields that exist.
        out.update({
            item.field.name:
            item.field.type_object().from_contents(item.contents)
            for item in response.data
        })

        return out

    @expose('acmwebsite.templates.survey')
    def respond(self):
        """Create an attendance survey form 

        :return: ``None`` or the survey passed into __init__
        :rtype: None or Dictionary
        """
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
    def _lookup(self, sid=None, *args):
        survey = DBSession.query(Survey).filter(Survey.id == sid).first()
        if not survey:
            abort(404, "No such survey")
        return SurveyController(survey), args
