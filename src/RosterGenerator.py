from UI.RosterWindow import Ui_RosterWindow
from PyQt5 import QtWidgets
from datetime import datetime

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
            self.ui.first_ukevakt.setValue(ukevakt_order[inst])
        self.app.nris.institution = inst
        self.ui.staff_list_2.clear()

        for staff in self.app.nris.institution.staff:
            name = staff.name
            if not staff.name or len(staff.name) < 1:
                name = staff.email

            self.ui.staff_list_2.insertItem(0, f"{name} ({self.staff_details(staff)})")

    #def institution_changed(self):

