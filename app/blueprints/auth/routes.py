from flask import Blueprint, render_template, request, redirect, flash, url_for
from app.blueprints.auth.auth_forms import SignInForm, SignUpForm
from app.models import User, db
from werkzeug.security import check_password_hash 
from flask_login import login_user, current_user, login_required, logout_user

auth = Blueprint('auth', __name__, template_folder='auth_templates', url_prefix = '/auth')

@auth.route('/signin', methods=['GET', 'POST'])
def signin():
    inform = SignInForm()
    if request.method == 'POST':
        if inform.validate_on_submit():
            user = User.query.filter_by(username=inform.username.data).first() 
            if user and check_password_hash(user.password, inform.password.data): 
                login_user(user)
                flash(f'Hello, {current_user.username}!', category='info')
                return redirect(url_for('home'))
        flash(f'Incorrect username or password.', category='danger')
        return redirect(url_for('auth.signin'))
    return render_template('signin.html', inform=inform)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    upform = SignUpForm()
    if request.method == 'POST':
        if upform.validate_on_submit():
            newuser = User(upform.username.data, upform.email.data, upform.password.data, upform.first_name.data, upform.last_name.data)
            try:
                db.session.add(newuser)
                db.session.commit()
            except:
                flash(f'That username or email is taken. Please try a different one.', category='danger')
                return redirect(url_for('auth.signup'))
            login_user(newuser)
            flash(f'Successfully registered! Welcome, {upform.first_name.data}!', category='success')
            return redirect(url_for('auth.signin'))
        else:
            flash('Please fill out required fields.', category='danger')
            return redirect(url_for('auth.signup'))
    return render_template('signup.html', upform=upform)


@auth.route('/logout')
@login_required
def signout():
    logout_user()
    flash('You have been signout', category='info')
    return redirect(url_for('auth.signin'))