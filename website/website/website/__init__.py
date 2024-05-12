from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import random
import string


db = SQLAlchemy()
DB_NAME = "database.db"

def transfer_from_checking_to_savings(user, amount):
        if user.bank_balance >= amount:
            user.bank_balance -= amount
            user.savings_balance += amount
        else:
            raise ValueError("Insufficient funds in checking account")

def transfer_from_savings_to_checking(user, amount):
        if user.savings_balance >= amount:
            user.savings_balance -= amount
            user.bank_balance += amount
        else:
            raise ValueError("Insufficient funds in savings account")
def generate_credit_score(min_balance=500, max_balance=850):
    """Generate a random bank credit score within a specified range."""
    return round(random.uniform(min_balance, max_balance), 2)

def generate_cc_number(length=10):
    """Generate a random bank account number of a given length."""
    return ''.join(random.choices(string.digits, k=length))

def generate_cc_balance(credit_score):
    # The higher the score, the higher the balance, capped at 50000
    max_balance = 50000
    if credit_score >= 800:
        return max_balance
    elif credit_score >= 500:
        return round((credit_score / 800) * max_balance)
    else:
        return 1000  # Minimum balance for low credit scores


def generate_bank_account_number(length=10):
    """Generate a random bank account number of a given length."""
    return ''.join(random.choices(string.digits, k=length))

def generate_random_balance(min_balance=1, max_balance=100000):
    """Generate a random bank balance within a specified range."""
    return round(random.uniform(min_balance, max_balance), 2)

def generate_savings_account_number(length=10):
    """Generate a random bank account number of a given length."""
    return ''.join(random.choices(string.digits, k=length))

def generate_savings_balance(min_balance=1, max_balance=100000):
    """Generate a random bank balance within a specified range."""
    return round(random.uniform(min_balance, max_balance), 2)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')