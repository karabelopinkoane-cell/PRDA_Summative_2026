from flask import Flask, render_template, request, redirect, url_for, flash, session
from pathlib import Path
import json
import os
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'prda-practice-secret-key')
DATA_FILE = Path(__file__).parent / 'data' / 'users.json'


def load_users():
    # Load all user profiles from the JSON file.
    if not DATA_FILE.exists():
        return {}
    try:
        return json.loads(DATA_FILE.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {}


def save_users(users):
    # Save all user profiles back to the JSON file.
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(users, indent=4), encoding='utf-8')


def validate_profile(full_name, username, email, phone, bio=''):
    # Validate profile fields before data is stored.
    errors = []
    if not full_name.strip():
        errors.append('Full name is required.')
    if not username.strip():
        errors.append('Username is required.')
    elif not re.fullmatch(r'[A-Za-z0-9_]{3,20}', username.strip()):
        errors.append('Username must be 3–20 characters and use only letters, numbers, or underscores.')
    if not re.fullmatch(r'[^@\s]+@[^@\s]+\.[^@\s]+', email.strip()):
        errors.append('Enter a valid email address.')
    if not re.fullmatch(r'\d{7,15}', phone.strip()):
        errors.append('Phone number must contain 7–15 digits only.')
    if len(bio.strip()) > 180:
        errors.append('Bio must be 180 characters or fewer.')
    return errors


@app.route('/')
def home():
    # Display the landing page.
    return render_template('home.html', current_username=session.get('username'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Register a new profile and store it in JSON.
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        bio = request.form.get('bio', '').strip()

        errors = validate_profile(full_name, username, email, phone, bio)
        users = load_users()
        if username in users:
            errors.append('That username already exists.')

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('register.html', form={
                'full_name': full_name,
                'username': username,
                'email': email,
                'phone': phone,
                'bio': bio,
            })

        users[username] = {
            'full_name': full_name,
            'username': username,
            'email': email,
            'phone': phone,
            'bio': bio,
        }
        save_users(users)
        session['username'] = username
        flash('Profile created successfully.', 'success')
        return redirect(url_for('profile', username=username))

    return render_template('register.html', form={})


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Simplified classroom login: username only, not production authentication.
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        users = load_users()
        if username not in users:
            flash('No profile was found for that username.', 'error')
            return render_template('login.html', username=username)
        session['username'] = username
        flash('Login successful.', 'success')
        return redirect(url_for('profile', username=username))
    return render_template('login.html', username='')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


@app.route('/profiles')
def profiles():
    # Display every stored profile dynamically.
    users = load_users()
    return render_template('profiles.html', users=list(users.values()))


@app.route('/profile/<username>')
def profile(username):
    # Display one stored user profile dynamically.
    users = load_users()
    user = users.get(username)
    if not user:
        flash('Profile not found.', 'error')
        return redirect(url_for('profiles'))
    return render_template('profile.html', user=user, is_owner=session.get('username') == username)


@app.route('/profile/<username>/edit', methods=['GET', 'POST'])
def edit_profile(username):
    # Preload and update an existing user profile.
    users = load_users()
    user = users.get(username)
    if not user:
        flash('Profile not found.', 'error')
        return redirect(url_for('profiles'))

    if session.get('username') != username:
        flash('Please log in as this user before editing the profile.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        bio = request.form.get('bio', '').strip()
        errors = validate_profile(full_name, username, email, phone, bio)

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('edit.html', user={
                'full_name': full_name,
                'username': username,
                'email': email,
                'phone': phone,
                'bio': bio,
            })

        users[username]['full_name'] = full_name
        users[username]['email'] = email
        users[username]['phone'] = phone
        users[username]['bio'] = bio
        save_users(users)
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile', username=username))

    return render_template('edit.html', user=user)


@app.route('/health')
def health():
    return {'status': 'ok'}, 200


if __name__ == '__main__':
    app.run(debug=True)
