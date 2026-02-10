import pandas as pd


def remove_worker():
    while True:
        removing = input("Do you want to remove any workers?(Y/N): ")

        if removing.title() == "Y":
            try:
                required_columns = ["Name", "Surname", "Age", "Gender", "ID"]
                df_worker = pd.read_csv("database.txt", sep=r" \| ", engine="python")

                if list(df_worker.columns) != required_columns:
                    print("Database file has corrupted. Please delete and recreate it.")
                    return

                if df_worker.empty:
                    print("There are no workers to remove yet.")
                    return

            except FileNotFoundError:
                print("Database file not found. Please ensure the file exists.")
                return

            except pd.errors.EmptyDataError:
                print("Database file is empty.")
                return

            else:
                name = input("Please enter the name of the worker, or type 'cancel' to exit: ")
                try:
                    if not name.replace(" ", "").isalpha():
                        raise TypeError

                except TypeError:
                    print("Name must contain only letters.")
                    print("Exiting...")
                    return

                else:
                    if name.lower() == "cancel":
                        print("Exiting...")
                        return
                    else:
                        df_worker = df_worker.loc[(df_worker["Name"].str.contains(name, case=False, na=False))]
                        if df_worker.empty:
                            print(f"There are no suitable workers named: {name.title()}")
                            return
                        else:
                            print(df_worker)
                            id_taker = input("Please enter the ID of the worker to remove, or type 'cancel' to exit: ")

                            if id_taker.lower() == "cancel":
                                print("Exiting...")
                                return

                            try:
                                assert len(id_taker) == 6
                                df_worker = df_worker.loc[(df_worker["ID"].str.contains(id_taker))]
                                if df_worker.empty:
                                    print("Please enter a valid ID.")
                                    return

                            except AssertionError:
                                print("Please be sure you entered 6 characters for ID.")
                                return

                            else:
                                run = True
                                while run:
                                    warn_message = input("Are you sure you want to remove this worker?(Y/N): ")
                                    if warn_message.title() == "Y":
                                        with open("database.txt", "r", encoding="utf-8") as worker_file:
                                            lines = worker_file.readlines()

                                        with open("database.txt", "w", encoding="utf-8") as file:
                                            for line in lines:
                                                l = line.split("|")
                                                if len(l) > 1:
                                                    current_id = l[-1].strip()
                                                    if current_id == id_taker:
                                                        continue
                                                    file.write(line)

                                        print("Worker removed successfully.")
                                        run = False

                                    elif warn_message.title() == "N":
                                        print("Exiting...")
                                        return

                                    else:
                                        print("Please enter a valid option.")

                                    if not run:
                                        break

        elif removing.title() == "N":
            print("Exiting...")
            return

        else:
            print("Please enter a valid option.")
