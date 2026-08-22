# -----------------------------
# Opportunity Tracker Program
# -----------------------------

# Imports modules
import json
import tkinter as tk
from tkinter import messagebox

# ---------
# Classes
# ---------

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

# --------------
# File Handling
# --------------

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

# -------------
# Main Window
# -------------

# Creates the main Tkinter Window
root = tk.Tk()
root.title("Opportunity Tracker")
root.geometry("600x600")
root.resizable(False, False) # Prevents user from resizing window

current_user = None # Stores the username of the student who is currently logged in

# Defines the colours and fonts used for GUI
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

# --------------
# GUI Functions
# --------------

# Removes all widgets from current screen
# Used when changing between different screens
def clear_screen():
    # Gets a list of all widgets currently inside root and removes them
    for widget in root.winfo_children():
        widget.destroy()

# Creates labels with the program's formatting
def label(parent, text, font=NORMAL_FONT, colour=TEXT):
    return tk.Label(parent, text=text, font=font, bg=BACKGROUND, fg=colour)

#Creates buttons with program's formatting
def button(parent, text, command, width=25):
    return tk.Button(
        parent, text=text, command=command, width=width,
        font=BUTTON_FONT, bg=PRIMARY, fg=WHITE
    )

# Creates an input box
def entry(parent, width=30, password=False):
    if password:
        # Adds password hashing
        return tk.Entry(parent, width=width, font=NORMAL_FONT, show="*")
    return tk.Entry(parent, width=width, font=NORMAL_FONT)

# Creates a frame using program's background colour
def frame(parent):
    return tk.Frame(parent, bg=BACKGROUND)

# Exits the program aftering user confirmation
def exit_program():
    # Creates a pop-up window that asks a Yes/No question
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        messagebox.showinfo("Goodbye", "Thank you for using Opportunity Tracker!")
        root.destroy() # Closes main Tkinter Window

# -------------
# Login Screen
# -------------

def login_screen():
    clear_screen() # Removes everything currently displayed

    main_frame = frame(root) # Creates a frame inside main window
    main_frame.pack(expand=True) # Places frame into the window and allows extra space to be used

    # Displays the program title and description
    label(main_frame, "Opportunity Tracker", TITLE_FONT, PRIMARY).pack(pady=(40, 10))
    label(main_frame, "Manage your opportunities in one place").pack(pady=(0, 30))

    # Creates buttons for the main program options
    button(main_frame, "Login", login_form).pack(pady=8)
    button(main_frame, "Create Account", signup).pack(pady=8)
    button(main_frame, "Exit", exit_program).pack(pady=8)

# ------------
# Login Form
# ------------

def login_form():
    global username_entry, password_entry # Allows function to create/change variables used by other functions

    clear_screen()

    main_frame = frame(root)
    main_frame.pack(expand=True)

    label(main_frame, "Login", HEADING_FONT, PRIMARY).pack(pady=(20, 25))

    label(main_frame, "Username").pack() # Displays username label
    username_entry = entry(main_frame) # Creates an input box for username
    username_entry.pack(pady=6) # Places the username input box

    label(main_frame, "Password").pack(pady=(10, 0)) # Displays password label
    password_entry = entry(main_frame, password=True) # Creates a hidden password inout box
    password_entry.pack(pady=6) # Places the password input box

    button(main_frame, "Login", login).pack(pady=(20, 8)) #Creates login button
    button(main_frame, "Back", login_screen).pack(pady=5) # Creates back button

# -----------------
# Login Validation
# -----------------

# Checks the user's login details against saved accounts
def login():
    global current_user # Allows function to change current_user
    # Retrieves text typed into entry-box and removes unnecessary space from start and end
    username = username_entry.get().strip()
    password = password_entry.get()

    # Checks whether username is entered
    if username == "":
        messagebox.showerror("Error", "Please enter your username.")
        username_entry.focus() # Moves cursor back into username box
        return

    # Checks whether password is entered
    if password == "":
        messagebox.showerror("Error", "Please enter your password.")
        password_entry.focus()
        return

    users = load_data("users.json") #Loads all resigstered accounts from JSON file

    # Searches through users to find matching details
    for user in users:
        if user["username"] == username and user["password"] == password:
            #Saves username as currently logged-in user
            current_user = username
            messagebox.showinfo("Login Successful", "Welcome back, " + username + "!")
            main_menu()
            return

    messagebox.showerror("Login Failed", "Incorrect username or password.")
    password_entry.delete(0, tk.END) # Deletes password that was entered
    password_entry.focus()

