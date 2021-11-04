

class Employee:
    """
    This is basically a person belonging to some institution/organisation for a monthly salary.
    """
    def __init__(self, email=None, content=None):

        self._name = None
        self._email = email
        self._institution = None
        self._position = None

        self._ukevakt = True
        self._shared_shifts = False
        self._vacancy_rate = 1.00

        if content:
            for k, v in content.items():
                setattr(self, k, v)

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

    @property
    def ukevakt(self):
        return self._ukevakt

    @ukevakt.setter
    def ukevakt(self, value):
        if not isinstance(value, bool):
            print(f"ukevakt expected bool, got {type(value)}")
            return
        self._ukevakt = value

    @property
    def shared_shifts(self):
        return self._shared_shifts

    @shared_shifts.setter
    def shared_shifts(self, value):
        if not isinstance(value, bool):
            print(f"ukevakt expected bool, got {type(value)}")
            return
        self._shared_shifts = value


class Institution:
    """
    An Institution consists of several employees (staff).
    """
    def __init__(self, name=None, leader=None, staff=None):
        self._staff = list()
        self._name = name
        self._leader = leader
        self._employee = None

        if isinstance(staff, list):
            self.create_staff(staff_list=staff)

    def create_staff(self, staff_list):
        for i in staff_list:
            if isinstance(i, dict):
                print("WTF - noone has thought this though yet ..")
                self._staff.append(Employee(content=i))
            elif "@" in i:
                self._staff.append(Employee(email=i))

    def new_employee(self, email):
        print("WE ARE HIRING A NEW EMPLOYEE")
        if email in [i.email for i in self._staff]:
            print(f"Employee {email} already working @{self.name}")
            return
        self._staff.append(Employee(email=email))
        self._employee = self._staff[-1]

    def fire_employee(self):
        del self._staff[self._staff.index(self._employee)]
        self._employee = self._staff[-1]

    @property
    def count_staff(self):
        return len(self._staff)

    @property
    def staff(self):
        return self._staff

    @property
    def staff_names(self):
        return [i.name for i in self._staff]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def employee(self):
        return self._employee

    @employee.setter
    def employee(self, value):
        if value in self._staff:
            self._employee = value
        elif value in [i.email for i in self._staff]:
            self._employee = self._staff[[i.email for i in self._staff].index(value)]
        elif "@" in value:
            print("employee setter found a new employee to hire ?")
            self.new_employee(email=value)

    @property
    def emails(self):
        return [x.email for x in self._staff]

    @employee.deleter
    def employee(self):
        del self._staff[self._staff.index(self._employee)]
        if self.count_staff > 0:
            self._employee = self._staff[-1]
        else:
            self._employee = None


class Organisation:
    """
    Organisation consists of several institutions working together. Each Institution contributes with Staff members.
    """
    def __init__(self, name=None, leader=None, institutions=None):
        self._name = name
        self._leader = leader

        # Keep one institution in front for actions:
        self._institution = None

        if institutions and isinstance(institutions, type(list)):
            self._institutions = institutions
        else:
            self._institutions = list()

    def add_institution(self, name=None):
        new_inst = Institution(name=name)
        self._institutions.append(new_inst)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def institutions(self):
        return self._institutions

    @property
    def institutions_names(self):
        return sorted([i.name for i in self._institutions])

    @property
    def count_institutions(self):
        return len(self._institutions)

    @property
    def institution(self):
        return self._institution

    @institution.setter
    def institution(self, name):
        if name in self._institutions:
            self._institution = name
        else:
            for inst in self._institutions:
                if name == inst.name:
                    self._institution = inst

    @institution.deleter
    def institution(self):
        if self._institution in self._institutions:
            deleted = self._institutions.pop(self._institutions.index(self.institution))
            print(f"{deleted.name} deleted from {self.name}...")
            self._institution = self.institutions[-1]
