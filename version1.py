import json

class Student:
    def __init__(self, username, password):
        self.username = username
        self.password = password

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

print("Welcome to the Opportunity Tracker!")

signup()