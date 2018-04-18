# -*- coding: utf-8 -*-
import re
import requests
import email
import tg
import transaction
import email.policy
from acmwebsite.model import MailMessage, DBSession
from acmwebsite.lib.helpers import log
from sqlalchemy.sql import exists

archivefiles_p = re.compile(r'<td><A href="([a-zA-Z0-9_-]+\.txt)">\[ Text \d+ \w+ \]</a></td>')
fromline_p = re.compile(r'^From: (\w+) at ([A-Za-z0-9.-]+) \(([^\)]+)\)$')
fromline2_p = re.compile(r'^From: (\w+) at ([A-Za-z0-9.-]+)$')
subject_p = re.compile(r'^(?:\[ACMx?\] )?(.*)$')
completed_one = False

def parse_message(msgstring):
    return email.message_from_string(msgstring, policy=email.policy.default)

def get_plaintext_body(message):
    body = ""

    if message.is_multipart():
        for part in message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    else:
        body = message.get_payload(decode=True)

    if isinstance(body, bytes):
        body = body.decode('utf-8')

    return body

def pmsync():
    log.info("Starting mail sync from pipermail")
    global completed_one
    session = requests.Session()
    pmurl = tg.config.get("mailman.pipermail.url")
    r = session.get(pmurl)
    r.raise_for_status()
    for m in archivefiles_p.finditer(r.text):
        name = m.group(1)
        log.info("Syncing archive {}...".format(name))
        ar = session.get(pmurl + "/" + name)
        lines = ar.text.splitlines()
        messages = []
        msglines = []
        for line, nextline in zip(lines, lines[1:] + ['']):
            m1 = fromline_p.match(line)
            m2 = fromline2_p.match(line)
            if line.startswith("From ") and nextline.startswith("From: ") and msglines:
                messages.append(parse_message('\n'.join(msglines)))
                msglines = []
            elif m1:
                msglines.append('From: "{}" <{}@{}>'.format(m1.group(3), m1.group(1), m1.group(2)))
            elif m2:
                msglines.append('From: {}@{}'.format(m2.group(1), m2.group(2)))
            else:
                msglines.append(line)
        messages.append(parse_message('\n'.join(msglines)))
        for message in messages:
            if DBSession.query(MailMessage).filter(MailMessage.message_id == message.get('message-id')).count():
                # this is already in our databases
                continue
            m = subject_p.match(message.get('subject', ''))
            subject = m.group(1)
            DBSession.add(
                MailMessage(
                    message_id=message.get('message-id'),
                    from_=message.get('from'),
                    date=email.utils.parsedate_to_datetime(message.get('date', '1 Jan 1970 00:00:00 -0000')),
                    subject=subject,
                    body=get_plaintext_body(message),
                    parent_message_id=message.get('in-reply-to'))
            )
        DBSession.flush()
        if completed_one:
            transaction.commit()
            log.info("Stopping sync for now as I think I have done everything else recently")
            return
    completed_one=True
    transaction.commit()
    log.info("Complete sync finished")

