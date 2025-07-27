import pandas as pd

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