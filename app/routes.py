from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from app.auth.login_manager import verify_credentials
from app.auth.stepup_handler import require_stepup
from app.risk.context_risk import evaluate_context_risk
from app.risk.keystroke_risk import update_keystroke_profile, evaluate_keystroke_risk
from app.risk.fusion_engine import fuse_risks
from app.models.user import User

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = verify_credentials(username, password)
        if user:
            login_user(user)
            # Evaluate context risk at login
            context_score = evaluate_context_risk(request)
            session['context_risk'] = context_score
            session['keystroke_profile'] = None  # Initialize empty profile
            session['needs_stepup'] = False
            return redirect(url_for('main.dashboard'))
    return render_template('login.html')

@main.route('/dashboard')
@login_required
def dashboard():
    if session.get('needs_stepup'):
        return redirect(url_for('main.stepup_auth'))
    return render_template('dashboard.html')

@main.route('/api/keystroke', methods=['POST'])
@login_required
def receive_keystrokes():
    keystroke_data = request.get_json()
    update_keystroke_profile(current_user.id, keystroke_data)
    keystroke_risk = evaluate_keystroke_risk(current_user.id)
    combined_risk = fuse_risks(session['context_risk'], keystroke_risk)
    if combined_risk >= 0.8:
        session['needs_stepup'] = True
    return jsonify({'status': 'ok'})

@main.route('/stepup', methods=['GET', 'POST'])
@login_required
def stepup_auth():
    if request.method == 'POST':
        password = request.form.get('password')
        if require_stepup(current_user, password):
            session['needs_stepup'] = False
            return redirect(url_for('main.dashboard'))
        else:
            logout_user()
            return redirect(url_for('main.login'))
    return render_template('stepup_auth.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))