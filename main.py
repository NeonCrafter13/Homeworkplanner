import sys
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QMainWindow,
    QAction,
    QGridLayout,
    QScrollArea,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
    QLineEdit,
    QDateEdit,
    QCheckBox
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QDateTime

from task import Task
import data

app = QApplication(sys.argv)

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

        # Todo: Add Task to QListWidget


class TasksWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.h = QHBoxLayout(self)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scrollcontent = QListWidget(self.scroll)

        for i in range(20):
            a = QListWidgetItem(str(i))
            self.scrollcontent.addItem(a)

        self.scroll.setWidget(self.scrollcontent)
        self.h.addWidget(self.scroll)
        self.setLayout(self.h)

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
        # self.setWindowIcon(QIcon("someIcon.png"))
        self.main = MainWidget()
        self.setCentralWidget(self.main)
        self.show()


# opens the Window
w = MainWindow()
# Closes App when Window is closed
sys.exit(app.exec_())

