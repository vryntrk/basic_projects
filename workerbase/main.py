from add import add_worker
from find import find_worker
from remove import remove_worker


def menu():
    print("--- MAIN MENU ---")
    print("1. Add Worker")
    print("2. Find Worker")
    print("3. Remove Worker")
    print("4. Exit")
    operation = input("Enter the operation number(1-4): ")
    return operation


def main():
    while True:
        choice = menu()
        if choice == "1":
            add_worker()
        elif choice == "2":
            find_worker()
        elif choice == "3":
            remove_worker()
        elif choice == "4":
            run = True
            while run:
                warning = input("Are you sure you want to exit?(Y/N): ")
                if warning.title() == "Y":
                    print("Exiting...")
                    run = False
                elif warning.title() == "N":
                    print("Operation cancelled.")
                    break
                else:
                    print("Please enter a valid option.")
            if not run:
                break
        else:
            print("Please enter a valid option")


if __name__ == "__main__":
    main()
