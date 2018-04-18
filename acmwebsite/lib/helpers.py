# -*- coding: utf-8 -*-
"""Template Helpers used in acm-website."""
import logging
import markdown as md
import docutils.core
from markupsafe import Markup
from datetime import datetime, time, timedelta
import tg

log = logging.getLogger(__name__)

# The mmadmin object
from acmwebsite.lib.mailmanapi import ListAdminAPI
mmadmin = ListAdminAPI(tg.config.get('mailman.url'), tg.config.get('mailman.secret'))


def current_year():
    now = datetime.now()
    return now.strftime('%Y')


def rst(source, multipar=False):
    """
    Parse a simple paragraph of reStructuredText. Methods which need
    more complicated things (like parsing a whole document) should
    use ``docutils.core.publish_parts`` directly.

    If ``multipar`` is ``True``, then this will allow multiple
    paragraphs.

    See http://docutils.sourceforge.net/docutils/examples.py for an
    example.
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
    day_fmt = '{0:%A}, ' if show_day else ''
    date_fmt = '{0.day} {0:%B %Y}'
    time_fmt = '{0:%H}:{0:%M}'
    if isinstance(datetime_obj, datetime):
        if not isinstance(duration, timedelta):
            # Format date without duration
            # For example, assume:
            #     datetime_obj = datetime(year=2017, month=10, day=31,
            #                             hour=17, minute=0, second=0)
            #     show_day = True
            # This will return:
            #     'Tuesday, 31 October 2017 at 17:00'
            return (day_fmt + date_fmt + ' at ' + time_fmt).format(datetime_obj)
        else:
            # Format date with duration if duration is not default
            # For example, assume:
            #     datetime_obj = datetime(year=2017, month=10, day=31,
            #                             hour=17, minute=0, second=0)
            #     show_day = True
            #     duration = timedelta(hours=3)
            # This will return:
            #     'Tuesday, 31 October 2017 from 17:00-20:00'

            default_duration = int(tg.config.get('meetings.default_duration'))
            if duration == timedelta(seconds=default_duration):
                return (day_fmt + date_fmt + ' at ' + time_fmt).format(datetime_obj)
            else:
                duration_str = (day_fmt + date_fmt + ' from ' + time_fmt).format(datetime_obj)
                duration_str += '-' + time_fmt.format(datetime_obj + duration)
                return duration_str
    if isinstance(datetime_obj, date):
        return (day_fmt + date_fmt).format(datetime_obj)
    if isinstance(datetime_obj, time):
        return (time_fmt).format(datetime_obj)


def proccess_attr(name, attr):
    if attr == True:
        return name
    if not attr:
        return None
    return attr


def strip_attrs(ty, *args):
    return {v: proccess_attr(v, getattr(ty, v)) for v in args}


def field_cn(ty, *args):
    args = [x for x in args if x]
    if ty.first_time:
        args.append('on-first-time')
    return ' '.join(args)


# Import commonly used helpers from WebHelpers2 and TG
from tg.util.html import script_json_encode

try:
    from webhelpers2 import date, html, number, misc, text
except SyntaxError:
    log.error("WebHelpers2 helpers not available with this Python Version")
