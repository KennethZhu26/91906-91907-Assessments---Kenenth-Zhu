import json

class Student:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Opportunity:
    def __init__(self, id, name, type, organisation, deadline):
        self.id = id
        self.name = name
        self.type = type
        self.organisation = organisation
        self.deadline = deadline

def load_data(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def signup():
    users = load_data("users.json")

    username = input("Create username: ")

    for user in users:
        if user["username"] == username:
            print("Username already exists.")
            return None

    password = input("Create password: ")

    if len(password) < 6:
        print("Password must be at least 6 characters.")
        return None

    new_student = Student(username, password)

    users.append({
        "username": new_student.username,
        "password": new_student.password
    })

    save_data("users.json", users)

    print("Account created successfully!")

    return username

def login():
    users = load_data("users.json")

    username = input("Username: ")
    password = input("Password: ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login successful!")
            return username

    print("Incorrect username or password.")
    return None

def get_opportunities():
    data = load_data("opportunities.json")
    opportunities = []

    for item in data:
        opportunity = Opportunity(
            item["id"],
            item["name"],
            item["type"],
            item["organisation"],
            item["deadline"]
        )

        opportunities.append(opportunity)

    return opportunities

def view_opportunities():
    opportunities = get_opportunities()

    print("\n===== Available Opportunities =====")

    if len(opportunities) == 0:
        print("No opportunities available.")
        return

    for opportunity in opportunities:
        print("-------------------------")
        print("ID:", opportunity.id)
        print("Name:", opportunity.name)
        print("Type:", opportunity.type)
        print("Organisation:", opportunity.organisation)
        print("Deadline:", opportunity.deadline)

def main():
    current_user = None

    while True:
        if current_user is None:
            print("\n===== Opportunity Tracker =====")
            print("1. Login")
            print("2. Create Account")
            print("3. Exit")

            choice = input("Select option: ")

            if choice == "1":
                current_user = login()

            elif choice == "2":
                current_user = signup()

            elif choice == "3":
                print("Goodbye!")
                break

            else:
                print("Invalid option.")

        else:
            print("\n===== Opportunity Tracker =====")
            print("Welcome,", current_user)
            print("1. View Available Opportunities")
            print("2. Apply for Opportunity")
            print("3. Logout")

            choice = input("Select option: ")

            if choice == "1":
                view_opportunities()

            elif choice == "2":
                print("Application system coming soon.")

            elif choice == "3":
                current_user = None
            print("Logged out.")

            else:
                print("Invalid option.")

print("Welcome to the Opportunity Tracker!")

signup()