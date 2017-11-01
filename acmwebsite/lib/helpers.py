# -*- coding: utf-8 -*-
"""Template Helpers used in acm-website."""
import logging
import markdown as md
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


def markdown(*args, strip_par=False, **kwargs):
    res = md.markdown(*args, **kwargs)
    if strip_par:
        res = res.replace('<p>', '').replace('</p>', '')
    return Markup(res)


def icon(icon_name):
    return Markup('<i class="glyphicon glyphicon-%s"></i>' % icon_name)


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
            # Format date with duration
            # For example, assume:
            #     datetime_obj = datetime(year=2017, month=10, day=31,
            #                             hour=17, minute=0, second=0)
            #     show_day = True
            #     duration = timedelta(hours=3)
            # This will return:
            #     'Tuesday, 31 October 2017 from 17:00-20:00'
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
