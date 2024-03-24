from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import NotFound, MethodNotAllowed

PRIVATE_FIELDS = {"id", "salt", "password_hash"}

db = SQLAlchemy()

class Base(db.Model):
    __abstract__ = True
    def get_attr(self, attr):
        try:
            return getattr(self, attr)
        except AttributeError:
            raise NotFound("Requested resource does not exist.")
    
    def set_attr(self, attr, value):
        try:
            if (not self.__class__.__table__.columns[attr].nullable) and (value is None):
                raise MethodNotAllowed()
            setattr(self, attr, value)
        except AttributeError:
            raise NotFound("Requested resource does not exist.")
        
    def to_dict(self) -> dict:
        dict_rep = dict()
        for field in self.__table__.c:
            if field.name in PRIVATE_FIELDS:
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

class Item(Base):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100))
    price = db.Column(db.DECIMAL)
    purchase_link = db.Column(db.String(2048))
    
user_preference = db.Table('user_preference',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)