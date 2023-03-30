from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    firstName = db.Column(db.String(20))
    surName = db.Column(db.String(20))
    email = db.Column(db.String(100))

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(20))
    type = db.Column(db.String(20))

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    workoutId = db.Column(db.Integer, db.ForeignKey('workout.id'))
    exerciseName = db.Column(db.String(50))