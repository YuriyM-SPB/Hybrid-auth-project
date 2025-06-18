# Hybrid Continuous Authentication System (PhD Project)

## Project description

This project implements a **hybrid continuous authentication system** based on two complementary techniques:

- **Risk-Based Authentication (RBA)** using contextual data (IP address, device fingerprint, geolocation, etc.) with machine learning (MLE-RBA model).
- **Keystroke Dynamics Authentication** using typing behavior as a continuous biometric.

The system continuously monitors user risk during an active session, combining contextual and behavioral signals, and triggers step-up authentication (additional password entry) when anomalies are detected.

**Goal:** Improve session security without constantly bothering the legitimate user.

---

## Current MVP features 

- User login with basic password authentication.
- Context risk scoring at login based on MLE-RBA.
- Continuous client-side keystroke capture.
- Keystroke behavior anomaly detection.
- Risk fusion engine (context + keystroke).
- Step-up authentication triggered on high combined risk.
- Simple session management and basic frontend templates.

---

## Planned enhancements

- Real feature extraction from request metadata (IP, User-Agent parsing).
- More advanced keystroke analysis (neural network / one-class SVM models).
- Admin dashboard (showing session risks, anomaly logs).
- Statistical evaluation (ROC, FAR/FRR) for thesis experiments.
- Production deployment options (Docker, Gunicorn, HTTPS).

---

## How to run locally

1. Clone the repository:

```bash
git clone <your-repo-url>
cd hybrid_auth_project
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Initialize the database and create a test user:
```bash
python setup_db.py
```

This creates a default user (e.g., username: testuser, password: testpassword) inside the local SQLite database.

4. Start the Flask application:
```bash
python run.py
```

5. Access the system:

Open your browser and navigate to http://127.0.0.1:5000/. Use the test credentials to log in.

## Requirements
Python 3.8+

Flask

Flask-Login

Flask-SQLAlchemy

Werkzeug

numpy

(Optional) scikit-learn, lightgbm (for MLE-RBA model training)

## License
For academic and research purposes only.
