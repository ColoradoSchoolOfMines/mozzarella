import datetime
import pytz

from icalendar import Calendar, Event
from tg import expose, response, request, config

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
        """ Returns the iCalendar version of the schedule """
        cal = Calendar()
        cal.add('prodid', config.get('meetings.icalendar.prodid'))
        cal.add('version', '2.0')
        default_duration = datetime.timedelta(
            seconds=int(config.get('meetings.default_duration'))
        )

        for m in self.meetings.all():
            event = Event()
            event.add('summary', m.title)
            event.add('description', m.description)
            event.add('location', m.location)
            d = m.date.replace(tzinfo=pytz.timezone(config.get('meetings.timezone')))
            event.add('dtstart', d)
            event.add('dtend', d + default_duration)
            event.add('dtstamp', d)

            cal.add_component(event)

        return cal.to_ical()
