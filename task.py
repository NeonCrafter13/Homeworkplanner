from PyQt5.QtCore import QDate


class Task():
    def __init__(self, subject: str, what: str, due_date: QDate, important=False):
        self.subject = subject
        self.what = what
        self.due_date = due_date  # QtCore.QDate
        self.important = important
