from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    firstName = db.Column(db.String(20))
    surName = db.Column(db.String(20))
    email = db.Column(db.String(100))