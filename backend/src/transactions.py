from .orm import db, User, Item, Transaction, TransactionUser
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
    
def levenshtein_distance(s1, s2):
    """
    Calculate the Levenshtein distance between two strings.
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def fuzzy_match(query:str, choices:list[str], threshold:float=.5) -> list[tuple[str, float]] | None:
    """
    Find fuzzy matches from a list of choices based on a query string and a threshold.
    """
    matches = []
    for choice in choices:
        distance = levenshtein_distance(query.lower(), choice.lower())
        similarity = 1 - (distance / max(len(query), len(choice)))
        if similarity >= threshold:
            matches.append((choice, similarity))
    return sorted(matches, key=lambda x: x[1], reverse=True) if len(matches) > 0 else None

def get_closest_item_id(query:str, threshold:float=.5) -> int:
    items = Item.query.all()
    item_dict = {i.name:i.id for i in items}
    match = fuzzy_match(query, item_dict.keys(), threshold)
    if not match:
        return match
    return item_dict[match[0][0]]  

def set_item(name:str, price:float=0) -> int:
    if len(name.split()) > 2:
        return
    item = Item(name=name, price=price)
    db.session.add(item)
    db.session.commit()
    return item.id

def get_transaction_by_id(id:int) -> Transaction:
    statement = sql.select(Transaction).where(Transaction.id == id)
    transaction = db.session.scalar(statement)
    if transaction is None:
        raise NotFound(f"No transaction with id {id} exists.")
    return transaction

def update_user_balance(user:User, amount:float) -> None:
    # TODO: Add a call to a method for the notification system
    if user.balance + amount < 0:
        raise BudgetError("Transaction exceeds user's budget.")
    user.balance += amount

def set_transaction_debts(transaction:Transaction, users:list[User]) -> None:
    amt = transaction.amount / (len(transaction.users) + 1)
    for user in users:
        user.transactions.append(transaction)
        statement = sql.update(TransactionUser).values(balance=amt).where(TransactionUser.user_id == user.id, TransactionUser.transaction_id == transaction.id)
        db.session.execute(statement)

def get_balance_for_transaction(user:User, transaction:Transaction) -> float:
    statement = sql.select(TransactionUser).where(TransactionUser.user_id == user.id, TransactionUser.transaction_id == transaction.id)
    balance = db.session.scalar(statement).balance
    return balance

def set_balance_for_transaction(user:User, transaction:Transaction, amount:float):
    statement = sql.update(TransactionUser).values(balance=amount).where(TransactionUser.user_id == user.id, TransactionUser.transaction_id == transaction.id)
    db.session.execute(statement)

def get_transactions_due(user:User) -> list[Transaction]:
    statement = sql.select(Transaction).join(TransactionUser).filter(TransactionUser.user_id == user.id, TransactionUser.balance > 0)
    transactions = db.session.scalars(statement).all()
    return transactions

def calculate_money_owed_by_user(user:User) -> float:
    # Calculate the amount the user owes to others
    total = 0
    for transaction in user.transactions:
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
    if transaction not in user.transactions:
        raise InvalidFieldError("User is not a part of this transaction")
    balance = -get_balance_for_transaction(user, transaction)
    update_user_balance(user, balance)
    set_balance_for_transaction(user, transaction, 0)

def pay_all_transactions_due(user:User) -> None:
    #Allow a user to pay all of their outstanding debts
    for transaction in user.transactions:
        pay_transaction(user, transaction) #TODO: test and make sure this doesn't cause issues