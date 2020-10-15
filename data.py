# Data Managment
# Loading Tasks from Somewhere (Should be returned as list of task.Task)
# Creating/Saving Tasks to Somwhere
# Editing Tasks
# probably Json, sqlite
#-------------------------------------------------------------------------------------
import json

filename = "./data/jsondata.json"
def Choices():
	print("Data Management")
	print("(1) View Data")
	print("(2) Edit Data")
	print("(3) Exit")

def view_data():
	with open (filename, "r") as f:
		temp = json.load(f)
		for entry in temp:
			name = entry["name"]
			homework = entry["homework"]
			due_date = entry["due_date"]
			print(f"Name: {name}")
			print(f"Homework: {homework}")
			print(f"Due Date: {due_date}")
			print("\n\n")

def add_data():
	item_data = {}
	with open (filename, "r") as f:
		temp = json.load(f)
	item_data["name"] = input("Your Name: ")
	item_data["homework"] = input("What Homework Do You Have: ")
	item_data["due_date"] = input("When Is The Homework Due: ")
	temp.append(item_data)
	with open (filename, 'w') as f:
		json.dump(temp, f, indent=4)


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

