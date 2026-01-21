import os, uuid


def add_worker():
    while True:
        adding = input("Do you want to add a worker?(Y/N): ")

        if adding.title() == "Y":
            if os.path.exists("database.txt"):
                id_number = str(uuid.uuid4())[:6]

                while True:
                    name = input("Please enter worker's name: ")
                    try:
                        if not name.replace(" ", "").isalpha():
                            raise TypeError
                        break

                    except TypeError:
                        print("Name must contain only letters.")

                while True:
                    surname = input("Please enter worker's surname: ")
                    try:
                        if not surname.replace(" ", "").isalpha():
                            raise TypeError
                        break

                    except TypeError:
                        print("Surname must contain only letters.")

                while True:
                    age = input("Please enter worker's age: ")
                    try:
                        int(age)
                        assert 18 <= int(age) <= 99
                        break

                    except ValueError:
                        print("Age must contain only numbers.")

                    except AssertionError:
                        print("Age should not be under 18 or over 99.")

                while True:
                    gender = input("Please enter worker's gender: ")
                    try:
                        if not gender.isalpha():
                            raise TypeError

                    except TypeError:
                        print("Gender must contain only letters.")

                    if gender.title() == "Male" or gender.title() == "Female":
                        worker_file = open("database.txt", "a+", encoding="utf-8")
                        worker_file.write(f"{name.title()} | {surname.title()} | {age} | {gender.title()} |  {id_number}\n")
                        worker_file.close()
                        print("Worker added successfully.")
                        break

                    else:
                        print("Gender must be entered as 'Male' or 'Female'.")

            else:
                worker_file = open("database.txt", "w", encoding="utf-8")
                worker_file.write("Name | Surname | Age | Gender | ID\n")
                worker_file.close()
                print("Database file created.")

        elif adding.title() == "N":
            print("Exiting...")
            return

        else:
            print("Please enter a valid option")
