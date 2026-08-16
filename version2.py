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

# =========================
# Signup
# =========================

def signup():
    global new_username_entry, new_password_entry, confirm_password_entry
    clear_screen()

    main_frame = frame(root)
    main_frame.pack(expand=True)

    label(main_frame, "Create Account", HEADING_FONT, PRIMARY).pack(pady=(15, 20))

    label(main_frame, "Username").pack()
    new_username_entry = entry(main_frame)
    new_username_entry.pack(pady=5)

    label(main_frame, "Password").pack(pady=(8, 0))
    new_password_entry = entry(main_frame, password=True)
    new_password_entry.pack(pady=5)

    label(main_frame, "Confirm Password").pack(pady=(8, 0))
    confirm_password_entry = entry(main_frame, password=True)
    confirm_password_entry.pack(pady=5)

    label(main_frame, "Password must be at least 6 characters.", ("Arial", 9)).pack(pady=5)

    button(main_frame, "Create Account", create_account).pack(pady=(15, 8))
    button(main_frame, "Back", login_screen).pack(pady=5)

def login_form():
    global username_entry, password_entry

    clear_screen()

    main_frame = frame(root)
    main_frame.pack(expand=True)

    label(main_frame, "Login", HEADING_FONT, PRIMARY).pack(pady=(20, 25))

    label(main_frame, "Username").pack()
    username_entry = entry(main_frame)
    username_entry.pack(pady=6)

    label(main_frame, "Password").pack(pady=(10, 0))
    password_entry = entry(main_frame, password=True)
    password_entry.pack(pady=6)

    button(main_frame, "Login", login).pack(pady=(20, 8))
    button(main_frame, "Back", login_screen).pack(pady=5)

def create_account():
    global current_user

    username = new_username_entry.get().strip()
    password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()

    if username == "":
        messagebox.showerror("Error", "Please enter a username.")
        new_username_entry.focus()
        return

    if password == "":
        messagebox.showerror("Error", "Please enter a password.")
        new_password_entry.focus()
        return

    if len(password) < 6:
        messagebox.showerror(
            "Password Error",
            "Password must be at least 6 characters.\nPlease create a new password."
        )
        new_password_entry.delete(0, tk.END)
        confirm_password_entry.delete(0, tk.END)
        new_password_entry.focus()
        return

    if password != confirm_password:
        messagebox.showerror(
            "Password Error",
            "Passwords do not match.\nPlease try again."
        )
        confirm_password_entry.delete(0, tk.END)
        confirm_password_entry.focus()
        return

    users = load_data("users.json")

    for user in users:
        if user["username"] == username:
            messagebox.showerror(
                "Error",
                "Username already exists.\nPlease choose another username."
            )
            new_username_entry.focus()
            return

    new_student = Student(username, password)

    users.append({
        "username": new_student.username,
        "password": new_student.password
    })

    save_data("users.json", users)

    current_user = username

    messagebox.showinfo(
        "Account Created",
        "Account created successfully!\nYou are now logged in."
    )

# =========================
# Login
# =========================

def login():
    global current_user

    username = username_entry.get().strip()
    password = password_entry.get()

    if username == "":
        messagebox.showerror("Error", "Please enter your username.")
        username_entry.focus()
        return

    if password == "":
        messagebox.showerror("Error", "Please enter your password.")
        password_entry.focus()
        return

    users = load_data("users.json")

    for user in users:
        if user["username"] == username and user["password"] == password:
            current_user = username
            messagebox.showinfo("Login Successful", "Welcome back, " + username + "!")
            return

    messagebox.showerror("Login Failed", "Incorrect username or password.")
    password_entry.delete(0, tk.END)
    password_entry.focus()

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

    label(main_frame, "Opportunity Tracker", TITLE_FONT, PRIMARY).pack(pady=(40, 10))
    label(main_frame, "Manage your opportunities in one place").pack(pady=(0, 30))

    button(main_frame, "Login", login_form).pack(pady=8)
    button(main_frame, "Create Account", signup).pack(pady=8)
    button(main_frame, "Exit", exit_program).pack(pady=8)



login_screen()
root.mainloop()