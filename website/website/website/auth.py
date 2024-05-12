from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   # from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from . import generate_bank_account_number, generate_random_balance, generate_savings_balance, generate_savings_account_number, generate_credit_score, generate_cc_number, generate_cc_balance, generate_credit_score,transfer_from_checking_to_savings


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('User already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(last_name) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            user_credit_score = generate_credit_score()
            bank_account_number = generate_bank_account_number()
            bank_balance = generate_random_balance()
            savings_number = generate_savings_account_number()
            savings_balance = generate_savings_balance()
            cc_number = generate_cc_number()
            user_cc_balance = generate_cc_balance(user_credit_score)
            new_user = User(
                email=email, first_name=first_name, last_name=last_name,
                password=generate_password_hash(password1),
                bank_account_number=bank_account_number, bank_balance=bank_balance,
                credit_score=user_credit_score, savings_number=savings_number,
                savings_balance=savings_balance, cc_number=cc_number,
                cc_balance=user_cc_balance
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))
        return render_template("sign_up.html", user=current_user)
    return render_template("sign_up.html", user=current_user)


