from app.utils.feature_extraction import extract_keystroke_features
from keystroke_model.profile_manager import update_profile, get_profile
import numpy as np
import logging

logger = logging.getLogger(__name__)

def process_keystroke_batch(user_id, keystroke_data):
    dwell_times, flight_times = extract_keystroke_features(keystroke_data)
    profile = get_profile(user_id)

    if not profile:
        logger.info(f"Initializing profile for user {user_id}")
        update_profile(user_id, dwell_times, flight_times)
        return 0.0

    def score(features, mean, std):
        if std == 0:
            return 0.0
        z_scores = [(f - mean) / std for f in features if f is not None and std > 0]
        outliers = [z for z in z_scores if abs(z) > 3]
        return len(outliers) / len(features) if features else 0.0

    risk_dwell = score(dwell_times, profile['mean_dwell'], profile['std_dwell'])
    risk_flight = score(flight_times, profile['mean_flight'], profile['std_flight'])
    total_risk = (risk_dwell + risk_flight) / 2

    logger.info(f"User {user_id} anomaly score: {total_risk:.3f}")
    update_profile(user_id, dwell_times, flight_times)
    return total_risk
