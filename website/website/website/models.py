from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    bank_account_number = db.Column(db.String(150))  # Field for randomly generated bank account number
    bank_balance = db.Column(db.Float, nullable=False)  
    savings_number = db.Column(db.String(150))  # Field for randomly generated savings account number
    savings_balance = db.Column(db.Float, nullable=False)
    credit_score = db.Column(db.Float)
    cc_number = db.Column(db.String(150))  # Field for randomly generated credit card number
    cc_balance = db.Column(db.Float) 
    reward_points = db.Column(db.Integer, default=0)  # Tracks user's reward points

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