import os
import pickle
import numpy as np

PROFILE_PATH = 'keystroke_model/baseline_profiles.pkl'

# Load all profiles from disk
def load_profiles():
    if not os.path.exists(PROFILE_PATH):
        return {}
    with open(PROFILE_PATH, 'rb') as f:
        return pickle.load(f)

# Save all profiles to disk
def save_profiles(profiles):
    with open(PROFILE_PATH, 'wb') as f:
        pickle.dump(profiles, f)

# Add or update a user's profile
def update_profile(user_id, dwell_times, flight_times):
    profiles = load_profiles()
    dwell_times = [d for d in dwell_times if d is not None]
    flight_times = [f for f in flight_times if f is not None]
    profile = {
        'mean_dwell': float(np.mean(dwell_times)) if dwell_times else 0,
        'std_dwell': float(np.std(dwell_times)) if dwell_times else 1,
        'mean_flight': float(np.mean(flight_times)) if flight_times else 0,
        'std_flight': float(np.std(flight_times)) if flight_times else 1
    }
    profiles[user_id] = profile
    save_profiles(profiles)

# Retrieve a user's profile
def get_profile(user_id):
    profiles = load_profiles()
    return profiles.get(user_id, None)
