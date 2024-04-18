from .orm import db, User, Item, Transaction, transaction_user_due
import sqlalchemy as sql
from werkzeug.exceptions import NotFound
from .auth import InvalidFieldError

class BudgetError(Exception):
    status_code = 409

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def __str__(self):
        return self.message
    
    def __repr__(self):
        return self.message

def get_transaction_by_id(id:int) -> Transaction:
    statement = sql.select(Transaction).where(Transaction.id == id)
    transaction = db.session.scalar(statement)
    if transaction is None:
        raise NotFound(f"No transaction with id {id} exists.")
    return transaction

def update_user_balance(user:User, amount:float) -> None:
    # TODO: Add a call to a method for the notification system
    if user.balance + amount < user.budget:
        raise BudgetError("Transaction exceeds user's budget.")
    user.balance += amount


def calculate_money_owed_by_user(user:User) -> float:
    # Calculate the amount the user owes to others
    total = 0
    for transaction in user.transactions_due:
        total += transaction.amount / len(transaction.users)
    return total


def calculate_money_owed_to_user(user:User) -> float:
    # Calculate the amount others owe the user
    total = 0
    for transaction in user.transactions:
        if user.id == transaction.purchaser_id:
            total += len(transaction.users_due) / len(transaction.users) * transaction.amount
    return total


def net_balance(user:User) -> float:
    #Return positive value if user is owed more than they owe to others, negative otherwise
    return calculate_money_owed_to_user(user) - calculate_money_owed_by_user(user)

def pay_transaction(user:User, transaction:Transaction) -> None:
    #Allow for a user to pay for a single transaction
    #TODO: add proper error handling
    if not (transaction in user.transactions):
        raise InvalidFieldError("User is not a part of this transaction")
    elif not (transaction in user.transactions_due):
        raise InvalidFieldError("User has already paid for this transaction")
    else:
        user.balance -= transaction.amount
        transaction.users_due.remove(user)

def pay_all_transactions_due(user:User) -> None:
    #Allow a user to pay all of their outstanding debts
    for transaction in user.transactions_due:
        pay_transaction(user, transaction) #TODO: test and make sure this doesn't cause issues