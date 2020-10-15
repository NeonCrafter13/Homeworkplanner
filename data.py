# Data Managment
# Loading Tasks from Somewhere (Should be returned as list of task.Task)
# Creating/Saving Tasks to Somwhere
# Editing Tasks
# probably Json, sqlite
#-------------------------------------------------------------------------------------
import json
from task import Task
from PyQt5.QtCore import QDate #Class of the Dates

filename = "./data/jsondata.json"
def Choices():
	print("Data Management")
	print("(1) View Data")
	print("(2) Edit Data")
	print("(3) Exit")

def view_data():
	with open (filename, "r") as f:
		temp = json.load(f)
		tasks = [] #Lists of Task.task
		for entry in temp:
			subject = entry["subject"]
			homework = entry["homework"]
			due_date = entry["due_date"] #List of 3 int for year, month, day
			due_date = QDate(*due_date)
			important = entry["important"]
			tasks.append(Task(subject, homework, due_date, important=important))
		return tasks
			

def add_data(task: Task):
	subject = task.subject
	homework = task.what
	due_date = task.due_date
	important = task.important
	item_data = {}
	with open (filename, "r") as f:
		temp = json.load(f)
	item_data["subject"] = subject
	item_data["homework"] = homework
	item_data["due_date"] = [*due_date.getDate()]
	item_data["important"] = important
	temp.append(item_data)
	with open (filename, 'w') as f:
		json.dump(temp, f, indent=4)

"""
while True:
	Choices()
	choice = input("\nEnter Number: ") 
	if choice == '1':
		view_data()
	elif choice == '2':
		add_data()
	elif choice == '3':
		break
	else:
		print("You did not select a number, please read more carefully")
"""
