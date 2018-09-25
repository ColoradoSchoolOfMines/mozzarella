"""The application's Globals object"""

import tg
from acmwebsite.lib.mailmanapi import ListAdminAPI

__all__ = ['Globals']


class Globals:
    """
    Container for objects available throughout the life of the application.

    One instance of Globals is created during application initialization and
    is available during requests via the ``app_globals`` variable.

    """
    def __init__(self):
        self._mmadmin = None


    @property
    def mmadmin(self):
        if self._mmadmin is None:
            self._mmadmin = ListAdminAPI(
                tg.config.get('mailman.url'),
                tg.config.get('mailman.secret'))
        return self._mmadmin
