class Task():
    def __init__(self, subject: str, what: str, deadline, important = False):
        self.subject = subject
        self.what = what
        self.deadline = deadline # QtCore.QDate
        self.important = important
