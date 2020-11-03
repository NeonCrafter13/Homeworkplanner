#! /usr/bin/env python3

import concurrent.futures

import subprocess


subprocess.run(["pip3", "install", "py_notifier"])
subprocess.run(["pip3", "install", "zmtools>=1.3.0"])

import configparser
import sys

from PyQt5.QtCore import QDateTime, QObject, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QCheckBox, QDateEdit, QHBoxLayout,
                             QLabel, QLineEdit, QListWidget, QListWidgetItem,
                             QMainWindow, QPushButton, QScrollArea,
                             QVBoxLayout, QWidget)

from zmtools import get_module


# Import all custom modules, attempting from PATH first and then /usr/share/homeworkplanner/
for m in ("data", "notifications", "task"):
    globals()[m] = get_module(m, "/usr/share/homeworkplanner/{}.py".format(m))

app = QApplication(sys.argv)

config = configparser.ConfigParser()
config.read("/usr/share/homeworkplanner/settings.ini")

try:
    if config["OPTIONS"]["notifications"] == "True":
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(notifications.start) #Starts Notifications
except:
    pass

try:
    if config["OPTIONS"]["delete_old"] == "True":
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(data.check_date)
except:
    pass

editIcon = QIcon("/usr/share/homeworkplanner/edit.png")
deleteIcon = QIcon("/usr/share/homeworkplanner/delete.png")

class RefreshTasksEvent(QObject):
    refresh = pyqtSignal()

Task = task.Task

refreshtasksevent = RefreshTasksEvent()

class EditWindow(QWidget):
    def __init__(self, task: Task, index: int):
        super().__init__()
        self.task = task
        self.index = index #Index of the task
        self.initMe()

    def initMe(self):
        self.h = QHBoxLayout(self)

        self.subject = QLineEdit(self.task.subject)
        self.h.addWidget(self.subject)

        self.what = QLineEdit(self.task.what)
        self.h.addWidget(self.what)

        self.due_date = QDateEdit(calendarPopup=True)
        self.h.addWidget(self.due_date)
        self.due_date.setDate(self.task.due_date)

        self.info = QLabel("Mark as important:")
        self.h.addWidget(self.info)

        self.important = QCheckBox()
        self.important.setChecked(self.task.important)
        self.h.addWidget(self.important)

        self.submitbutton = QPushButton("Submit")
        self.submitbutton.clicked.connect(self.submit)
        self.h.addWidget(self.submitbutton)

        self.setLayout(self.h)

    def submit(self):
        # Creates new Task
        subject = self.subject.text()
        what = self.what.text()
        due_date = self.due_date.date()
        important = self.important.isChecked()
        newtask = Task(subject, what, due_date, important)

        #Change Json
        data.edit_data(self.index, newtask)

        self.setParent(None)
        refreshtasksevent.refresh.emit()

class TaskView(QWidget):
    def __init__(self, task: Task, index: int):
        super().__init__()
        self.task = task
        self.index = index
        self.initMe()

    def initMe(self):

        if self.task.important:
            self.setStyleSheet("color: #DC143C;\nfont-weight: bold;")

        self.h = QHBoxLayout(self)

        self.h.addWidget(QLabel(self.task.subject))

        self.h.addWidget(QLabel(self.task.what))

        self.h.addWidget(QLabel(self.task.due_date.toString()))

        self.editBtn = QPushButton(icon=editIcon)
        self.editBtn.clicked.connect(self.edit)
        self.h.addWidget(self.editBtn)

        self.deleteBtn = QPushButton(icon=deleteIcon)
        self.deleteBtn.clicked.connect(self.delete)
        self.h.addWidget(self.deleteBtn)

        self.setLayout(self.h)

    def edit(self):
        self.editwindow = EditWindow(self.task, self.index)
        self.editwindow.show()

    def delete(self):
        data.delete_data(self.index)
        refreshtasksevent.refresh.emit()

class NewTaskWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.h = QHBoxLayout(self)

        self.subject = QLineEdit("Subject:")
        self.h.addWidget(self.subject)

        self.what = QLineEdit("What:")
        self.h.addWidget(self.what)

        self.due_date = QDateEdit(calendarPopup=True)
        self.h.addWidget(self.due_date)
        self.due_date.setDateTime(QDateTime.currentDateTime())

        self.info = QLabel("Mark as important:")
        self.h.addWidget(self.info)

        self.important = QCheckBox()
        self.h.addWidget(self.important)

        self.submitbutton = QPushButton("Submit")
        self.submitbutton.clicked.connect(self.submit)
        self.h.addWidget(self.submitbutton)

        self.setLayout(self.h)

    def submit(self):
        # Creates new Task
        subject = self.subject.text()
        what = self.what.text()
        due_date = self.due_date.date()
        important = self.important.isChecked()
        newtask = Task(subject, what, due_date, important)

        #Add to Json
        data.add_data(newtask)

        refreshtasksevent.refresh.emit()

class TasksWidget(QWidget):
    def __init__(self):
        super().__init__()

        refreshtasksevent.refresh.connect(self.reloadTasks)

        self.initMe()

    def initMe(self):
        self.h = QHBoxLayout(self)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scrollcontent = QListWidget()

        i = 0
        for task in data.view_data():
            itemN = QListWidgetItem()

            itemN = QListWidgetItem()
            widget = TaskView(task, i)
            itemN.setSizeHint(widget.sizeHint())
            itemN.setFlags(Qt.ItemIsSelectable)

            self.scrollcontent.addItem(itemN)
            self.scrollcontent.setItemWidget(itemN, widget)

            i += 1

        self.scroll.setWidget(self.scrollcontent)
        self.h.addWidget(self.scroll)
        self.setLayout(self.h)

    def reloadTasks(self):

        self.scrollcontent.clear()
        i = 0
        for task in data.view_data():
            itemN = QListWidgetItem()

            itemN = QListWidgetItem()
            widget = TaskView(task, i)
            itemN.setSizeHint(widget.sizeHint())
            itemN.setFlags(Qt.ItemIsSelectable)

            self.scrollcontent.addItem(itemN)
            self.scrollcontent.setItemWidget(itemN, widget)
            i += 1

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.v = QVBoxLayout(self)
        self.v.addWidget(QLabel("Create new Task:"))
        self.v.addWidget(NewTaskWidget())
        self.v.addWidget(QLabel("Tasks:"))
        self.v.addWidget(TasksWidget())
        self.setLayout(self.v)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.setWindowTitle("Homeworkplanner") # Change later to better name
        self.setWindowIcon(QIcon("/usr/share/homeworkplanner/icon.png"))
        self.main = MainWidget()
        self.setCentralWidget(self.main)
        self.show()

# opens the Window
w = MainWindow()
# Closes App when Window is closed
sys.exit(app.exec_())
