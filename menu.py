from session_utils import ask_for_session, ask_for_session_and_driver
from output import print_session_info, print_standings
from laps import lap_time_menu

def clear_terminal():
    """
    Clear the terminal screen (Unix-based systems).
    """
    print("\033c", end="")

def pause():
    input("\nPress Enter to return to menu...")
    clear_terminal()

def print_menu():
    """
    Print a menu to showcase all functions
    """
    while True:
        print("=== F1 Date Tool ===")
        print("1. View Race Results")
        print("2. View Lap Times")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            session = ask_for_session()
            if session:
                print_session_info(session)
                print_standings(session)
            pause()

        elif choice == "2":
            session, driver= ask_for_session_and_driver()
            if session and driver:
                lap_time_menu(session, driver)
            pause()

        elif choice == "0":
            print("Goodbye!")
            return
        else:
            print("Invalid choice.")
            input("Press Enter to try again...")
            clear_terminal()