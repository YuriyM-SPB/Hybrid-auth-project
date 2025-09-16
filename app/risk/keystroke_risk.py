import numpy as np
from app.utils.feature_extraction import extract_keystroke_features
from keystroke_model.profile_manager import get_profile, update_profile

def z_score(value, mean, std):
    if std <= 0:
        return 0
    return (value - mean) / std

def process_keystroke_batch(user_id, keystroke_data):
    """Return anomaly score [0,1]."""
    dwell_times, flight_times = extract_keystroke_features(keystroke_data)

    # Skip empty
    if not dwell_times and not flight_times:
        return 0.0

    profile = get_profile(user_id)
    if profile is None:
        update_profile(user_id, dwell_times, flight_times)
        return 0.0  

    # Compute averages for current batch
    avg_dwell = np.mean([d for d in dwell_times if d is not None]) if dwell_times else profile["mean_dwell"]
    avg_flight = np.mean([f for f in flight_times if f is not None]) if flight_times else profile["mean_flight"]

    # Z-scores
    zd = z_score(avg_dwell, profile["mean_dwell"], profile["std_dwell"])
    zf = z_score(avg_flight, profile["mean_flight"], profile["std_flight"])

    distance = np.sqrt(zd**2 + zf**2)

    # Normalize to [0,1] risk score
    risk_score = min(distance / 5.0, 1.0)  

    # Update profile if not anomalous
    if risk_score < 0.5:
        update_profile(user_id, dwell_times, flight_times)

    return float(risk_score)
