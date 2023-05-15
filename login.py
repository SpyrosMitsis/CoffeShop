import hashlib
import csv
import uuid
import os


def get_username():
    """
    prompts the user for a username
    :return: returns entered username
    """
    username = input("Enter username\n> ")
    username = username.replace(" ", "")
    if not username: 
        print("Username field cannot be empty!")
        return get_username()

    return username


def get_password(x="login"):
    """
    prompts the user for a password, can be used for log in or sign up
    :param x: x by default is in login mode if x is in sign up mode
    the function prompts the users to re-enter the password and
    ensures that they are the same
    :return: returns the password hashed in sha256 with the use
    of the hashlib library
    """

    if x == "login":
        password = input("Enter password\n> ")
        if not password:
            print("Password field cannot be empty!")
            return get_password("login")
        hashed = hashlib.sha256(password.encode())

        return hashed.hexdigest()
    if x == "sign_up":
        password1 = input("Enter password\n> ")
        password2 = input("Confirm password\n> ")
        if not password1 or not password2:
            print("Password field cannot be empty!")
            return get_password("sign_up")

        if password1 == password2:
            hashed = hashlib.sha256(password1.encode())

            return hashed.hexdigest()
        else:
            print("Password don't match!")
            return get_password("sign_up")
    else:
        print("passed argument not recognised!")
        return ValueError


def sign_up():
    """
    creates a new user to login, a universally unique identifier for each user
            and stores all the values inside a csv file called login.csv.
    Check if the username is already taken.
    Also checks if the file is empty and if it is, it adds a header to the csv
    """
    username = get_username()
    password = get_password("sign_up")
    unique_id = uuid.uuid4().hex[:4]

    if os.path.isfile("data/login.csv"):
        with open("data/login.csv", "r", newline="", encoding="utf-8") \
                as csv_file:
            dict_reader = csv.DictReader(csv_file)
            for i in dict_reader:
                if i.get("username") == username:
                    print("Username already taken")
                    return

    credentials = {
        "username": username,
        "password": password,
        "UUID": unique_id
    }

    with open("data/login.csv", "a", newline="", encoding="utf-8") as csv_file:
        dict_writer = csv.DictWriter(csv_file,
                                     fieldnames=list(credentials.keys()))

        # if the login file is empty (new) then append a header
        if os.stat("data/login.csv").st_size == 0:
            dict_writer.writeheader()
        dict_writer.writerow(credentials)


def login():
    """
    It is a log in prompt.
    opens the login.csv file and checks the entries
    :return: if the credentials match it returns the username
    else it returns False
    """
    username = get_username()
    passwd = get_password()
    user = {}

    with open("data/login.csv", "r", newline="", encoding="utf-8") as csv_file:
        dict_reader = csv.DictReader(csv_file)
        dict_list = list(dict_reader)

    for i in dict_list:
        if username == i.get("username") and passwd == i.get("password"):
            user["username"] = username
            user["uuid"] = i.get("uuid")
            print("Log In successful")
            return user
        else:
            continue
    print("Username or password is incorrect!")
    return False


def forgot_password():
    """
    resets a password for a specific user by reading the login.csv file
    as a list of dictionaries.
    modifies the credentials and re-writes the file

    """
    username = get_username()

    keys = ["username", "password", "uuid"]

    with open("data/login.csv", 'r', newline="", encoding="utf-8") as csv_file:
        dict_reader = csv.DictReader(csv_file)
        list_of_logins = list(dict_reader)

    for i in list_of_logins:
        if username != i.get("username"):
            continue
        i["password"] = get_password("sign_up")

    with open("data/login.csv", 'w', newline="", encoding="utf-8") as csv_file:

        dict_writer = csv.DictWriter(csv_file, keys)

        dict_writer.writeheader()
        dict_writer.writerows(list_of_logins)
    print("Password successfully changed")


if __name__ == "__main__":
    # get_username()
    # get_password()
    # sign_up()
    # forgot_password()
    login()
