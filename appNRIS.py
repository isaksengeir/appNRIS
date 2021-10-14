from PyQt5 import QtWidgets
from UI.MainWindow import Ui_MainWindow
from src.Organisation import Organisation
from src.Settings import Settings
from src.GoogleCalendar import MyCalendar, GoogleCalendarService
import sys
import pickle
import os
main_dir = os.path.dirname(os.path.abspath(__file__))
appstuff = f"{main_dir}/.appstuff.pkl"


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



        print(self.cal.calendars)

        # Just for testing purposes:
        self.update_table_headers()
        self.update_roster()


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

        self.cal = MyCalendar(token=self.settings.token, credentialsfile=self.settings.client_secret,
                              scopes=self.settings.scopes)

        self.cal.change_calendar(calendar_name="1.linje-vaktliste")

    def scalable_tables(self):
        # Make table widget rescale columns when window is resized:
        self.tableRoster.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))
        self.tableRoster.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))

        self.tableStaff.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))
        self.tableStaff.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))

    def update_table_headers(self):
        index = 0
        inst = [x.name for x in self.nris.institutions]

        self.tableRoster.setColumnCount(len(inst))
        self.tableStaff.setColumnCount(len(inst))
        self.tableRoster.setRowCount(0)
        self.tableStaff.setRowCount(0)
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
        events = self.cal.get_future_events
        #for event in events:
        #    print(event["summary"])

        #weeks = [str(x) for x in range(1, 50)]
        #index = 0
        #for w in weeks:
        #    item = QtWidgets.QTableWidgetItem()
        #    item.setText(w)
        #    self.tableRoster.setVerticalHeaderItem(index, item)
        #    index += 1

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
