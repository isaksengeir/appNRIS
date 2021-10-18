# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(867, 664)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tableRoster = QtWidgets.QTableWidget(self.tab)
        self.tableRoster.setMinimumSize(QtCore.QSize(650, 250))
        self.tableRoster.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableRoster.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableRoster.setObjectName("tableRoster")
        self.tableRoster.setColumnCount(0)
        self.tableRoster.setRowCount(0)
        self.tableRoster.horizontalHeader().setHighlightSections(True)
        self.verticalLayout_3.addWidget(self.tableRoster)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.button_new_shift = QtWidgets.QPushButton(self.tab)
        self.button_new_shift.setObjectName("button_new_shift")
        self.gridLayout_8.addWidget(self.button_new_shift, 0, 0, 1, 1)
        self.button_swap_shifts = QtWidgets.QPushButton(self.tab)
        self.button_swap_shifts.setObjectName("button_swap_shifts")
        self.gridLayout_8.addWidget(self.button_swap_shifts, 0, 1, 1, 1)
        self.button_new_roster = QtWidgets.QPushButton(self.tab)
        self.button_new_roster.setObjectName("button_new_roster")
        self.gridLayout_8.addWidget(self.button_new_roster, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem, 0, 3, 1, 1)
        self.button_delete_shift = QtWidgets.QPushButton(self.tab)
        self.button_delete_shift.setObjectName("button_delete_shift")
        self.gridLayout_8.addWidget(self.button_delete_shift, 0, 4, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_8)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_14 = QtWidgets.QLabel(self.tab)
        self.label_14.setObjectName("label_14")
        self.gridLayout_7.addWidget(self.label_14, 0, 0, 1, 1)
        self.spinBox_year = QtWidgets.QSpinBox(self.tab)
        self.spinBox_year.setMinimum(1950)
        self.spinBox_year.setMaximum(2200)
        self.spinBox_year.setProperty("value", 2021)
        self.spinBox_year.setObjectName("spinBox_year")
        self.gridLayout_7.addWidget(self.spinBox_year, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setObjectName("label_11")
        self.gridLayout_7.addWidget(self.label_11, 0, 2, 1, 1)
        self.plainTextEdit_summary = QtWidgets.QPlainTextEdit(self.tab)
        self.plainTextEdit_summary.setObjectName("plainTextEdit_summary")
        self.gridLayout_7.addWidget(self.plainTextEdit_summary, 0, 3, 2, 1)
        self.checkBox_ukevakt = QtWidgets.QCheckBox(self.tab)
        self.checkBox_ukevakt.setObjectName("checkBox_ukevakt")
        self.gridLayout_7.addWidget(self.checkBox_ukevakt, 0, 4, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setObjectName("label_15")
        self.gridLayout_7.addWidget(self.label_15, 1, 0, 1, 1)
        self.spinBox_week = QtWidgets.QSpinBox(self.tab)
        self.spinBox_week.setMinimum(1)
        self.spinBox_week.setMaximum(53)
        self.spinBox_week.setProperty("value", 41)
        self.spinBox_week.setObjectName("spinBox_week")
        self.gridLayout_7.addWidget(self.spinBox_week, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(17, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_7.addItem(spacerItem1, 1, 2, 1, 1)
        self.button_reminer = QtWidgets.QPushButton(self.tab)
        self.button_reminer.setObjectName("button_reminer")
        self.gridLayout_7.addWidget(self.button_reminer, 1, 4, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_7)
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setObjectName("label_12")
        self.gridLayout_10.addWidget(self.label_12, 0, 0, 1, 1)
        self.lineEdit_new_attendee = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_new_attendee.setObjectName("lineEdit_new_attendee")
        self.gridLayout_10.addWidget(self.lineEdit_new_attendee, 0, 1, 1, 1)
        self.button_add_attendee = QtWidgets.QPushButton(self.tab)
        self.button_add_attendee.setObjectName("button_add_attendee")
        self.gridLayout_10.addWidget(self.button_add_attendee, 0, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_10)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.listWidget_attendees = QtWidgets.QListWidget(self.tab)
        self.listWidget_attendees.setObjectName("listWidget_attendees")
        self.gridLayout_9.addWidget(self.listWidget_attendees, 0, 0, 2, 1)
        self.comboBox_status = QtWidgets.QComboBox(self.tab)
        self.comboBox_status.setMinimumSize(QtCore.QSize(150, 0))
        self.comboBox_status.setObjectName("comboBox_status")
        self.comboBox_status.addItem("")
        self.comboBox_status.addItem("")
        self.comboBox_status.addItem("")
        self.comboBox_status.addItem("")
        self.comboBox_status.addItem("")
        self.gridLayout_9.addWidget(self.comboBox_status, 0, 1, 1, 2)
        self.button_delete_attendee = QtWidgets.QPushButton(self.tab)
        self.button_delete_attendee.setObjectName("button_delete_attendee")
        self.gridLayout_9.addWidget(self.button_delete_attendee, 0, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_9.addItem(spacerItem2, 1, 1, 1, 1)
        self.button_save_event = QtWidgets.QPushButton(self.tab)
        self.button_save_event.setObjectName("button_save_event")
        self.gridLayout_9.addWidget(self.button_save_event, 1, 2, 1, 2)
        self.verticalLayout_3.addLayout(self.gridLayout_9)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableStaff = QtWidgets.QTableWidget(self.tab_2)
        self.tableStaff.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.tableStaff.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableStaff.setObjectName("tableStaff")
        self.tableStaff.setColumnCount(0)
        self.tableStaff.setRowCount(0)
        self.tableStaff.horizontalHeader().setHighlightSections(True)
        self.verticalLayout_2.addWidget(self.tableStaff)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.button_new_employee = QtWidgets.QPushButton(self.tab_2)
        self.button_new_employee.setObjectName("button_new_employee")
        self.gridLayout.addWidget(self.button_new_employee, 0, 0, 1, 1)
        self.button_new_institution = QtWidgets.QPushButton(self.tab_2)
        self.button_new_institution.setObjectName("button_new_institution")
        self.gridLayout.addWidget(self.button_new_institution, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 2, 1, 1)
        self.button_staff_delete = QtWidgets.QPushButton(self.tab_2)
        self.button_staff_delete.setObjectName("button_staff_delete")
        self.gridLayout.addWidget(self.button_staff_delete, 0, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_13 = QtWidgets.QGridLayout()
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_staff_name = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_staff_name.setText("")
        self.lineEdit_staff_name.setObjectName("lineEdit_staff_name")
        self.gridLayout_4.addWidget(self.lineEdit_staff_name, 0, 1, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit_staff_institution = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_staff_institution.setObjectName("lineEdit_staff_institution")
        self.gridLayout_3.addWidget(self.lineEdit_staff_institution, 0, 1, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_3, 0, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.lineEdit_staff_email = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_staff_email.setObjectName("lineEdit_staff_email")
        self.gridLayout_2.addWidget(self.lineEdit_staff_email, 0, 1, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_2, 0, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_13)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_5.addWidget(self.label_4, 0, 0, 1, 1)
        self.spinbox_shift_frq = QtWidgets.QDoubleSpinBox(self.tab_2)
        self.spinbox_shift_frq.setSingleStep(0.1)
        self.spinbox_shift_frq.setProperty("value", 1.0)
        self.spinbox_shift_frq.setObjectName("spinbox_shift_frq")
        self.gridLayout_5.addWidget(self.spinbox_shift_frq, 0, 1, 1, 1)
        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_6.addWidget(self.checkBox, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem4, 0, 2, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_6.addWidget(self.pushButton_3, 0, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_6)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.tab_3)
        self.calendarWidget.setGeometry(QtCore.QRect(20, 12, 711, 331))
        self.calendarWidget.setObjectName("calendarWidget")
        self.list_calendarEvents = QtWidgets.QListWidget(self.tab_3)
        self.list_calendarEvents.setGeometry(QtCore.QRect(20, 350, 711, 81))
        self.list_calendarEvents.setObjectName("list_calendarEvents")
        self.tabWidget.addTab(self.tab_3, "")
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 867, 22))
        self.menubar.setObjectName("menubar")
        self.menuNRIS = QtWidgets.QMenu(self.menubar)
        self.menuNRIS.setObjectName("menuNRIS")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionInfo = QtWidgets.QAction(MainWindow)
        self.actionInfo.setObjectName("actionInfo")
        self.menuNRIS.addAction(self.actionInfo)
        self.menubar.addAction(self.menuNRIS.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_new_shift.setText(_translate("MainWindow", "New shift"))
        self.button_swap_shifts.setText(_translate("MainWindow", "Swap"))
        self.button_new_roster.setText(_translate("MainWindow", "New roster"))
        self.button_delete_shift.setText(_translate("MainWindow", "Delete"))
        self.label_14.setText(_translate("MainWindow", "Year:"))
        self.label_11.setText(_translate("MainWindow", "Summary:"))
        self.checkBox_ukevakt.setText(_translate("MainWindow", "Ukevakt"))
        self.label_15.setText(_translate("MainWindow", "Week"))
        self.button_reminer.setText(_translate("MainWindow", "Remind"))
        self.label_12.setText(_translate("MainWindow", "Attendees:"))
        self.button_add_attendee.setText(_translate("MainWindow", "Add"))
        self.comboBox_status.setItemText(0, _translate("MainWindow", "needsAction"))
        self.comboBox_status.setItemText(1, _translate("MainWindow", "accepted"))
        self.comboBox_status.setItemText(2, _translate("MainWindow", "declined"))
        self.comboBox_status.setItemText(3, _translate("MainWindow", "tentative"))
        self.comboBox_status.setItemText(4, _translate("MainWindow", "who knows..."))
        self.button_delete_attendee.setText(_translate("MainWindow", "Delete"))
        self.button_save_event.setText(_translate("MainWindow", "Save and update calendar"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Roster"))
        self.button_new_employee.setText(_translate("MainWindow", "New emplyee"))
        self.button_new_institution.setText(_translate("MainWindow", "New Institution"))
        self.button_staff_delete.setText(_translate("MainWindow", "Delete"))
        self.label.setText(_translate("MainWindow", "Name"))
        self.label_2.setText(_translate("MainWindow", "Institution"))
        self.label_3.setText(_translate("MainWindow", "email"))
        self.label_4.setText(_translate("MainWindow", "Shift frequency"))
        self.checkBox.setText(_translate("MainWindow", "Shared shifts"))
        self.pushButton_3.setText(_translate("MainWindow", "Save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Staff"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Calendar"))
        self.menuNRIS.setTitle(_translate("MainWindow", "File"))
        self.actionInfo.setText(_translate("MainWindow", "Info"))
