from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound

db = SQLAlchemy()

PRIVATE_FIELDS = {"user": {"id", "salt", "password_hash"},
                  "item": {},
                  "transaction": {}
                }

class Base(db.Model):
    __abstract__ = True
    def get_attr(self, attr):
        try:
            if attr in PRIVATE_FIELDS[self.__tablename__]:
                raise AttributeError()
            return getattr(self, attr)
        except AttributeError:
            raise NotFound(f"Requested resource does not exist. {self.__tablename__} has no attribute {attr}.")
    
    def set_attr(self, attr, value):
        try:
            self.get_attr(attr) # Checks if attr exists
            setattr(self, attr, value)
        except AttributeError:
            raise NotFound(f"Requested resource does not exist. {self.__tablename__} has no attribute {attr}.")
        
    def to_dict(self) -> dict:
        dict_rep = dict()
        for field in self.__table__.c:
            if field.name in PRIVATE_FIELDS[self.__tablename__]:
                continue
            attr = getattr(self, field.name)
            attr = str(attr) if type(attr) is bytearray else attr
            dict_rep.update({field.name : attr})
        return dict_rep
    
    def __repr__(self) -> str:
        rep_str = f"{self.__tablename__}("
        for field in self.__table__.c:
            attr = getattr(self, field.name)
            rep_str += f"{field.name}={attr}, "
        rep_str += "\b\b)"
        return rep_str

user_preference = db.Table('user_preference',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)

transaction_join = db.Table('transaction_user',
    db.Column('transaction_id', db.Integer, db.ForeignKey('transaction.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
)

class User(Base):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.BINARY(32), nullable=False)
    salt = db.Column(db.BINARY(32), nullable=False)
    household_id = db.Column(db.Integer)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(10))
    budget = db.Column(db.DECIMAL)
    items = db.relationship('Item', secondary=user_preference, back_populates="users")
    transactions = db.relationship('Transaction', secondary=transaction_join, back_populates="users")

class Item(Base):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.DECIMAL)
    purchase_link = db.Column(db.String(2048))
    users = db.relationship('User', secondary=user_preference, back_populates="items")

class Transaction(Base):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    amount = db.Column(db.DECIMAL, nullable=False)
    completed = db.Column(db.BOOLEAN, nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    users = db.relationship('User', secondary=transaction_join, back_populates="transactions")
    