# ---------------
# Sign Up Screen
# ---------------

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

    label(main_frame, "Password must be at least 6 characters.", ("Arial", 9)).pack(pady=5) # Displays the minimum password lengh requirement

    # Handles the account creation process
    def create_account():
        global current_user

        username = new_username_entry.get().strip()
        password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()

        #Validates that a username has been entered
        if username == "":
            messagebox.showerror("Error", "Please enter a username.")
            new_username_entry.focus()
            return

        #Validates that a password has been entered
        if password == "":
            messagebox.showerror("Error", "Please enter a password.")
            new_password_entry.focus()
            return

        #Checks that the password meets the minimum length
        if len(password) < 6:
            messagebox.showerror(
                "Password Error",
                "Password must be at least 6 characters.\nPlease create a new password."
            )
            new_password_entry.delete(0, tk.END) # Deletes incorrect password
            confirm_password_entry.delete(0, tk.END) # Deletes confirmation password
            new_password_entry.focus()
            return

        #Checks whether both enteries are the same
        if password != confirm_password:
            messagebox.showerror(
                "Password Error",
                "Passwords do not match.\nPlease try again."
            )
            confirm_password_entry.delete(0, tk.END)
            confirm_password_entry.focus()
            return

        users = load_data("users.json") # Loads existing users before adding new account

        # Checks whether username is already in use
        for user in users:
            if user["username"] == username:
                messagebox.showerror(
                    "Error",
                    "Username already exists.\nPlease choose another username."
                )
                new_username_entry.focus()
                return

        new_student = Student(username, password) #Creates a Student object using validated information

        # Converts Student object into a dictionary for JSON storage
        users.append({
            "username": new_student.username,
            "password": new_student.password
        })

        save_data("users.json", users) #Saves the updated user list

        current_user = username #Automatically logs new user in

        messagebox.showinfo("Account Created", "Account created successfully!\nYou are now logged in.")
        main_menu()

    button(main_frame, "Create Account", create_account).pack(pady=(15, 8))
    button(main_frame, "Back", login_screen).pack(pady=5)

# ----------
# Main Menu
# ----------

def main_menu():
    clear_screen()

    main_frame = frame(root)
    main_frame.pack(expand=True)

    label(main_frame, "Opportunity Tracker", TITLE_FONT, PRIMARY).pack(pady=(30, 10))
    label(main_frame, "Welcome, " + current_user, HEADING_FONT).pack(pady=(0, 30))

    button(main_frame, "View Opportunities", view_opportunities).pack(pady=8)
    button(main_frame, "Apply for Opportunity", apply_opportunity).pack(pady=8)
    button(main_frame, "Logout", logout).pack(pady=8)

# -------------------
# View Opportunities
# -------------------

