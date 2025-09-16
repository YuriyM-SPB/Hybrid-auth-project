from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify, flash
from flask_login import login_user, login_required, logout_user, current_user

from app.auth.login_manager import verify_credentials
from app.auth.stepup_handler import require_stepup
from app.risk.context_risk import evaluate_context_risk
from app.risk.keystroke_risk import process_keystroke_batch
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
            context_score = evaluate_context_risk(request)
            session['context_risk'] = context_score
            session['keystroke_score'] = 0.0
            session['needs_stepup'] = False
            #flash(f"Context risk score: {context_score:.3f}", 'info')
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid username or password", 'danger')
    return render_template('login.html')

@main.route('/dashboard')
@login_required
def dashboard():
    if session.get('needs_stepup'):
        return redirect(url_for('main.stepup_auth'))
    keystroke_score = session.get('keystroke_score', 0.0)
    context_score = session.get('context_risk', 0.0)
    return render_template('dashboard.html', keystroke_score=keystroke_score, context_score=context_score)

@main.route('/api/keystroke', methods=['POST'])
@login_required
def receive_keystrokes():
    keystroke_data = request.get_json()
    score = process_keystroke_batch(current_user.id, keystroke_data)
    session['keystroke_score'] = score
    combined, needs_stepup = fuse_risks(session['context_risk'], score)
    if needs_stepup:
        session['needs_stepup'] = True
    return jsonify({
        'keystroke_score': score,
        'context_score': session['context_risk'],
        'combined_risk': combined,
        'needs_stepup': session['needs_stepup']
    })

@main.route('/api/risk_status')
@login_required
def risk_status():
    return jsonify({
        'context_score': session.get('context_risk', 0.0),
        'keystroke_score': session.get('keystroke_score', 0.0),
        'combined_risk': max(session.get('context_risk', 0.0), session.get('keystroke_score', 0.0)),
        'needs_stepup': session.get('needs_stepup', False)
    })



@main.route('/stepup', methods=['GET', 'POST'])
@login_required
def stepup_auth():
    if request.method == 'POST':
        password = request.form.get('password')
        if require_stepup(current_user, password):
            session['needs_stepup'] = False
            flash("Step-up authentication successful.", 'success')
            return redirect(url_for('main.dashboard'))
        else:
            logout_user()
            flash("Step-up authentication failed. Logged out.", 'danger')
            return redirect(url_for('main.login'))
    return render_template('stepup_auth.html')

@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    #flash("You have been logged out.", 'info')
    return redirect(url_for('main.login'))
