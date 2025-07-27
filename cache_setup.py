import os
import fastf1
import logging 

def setup_cache(CACHE_DIR='cache'):
    # Suppress FastF1 internal logs
    logging.getLogger('fastf1').setLevel(logging.CRITICAL)

    # Create cache directory if it doesn't exist
    os.makedirs(CACHE_DIR, exist_ok=True)
    fastf1.Cache.enable_cache(CACHE_DIR)