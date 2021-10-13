

class Employee:
    """
    This is basically a person belonging to some institution/organisation for a monthly salary.
    """
    def __init__(self, name=None):

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
    def __init__(self, name=None, leader=None, staff=None):
        self._staff = list()
        self._name = name
        self._leader = leader
        if isinstance(dict, staff):
            self._staff = staff
        elif isinstance(list, staff):
            self.create_staff(staff)
        else:
            self._staff = dict()

    def create_staff(self, staff_list):
        self._staff = dict()
        for i in staff_list:
            self._staff[i.name] = i

    def new_employee(self, name):
        self._staff[name] = Employee(name=name)

    def fire_employee(self, name):
        del self._staff[name]

    @property
    def count_staff(self):
        return len(self._staff)

    @property
    def staff(self):
        return self._staff.values()


class Organisation:
    """
    Organisation consists of several institutions working together. Each Institution contributes with Staff members.
    """
    def __init__(self, name=None, leader=None, institutions=None):
        self._name = name
        self._leader = leader
        if type(list, institutions):
            self._inst = institutions
        else:
            self._inst = list()

    def add_institution(self, name=None):
        new_inst = Institution(name=name)
        self._inst.append(new_inst)

    @property
    def institutions(self):
        return self._inst
