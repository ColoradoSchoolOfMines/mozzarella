import concurrent.futures
import requests
import re

from acmwebsite.lib.mpapi_connector import uidinfo



class MailmanSession(requests.Session):
    def __init__(self, admin_url, admin_auth):
        super().__init__()
        self.admin_url = admin_url
        self.admin_auth = admin_auth

    def authenticate(self):
        if self.admin_url is None or self.admin_auth is None:
            raise ValueError("admin_url or admin_auth is not set")
        r = super().post(self.admin_url, data={"adminpw": self.admin_auth})
        r.raise_for_status()

    def get(self, *args, **kwargs):
        r = super().get(*args, **kwargs)

        if "Let me in..." in r.text:
            # Mailman wants us to authenticate
            self.authenticate()

            # Redo the GET request
            return super().get(*args, **kwargs)

        return r

    def post(self, *args, **kwargs):
        r = super().post(*args, **kwargs)

        if "Let me in..." in r.text:
            # Mailman wants us to authenticate
            self.authenticate()

            # Redo the POST request
            return super().post(*args, **kwargs)

        return r


class ListAdminAPI:
    def __init__(self, admin_url, admin_auth):
        self.admin_url = admin_url
        self.session = MailmanSession(admin_url, admin_auth)

    def member_options_url(self, email):
        return self.admin_url.replace("/admin/", "/options/") + "/" + email

    def bulk_subscribe(self, *emails, invite=False, welcome=True, notify_owner=True, message=''):
        post_data = {
            "subscribe_or_invite": int(invite),
            "send_welcome_msg_to_this_batch": int(welcome),
            "send_notifications_to_list_owner": int(notify_owner),
            "subscribees": '\n'.join(emails) + '\n',
            "invitation": message + '\n'
        }
        r = self.session.post(self.admin_url + "/members/add", data=post_data)
        if not r.ok:
            raise RuntimeError("Error subscribing members")

    def bulk_unsubscribe(self, *emails, notify_user=True, notify_owner=True):
        post_data = {
            "send_unsub_ack_to_this_batch": int(notify_user),
            "send_unsub_notifications_to_list_owner": int(notify_owner),
            "unsubscribees": '\n'.join(emails) + '\n'
        }
        r = self.session.post(self.admin_url + "/members/remove", data=post_data)
        if not r.ok:
            raise RuntimeError("Error unsubscribing members")

    def get_member_options(self, email):
        r = self.session.get(self.member_options_url(email))
        if not r.ok:
            raise RuntimeError("Unable to get member options")

        p = re.compile(r'<input type=radio name="([^"]*)" value="([^"]*)" CHECKED>')
        opts = {}
        for m in p.finditer(r.text):
            opts[m.group(1)] = int(m.group(2))

        name_regex = re.compile(r'name="fullname" size="[^"]*" value="([^"]*)"')
        m = name_regex.search(r.text)
        if m:
            opts["fullname"] = m.group(1)
        return opts

    def set_member_options(self, email, fullname='', **kwargs):
        def check_response(future):
            if not future.result().ok:
                raise RuntimeError("Unable to set options on mailman")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            if kwargs:
                opts = {}
                for k, v in kwargs.items():
                    opts[k] = int(v)
                opts['options-submit'] = 1
                options_f = executor.submit(self.session.post, self.member_options_url(email), data=opts)
                options_f.add_done_callback(check_response)
            if fullname:
                opts = {'change-of-address': 1, 'fullname': fullname}
                fullname_f = executor.submit(self.session.post, self.member_options_url(email), data=opts)
                fullname_f.add_done_callback(check_response)

    def mymail_subscribe(self, mines_username, fullname='', message=''):
        info = uidinfo(mines_username)
        if not fullname:
            fullname = info["first"] + " " + info["sn"]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            mines_f = executor.submit(self.bulk_subscribe, mines_username + '@mines.edu', message=message)
            mymail_f = executor.submit(self.bulk_subscribe, mines_username + '@mymail.mines.edu', notify_owner=False, welcome=False)
            mines_f.add_done_callback(lambda f:self.set_member_options(mines_username + '@mines.edu', fullname=fullname))
            mymail_f.add_done_callback(lambda f:self.set_member_options(mines_username + '@mymail.mines.edu', fullname=fullname + " (alias for posting)", disablemail=True, conceal=1))

