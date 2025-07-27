import fastf1
import pandas as pd

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
            if year < 2018:
                print("Lap data before 2018 may be incomplete or unavailable.")
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
    try:
        session = fastf1.get_session(year, race, session_type)
        session.load()
    except Exception as e:
        print(f"Failed to load session data: {e}")
        return None
    
    print("Session loaded successfully!")
    return session


def ask_for_session_and_driver():
    """
    Prompt the user for year, race, session type, and driver. Then load and return the FastF1 information.
    """
    session = ask_for_session()
    if not session:
        return None, None
    
    try:
        laps = session.laps
    except Exception:
        print("\nThis session has no lap data available.")
        return None, None
    
    if laps.empty:
        print("\nThis session has no lap data available.")
        return None, None
    
    drivers = list(session.laps['Driver'].unique())
    print("\nAvailable drivers in this session:")
    for code in drivers:
        try:
            info = session.get_driver(code)
            print(f"{code}: {info['FullName']}")
        except Exception:
            print(f"{code}: [Name unavailable]")

    while True:
        driver_code = input("\nEnter the 3-letter driver code (e.g., NOR): ").strip().upper()
        if driver_code in drivers:
            return session, driver_code
        else:
            print("Invalid driver code. Please choose from the list.")