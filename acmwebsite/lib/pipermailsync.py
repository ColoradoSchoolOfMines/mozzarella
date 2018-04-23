import re
import requests
import email
import tg
import transaction
import email.policy
import logging
from acmwebsite.model import MailMessage, MailAttachment, DBSession
from sqlalchemy.sql import exists
from  depot.io.utils import FileIntent

log = logging.getLogger(__name__)

nextpart = '-------------- next part --------------\n'
archivefiles_p = re.compile(
    r'<td><A href="([a-zA-Z0-9_-]+\.txt)">\[ Text \d+ \w+ \]</a></td>')
fromline_p = re.compile(r'^From: (\w+) at ([A-Za-z0-9.-]+) \(([^\)]+)\)$')
fromline2_p = re.compile(r'^From: (\w+) at ([A-Za-z0-9.-]+)$')
subject_p = re.compile(r'^(?:\[ACMx?\] )?(.*)$')
scrubbed_p = re.compile(r'An? ([\w-]+) attachment was scrubbed...')


def parse_message(msgstring):
    return email.message_from_string(msgstring, policy=email.policy.default)


def parse_attachment(attstring):
    if not attstring:
        return

    m = scrubbed_p.match(attstring)
    if m:
        atype = m.group(1)
    else:
        return

    aparts = {}
    for line in attstring.splitlines():
        k, s, v = line.partition(': ')
        if not s:
            continue
        aparts[k.casefold()] = v

    if 'type' not in aparts.keys() and atype == 'HTML':
        aparts['type'] = 'text/html'

    if aparts.get('type') == 'application/pgp-signature':
        # Unfortunately, Mailman has a tendency to mutilate the
        # messages, so PGP signatures aren't useful :-(
        return False

    if 'url' not in aparts.keys() or '/private/' in aparts['url']:
        return

    r = requests.get(aparts['url'][1:-1])
    if not r.ok:
        log.warning("Failed to download attachment {}".format(r.url))
        return

    return FileIntent(r.content, aparts.get('name'), aparts.get('type'))


def get_plaintext_body(message):
    body = ""

    if message.is_multipart():
        for part in message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)
                break
    else:
        body = message.get_payload(decode=True)

    if isinstance(body, bytes):
        body = body.decode('utf-8')
    return body


def pmsync():
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
            message_id = message.get('message-id')
            date = email.utils.parsedate_to_datetime(
                message.get('date', '1 Jan 1970 00:00:00 -0000'))

            if (DBSession.query(MailMessage)
                         .filter(MailMessage.message_id == message_id)
                         .count()):
                # this is already in our databases
                transaction.commit()
                return

            m = subject_p.match(message.get('subject', ''))
            subject = m.group(1)

            body = get_plaintext_body(message)
            attachments = []
            while True:
                nbody, _, attstring = body.rpartition(nextpart)
                attachment = parse_attachment(attstring)
                if attachment is None:
                    break
                if attachment is not False:
                    attachments.append(attachment)
                body = nbody

            mm = MailMessage(
                message_id=message_id,
                from_=message.get('from'),
                date=date,
                subject=subject,
                body=body,
                parent_message_id=message.get('in-reply-to'))
            DBSession.add(mm)

            for f in reversed(attachments):
                DBSession.add(
                    MailAttachment(
                        message=mm,
                        file=f))

            DBSession.flush()

    transaction.commit()

