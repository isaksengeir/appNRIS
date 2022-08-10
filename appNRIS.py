import PyQt5.QtGui
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from UI.MainWindow import Ui_MainWindow
from src.RosterGenerator import RosterWindow
from src.Organisation import Organisation
from src.Settings import Settings
from src.static_methods import week_to_date
from src.Event import RT_Event
from src.GoogleCalendar import RTCalendar
import sys
import pickle
import os
from datetime import datetime

main_dir = os.path.dirname(os.path.abspath(__file__))
appstuff = f"{main_dir}/.appstuff.pkl"
colors = {"blue": "#2e54ff", "green": "#08a91e", "yellow": "#db8f00", "orange": "#ff5733", "red": "#bf0000",
          "grey": "#a3a3a3", "ukevakt": "#1c1507"}

response_colors = {"accepted": colors["green"], "needsAction": colors["blue"], "declined": colors["orange"],
                   "tentative": colors["yellow"]}


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # import Organisation, Settings,... objects
        if os.path.isfile(appstuff):
            print(f"APPSTUFF exists")
            self.nris, self.settings, self.cal = self.pickle_loader(appstuff)[:]
        else:
            print(f"This is your first time, isn't it?")
            self.init_nris()

        self.setupUi(self)
        self.setWindowTitle("appNRIS")

        # Fix tableWidgets to scale with window resize:
        self.scalable_tables()

        # TODO delete this ... just for testing
        print(self.cal.calendars)

        self.events = list()
        self.roster_event = dict()
        self.events_modified = list()
        self.ids_to_del = list()
        self.last_update = None

        self.update_table_headers()
        self.get_calendar_roster_events()
        self.update_roster()
        self.fill_staff_lists()
        self.clear_staff_widgets()

        #self.tableRoster.cellClicked.connect(self.roster_clicked)
        self.tableRoster.itemSelectionChanged.connect(self.roster_clicked)
        self.tableStaff.itemSelectionChanged.connect(self.staff_clicked)

        self.tableRoster.verticalHeader().sectionClicked.connect(self.week_number_clicked)
        self.listWidget_attendees.itemClicked.connect(self.update_response_combobox)
        #self.comboBox_status.currentTextChanged.connect(self.set_response)
        self.comboBox_status.activated.connect(self.set_response)
        self.button_delete_shift.clicked.connect(self.delete_event)
        self.checkBox_ukevakt.clicked.connect(self.ukevakt_toggle)
        self.button_update.clicked.connect(self.get_calendar_roster_events)
        self.button_save_changes.clicked.connect(self.save_to_calendar)
        self.button_add_attendee.clicked.connect(self.add_attendee)
        self.button_delete_attendee.clicked.connect(self.delete_attendee)
        self.button_set_summary.clicked.connect(self.set_summary_text)
        self.button_swap_shifts.clicked.connect(self.swap_shifts)
        self.button_reminer.clicked.connect(self.remind_event)
        self.button_new_roster.clicked.connect(self.new_roster_window)
        ###### STAFF
        self.button_new_employee.clicked.connect(self.new_employee)
        self.button_staff_delete.clicked.connect(self.remove_employee)
        self.button_save_to_employee.clicked.connect(self.save_to_employee)
        ### CALENDAR
        self.calendarWidget.selectionChanged.connect(self.calendar_date_changed)

        # Time to show yourself:
        self.show()
        self.spinBox_year.setValue(datetime.now().year)
        self.spinBox_week.setValue(datetime.now().isocalendar()[1])

    def week_number_clicked(self):
        print("You clicked an entire week! jai!")

    def calendar_date_changed(self):
        print("HELLO")
        # date_ = self.calendarWidget.selectedDate()
        # print(f"{date_.weekNumber()[0]}: {date_.year()}-{date_.month()}-{date_.day()} "
        #      f"{date_.shortDayName(date_.dayOfWeek())}")
        date_ = self.calendarWidget.selectedDate().toPyDate()
        print(date_)

    def init_nris(self):
        """
        If appNRIS have never used before - well, we need to start somewhere... and this just happened to be somewhere:
        """
        # TODO this is a good place to ask for credentials file!
        # --> No credential file, well... no Google service either! Maybe just break up here?
        self.settings = Settings()
        self.settings.token = f"{main_dir}/src/token.json"
        self.settings.client_secret = f"{main_dir}/client_secret.json"

        self.nris = Organisation(name="NRIS", leader="TM")
        inst_names = ["NTNU", "Sigma2", "UiB", "UiO", "UiT"]
        for inst in inst_names:
            self.nris.add_institution(name=inst)

        self.cal = RTCalendar(token=self.settings.token, credentialsfile=self.settings.client_secret,
                              scopes=self.settings.scopes)

        self.cal.change_calendar(calendar_name="1.linje-vaktliste")

    def scalable_tables(self):
        # Make table widget rescale columns when window is resized:
        self.tableRoster.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))
        self.tableStaff.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))
        #self.tableRoster.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(3))
        self.tableRoster.verticalHeader().setDefaultSectionSize(50)

    def update_statusbar(self):
        """

        """
        status_txt = f"Last updated: {self.last_update} - "
        if len(self.events_modified) > 0:
            status_txt += f"{len(self.events_modified)} local changes unsaved. "
        else:
            status_txt += "All local events synced to Google calendar."

        self.statusbar.showMessage(status_txt)

    @property
    def selected_cells(self):
        cells = list()
        for i in self.tableRoster.selectedItems():
            cells.append((i.row(), i.column()))
        return cells

    @property
    def selected_by_columns(self):
        cells = dict()
        for i in self.tableRoster.selectedItems():
            if i.column() not in cells:
                cells[i.column()] = list()
            cells[i.column()].append(i.row())
        return cells

    @property
    def current_cell(self):
        """
        returns current row and column indexes
        """
        return self.tableRoster.currentRow(), self.tableRoster.currentColumn()

    @property
    def current_event(self):
        if self.current_cell not in self.roster_event.keys():
            return None
        return self.roster_event[self.current_cell]

    def get_calendar_roster_events(self):
        """
        TODO this now default to do one year ahead ... make it more flexible, or is it ok?
        """
        # Get calendar events from_date --> to_date
        week_today = datetime.now().isocalendar()[1]
        year_today = datetime.now().year
        date1 = week_to_date(year=year_today, week=week_today)[0]
        date2 = week_to_date(year=year_today + 1, week=week_today)[0]

        self.events = [RT_Event(event=event) for event in self.cal.get_events(from_date=date1, to_date=date2)]

        self.last_update = self.get_now_str()
        self.events_modified.clear()
        self.update_roster()
        self.auto_make_staff()

    def auto_make_staff(self):
        print(self.nris.institutions_names)
        for event in self.events:
            if event.institution:
                i = [x.lower() for x in self.nris.institutions_names].index(event.institution.lower())
                inst = self.nris.institutions_names[i]

                self.nris.institution = inst
                if event.attendees:
                    for who in event.attendees.all:
                        if who.email not in self.nris.institution.emails:
                            self.nris.institution.employee = who.email

        self.fill_staff_lists()

    def roster_clicked(self):
        self.clear_text()
        if self.current_cell[1] >= 0:
            inst = self.tableRoster.horizontalHeaderItem(self.current_cell[1]).text()
            self.nris.institution = inst

        self.update_buttons()
        self.update_emails()

        if not self.current_event:

            self.update_buttons()
            self.default_shift()
            return

        if self.current_event.ukevakt:
            self.checkBox_ukevakt.setChecked(True)
        else:
            self.checkBox_ukevakt.setChecked(False)

        self.plainTextEdit_summary.setPlainText(self.current_event.summary)
        self.spinBox_year.setValue(int(self.current_event.start_year))
        self.spinBox_week.setValue(int(self.current_event.start_week))

        self.update_attendees_status()

    def default_shift(self):
        try:
            year, week = self.tableRoster.verticalHeaderItem(self.current_cell[0]).text().split("-")
        except AttributeError:
            return

        self.spinBox_year.setValue(int(year))
        self.spinBox_week.setValue(int(week))
        self.plainTextEdit_summary.setPlainText(f"{self.nris.institution.name}: ")

    def update_roster(self):
        """
        Show events one year ahead in time... for now at least
        """
        self.tableRoster.clearSelection()
        self.tableRoster.setRowCount(0)
        self.roster_event.clear()

        week = None

        for event in self.events:
            w1 = event.start_week
            y1 = event.start_year

            # New week, new row with new vertical header
            if w1 != week:
                week = w1
                rows = self.tableRoster.rowCount()
                self.tableRoster.insertRow(rows)
                item = QtWidgets.QTableWidgetItem()
                item.setText(f"{y1}-{str(week)} ")
                self.tableRoster.setVerticalHeaderItem(rows, item)

            if event.institution in self.nris.institutions_names:
                inst = event.institution
            else:
                inst = self.guess_institution(event=event)
                event.institution = inst
            if event.institution:
                _i = int(self.tableRoster.rowCount() - 1)
                _j = self.nris.institutions_names.index(inst)
                self.roster_event[(_i, _j)] = event
                self.tableRoster.setItem(_i, _j, QtWidgets.QTableWidgetItem(event.summary_names))

        self.color_roster_events()
        self.update_statusbar()
        self.roster_clicked()

    def update_emails(self):
        emails = list()
        emails.append("")
        self.comboBox_new_attendee.clear()
        try:
            for employee in self.nris.institution.staff:
                emails.append(employee.email)
        except AttributeError:
            return
        if len(emails) > 0:
            self.comboBox_new_attendee.addItems(emails)

    def clear_text(self):
        self.listWidget_attendees.clear()
        self.plainTextEdit_summary.clear()
        self.comboBox_new_attendee.clear()

    def default_empty_shift(self):
        # TODO update year, week, and parts of summary based on current cell
        pass

    def swap_shifts(self):
        """
        will swap attendees in event i and and even j
        """
        a, b = self.selected_cells[:]

        self.roster_event[a].attendees, self.roster_event[b].attendees = self.roster_event[b].attendees, \
                                                                         self.roster_event[a].attendees
        self.roster_event[a].summary, self.roster_event[b].summary = self.roster_event[b].summary_names, \
                                                                    self.roster_event[a].summary_names


        #self.append_local_change(cells=[a, b])
        self.events_modified.extend([a, b])
        self.update_roster()

    def update_attendees_status(self):
        self.listWidget_attendees.clear()
        if self.current_event.attendees is None:
            return

        if not self.current_event.attendees.all is None:
            for who in self.current_event.attendees.all:
                self.listWidget_attendees.insertItem(0, f"{who.email} ({who.responseStatus})")
                self.listWidget_attendees.item(0).setForeground(PyQt5.QtGui.QColor(response_colors[who.responseStatus]))
        else:
            pass

    def add_attendee(self):
        attendee = self.comboBox_new_attendee.currentText()

        if not "@" in attendee:
            print(f"{attendee} does not seem like a valid email...")
            return

        if not self.current_event:
            print("No events exist here... I am not sure what to do about this.... ")
        if not self.current_event.attendees:
            self.current_event.attendees = {"email": attendee, "responseStatus": "needsAction"}
        else:
            self.current_event.attendees.attendee = {"email": attendee, "responseStatus": "needsAction"}

        self.append_local_change()
        self.roster_clicked()

    def delete_attendee(self):
        try:
            email = self.listWidget_attendees.currentItem().text().split()[0]
        except AttributeError:
            return
        print(email)

        self.current_event.attendees.attendee = email
        del self.current_event.attendees.attendee
        self.color_roster_events()
        self.append_local_change()
        self.roster_clicked()

    def update_table_headers(self):
        index = 0
        inst = [x.name for x in self.nris.institutions]

        self.comboBox_institution.addItems(inst)

        self.tableRoster.setColumnCount(len(inst))
        self.tableStaff.setColumnCount(len(inst))

        for i in sorted(inst):
            item = QtWidgets.QTableWidgetItem()
            item.setText(str(i))
            # TODO can we make a copy of item instead of creating a new one? Using the same item below does not work...
            item2 = QtWidgets.QTableWidgetItem()
            item2.setText(str(i))

            self.tableRoster.setHorizontalHeaderItem(index, item)
            self.tableStaff.setHorizontalHeaderItem(index, item2)

            index += 1

    def get_institution_table_column(self):
        """
        Get column index for institution
        """
        institutions = [x.name.lower() for x in self.nris.institutions]
        column = dict()
        c = 0
        for inst in sorted(institutions):
            column[inst] = c
            c += 1
        return column

    @staticmethod
    def get_now_str():
        n = datetime.now()
        return f"{n.year}-{n.month:02d}-{n.day:02d} {n.hour:02d}:{n.minute:02d}:{n.second:02d}"

    def update_buttons(self):
        self.button_swap_shifts.setEnabled(False)

        if self.current_event:
            self.button_new_shift.setEnabled(False)
        else:
            self.button_new_shift.setEnabled(True)
        # Can only swap within one institution (column):
        if len(self.selected_by_columns.keys()) == 1:
            # Can only swap 2 shifts:
            for j in self.selected_by_columns.keys():
                if len(self.selected_by_columns[j]) == 2:
                    self.button_swap_shifts.setEnabled(True)

    def guess_institution(self, event):
        institutions = [x.name.lower() for x in self.nris.institutions]

        if not event.institution:
            return None

        if event.institution.lower() not in institutions:
            print(f"{event.institution} does not seem to be a part of {self.nris.name} consisting of "
                  f"{self.nris.institutions_names}")
            return None
        else:
            return self.nris.institutions_names[institutions.index(event.institution.lower())]

    def update_response_combobox(self):
        response = self.listWidget_attendees.currentItem().text().split()[-1][1:-1]
        self.comboBox_status.setCurrentText(response)

    def set_response(self):
        if not self.current_event.attendees:
            return

        email = None
        for i in self.listWidget_attendees.selectedItems():
            email = i.text().split()[0]

        if not email:
            return

        response = self.comboBox_status.currentText()

        for who in self.current_event.attendees.all:
            if who.email == email:
                who.responseStatus = response

        self.append_local_change()

    def save_to_calendar(self):
        print(f"Pushing {len(self.events_modified)} to calendar")


        for ij in self.events_modified:
            if ij in self.roster_event.keys():
                # commented this out to avoid saving to calendar for debugging/testing purposes:
                self.cal.update_event(body=self.roster_event[ij].body, event_id=self.roster_event[ij].id)
                print(self.roster_event[ij].body["summary"])

        for id in self.ids_to_del:
            #self.cal.delete_event(id)
            print(f"deleting event {id}")

        self.ids_to_del.clear()
        self.events_modified.clear()
        self.update_roster()

    def remind_event(self):
        self.cal.remind_event(event_id=self.current_event.id)

    def decide_event_foreground(self, event):
        """
        When multiple attendees, color event in roster table based on worst attendee.
        """
        txt_color = colors["green"]

        if event.attendees and not event.attendees.all is None:
            for attendee in event.attendees.all:
                if attendee.responseStatus != "accepted":
                    txt_color = response_colors[attendee.responseStatus]
                    break
        else:
            txt_color = colors["orange"]

        return txt_color

    def color_roster_events(self):
        """
        Color roster table events
        """
        for i in range(self.tableRoster.rowCount()):
            for j in range(self.tableRoster.columnCount()):
                ij = (i, j)
                if ij in self.roster_event.keys():

                    event = self.roster_event[ij]
                    if event.ukevakt:
                        self.tableRoster.item(i, j).setBackground(PyQt5.QtGui.QColor(colors["ukevakt"]))
                    else:
                        self.tableRoster.item(i, j).setData(PyQt5.QtCore.Qt.BackgroundRole, None)

                    if ij in self.events_modified:
                        txt_clr = colors["grey"]
                    else:
                        txt_clr = self.decide_event_foreground(event)

                    self.tableRoster.item(i, j).setForeground(PyQt5.QtGui.QColor(txt_clr))

    def ukevakt_toggle(self):

        i, j = self.current_cell
        try:
            self.tableRoster.item(i,j).type()
        except AttributeError:
            return

        if self.checkBox_ukevakt.isChecked():
            self.tableRoster.item(i, j).setBackground(PyQt5.QtGui.QColor(colors["ukevakt"]))
            self.current_event.ukevakt = True

        else:
            self.tableRoster.item(i, j).setData(PyQt5.QtCore.Qt.BackgroundRole, None)
            self.current_event.ukevakt = False

        self.tableRoster.item(i, j).setText(self.current_event.summary_names_ukevakt)
        self.append_local_change()

    def set_summary_text(self):

        if not self.current_event:
            return

        txt = self.plainTextEdit_summary.toPlainText()
        i, j = self.current_cell
        self.current_event.summary = txt

        # Update text
        self.tableRoster.item(i, j).setText(self.current_event.summary_names)

        self.append_local_change()

    def append_local_change(self, cells=None):
        if not cells:
            cells = [self.current_cell]

        for cell in cells:
            if cell not in self.events_modified:
                self.events_modified.append(self.current_cell)

        self.color_roster_events()
        self.update_statusbar()

    def delete_event(self):
        try:
            self.current_event.id
        except AttributeError:
            return

        self.ids_to_del = list()
        events_ij = list()

        for ij in self.selected_cells:
            if ij in self.roster_event.keys():
                events_ij.append(ij)

        if len(events_ij) == 0:
            return

        cont = QMessageBox.question(self, 'MessageBox', f"Delete {len(events_ij)} shift(s) from calender?",
                                    QMessageBox.Yes | QMessageBox.No)
        if cont == QMessageBox.Yes:
            for ij in events_ij:
                self.events_modified.append(ij)
                self.ids_to_del.append(self.roster_event[ij].id)
                del self.events[self.events.index(self.roster_event[ij])]
                del self.roster_event[ij]

        #self.get_calendar_roster_events()
        self.update_roster()

    ######STAFF######
    def fill_staff_lists(self):
        self.tableStaff.setRowCount(0)
        institutions = [i.name for i in self.nris.institutions]

        for i in range(len(institutions)):
            self.nris.institution = institutions[i]
            staff = self.nris.institution.staff
            for j in range(len(staff)):
                empl = staff[j]
                if j >= self.tableStaff.rowCount():
                    rows = self.tableStaff.rowCount()
                    self.tableStaff.insertRow(rows)
                who = empl.email
                # TODO it is nicer to display name, but need some rewrting since everything is looking for email now...
                #if not who:
                #    who = empl.email.split("@")[0]
                self.tableStaff.setItem(j, i, QtWidgets.QTableWidgetItem(who))

    def staff_clicked(self):
        self.clear_staff_widgets()
        employee = self.tableStaff.currentItem()

        try:
            inst = self.tableStaff.horizontalHeaderItem(self.tableStaff.currentColumn()).text()
        except AttributeError:
            return

        self.comboBox_institution.setCurrentText(inst)
        self.nris.institution = inst

        if employee:
            self.nris.institution.employee = employee.text()
            self.fill_staff_widgets()
            self.button_save_to_employee.setEnabled(True)

    def clear_staff_widgets(self):
        self.button_save_to_employee.setEnabled(False)
        self.lineEdit_staff_name.clear()
        self.lineEdit_staff_email.clear()
        self.spinbox_shift_frq.setValue(1.00)
        self.checkBox_sharedshifts.setChecked(False)
        self.checkBox_does_ukevakt.setChecked(True)

    def fill_staff_widgets(self):
        who = self.nris.institution.employee
        self.lineEdit_staff_name.setText(who.name)
        self.lineEdit_staff_email.setText(who.email)
        self.spinbox_shift_frq.setValue(who.vacancy_rate)
        self.checkBox_does_ukevakt.setChecked(who.ukevakt)
        self.checkBox_sharedshifts.setChecked(who.shared_shifts)

    def new_employee(self):
        inst = self.comboBox_institution.currentText()
        email = self.lineEdit_staff_email.text()
        if not "@" in email:
            print("Invalid email address")
            return

        self.nris.institution = inst # change to correct institution
        self.nris.institution.new_employee(email=email)

        self.save_to_employee()

    def save_to_employee(self):
        self.nris.institution.employee.email = self.lineEdit_staff_email.text()
        self.nris.institution.employee.name = self.lineEdit_staff_name.text()
        self.nris.institution.employee.institution = self.comboBox_institution.currentText()
        self.nris.institution.employee.vacancy_rate = float(self.spinbox_shift_frq.value())
        self.nris.institution.employee.ukevakt = self.checkBox_does_ukevakt.isChecked()
        self.nris.institution.employee.shared_shifts = self.checkBox_sharedshifts.isChecked()

        self.fill_staff_lists()

    def remove_employee(self):
        email = self.tableStaff.currentItem().text()
        self.nris.institution.employee = email
        del self.nris.institution.employee
        self.fill_staff_lists()

    def save_objects(self, obj, filename):
        """
        When app is closed, save objects for next session ...
        """
        with open(filename, "wb") as savestuff:
            pickle.dump(obj, savestuff, pickle.HIGHEST_PROTOCOL)

    def pickle_loader(self, filename):
        """
        Load pickle
        """
        with open(filename, "rb") as pkl:
            stuff = pickle.load(pkl)
        return stuff

    def closeEvent(self, event):
        # Time to save objects
        print("Time to save stuff and say Goodbye")
        save_data = [self.nris, self.settings, self.cal]
        self.save_objects(obj=save_data, filename=appstuff)

    def new_roster_window(self):
        new_roster = RosterWindow(self)
        new_roster.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
