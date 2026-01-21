import pandas as pd


def find_worker():
    while True:
        finding = input("Do you want to find any workers?(Y/N): ")

        if finding.title() == "Y":
            try:
                required_columns = ["Name", "Surname", "Age", "Gender", "ID"]
                df_worker = pd.read_csv("database.txt", sep=r" \| ", engine="python")

                if list(df_worker.columns) != required_columns:
                    print("Database file has corrupted. Please delete and recreate it.")
                    return

                if df_worker.empty:
                    print("There are no workers to display yet.")
                    return

            except FileNotFoundError:
                print("Database file not found. Please ensure the file exists.")
                return

            except pd.errors.EmptyDataError:
                print("Database file is empty.")
                return

            else:
                print("1. All Workers")
                print("2. Find by Name")
                print("3. Find by Surname")
                print("4. Find by Age")
                print("5. Find by Gender")
                category = input("Choose a category: ")

                if category == "1":
                    print(df_worker)
                    return

                elif category == "2":
                    target_name = input("Enter the name: ")
                    try:
                        if not target_name.replace(" ", "").isalpha():
                            raise TypeError

                    except TypeError:
                        print("Name must contain only letters.")
                        print("Exiting...")
                        return

                    else:
                        df_worker = df_worker.loc[(df_worker["Name"].str.contains(target_name, case=False, na=False))]

                        if df_worker.empty:
                            print(f"There are no suitable names that contain: {target_name.title()}")
                            return
                        else:
                            print(df_worker)

                elif category == "3":
                    target_surname = input("Enter the surname: ")
                    try:
                        if not target_surname.replace(" ", "").isalpha():
                            raise TypeError

                    except TypeError:
                        print("Surname must contain only letters.")
                        print("Exiting...")
                        return

                    else:
                        df_worker = df_worker.loc[(df_worker["Surname"] == target_surname.title())]

                        if df_worker.empty:
                            print(f"There are no suitable workers with surname: {target_surname.title()}")
                            return
                        else:
                            print(df_worker)

                elif category == "4":
                    min_age = input("Enter the age (min): ")
                    max_age = input("Enter the age (max): ")
                    try:
                        int(min_age)
                        int(max_age)
                        assert 18 <= int(min_age) <= int(max_age) <= 99

                    except ValueError:
                        print("Age(s) must contain only numbers.")
                        print("Exiting...")
                        return

                    except AssertionError:
                        print("Ages must be between 18 and 99. Also, maximum age must be greater than or equal to minimum age.")
                        print("Exiting...")
                        return

                    else:
                        df_worker = df_worker.loc[(df_worker["Age"] >= int(min_age)) & (df_worker["Age"] <= int(max_age))]

                        if df_worker.empty:
                            if min_age == max_age:
                                print(f"There are no suitable workers age of {min_age}.")
                                return
                            else:
                                print(f"There are no suitable workers between the ages of {min_age} and {max_age}.")
                                return
                        else:
                            print(df_worker)

                elif category == "5":
                    target_gender = input("Enter the gender: ")
                    try:
                        if not target_gender.isalpha():
                            raise TypeError

                    except TypeError:
                        print("Gender must contain only letters.")
                        print("Exiting...")
                        return

                    else:
                        if target_gender.title() == "Male" or target_gender.title() == "Female":
                            df_worker = df_worker.loc[(df_worker["Gender"] == target_gender.title())]

                            if df_worker.empty:
                                print(f"There are no suitable workers gender of '{target_gender.title()}'.")
                                return
                            else:
                                print(df_worker)
                        else:
                            print("Please enter the gender as 'Male' or 'Female'.")
                            return

                else:
                    print("Please enter a valid option.")

        elif finding.title() == "N":
            print("Exiting...")
            return

        else:
            print("Please enter a valid option.")