def view_opportunities():
    clear_screen()

    label(root, "Available Opportunities", HEADING_FONT, PRIMARY).pack(pady=15)

    opportunities = get_opportunities()  # Gets all opportunities from JSON file

    #Checks whether opportunities list is empty
    if len(opportunities) == 0:
        label(root, "No opportunities available.").pack(pady=30)
    else:
        canvas = tk.Canvas(root, bg=BACKGROUND, highlightthickness=0) # Creates an area that contains other widgets
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=5) # Formatting Canvas

        # Creates a vertical scrollbar on the right
        scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=5)

        canvas.configure(yscrollcommand=scrollbar.set) #Connects scrollbar to the canvas

        opportunity_frame = frame(canvas) # Places opportunities inside this frame
        canvas.create_window((0, 0), window=opportunity_frame, anchor="nw") # Places frame inside Canvas with top left corner as anchor

        # Goes through every Opportunity objet
        for opportunity in opportunities:
            card = tk.Frame(opportunity_frame, bg=WHITE, bd=1, relief="solid")
            card.pack(fill="x", padx=10, pady=8)

            tk.Label(card, text=opportunity.name, font=("Arial", 13, "bold"), bg=WHITE, fg=PRIMARY).pack(anchor="w", padx=12, pady=(10, 4))
            tk.Label(card, text="ID: " + str(opportunity.id), font=NORMAL_FONT, bg=WHITE, fg=TEXT).pack(anchor="w", padx=12)
            tk.Label(card, text="Type: " + opportunity.type, font=NORMAL_FONT, bg=WHITE, fg=TEXT).pack(anchor="w", padx=12)
            tk.Label(card, text="Organisation: " + opportunity.organisation, font=NORMAL_FONT, bg=WHITE, fg=TEXT).pack(anchor="w", padx=12)
            tk.Label(card, text="Deadline: " + opportunity.deadline, font=NORMAL_FONT, bg=WHITE, fg=TEXT).pack(anchor="w", padx=12, pady=(0, 10))

        opportunity_frame.update_idletasks() # Updates the scrollable area to fit all opportunity cards
        canvas.configure(scrollregion=canvas.bbox("all")) # Tells the Canvas how large scrollable area (area containing all objects)

    button(root, "Back", main_menu, width=15).pack(pady=10)

# ------------------------
# Opportunity Application
# ------------------------

def apply_opportunity():
    clear_screen()

    main_frame = frame(root)
    main_frame.pack(expand=True)

    label(main_frame, "Apply for Opportunity", HEADING_FONT, PRIMARY).pack(pady=20)
    label(main_frame, "Enter Opportunity ID:").pack()

    id_entry = entry(main_frame, width=20)
    id_entry.pack(pady=10)

    #Handles application submission
    def submit_application():
        value = id_entry.get().strip() # Gets the text entered into ID box

        # Checks user has entered an ID
        if value == "":
            messagebox.showerror("Error", "Please enter an opportunity ID.")
            id_entry.focus()
            return

        #Checks that ID is a number
        try:
            choice = int(value)
        except ValueError:
            messagebox.showerror("Error", "Opportunity ID must be a number.")
            id_entry.delete(0, tk.END) # Clears the invalid input
            id_entry.focus()
            return

        opportunities = get_opportunities() # Loads all avaliable opportunities
        applications = load_data("applications.json") # Loads all existing applications

        # Searches for an opportunity matching with the entered ID
        for opportunity in opportunities:
            if opportunity.id == choice:

                # Prevents same user from applying multiple times
                for application in applications:
                    if (application["username"] == current_user and
                            application["opportunity_id"] == opportunity.id):
                        messagebox.showerror(
                            "Already Applied",
                            "You have already applied for this opportunity."
                        )
                        return

                # Creates a new Application object
                new_application = Application(
                    current_user,
                    opportunity.id,
                    opportunity.name,
                    "Applied"
                )

                # Converts Application object into dictionary
                applications.append({
                    "username": new_application.username,
                    "opportunity_id": new_application.opportunity_id,
                    "opportunity_name": new_application.opportunity_name,
                    "status": new_application.status
                })

                # Saves the new application list
                save_data("applications.json", applications)

                messagebox.showinfo(
                    "Application Submitted",
                    "Your application has been submitted successfully!"
                )
                main_menu()
                return

        messagebox.showerror("Error", "Opportunity not found.")
        id_entry.delete(0, tk.END) # Clears invalid opportunity ID
        id_entry.focus()

    button(main_frame, "Submit Application", submit_application).pack(pady=10)
    button(main_frame, "Back", main_menu).pack(pady=5)

# ----------------
# Logout Function
# ----------------

# Logs the current user out and returns to login screen
def logout():
    global current_user

    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        # Changes current_user to none so that no one is logged in
        current_user = None
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")
        login_screen()

# ---------------------
# Starting the program
# ---------------------

login_screen() # Calls function and starts by displaying login screen
root.mainloop() # Keeps Tkinter window running and waits for interactions