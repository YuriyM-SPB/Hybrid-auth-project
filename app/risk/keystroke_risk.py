from app.utils.feature_extraction import extract_keystroke_features

# In-memory store for session typing profiles
keystroke_profiles = {}

# Update the user's keystroke profile with new typing batch
def update_keystroke_profile(user_id, keystroke_data):
    if user_id not in keystroke_profiles:
        keystroke_profiles[user_id] = []
    features = extract_keystroke_features(keystroke_data)
    keystroke_profiles[user_id].append(features)

# Evaluate typing anomaly for the session
def evaluate_keystroke_risk(user_id):
    profiles = keystroke_profiles.get(user_id, [])
    if len(profiles) < 2:
        return 0.0  # Not enough data, assume low risk
    
    # Compare last sample with average profile
    import numpy as np
    baseline = np.mean(profiles[:-1], axis=0)
    latest = profiles[-1]
    
    distance = np.linalg.norm(baseline - latest)
    # Normalize distance to [0,1] risk score range
    risk_score = min(distance / 1.0, 1.0)  # 1.0 is arbitrary max expected distance
    return risk_score