import PyQt5.QtGui
from PyQt5 import QtWidgets
from UI.MainWindow import Ui_MainWindow
from src.Organisation import Organisation
from src.Settings import Settings
from src.static_methods import week_to_date
from src.GoogleCalendar import MyCalendar, GoogleCalendarService, RTCalendar
import sys
import pickle
import os
from datetime import date, datetime
main_dir = os.path.dirname(os.path.abspath(__file__))
appstuff = f"{main_dir}/.appstuff.pkl"
colors = {"blue": "#2e54ff", "green": "#08a91e", "yellow": "#db8f00", "orange": "#ff5733", "red": "#bf0000"}

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
        # Just for testing purposes:
        self.update_table_headers()
        self.update_roster()

        #self.tableRoster.cellClicked.connect(self.roster_clicked)
        self.tableRoster.itemSelectionChanged.connect(self.roster_clicked)
        #self.tableRoster.itemChanged

        # Time to show yourself:
        self.show()

    def init_nris(self):
        """
        If appNRIS have never used before - well, we need to start somewhere...
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

    def roster_clicked(self):
        print(self.tableRoster.currentItem())
        print(self.tableRoster.currentItem().text())
        event = self.roster_event[(self.tableRoster.currentRow(), self.tableRoster.currentColumn())]


        start = datetime.strptime(event["start"].get("date"), "%Y-%m-%d")
        end = datetime.strptime(event["end"].get("date"), "%Y-%m-%d")

        if "ukevakt" in event["summary"].lower() or "ukesvakt" in event["summary"].lower():
            print("Found UKEVAKT")
            self.checkBox_ukevakt.setChecked(True)
        else:
            self.checkBox_ukevakt.setChecked(False)

        self.plainTextEdit_summary.setPlainText(event["summary"])
        self.spinBox_year.setValue(start.year)
        self.spinBox_week.setValue(start.isocalendar().week)
        self.listWidget_attendees.clear()

        try:
            for who in event["attendees"]:
                self.listWidget_attendees.insertItem(0, f"{who['email']} ({who['responseStatus']})")
        except KeyError:
            pass

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

    def update_roster(self):
        """
        Show events one year ahead in time... for now at least
        """
        week_today = datetime.now().isocalendar()[1]
        year_today = datetime.now().year
        date1 = week_to_date(year=year_today, week=week_today)[0]
        date2 = week_to_date(year=year_today+1, week=week_today)[0]
        events = self.cal.get_events(from_date=date1, to_date=date2)

        # Get table indexes for institutions (sorted alphabetically)
        institutions = [x.name.lower() for x in self.nris.institutions]
        column = dict()
        c = 0
        for inst in sorted(institutions):
            column[inst] = c
            c += 1

        week = None
        for event in events:
            starts = event['start'].get('dateTime', event['start'].get('date'))
            # TODO probabøu enough with: event["start"].get("date")
            ends = event['end'].get('dateTime', event['end'].get('date'))
            w1 = date(*map(int, starts.split("T")[0].split("-")[0:3])).isocalendar()[1]
            w2 = date(*map(int, ends.split("T")[0].split("-")[0:3])).isocalendar()[1]

            # New week, new row with new vertical header
            if w1 == w2 and w1 != week:
                # Todo print year perheps ?
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
            if "ukevakt" in event["summary"].lower() or "ukesvakt" in event["summary"].lower():
                self.tableRoster.item(_i, _j).setBackground(PyQt5.QtGui.QColor("#525252"))
            txt_color = colors["green"]
            if "attendees" in event.keys():
                for who in event["attendees"]:
                    if who["responseStatus"] != "accepted":
                        txt_color = response_colors[who["responseStatus"]]
                        break
            else:
                txt_color = colors["orange"]
            self.tableRoster.item(_i, _j).setForeground(PyQt5.QtGui.QColor(txt_color))



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
