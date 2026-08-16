#=============================
# Opportunity Tracker Program
#=============================

import json
import tkinter as tk
from tkinter import messagebox

# Classes

# Stores the username and password of a student
# Used when creating a new students' account
class Student:
    def __init__(self, username, password):
        self.username = username
        self.password = password

# Stores all information regarding avaliable opportunities
class Opportunity:
    def __init__(self, id, name, type, organisation, deadline):
        self.id = id
        self.name = name
        self.type = type
        self.organisation = organisation
        self.deadline = deadline

# Stores information regarding a student's application
# This records who has applied, which opportunity they have applied for and application status
class Application:
    def __init__(self, username, opportunity_id, opportunity_name, status):
        self.username = username
        self.opportunity_id = opportunity_id
        self.opportunity_name = opportunity_name
        self.status = status

# File Handling

# Loads data from JSON file and then returns as Python data
# If file does not yet exist, empty list is returned instead of crashing
def load_data(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Saves Python data to JSON file so that information can be used again even after restarting
def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Account Functions

# Allows a new student to create an account and then saves their details to users.json
def signup():
    users = load_data("users.json")

    username = input("Create username: ")

    # Checks all existing users to make sure username is not already taken
    for user in users:
        if user["username"] == username:
            print("Username already exists.")
            return None

    password = input("Create password: ")

    # Checks that password created meets the minimum length requirement
    if len(password) < 6:
        print("Password must be at least 6 characters.")
        return None

    # Creates a Student object using the new account details
    new_student = Student(username, password)

    # Adds the new student's details to the list of users
    users.append({
        "username": new_student.username,
        "password": new_student.password
    })

    # Saves the updated user list to the JSON file
    save_data("users.json", users)

    print("Account created successfully!")
    print("You are now logged in.")

    # Returns the username so that student can be logged in immediately after sign up
    return username

# Checks the username and password against the account details stored in users.json
def login():
    users = load_data("users.json")

    username = input("Username: ")
    password = input("Password: ")

    # Searches through each stored user to find matching login details
    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login successful!")
            return username

    # Runs if no account matches login details entered
    print("Incorrect username or password.")
    return None

# Opportunity Functions

# Loads opportunities from the JSON file and the converts them into Opportunity objects
def get_opportunities():
    data = load_data("opportunities.json")
    opportunities = []

    # Goes through each opportunity stored in JSON file
    for item in data:
        opportunity = Opportunity(
            item["id"],
            item["name"],
            item["type"],
            item["organisation"],
            item["deadline"]
        )

        # Adds each Opportunity object to opportunities list
        opportunities.append(opportunity)

    return opportunities

root = tk.Tk()
root.title("Opportunity Tracker")
root.geometry("600x600")
root.resizable(False, False)

current_user = None

BACKGROUND = "#F2F4F7"
PRIMARY = "#2F5D8C"
SECONDARY = "#E8EEF5"
TEXT = "#222222"
WHITE = "#FFFFFF"

TITLE_FONT = ("Arial", 24, "bold")
HEADING_FONT = ("Arial", 18, "bold")
NORMAL_FONT = ("Arial", 11)
BUTTON_FONT = ("Arial", 11, "bold")

root.configure(bg=BACKGROUND)

# =========================
# GUI Helper Functions
# =========================

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()


def label(parent, text, font=NORMAL_FONT, colour=TEXT):
    return tk.Label(
        parent,
        text=text,
        font=font,
        bg=BACKGROUND,
        fg=colour
    )


def button(parent, text, command, width=25):
    return tk.Button(
        parent,
        text=text,
        command=command,
        width=width,
        font=BUTTON_FONT,
        bg=PRIMARY,
        fg=WHITE
    )


def entry(parent, width=30, password=False):
    if password:
        return tk.Entry(
            parent,
            width=width,
            font=NORMAL_FONT,
            show="*"
        )

    return tk.Entry(
        parent,
        width=width,
        font=NORMAL_FONT
    )


def frame(parent):
    return tk.Frame(
        parent,
        bg=BACKGROUND
    )

# Displays all avaliable opportunities if selected
def view_opportunities():
    opportunities = get_opportunities()

    print("\n===== Available Opportunities =====")

    # Checks whether there are any opportunities to display
    if len(opportunities) == 0:
        print("No opportunities available.")
        return

    # Displays the details of each avaliable opportunity
    for opportunity in opportunities:
        print("-------------------------")
        print("ID:", opportunity.id)
        print("Name:", opportunity.name)
        print("Type:", opportunity.type)
        print("Organisation:", opportunity.organisation)
        print("Deadline:", opportunity.deadline)

# Allows student to apply for opportunity using its corresponding ID
def apply_opportunity(username):
    opportunities = get_opportunities()
    applications = load_data("applications.json")

    # Attempts to convert user's input into an integer to prevent errors from entering letters
    try:
        choice = int(input("\nEnter opportunity ID to apply for: "))
    except ValueError:
        print("Please enter a number.")
        return

    # Searches for an opportunity with an ID which matches the user's input
    for opportunity in opportunities:
        if opportunity.id == choice:

            # Creates an Application object for the selected opportunity
            new_application = Application(
                username,
                opportunity.id,
                opportunity.name,
                "Applied"
            )

            # Adds the application information to the application list
            applications.append({
                "username": new_application.username,
                "opportunity_id": new_application.opportunity_id,
                "opportunity_name": new_application.opportunity_name,
                "status": new_application.status
            })

            # Saves the new application to applications.json
            save_data("applications.json", applications)

            print("Application submitted successfully!")
            return

    # Runs if entered ID does not match with any avaliable opportunities
    print("Opportunity not found.")


def login_screen():
    clear_screen()

    main_frame = frame(root)
    main_frame.pack(expand=True)

    label(
        main_frame,
        "Opportunity Tracker",
        TITLE_FONT,
        PRIMARY
    ).pack(pady=(40, 10))

    label(
        main_frame,
        "Manage your opportunities in one place"
    ).pack(pady=(0, 30))

    button(
        main_frame,
        "Login",
        login_form
    ).pack(pady=8)

    button(
        main_frame,
        "Create Account",
        signup
    ).pack(pady=8)

    button(
        main_frame,
        "Exit",
        exit_program
    ).pack(pady=8)

login_screen()
root.mainloop()