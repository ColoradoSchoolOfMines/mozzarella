import requests
from urllib.parse import quote

mpapi_base = 'https://mastergo.mines.edu/mpapi/'

class InvalidUsername(Exception):
    pass

def auth(username, password):
    r = requests.post(mpapi_base + 'auth', data={'username': username, 'password': password})
    r.raise_for_status()
    data = r.json()
    return data["result"] == "success"

def uidinfo(username):
    r = requests.get(mpapi_base + 'uid/' + quote(username, safe=''))
    r.raise_for_status()
    data = r.json()
    if data["result"] != "success":
        raise InvalidUsername("Bad Mines Username")
    return data["attributes"]

