from UI.RosterWindow import Ui_RosterWindow
from PyQt5 import QtWidgets
#import appNRIS


class RosterWindow(QtWidgets.QMainWindow, Ui_RosterWindow):
    def __init__(self, parent):
        super(RosterWindow, self).__init__(parent)

        self.app = parent
        self.ui = Ui_RosterWindow()

        self.ui.setupUi(self)

        self.setWindowTitle("APPnris - Roster generator")

        # START
        self.fill_institution_list()

        # CONNECT STUFF
        self.ui.button_cancel.clicked.connect(self.close)
        self.ui.comboBox_institution_2.currentTextChanged.connect(self.fill_staff_list)


        self.fill_staff_list()

    def fill_institution_list(self):
        inst_names = [inst.name for inst in self.app.nris.institutions]
        self.ui.comboBox_institution_2.addItems(inst_names)

    def fill_staff_list(self):
        try:
            inst = self.ui.comboBox_institution_2.currentText()
        except AttributeError:
            return
        self.app.nris.institution = inst
        self.ui.staff_list_2.clear()

        for staff in self.app.nris.institution.staff:
            self.ui.staff_list_2.insertItem(0, f"{staff.name} <> {staff.email} ")

    #def institution_changed(self):

