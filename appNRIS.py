from PyQt5 import QtWidgets
from UI.MainWindow import Ui_MainWindow
from src.Organisation import Organisation
import sys
import _pickle as pickle

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)
        self.setWindowTitle("appNRIS")

        self.scalable_tables()

        # Just for testing purposes:
        self.insert_roster_headers()
        self.insert_weeks()
        # Time to show yourself:
        self.show()

    def scalable_tables(self):
        # Make table widget rescale columns when window is resized:
        self.tableRoster.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))
        self.tableRoster.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))

        self.tableStaff.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))
        self.tableStaff.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))

    def insert_roster_headers(self):
        inst = ["UiT", "UiB", "UiO", "NTNU", "Sigma2"]
        index = 0
        self.tableRoster.setColumnCount(5)
        self.tableRoster.setRowCount(50)
        for i in sorted(inst):
            item = QtWidgets.QTableWidgetItem()
            item.setText(i)
            self.tableRoster.setHorizontalHeaderItem(index, item)
            index += 1

    def insert_weeks(self):

        weeks = [str(x) for x in range(1, 50)]
        index = 0
        for w in weeks:
            item = QtWidgets.QTableWidgetItem()
            item.setText(w)
            self.tableRoster.setVerticalHeaderItem(index, item)
            index += 1

    def import_objects(self):
        """
        On startup, read objects from last session ...
        """


    def save_objects(self):
        """
        When app is closed, save objects for next session ...
        """
        pass

    def closeEvent(self, event):
        # Time to save objects
        print("Time to save stuff and say Goodbye")


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
