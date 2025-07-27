import pandas as pd
import matplotlib.pyplot as plt

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