from flask import Flask, render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, current_user
from . import db
from .models import User

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
        return render_template("home.html", user=current_user)

@views.route('/visitor_home')
def visitor_home():
    return render_template('visitor_home.html', user=current_user)

@views.route('/credit_card')
@login_required
def credit_card():
    return render_template('credit_card.html', user=current_user)

@views.route('/savings')
@login_required
def auto():
    return render_template('savings.html', user=current_user)

@views.route('/rewards')
@login_required
def rewards():
    return render_template('rewards.html', user=current_user)

@views.route('/checking')
@login_required
def checking():
    return render_template('checking.html', user=current_user)

@views.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        to_account = request.form['to_account']

        try:
            if to_account == 'saving_balance':
                current_user.saving_balance(amount)
            elif to_account == 'bank_balance':
                current_user.bank_balance(amount)
            db.session.commit()
            flash('Transfer successful!', 'success')
        except ValueError as e:
            db.session.rollback()
            flash(str(e), 'error')

    return render_template('transfer.html', user=current_user)