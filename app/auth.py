import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from app.services.transactional_emails import *
from .models import User, Role
from . import db
import uuid

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


# @auth.route('/login', methods=['POST'])
# def login_post():
#     email = request.form.get('email')
#     password = request.form.get('password')
#     remember = True if request.form.get('remember') else False
#
#     user = User.query.filter_by(email=email).first()
#
#     # check if the user actually exists
#     # take the user-supplied password, hash it, and compare it to the hashed password in the database
#     if not user or not check_password_hash(user.password, password):
#         flash('Please check your login details and try again.')
#         return redirect(url_for('auth.login'))  # if the user doesn't exist or password is wrong, reload the page
#
#     # if the above check passes, then we know the user has the right credentials
#     login_user(user, remember=remember)
#     return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in
    # database

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/register', methods=["GET", "POST"])
def register():
    """Register a new user on Repo Log App with email
       having samedayauto.net domain only.Other domain
       user are not allowed on Repo log app."""
    data = {
        'title': 'Request Access',
        'form_action': '/register',
        'form-description': 'Verify your email address to continue your registration.',
        'button_message': 'Verify my email',
        'after_link_href': '/reset-password',
        'after_link_text': 'Forgot your password?'
    }
    if request.method == 'GET':
        return render_template('email-form.html', data=data)
    elif request.method == 'POST':
        email = request.form['email']
        u = str(uuid.uuid1())
        if email.split('@')[1].lower() in ['samedayauto.net']:

            # check if new user exists
            new_user = User.query.filter_by(email=email).first()
            if new_user:
                message = 'User already exists, click link above to reset your password'
                return render_template('email-form.html', data=data, message=message)

            # create new user with the form data
            new_user = User(
                email=email,
                ip=f'{str(request.environ["REMOTE_ADDR"])}',
                verified=False,
                created=datetime.datetime.now(),
                activity=datetime.datetime.now(),
                uuid=f'{u}'
            )
            # add the new user to the database
            db.session.add(new_user)
            db.session.commit()
        else:
            message = "Unauthorized"
            return render_template('email-form.html', data=data, message=message)
        try:
            send_verification_email(email, u)
            message = "Please check your inbox for an email from us"
        except AssertionError:
            message = "Unauthorized"
        return render_template('email-form.html', data=data, message=message)


@auth.route('/verify/<unique_id>', methods=["GET", "POST"])
def create_pw(unique_id):
    """Create password for user using the
       link send to registered email"""
    user = lookup_user('uuid', unique_id)
    if request.method == 'GET':
        if not user.verified:
            resp = make_response(render_template('verify.html', user=user))
            resp.set_cookie('sda', unique_id)
            return resp
        else:
            return redirect('/')
    if request.method == 'POST':
        user.password = hash_password(request.form['new-password'])
        user.verified = True
        if user.email in ['darren.maloney@samedayauto.net',
                          'dev@samedayauto.net',
                          'russell.warden@samedayauto.net']:
            role = Role.query.filter(Role.name == 'Admin').first()
            user.roles.append(role)
        db.session.add(user)
        db.session.commit()

        login_user(user, remember=False)
        return redirect(url_for('main.repo_log'))
        # db_ref = db.collection('users').document(user['email'])
        # db_ref.set(user)
        # resp = make_response(redirect('/repo-log'))
        # resp.set_cookie('sda', user['uuid'])
        # return resp


@auth.route('/reset-password', methods=["GET", "POST"])
def reset():
    """Forget password using registered email id
    and a password reset link is send to email."""
    data = {
        'title': 'Reset your password',
        'form_action': '/reset-password',
        'form-description': 'Enter your email address and we will send you a password reset link.',
        'button_message': 'Send reset link',
        'after_link_href': "/register",
        'after_link_text': 'Create a new account'
    }
    if request.method == 'GET':
        return render_template('email-form.html', data=data)
    elif request.method == 'POST':
        email = request.form['email']
        try:
            # assert lookup_user('email', email) is not None
            user = lookup_user('email', email)
            user.verified = False
            user.activity = datetime.datetime.now()
            # db_ref = db.collection('users').document(f'{email}')
            # db_ref.set(user)
            db.session.add(user)
            db.session.commit()
            send_password_reset_link(email)
            message = "Check your inbox. A link to reset your password was sent."
        except TypeError:
            message = 'Unknown email.'

        return render_template('email-form.html', data=data, message=message)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
