import os
import fastf1

# Create cache directory if it doesn't exist
os.makedirs('cache', exist_ok=True)

fastf1.Cache.enable_cache('cache')

results = fastf1.get_session(2025, 'Australia', 'Race')
results.load()
print(results)