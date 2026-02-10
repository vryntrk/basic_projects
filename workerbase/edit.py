import pandas as pd
from find import find_func


def edit_func(dataframe):
    run = True
    while run:
        warn_message = input("Are you sure you want to edit this worker?(Y/N): ")
        if warn_message.title() == "Y":
            with open("database.txt", "w", encoding="utf-8") as f:
                f.write("Name | Surname | Age | Gender | ID\n")

                for index, row in dataframe.iterrows():
                    f.write(f"{row['Name']} | {row['Surname']} | {row['Age']} | {row['Gender']} | {row['ID']}\n")
            run = False
        elif warn_message.title() == "N":
            print("Exiting...")
            return
        else:
            print("Please enter a valid option.")
        if not run:
            break


def edit_worker():
    while True:
        editing = input("Do you want to edit any workers?(Y/N): ")

        if editing.title() == "Y":
            try:
                required_columns = ["Name", "Surname", "Age", "Gender", "ID"]
                df_worker = pd.read_csv("database.txt", sep=r" \| ", engine="python")

                if list(df_worker.columns) != required_columns:
                    print("Database file has corrupted. Please delete and recreate it.")
                    return

                if df_worker.empty:
                    print("There are no workers to edit yet.")
                    return

            except FileNotFoundError:
                print("Database file not found. Please ensure the file exists.")
                return

            except pd.errors.EmptyDataError:
                print("Database file is empty.")
                return

            else:
                find_func()
                edit_id = input("Please enter the ID of the worker to remove, or type 'cancel' to exit: ")

                if edit_id.lower() == "cancel":
                    print("Exiting...")
                    return

                try:
                    assert len(edit_id) == 6
                    df_worker = df_worker.loc[(df_worker["ID"].str.contains(edit_id))]
                    if df_worker.empty:
                        print("Please enter a valid ID.")
                        return

                except AssertionError:
                    print("Please be sure you entered 6 characters for ID.")
                    return

                else:
                    df_worker = pd.read_csv("database.txt", sep=r" \| ", engine="python")
                    print("1. Edit The Name")
                    print("2. Edit The Surname")
                    print("3. Edit The Age")
                    print("4. Edit The Gender")
                    print("5. Exit")
                    selection = input("Please select an option: ")

                    if selection == "1":
                        new_name = input("Please enter the new name: ")
                        try:
                            if not new_name.replace(" ", "").isalpha():
                                raise TypeError

                        except TypeError:
                            print("Name must contain only letters.")

                        else:
                            df_worker.loc[df_worker["ID"].str.strip() == edit_id, "Name"] = new_name.title()
                            edit_func(df_worker)
                            print("Worker's name updated successfully.")

                    elif selection == "2":
                        new_surname = input("Please enter the new surname: ")
                        try:
                            if not new_surname.replace(" ", "").isalpha():
                                raise TypeError

                        except TypeError:
                            print("Surname must contain only letters.")

                        else:
                            df_worker.loc[df_worker["ID"].str.strip() == edit_id, "Surname"] = new_surname.title()
                            edit_func(df_worker)
                            print("Worker's surname updated successfully.")

                    elif selection == "3":
                        new_age = input("Please enter the new age: ")
                        try:
                            int(new_age)
                            assert 18 <= int(new_age) <= 99

                        except ValueError:
                            print("Age must contain only numbers.")
                            print("Exiting...")
                            return

                        except AssertionError:
                            print("Age must be between 18 and 99.")
                            print("Exiting...")
                            return

                        else:
                            df_worker.loc[df_worker["ID"].str.strip() == edit_id, "Age"] = int(new_age)
                            edit_func(df_worker)
                            print("Worker's age updated successfully.")

                    elif selection == "4":
                        new_gender = input("Please enter the new gender: ")
                        try:
                            if not new_gender.isalpha():
                                raise TypeError

                        except TypeError:
                            print("Gender must contain only letters.")
                            print("Exiting...")
                            return

                        else:
                            if new_gender.title() == "Male" or new_gender.title() == "Female":
                                df_worker.loc[df_worker["ID"].str.strip() == edit_id, "Gender"] = new_gender.title()
                                edit_func(df_worker)
                                print("Worker's gender updated successfully.")
                            else:
                                print("Please enter the gender as 'Male' or 'Female'.")
                                return

                    elif selection == "5":
                        print("Operation canceled. Exiting...")
                        return

                    else:
                        print("Please enter a valid option.")

        elif editing.title() == "N":
            print("Exiting...")
            return

        else:
            print("Please enter a valid option.")
