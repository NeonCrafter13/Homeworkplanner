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
    QAbstractItemView
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

app = QApplication(sys.argv)

class TasksWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.h = QHBoxLayout(self)
        self.scroll = QScrollArea()
        # self.h.addWidget(scroll)
        self.scroll.setWidgetResizable(True)
        self.scrollcontent = QListWidget(self.scroll)

        for i in range(20):
            a = QListWidgetItem(str(i))
            self.scrollcontent.addItem(a)

        self.scroll.setWidget(self.scrollcontent)
        self.h.addWidget(self.scroll)
        self.setLayout(self.h)
        # self.scroll.show()

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.v = QVBoxLayout(self)
        self.v.addWidget(QLabel("NEW"))
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

