from .orm import User
from .orm import Item
from .orm import Transaction


def calculate_money_owed_by_user(user:User) -> int:
    # Calculate the amount the user owes to others
    total = 0
    for transaction in user.transactions:
        if len(transaction.users_due) != 0:
            if User in transaction.users_due:
                total += transaction.amount / (len(transaction.users) + 1)
    return total
        


def calculate_money_owed_to_user(user:User) -> int:
    # Calculate the amount others owe the user
    total = 0
    for transaction in user.transactions:
        if len(transaction.users_due) != 0:
            if User.id == transaction.purchaser_id:
                total += len(transaction.users_due) / (len(transaction.users) + 1) * transaction.amount
    
    return total


def net_balance(user:User) -> int:
    #Return positive value if user is owed more than they owe to others, negative otherwise
    return calculate_money_owed_to_user(User) - calculate_money_owed_by_user(User)

def pay_transaction(user:User, transaction:Transaction) -> None:
    #Allow for a user to pay for a single transaction
    #TODO: add proper error handling
    if not (transaction in user.transactions):
        print("User is not a part of this transaction")
    elif not (transaction in user.transactions_due):
        print("User has already paid for this transaction")
    else:
        user.transactions_due.remove(transaction)
        transaction.users_due.remove(user)

def pay_all_transactions_due(user:User) -> None:
    #Allow a user to pay all of their outstanding debts
    for transaction in user.transactions_due:
        pay_transaction(user, transaction) #TODO: test and make sure this doesn't cause issues