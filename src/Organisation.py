

class Employee:
    """
    This is basically a person belonging to some organisation for a monthly salary.
    """
    def __init__(self):

        self._name = None
        self._email = None
        self._institution = None
        self._position = None
        self._vacancy_rate = 100.00

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value:
            print(f"{value} does not seem to be a proper email address")
            return
        self._email = value

    @property
    def institution(self):
        return self._institution

    @institution.setter
    def institution(self, value):
        self._institution = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def vacancy_rate(self):
        return self._vacancy_rate

    @vacancy_rate.setter
    def vacancy_rate(self, value):
        try:
            value = float(value)
        except ValueError:
            print(f"vacancy_rate must be int or float. Got {type(value)}")
            return
        if value < 0:
            print(f"vacancy_rate can not be < 0. Got {value}")
            return
        self._vacancy_rate = float(value)


class Institution:
    """
    An Institution consists of several employees (staff).
    """
    def __init__(self):
        self._staff = list()
        self._name = None
        self._leader = None


    @property
    def employees(self):
        return len(self._staff)


class Organisation:
    """
    Organisation consists of several institutions working together. Each Institution contributes with Staff members.
    """
    def __init__(self):
        pass