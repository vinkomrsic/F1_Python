import os
import fastf1
import logging
import matplotlib.pyplot as plt
import numpy as np

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
            clear_terminal()

        elif choice == "2":
            session, driver= ask_for_session_and_driver()
            if session and driver:
                lap_time_menu(session, driver)
            input("\nPress Enter to return to menu...")
            clear_terminal()

        elif choice == "0":
            print("Goodbye!")
            return
        else:
            print("Invalid choice.")
            input("Press Enter to try again...")
            clear_terminal()

def lap_time_menu(session, driver):
    """
    Submenu to let the user choose between table or statistic
    """
    while True:
        print(f"\n=== Lap Time Options for {driver} ===")
        print("1. View lap time table")
        print("2. View lap time graph")
        print("3. View both")
        print("0. Back to main menu")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            print_driver_lap_times(session, driver)
            input("\nPress Enter to return to lap time menu...")
        elif choice == "2":
            print_driver_lap_times_statistic(session, driver)
            input("\nPress Enter to return to lap time menu...")
        elif choice == "3":
            print_driver_lap_times(session, driver)
            print_driver_lap_times_statistic(session, driver)
            input("\nPress Enter to return to lap time menu...")
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")


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
        
        # Format timedelta to readable time (e.g., +13.773s)
        def format_time(t):
            if pd.isnull(t):
                return 'N/A'
            total_sec = t.total_seconds()
            if total_sec > 3600:
                hours = int(total_sec // 3600)
                minutes = int((total_sec % 3600) // 60)
                seconds = total_sec % 60
                return f"{hours}:{minutes:02d}:{seconds:06.3f}"
            else:
                minutes = int(total_sec // 60)
                seconds = total_sec % 60
                return f"{minutes}:{seconds:06.3f}"

        df['Time'] = df['Time'].apply(format_time)

        table_str = df[display_cols].to_string(
            index=False,
            formatters={
                'Position': lambda x: str(int(x))
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
    """
    Display lap times for the selected driver in the session.
    """
    laps = session.laps.pick_drivers(driver).sort_values(by='LapNumber')
    if laps.empty:
        print("\nNo lap data available for the selected driver.")
        return
    
    # Find the index of the fastest lap (lowest non-null LapTime)
    valid_laps = laps.dropna(subset=['LapTime'])
    fastest_lap_time = valid_laps['LapTime'].min()
    fastest_lap_idx = valid_laps[valid_laps['LapTime'] == fastest_lap_time].index[0] if not valid_laps.empty else None
    
    print(f"\n=== Lap Times for {driver} ===")
    print(f"{'Lap':<5} {'LapTime' :<10} {'Compound':<10} {'Pit':<5} {'Note'}")
    print("-" * 55)
    for idx, row in laps.iterrows():
        lap_num = int(row['LapNumber'])
        lap_time = row['LapTime']

        # Format time to show as M:SS.mmm
        if pd.isnull(lap_time):
            lap_time_str = 'N/A'
        else:
            total_seconds = lap_time.total_seconds()
            minutes = int(total_seconds // 60)
            seconds = total_seconds % 60
            lap_time_str = f"{minutes}:{seconds:06.3f}"
        
        compound = row.get('Compound', 'N/A')
        pit = 'Yes' if pd.notna(row.get('PitInTime')) else ''

        # Highlight fastest lap
        note = "FASTEST" if idx == fastest_lap_idx else ""

        print(f"{int(row['LapNumber']):<5} {lap_time_str:<10} {compound:<10} {pit:<5} {note}")


def print_driver_lap_times_statistic(session, driver):
    laps = session.laps.pick_drivers(driver).sort_values(by='LapNumber')
    valid_laps = laps.dropna(subset=['LapTime'])

    if laps.empty:
        print("\nNo lap data available for the selected driver.")
        return
    
    # Extract lap data
    lap_numbers = valid_laps['LapNumber'].to_numpy()
    lap_times = valid_laps['LapTime'].dt.total_seconds().to_numpy()
    pit_flags = valid_laps['PitInTime'].notna().to_numpy()

    # Fastest lap
    fastest_idx = lap_times.argmin()
    fastest_lap_num = lap_numbers[fastest_idx]
    fastest_lap_time = lap_times[fastest_idx]

    # Seperate laps
    lap_numbers_no_pit = lap_numbers[~pit_flags]
    lap_times_no_pit = lap_times[~pit_flags]
    lap_numbers_pit = lap_numbers[pit_flags]
    lap_times_pit = lap_times[pit_flags]

    # === Plotting ===
    plt.style.use('classic')
    fig, ax = plt.subplots(figsize=(12, 6))

    # Normal laps
    ax.plot(lap_numbers_no_pit, lap_times_no_pit, 'o-', label='Normal Lap', color='#007acc')

    # Pit stop laps
    ax.plot(lap_numbers_pit, lap_times_pit, 'o', linestyle='None', label='Pit Stop Lap', color='#d62728')
    for lap_num, lap_time in zip(lap_numbers_pit, lap_times_pit):
        ax.fill_between([lap_num - 0.4, lap_num + 0.4], 0, lap_time, color='#d62728', alpha=0.1)

    # Fastest lap
    ax.plot(fastest_lap_num, fastest_lap_time, 'o', color='#2ca02c', label='Fastest Lap Time', markersize=10)
    ax.fill_between([fastest_lap_num - 0.4, fastest_lap_num + 0.4], 0, fastest_lap_time,
                     color='#2ca02c', alpha=0.15)
    
    ax.set_title(f"Lap Times for {driver}", fontsize=16, weight='bold')
    ax.set_xlabel("Lap Number", fontsize=12)
    ax.set_ylabel("Lap Times (seconds)", fontsize=12)
    ax.grid(True, linestyle='-', linewidth=0.5, alpha=0.7)
    ax.legend(loc='upper right', fontsize=10)
    ax.set_facecolor('#f9f9f9')

    plt.tight_layout()
    plt.show()

def main():
    print_menu()

if __name__ == "__main__":
    import pandas as pd 
    main()