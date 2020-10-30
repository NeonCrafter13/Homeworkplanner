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

def delete_data(index: int):
	view_data()
	new_data = []
	with open (filename, "r") as f:
		temp = json.load(f)
		data_length = len(temp)-1
	delete_option = index
	i = 0
	for entry in temp:
		if i == int(delete_option):
			pass
			i=i+1
		else:
			new_data.append(entry)
			i=i+1
	with open (filename, 'w') as f:
		json.dump(new_data, f, indent=4)

def edit_data(index: int, task: Task):
	subject = task.subject
	homework = task.what
	due_date = task.due_date
	important = task.important

	new_data = []
	with open (filename, "r") as f:
		temp = json.load(f)
		data_length = len(temp)-1
	edit_option = index
	i = 0
	item_data = {}
	for entry in temp:
		if i == int(edit_option):
			item_data["subject"] = subject
			item_data["homework"] = homework
			item_data["due_date"] = [*due_date.getDate()]
			item_data["important"] = important
			new_data.append(item_data)
		else:
			new_data.append(entry)
			i=i+1
	with open (filename, 'w') as f:
		json.dump(new_data, f, indent=4)
		
def check_date(): #checks date then if the date is false it gets deleted 
    view_data()
    today = str(date.today())
    today = today.replace("-", "")
    print(today)  # '2017-12-26'
    lis = []
    with open(filename, "r") as f:
        temp = json.load(f)
        for entry in temp:
            name = entry["name"]
            homework = entry["homework"]
            due_date = entry["due_date"]
            print(due_date)
            if today < due_date:
                print("Old date")
                old_data = True
                lis.append({"name": name, "homework": homework, "due_date": due_date, "old_data": old_data})
    with open(filename, 'w') as f:
        json.dump(lis, f, indent=4)
		
def turn_true():  # Makes old_task = True or false depending on current time compared to due_date
    view_data()
    new_data = []
    current_time = datetime.datetime.today().strftime("%Y%m%d")
    current_time = current_time.replace(".", " ")
    with open(filename, "r") as f:
        temp = json.load(f)
    i = 0
    for entry in temp:
        due_date = entry["due_date"]
        if current_time > due_date:
            name = entry["name"]
            homework = entry["homework"]
            due_date = entry["due_date"]
            old_data = entry["old_data"]
            old_data = True
            new_data.append({"name": name, "homework": homework, "due_date": due_date, "old_data": old_data})
            i = i + 1
        else:
            new_data.append(entry)
            i = i + 1
    with open(filename, 'w') as f:
        json.dump(new_data, f, indent=4)
	
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
