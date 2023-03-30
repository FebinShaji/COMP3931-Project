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

class UserWeight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)
    weight = db.Column(db.Float)

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    workoutId = db.Column(db.Integer, db.ForeignKey('workout.id'))
    exerciseName = db.Column(db.String(50))

class Exercises(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    workoutId = db.Column(db.Integer, db.ForeignKey('workout.id'))
    exerciseId = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    date = db.Column(db.DateTime)
    set1weight = db.Column(db.Float)
    set2weight = db.Column(db.Float)
    set3weight = db.Column(db.Float)
    set4weight = db.Column(db.Float)