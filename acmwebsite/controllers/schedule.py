import datetime

from icalendar import Calendar, Event
from tg import expose, response, request

from acmwebsite.lib.base import BaseController
from acmwebsite.lib.helpers import log
from acmwebsite.model import DBSession, Meeting


class ScheduleController(BaseController):
    def __init__(self):
        self.meetings = DBSession.query(Meeting).order_by(Meeting.date)

    @expose('acmwebsite.templates.schedule')
    @expose(content_type='text/calendar')
    def index(self):
        """
        Handle the schedule page. If the request is for the .ics file, it will
        return the schedule in iCal format.
        """
        if request.response_type == 'text/calendar':
            return self.ical_schedule()

        # Filter meetings that occurred in the past
        upcoming_meetings = self.meetings.filter(
            Meeting.date > datetime.datetime.now() - datetime.timedelta(hours=3)
        ).all()

        return dict(page='schedule', meetings=upcoming_meetings)

    def ical_schedule(self):
        """ Returns the iCal version of the ACM schedule """
        cal = Calendar()
        cal.add('prodid', '-//Mines ACM//web//EN')
        cal.add('version', '2.0')

        for m in self.meetings.all():
            event = Event()
            event.add('summary', m.title)
            event.add('description', m.description)
            event.add('location', m.location)
            event.add('dtstart', m.date)
            event.add('dtend', m.date + datetime.timedelta(hours=2))
            event.add('dtstamp', m.date)

            cal.add_component(event)

        return cal.to_ical()
