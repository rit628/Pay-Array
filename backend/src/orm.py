from flask_sqlalchemy import SQLAlchemy

def orm_object_to_dict(obj) -> dict:
    dict_rep = dict()
    for field in obj.__table__.c:
        attr = getattr(obj, field.name)
        attr = str(attr) if type(attr) is bytearray else attr
        dict_rep.update({field.name : attr})
    return dict_rep

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.BINARY(32), nullable=False)
    salt = db.Column(db.BINARY(32), nullable=False)
    household_id = db.Column(db.Integer)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(10))
    budget = db.Column(db.DECIMAL)

    def __repr__(self):
        return f'''<User(id={self.id}, username={self.username}, email={self.email}, 
                    household_id={self.household_id}, first_name={self.first_name}, 
                    last_name={self.first_name}, phone={self.phone}, budget={self.budget})'''

class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100))
    price = db.Column(db.DECIMAL)
    purchase_link = db.Column(db.String(2048))

    def __repr__(self):
        return f"<Item(id={self.id}, name={self.name}, price={self.price}, purchase_link={self.purchase_link}"
    
user_preference = db.Table('user_preference',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'), primary_key=True)
)