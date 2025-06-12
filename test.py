import os
import fastf1
import logging

# Suppress FastF1 internal logs
logging.getLogger('fastf1').setLevel(logging.CRITICAL)

# Cache directory constant
CACHE_DIR = 'cache'

# Create cache directory if it doesn't exist
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

def clear_terminal():
    """
    Clear the terminal screen (Unix-based systems).
    """
    print("\033c", end="")

def print_menu():
    """
    Print a menu to showcase all functions
    """
    while True:
        clear_terminal()
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
                input("\nPress Enter to return to menu...")

        elif choice == "2":
            session, driver= ask_for_session_and_driver()
            if session and driver:
                print_driver_lap_times(session, driver)
                input("\nPress Enter to return to menu...")

        elif choice == "0":
            print("Goodbye!")
            return
        else:
            print("Invalid choice.")


def ask_for_session():
    """
    Prompt the user for year, race, and session type, then load and return the FastF1 session.
    """
    print("\n=== Formula 1 Results ===")
    while True:
        try:
            year = int(input("Enter the year of the session (e.g., 2025): "))
            if year < 1950:
                print("The first F1 World Championship was in 1950. Please enter a valid year.")
                continue
            break
        except ValueError:
            print("Please enter a valid integer for the year.")
        
    while True:
        race = input("Enter the name of the race (e.g., 'Australia'): ")
        if not race:
            print("Race name cannot be empty.")
            continue
        break

    valid_sessions = ['FP1', 'FP2', 'FP3', 'Q', 'SQ', 'SS', 'Sprint', 'Race']
    while True:
        session_type = input("Enter the session type (e.g., 'FP1', 'Q', 'Race'): ").strip()
        session_type = session_type.capitalize() if session_type.lower() == 'race' else session_type.upper()
        if session_type.upper() not in [s.upper() for s in valid_sessions]:
            print(f"Invalid session type. Valid options: {', '.join(valid_sessions)}")
            continue
        break

    print("\nLoading session...")
    session = fastf1.get_session(year, race, session_type)
    session.load()
    print("Session loaded successfully!")
    return session


def ask_for_session_and_driver():
    """
    Prompt the user for year, race, session type, and driver, then load and return the FastF1  information.
    """
    session = ask_for_session()
    if not session:
        return None, None
    
    drivers = list(session.laps['Driver'].unique())
    print("\nAvailable drivers in this session:")
    for code in drivers:
        info = session.get_driver(code)
        print(f"{code}: {info['FullName']}")

    while True:
        driver_code = input("\nEnter the 3-letter driver code (e.g., NOR): ").strip().upper()
        if driver_code in drivers:
            return session, driver_code
        else:
            print("Invalid driver code. Please choose from the list.")


def print_session_info(session):
    """
    Print basic info about the loaded session.
    """
    print("\n=== Session Info ===")
    print(f"Event: {session.event['EventName']}")
    print(f"Location: {session.event['Location']}")
    print(f"Country: {session.event['Country']}")
    print(f"Date: {session.date}")
    print(f"Session Type: {session.name}")


def print_standings(session):
    """
    Print the official standings/results of the session.
    """
    standings = session.results 
    if standings is not None and not standings.empty:
        df = standings.copy()
        df['DriverName'] = [session.get_driver(code)['FullName'] for code in df.index]
        # Handle team column name variations
        team_col = next((col for col in ['TeamName', 'Team'] if col in df.columns), None)
        if not team_col:
            print("Could not find team information.")
            return
        display_cols = ['Position', 'DriverName', team_col, 'Time']
        # Convert to string and split into lines 
        table_str = df[display_cols].to_string(
            index=False,
            formatters={
                'Position' : lambda x: str(int(x))
            }
        )
        lines = table_str.split('\n')
        header = lines[0]
        separator = '-' * len(header)
        print("\n=== Standings ===")
        print(header)
        print(separator)
        for line in lines[1:]:
            print(line)
    else:
        print("No standings available for this session.")


def print_driver_lap_times(session, driver):
    pass


def main():
    print_menu()

if __name__ == "__main__":
    main()