import pickle
import os

# Load the MLE-RBA model
model_path = os.getenv('MLE_RBA_MODEL_PATH', 'MLE_RBA/rba_model.pkl')
with open(model_path, 'rb') as file:
    rba_model = pickle.load(file)

# Evaluate context risk based on login request
def evaluate_context_risk(request):
    # Extract contextual features from the request
    features = extract_features_from_request(request)
    
    # Predict risk score
    risk_score = rba_model.predict_proba([features])[0][1]  # Assuming 1 = attacker
    return risk_score

# Dummy feature extractor
def extract_features_from_request(request):
    # TODO: Implement realistic feature extraction
    # Example: IP address, User-Agent hash, etc.
    return [0.5, 0.2, 0.7]  # Placeholder dummy features