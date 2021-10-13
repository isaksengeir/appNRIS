import os


class Settings:
    """
    Object to store appNRIS settings
    """
    def __init__(self):
        self._token = None
        self._scopes = ['https://www.googleapis.com/auth/calendar']
        self._default_calendar = "1.linje-vaktliste"
        self._roster_calendar = "1.linje-vaktliste"


    @property
    def default_calendar(self):
        return self._default_calendar

    @default_calendar.setter
    def default_calendar(self, value):
        self._default_calendar = value

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        if os.path.exists(value):
            self._token = value
        else:
            print(f"Can not find: {value}")

    @property
    def scopes(self):
        return self._scopes

    @scopes.setter
    def scopes(self, value):
        if isinstance(list, value):
            self._scopes = value
        else:
            print(f"scopes must be list. Got {type(value)}")
