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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initMe()

    def initMe(self):
        self.setWindowTitle("Homeworkplanner") # Change later to better name
        # self.setWindowIcon(QIcon("someIcon.png"))


        self.show()


# opens the Window
w = MainWindow()
# Closes App when Window is closed
sys.exit(app.exec_())

