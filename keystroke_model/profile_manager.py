import os
import pickle
import numpy as np

PROFILE_PATH = os.path.join(os.path.dirname(__file__), "baseline_profiles.pkl")

# In-memory profiles
if os.path.exists(PROFILE_PATH):
    with open(PROFILE_PATH, "rb") as f:
        profiles = pickle.load(f)
else:
    profiles = {}


def get_profile(user_id):
    """Return the profile dict for a user, or None if not found."""
    return profiles.get(user_id)


def save_profiles():
    """Persist profiles to disk."""
    with open(PROFILE_PATH, "wb") as f:
        pickle.dump(profiles, f)


def update_profile(user_id, dwell_times, flight_times):
    """Update or create a profile for a user based on new dwell/flight samples."""
    # Filter out None values
    dwell_times = [d for d in dwell_times if d is not None]
    flight_times = [f for f in flight_times if f is not None]

    if not dwell_times and not flight_times:
        return

    if user_id not in profiles:
        profiles[user_id] = {
            "mean_dwell": float(np.mean(dwell_times)) if dwell_times else 0,
            "std_dwell": float(np.std(dwell_times)) if dwell_times else 1,
            "mean_flight": float(np.mean(flight_times)) if flight_times else 0,
            "std_flight": float(np.std(flight_times)) if flight_times else 1,
        }
    else:
        # Update existing profile (simple moving average)
        prof = profiles[user_id]
        if dwell_times:
            new_mean = float(np.mean(dwell_times))
            prof["mean_dwell"] = 0.9 * prof["mean_dwell"] + 0.1 * new_mean
            prof["std_dwell"] = max(
                1e-3, 0.9 * prof["std_dwell"] + 0.1 * float(np.std(dwell_times))
            )
        if flight_times:
            new_mean = float(np.mean(flight_times))
            prof["mean_flight"] = 0.9 * prof["mean_flight"] + 0.1 * new_mean
            prof["std_flight"] = max(
                1e-3, 0.9 * prof["std_flight"] + 0.1 * float(np.std(flight_times))
            )

    save_profiles()