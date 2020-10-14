class Task(self):
    def __init__(self, subject: str, what: str, deadline, important = False):
        self.subject = subject
        self.what = what
        self.deadline = deadline # Probably Datetime Object?
        self.important = important
