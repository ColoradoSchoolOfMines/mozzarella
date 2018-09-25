"""
Templating helper functions for generating views in Mozzarella.
"""
import docutils.core
from markupsafe import Markup
from datetime import datetime, time, timedelta
import tg


def rst(source, multipar=False):
    """Parse a simple paragraph of reStructuredText. Methods which need
    more complicated things (like parsing a whole document) should
    use ``docutils.core.publish_parts`` directly. [1]_

    If ``multipar`` is ``True``, then this will allow multiple
    paragraphs.

    .. [1] See http://docutils.sourceforge.net/docutils/examples.py
           for an example.
    """
    body = docutils.core.publish_parts(
        source,
        writer_name='html',
        settings_overrides={
            'file_insertion_enabled': 0,
            'raw_enabled': 0})['body']
    if not multipar:
        body = body.replace('<p>', '').replace('</p>', '')
    return Markup(body)


def ftime(datetime_obj, duration=None, show_day=False):
    """
    Format a ``date``, ``datetime``, or ``time`` object for view on
    the page. Optionally takes a duration to show a range of time.

    :param datetime_obj: A ``date``, ``datetime`` or ``time`` to format.
    :param duration: A ``timedelta`` indicating how long something
                     lasts.
    :param show_day: Show the day of the week.
    :rtype: string

    >>> t = datetime(year=2017, month=10, day=31, hour=17, minute=0, second=0)
    >>> ftime(t, show_day=True)
    'Tuesday, 31 October 2017 at 17:00'
    >>> duration = timedelta(hours=3)
    >>> ftime(t, duration=duration, show_day=True)
    'Tuesday, 31 October 2017 from 17:00-20:00'

    .. admonition:: Changed from early Mozzarella

        No special behavior when the duration is the default duration.
        Always show the duration if given: you must explicity pass
        ``None`` for the duration if you do not want it to show.

    """
    day_fmt = '{0:%A}, ' if show_day else ''
    date_fmt = '{0.day} {0:%B %Y}'
    time_fmt = '{0:%H}:{0:%M}'
    if isinstance(datetime_obj, datetime):
        if duration is None:
            # Format date without duration
            return (day_fmt + date_fmt + ' at ' + time_fmt).format(datetime_obj)
        elif isinstance(duration, timedelta):
            # Format date with duration
            duration_str = (day_fmt + date_fmt + ' from ' + time_fmt).format(datetime_obj)
            duration_str += '-' + time_fmt.format(datetime_obj + duration)
            return duration_str
        else:
            raise TypeError("duration must be a timedelta")
    if isinstance(datetime_obj, date):
        return (day_fmt + date_fmt).format(datetime_obj)
    if isinstance(datetime_obj, time):
        return (time_fmt).format(datetime_obj)
