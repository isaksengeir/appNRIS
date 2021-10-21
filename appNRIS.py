import PyQt5.QtGui
from PyQt5 import QtWidgets, QtCore
from UI.MainWindow import Ui_MainWindow
from src.Organisation import Organisation
from src.Settings import Settings
from src.static_methods import week_to_date, event_body
from src.GoogleCalendar import MyCalendar, GoogleCalendarService, RTCalendar
import sys
import pickle
import os
from datetime import date, datetime
main_dir = os.path.dirname(os.path.abspath(__file__))
appstuff = f"{main_dir}/.appstuff.pkl"
colors = {"blue": "#2e54ff", "green": "#08a91e", "yellow": "#db8f00", "orange": "#ff5733", "red": "#bf0000",
          "grey": "#a3a3a3", "ukevakt": "#525252"}

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

        self.roster_event = dict()
        self.events_modified = list()
        self.last_update = None
        # Just for testing purposes:
        self.update_table_headers()
        self.update_roster()

        #self.tableRoster.cellClicked.connect(self.roster_clicked)
        self.tableRoster.itemSelectionChanged.connect(self.roster_clicked)
        #self.tableRoster.itemChanged
        self.listWidget_attendees.itemClicked.connect(self.update_response_combobox)
        #self.comboBox_status.currentTextChanged.connect(self.set_response)
        self.comboBox_status.activated.connect(self.set_response)
        self.button_delete_shift.clicked.connect(self.delete_event)
        self.checkBox_ukevakt.clicked.connect(self.ukevakt_toggle)
        self.button_update.clicked.connect(self.update_roster)
        self.button_save_changes.clicked.connect(self.save_to_calendar)
        self.button_add_attendee.clicked.connect(self.add_attendee)

        # Time to show yourself:
        self.show()

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
        self.tableRoster.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(3))

        self.tableStaff.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))
        self.tableStaff.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))

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

    @current_event.setter
    def current_event(self, value):
        self.roster_event[self.current_cell] = value

    def roster_clicked(self):

        start = datetime.strptime(self.current_event["start"].get("date"), "%Y-%m-%d")
        #end = datetime.strptime(self.current_event["end"].get("date"), "%Y-%m-%d")

        if "ukevakt" in self.current_event["summary"].lower() or "ukesvakt" in self.current_event["summary"].lower():
            self.checkBox_ukevakt.setChecked(True)
        else:
            self.checkBox_ukevakt.setChecked(False)

        self.plainTextEdit_summary.setPlainText(self.current_event["summary"])
        self.spinBox_year.setValue(start.year)
        self.spinBox_week.setValue(start.isocalendar().week)

        self.update_attendees_status()

    def update_attendees_status(self):
        self.listWidget_attendees.clear()
        try:
            for who in self.current_event["attendees"]:
                self.listWidget_attendees.insertItem(0, f"{who['email']} ({who['responseStatus']})")
                self.listWidget_attendees.item(0).setForeground(PyQt5.QtGui.QColor(response_colors[who['responseStatus']]))
        except KeyError:
            pass

    def add_attendee(self):
        attendee = self.lineEdit_new_attendee.text()

        if not "@" in attendee:
            print(f"{attendee} does not seem like a valid email...")
            return

        if not self.current_event:
            # TODO implement this in class (auto-fill institution, week, year from gui)
            self.current_event = event_body()

        if not "attendees" in self.current_event:
            self.current_event["attendees"] = list()

        self.current_event["attendees"].append({"email": attendee, "responseStatus": "needsAction"})
        print(self.current_event["attendees"])
        if self.current_cell not in self.events_modified:
            self.events_modified.append(self.current_cell)
        self.listWidget_attendees.insertItem(0, attendee)


    def update_table_headers(self):
        index = 0
        inst = [x.name for x in self.nris.institutions]

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
        institutions = [x.name.lower() for x in self.nris.institutions]
        column = dict()
        c = 0
        for inst in sorted(institutions):
            column[inst] = c
            c += 1
        return column

    def get_now_str(self):
        n = datetime.now()
        return f"{n.year}-{n.month:02d}-{n.day:02d} {n.hour:02d}:{n.minute:02d}:{n.second:02d}"

    def update_roster(self):
        """
        Show events one year ahead in time... for now at least
        """
        self.tableRoster.clearSelection()
        self.tableRoster.setRowCount(0)
        self.roster_event.clear()
        self.events_modified.clear()

        # Get calendar events from_date --> to_date
        week_today = datetime.now().isocalendar()[1]
        year_today = datetime.now().year
        date1 = week_to_date(year=year_today, week=week_today)[0]
        date2 = week_to_date(year=year_today+1, week=week_today)[0]

        self.last_update = self.get_now_str()
        events = self.cal.get_events(from_date=date1, to_date=date2)

        # Get table indexes for institutions (sorted alphabetically)
        column = self.get_institution_table_column()

        week = None
        for event in events:
            starts = event['start'].get('dateTime', event['start'].get('date'))
            # TODO probabøu enough with: event["start"].get("date")
            ends = event['end'].get('dateTime', event['end'].get('date'))
            w1 = date(*map(int, starts.split("T")[0].split("-")[0:3])).isocalendar()[1]
            w2 = date(*map(int, ends.split("T")[0].split("-")[0:3])).isocalendar()[1]

            # New week, new row with new vertical header
            if w1 == w2 and w1 != week:
                # Todo print year perhaps ?
                week = w1
                rows = self.tableRoster.rowCount()
                self.tableRoster.insertRow(rows)
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(week))
                self.tableRoster.setVerticalHeaderItem(rows, item)

            inst = event["summary"].split(":")[0].lower()
            inst = inst.split("(")[0].strip()
            who = event["summary"].split(":")[1]

            _i = int(self.tableRoster.rowCount() - 1)
            _j = int(column[inst])
            self.roster_event[(_i, _j)] = event
            self.tableRoster.setItem(_i, _j, QtWidgets.QTableWidgetItem(who))

            self.color_roster_events()
            self.update_statusbar()

    def update_response_combobox(self):
        response = self.listWidget_attendees.currentItem().text().split()[-1][1:-1]
        print(response)

        self.comboBox_status.setCurrentText(response)

    def set_response(self):
        if "attendees" not in self.current_event.keys():
            return

        email = None
        for i in self.listWidget_attendees.selectedItems():
            email = i.text().split()[0]

        if not email:
            return
        response = self.comboBox_status.currentText()

        for who in self.current_event["attendees"]:
            if who["email"] == email:
                who["responseStatus"] = response

        print(self.current_event["attendees"])

        i,j = self.current_cell
        self.events_modified.append((i, j))
        self.roster_clicked()
        self.color_roster_events()
        self.update_statusbar()

    def save_to_calendar(self):
        print(f"Will now push {len(self.events_modified)} to calendar")

        for ij in self.events_modified:
            print(self.roster_event[ij]["id"])
            self.cal.update_event(body=self.roster_event[ij], event_id=self.roster_event[ij]["id"])

        self.update_roster()

    def decide_event_foreground(self, event):
        """
        When multiple attendees, color event in roster table based on worst attendee.
        """
        txt_color = colors["green"]
        if "attendees" in event.keys():
            for who in event["attendees"]:
                if who["responseStatus"] != "accepted":
                    txt_color = response_colors[who["responseStatus"]]
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
                    if "ukevakt" in event["summary"].lower() or "ukesvakt" in event["summary"].lower():
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
        if self.checkBox_ukevakt.isChecked():
            self.tableRoster.item(i, j).setBackground(PyQt5.QtGui.QColor(colors["ukevakt"]))
            self.current_event["summary"] += " (Ukevakt)"

        else:
            self.tableRoster.item(i, j).setData(PyQt5.QtCore.Qt.BackgroundRole, None)
            self.current_event["summary"] = self.current_event["summary"].replace(" (Ukevakt)", "")\
                .replace(" (ukevakt)", "").replace(" (Ukesvakt)", "")

        self.tableRoster.item(i, j).setText(self.current_event["summary"].split(":")[1])
        self.events_modified.append((i, j))
        self.roster_clicked()
        self.color_roster_events()
        self.update_statusbar()

    def delete_event(self):
        print(f"This will delete id {self.current_event['id']}")
        #self.cal.delete_event(self.current_event['id'])
        self.update_roster()

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


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
