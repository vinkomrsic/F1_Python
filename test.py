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
    Clear the terminal screen (MacOS only)
    """
    print("\033c", end="")

def ask_for_session():
    """
    Prompt the user for year, race, and session type, then load and return the FastF1 session.
    """
    print("\n=== Formula 1 Results ===")
    year = int(input("Enter the year of the session (e.g., 2025): "))
    race = input("Enter the name of the race (e.g., 'Australia'): ")
    session_type = input("Enter the session type (e.g., 'FP1', 'Q', 'Race'): ")

    print("Loading session...")
    session = fastf1.get_session(year, race, session_type)
    session.load()
    print("Session loaded seccessfully!")
    return session


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
        team_col = 'TeamName' if 'TeamName' in df.columns else 'Team'
        display_cols = ['Position', 'DriverName', team_col, 'Time']
        # Convert to string and split into lines 
        table_str = df[display_cols].to_string(
            index = False,
            formatters={
                'Position' : lambda x: str(int(x))
            }
        )
        lines = table_str.split('\n')
        header = lines[0]
        seperator = '-' * len(header)
        print("\n=== Standings ===")
        print(header)
        print(seperator)
        for line in lines[1:]:
            print(line)
    else:
        print("No standings available for this session.")

def main():
    clear_terminal()
    session = ask_for_session()
    print_session_info(session)
    print_standings(session)

if __name__ == "__main__":
    main()