from PyQt5 import QtWidgets
from UI.MainWindow import Ui_MainWindow
import sys


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)
        self.setWindowTitle("appNRIS")

        # Make table widget rescale columns when window is resized:
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))
        self.tableWidget.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))

        # Just for testing purposes:
        self.insert_roster_headers()
        self.insert_weeks()
        # Time to show yourself:
        self.show()

    def insert_roster_headers(self):
        inst = ["UiT", "UiB", "UiO", "NTNU", "Sigma2"]
        index = 0
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(50)
        for i in sorted(inst):
            item = QtWidgets.QTableWidgetItem()
            item.setText(i)
            self.tableWidget.setHorizontalHeaderItem(index, item)
            index += 1

    def insert_weeks(self):
        weeks = [str(x) for x in range(1, 50)]
        index = 0
        for w in weeks:
            item = QtWidgets.QTableWidgetItem()
            item.setText(w)
            self.tableWidget.setVerticalHeaderItem(index, item)
            index += 1


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
