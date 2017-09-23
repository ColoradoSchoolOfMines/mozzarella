import datetime

from icalendar import Calendar, Event
from tg import expose, response

from acmwebsite.lib.base import BaseController
from acmwebsite.lib.helpers import log
from acmwebsite.model import DBSession, Meeting


class ScheduleController(BaseController):
    def __init__(self):
        self.meetings = DBSession.query(Meeting).order_by(Meeting.date).all()

    @expose('acmwebsite.templates.schedule')
    @expose('json', exclude_names=['page'])
    def _index(self):
        """Handle the schedule page."""

        # Allow CORS
        response.headers.add("Access-Control-Allow-Origin", "*")
        return dict(page='schedule', meetings=self.meetings.filter(
            Meeting.date > datetime.datetime.now() - datetime.timedelta(hours=3)
        ))

    @expose(content_type='text/calendar')
    def acm(self):
        cal = Calendar()
        cal.add('prodid', '-//Mines ACM//web//EN')
        cal.add('version', '2.0')

        for m in self.meetings:
            event = Event()
            event.add('summary', m.title)
            event.add('description', m.description)
            event.add('location', m.location)
            event.add('dtstart', m.date)
            event.add('dtend', m.date + datetime.timedelta(hours=2))
            event.add('dtstamp', m.date)
            cal.add_component(event)

        return cal.to_ical()
