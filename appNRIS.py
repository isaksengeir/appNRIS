from PyQt5 import QtWidgets
from UI.MainWindow import Ui_MainWindow
import sys


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setupUi(self)
        self.setWindowTitle("appNRIS")

        # Make table widget rescale columns when window is resized:
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode(1))

        # Time to show yourself:
        self.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
