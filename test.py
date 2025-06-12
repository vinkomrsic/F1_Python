import os
import fastf1

# Create cache directory if it doesn't exist
os.makedirs('cache', exist_ok=True)
fastf1.Cache.enable_cache('cache')

# Function to ask the user for a session
def ask_for_session():
    year = int(input("Enter the year of the session (e.g., 2025): "))
    race = input("Enter the name of the race (e.g., 'Australia'): ")
    session_type = input("Enter the session type (e.g., FP1, Q, Race): ")

    results = fastf1.get_session(year, race, session_type)
    return results


ask_for_session().load()
#print(ask_for_session().results)