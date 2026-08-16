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

current_user = None
root.configure(bg=BACKGROUND)

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()


def label(parent, text, font=NORMAL_FONT, colour=TEXT):
    return tk.Label(parent, text=text, font=font, bg=BACKGROUND, fg=colour)


def button(parent, text, command, width=25):
    return tk.Button(
        parent, text=text, command=command, width=width,
        font=BUTTON_FONT, bg=PRIMARY, fg=WHITE
    )


def entry(parent, width=30, password=False):
    if password:
        return tk.Entry(parent, width=width, font=NORMAL_FONT, show="*")
    return tk.Entry(parent, width=width, font=NORMAL_FONT)


def frame(parent):
    return tk.Frame(parent, bg=BACKGROUND)

def exit_program():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        messagebox.showinfo("Goodbye", "Thank you for using Opportunity Tracker!")
        root.destroy()

def login_screen():
    clear_screen()

    main_frame = frame(root)
    main_frame.pack(expand=True)

    label(main_frame, "Opportunity Tracker", TITLE_FONT, PRIMARY).pack(pady=(40, 10))
    label(main_frame, "Manage your opportunities in one place").pack(pady=(0, 30))

    button(main_frame, "Login", login_form).pack(pady=8)
    button(main_frame, "Create Account", signup).pack(pady=8)
    button(main_frame, "Exit", exit_program).pack(pady=8)

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
            main_menu()
            return

    messagebox.showerror("Login Failed", "Incorrect username or password.")
    password_entry.delete(0, tk.END)
    password_entry.focus()


def signup():
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

        messagebox.showinfo("Account Created", "Account created successfully!\nYou are now logged in.")
        main_menu()

    button(main_frame, "Create Account", create_account).pack(pady=(15, 8))
    button(main_frame, "Back", login_screen).pack(pady=5)



def main_menu():
    clear_screen()

    main_frame = frame(root)
    main_frame.pack(expand=True)

    label(main_frame, "Opportunity Tracker", TITLE_FONT, PRIMARY).pack(pady=(30, 10))
    label(main_frame, "Welcome, " + current_user, HEADING_FONT).pack(pady=(0, 30))

    button(main_frame, "View Opportunities", view_opportunities).pack(pady=8)
    button(main_frame, "Apply for Opportunity", apply_opportunity).pack(pady=8)
    button(main_frame, "Logout", logout).pack(pady=8)



def view_opportunities():
    clear_screen()

    label(root, "Available Opportunities", HEADING_FONT, PRIMARY).pack(pady=15)

    opportunities = get_opportunities()

    if len(opportunities) == 0:
        label(root, "No opportunities available.").pack(pady=30)
    else:
        canvas = tk.Canvas(root, bg=BACKGROUND, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=5)

        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=5)

        canvas.configure(yscrollcommand=scrollbar.set)

        opportunity_frame = frame(canvas)
        canvas.create_window((0, 0), window=opportunity_frame, anchor="nw")

        for opportunity in opportunities:
            card = tk.Frame(opportunity_frame, bg=WHITE, bd=1, relief="solid")
            card.pack(fill="x", padx=10, pady=8)

            tk.Label(card, text=opportunity.name, font=("Arial", 13, "bold"), bg=WHITE, fg=PRIMARY).pack(anchor="w", padx=12, pady=(10, 4))
            tk.Label(card, text="ID: " + str(opportunity.id), font=NORMAL_FONT, bg=WHITE, fg=TEXT).pack(anchor="w", padx=12)
            tk.Label(card, text="Type: " + opportunity.type, font=NORMAL_FONT, bg=WHITE, fg=TEXT).pack(anchor="w", padx=12)
            tk.Label(card, text="Organisation: " + opportunity.organisation, font=NORMAL_FONT, bg=WHITE, fg=TEXT).pack(anchor="w", padx=12)
            tk.Label(card, text="Deadline: " + opportunity.deadline, font=NORMAL_FONT, bg=WHITE, fg=TEXT).pack(anchor="w", padx=12, pady=(0, 10))

        opportunity_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    button(root, "Back", main_menu, width=15).pack(pady=10)

def apply_opportunity():
    clear_screen()

    main_frame = frame(root)
    main_frame.pack(expand=True)

    label(main_frame, "Apply for Opportunity", HEADING_FONT, PRIMARY).pack(pady=20)
    label(main_frame, "Enter Opportunity ID:").pack()

    id_entry = entry(main_frame, width=20)
    id_entry.pack(pady=10)

    def submit_application():
        value = id_entry.get().strip()

        if value == "":
            messagebox.showerror("Error", "Please enter an opportunity ID.")
            id_entry.focus()
            return

        try:
            choice = int(value)
        except ValueError:
            messagebox.showerror("Error", "Opportunity ID must be a number.")
            id_entry.delete(0, tk.END)
            id_entry.focus()
            return

        opportunities = get_opportunities()
        applications = load_data("applications.json")

        for opportunity in opportunities:
            if opportunity.id == choice:

                for application in applications:
                    if (application["username"] == current_user and
                            application["opportunity_id"] == opportunity.id):
                        messagebox.showerror(
                            "Already Applied",
                            "You have already applied for this opportunity."
                        )
                        return

                new_application = Application(
                    current_user,
                    opportunity.id,
                    opportunity.name,
                    "Applied"
                )

                applications.append({
                    "username": new_application.username,
                    "opportunity_id": new_application.opportunity_id,
                    "opportunity_name": new_application.opportunity_name,
                    "status": new_application.status
                })

                save_data("applications.json", applications)

                messagebox.showinfo(
                    "Application Submitted",
                    "Your application has been submitted successfully!"
                )
                main_menu()
                return

        messagebox.showerror("Error", "Opportunity not found.")
        id_entry.delete(0, tk.END)
        id_entry.focus()

    button(main_frame, "Submit Application", submit_application).pack(pady=10)
    button(main_frame, "Back", main_menu).pack(pady=5)

def logout():
    global current_user

    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        current_user = None
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")
        login_screen()

login_screen()
root.mainloop()