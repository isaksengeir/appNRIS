from UI.RosterWindow import Ui_RosterWindow
from PyQt5 import QtWidgets
from datetime import datetime
import random

ukevakt_order = {"UiT": 1, "NTNU": 2, "UiB": 3, "UiO": 4}

class RosterWindow(QtWidgets.QMainWindow, Ui_RosterWindow):
    def __init__(self, parent):
        super(RosterWindow, self).__init__(parent)

        self.app = parent
        self.ui = Ui_RosterWindow()

        self.ui.setupUi(self)

        self.setWindowTitle("APPnris - Roster generator")

        # START
        self.fill_institution_list()
        self.ui.year1_2.setValue(datetime.now().year)
        self.ui.week1_2.setValue(datetime.now().isocalendar()[1])
        self.ui.year2_2.setValue(datetime.now().year)

        # CONNECT STUFF
        self.ui.button_cancel.clicked.connect(self.close)
        self.ui.comboBox_institution_2.currentTextChanged.connect(self.fill_staff_list)
        self.ui.button_generate_roster.clicked.connect(self.make_roster)

        self.fill_staff_list()

    def fill_institution_list(self):
        inst_names = [inst.name for inst in self.app.nris.institutions]
        self.ui.comboBox_institution_2.addItems(inst_names)

    @staticmethod
    def staff_details(staff):
        det = f"{staff.email}, {staff.vacancy_rate:.2f}"
        if staff.ukevakt:
            det += ", ukevakt"
        if staff.shared_shifts:
            det += ", sharing"
        return det

    def fill_staff_list(self):
        try:
            inst = self.ui.comboBox_institution_2.currentText()
        except AttributeError:
            return
        if inst in ukevakt_order.keys():
            self.ui.first_ukevakt_3.setValue(ukevakt_order[inst])

        self.app.nris.institution = inst
        self.ui.staff_list_2.clear()

        for staff in self.app.nris.institution.staff:
            name = staff.name
            # If employee has no name, give use email user as name:
            if not staff.name or len(staff.name) < 1:
                name = staff.email.split("@")[0]

            self.ui.staff_list_2.insertItem(0, f"{name}, {self.staff_details(staff)}")

    def get_staff(self):
        return [self.app.nris.institution.staff]

    def make_roster(self):
        self.ui.tableWidget_roster_2.setRowCount(0)

        year1 = self.ui.year1_2.text()
        w1 = self.ui.week1_2.text()
        year2 = self.ui.year2_2.text()
        w2 = self.ui.week2_2.text()

        staff = list()
        for i in range(self.ui.staff_list_2.count()):
            email = self.ui.staff_list_2.item(i).text().split(",")[1].strip()
            if self.app.nris.institution.get_employee_obj(email=email).vacancy_rate > 0:
                staff.append(self.app.nris.institution.get_employee_obj(email=email))

        # Random order of shifts ?
        if self.ui.checkBox_rondomOrder.isChecked():
            staff = random.sample(staff, len(staff))

        print([x.name for x in staff])

        # NOW IT IS TIME TO FILL UP THE ROSTER for year1, w1 to year2, w2 :
        self.populate_roster(staff=staff, w1=w1, w2=w2, y1=year1, y2=year2)

    def populate_roster(self, staff, y1, w1, y2, w2):
        week = int(w1)
        year = int(y1)
        i = 0
        row = 0
        ukevakt_year = self.ukevakt_year

        while True:

            _from, _to = None, None
            name = staff[i].name
            if not name:
                name = staff[i].email.split("@")[0]
            email = staff[i].email
            ukevakt = ""
            if week in ukevakt_year:
                ukevakt = "X"

            self.ui.tableWidget_roster_2.insertRow(row)
            self.ui.tableWidget_roster_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(week)))
            self.ui.tableWidget_roster_2.setItem(row, 3, QtWidgets.QTableWidgetItem(name))
            self.ui.tableWidget_roster_2.setItem(row, 4, QtWidgets.QTableWidgetItem(ukevakt))
            self.ui.tableWidget_roster_2.setItem(row, 5, QtWidgets.QTableWidgetItem(email))



            # Check if we are done:
            if week == int(w2) and year == int(y2):
                break

            # Go to next week
            week += 1
            row += 1
            if week > 52:
                week = 1
                year += 1
            if i < (len(staff) - 2):
                i += 1
            else:
                i = 0

        print("Done populating roster")


    @property
    def ukevakt_year(self):
        w1 = int(self.ui.first_ukevakt_3.text())
        frq = int(self.ui.first_ukevakt_4.text())

        return [x for x in list(range(w1, 52, frq)) if x >= w1]