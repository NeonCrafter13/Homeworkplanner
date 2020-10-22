from pynotifier import Notification
import data
from PyQt5.QtCore import QDate
import os

current_date = QDate.currentDate()
def start():
        
    for task in data.view_data():
        if task.important:
            Notification(
                title=task.subject,
                description=f"what: {task.what},\ndue_date: {task.due_date.toString()}",
                # On Windows .ico is required, on Linux - .png
                icon_path='path/to/image/file/icon.png',
                duration=5,                              # Duration in seconds
                urgency=Notification.URGENCY_CRITICAL
            ).send()
        elif task.due_date == current_date.addDays(1):
            Notification(
                title=task.subject,
                description=task.what,
                # On Windows .ico is required, on Linux - .png
                icon_path='path/to/image/file/icon.png',
                duration=5,                              # Duration in seconds
                urgency=Notification.URGENCY_LOW
            ).send()
        
