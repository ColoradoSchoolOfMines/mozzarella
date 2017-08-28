# -*- coding: utf-8 -*-
"""Profile controller module"""

from tg import expose, redirect, validate, flash, url, lurl, abort, require, request

from acmwebsite.lib.base import BaseController
from acmwebsite.lib.helpers import log
from acmwebsite.model import DBSession, Meeting

class MeetingController(BaseController):
    def __init__(self, meeting):
        self.meeting = meeting

    @expose()
    def survey(self, *args):
        survey = self.meeting.survey
        if not survey:
            abort(404, "No survey for meeting")
        redirect('/s/{}/{}'.format(self.meeting.survey.id, '/'.join(args)))

class MeetingsController(BaseController):
    @expose()
    def _lookup(self, mid, *args):
        meeting = DBSession.query(Meeting).filter(Meeting.id==mid).first()
        if not meeting:
            abort(404, "No such meeting")
        return MeetingController(meeting), args

